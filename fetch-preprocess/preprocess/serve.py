from dependency import Dependency, Course, create_courses

import sys
import json

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

with open(sys.argv[1]) as f:
    json_file = json.loads(f.readline())
    courses = create_courses(json_file["units"])

#### Return a list of all nodes and edges in the graph
# Nodes have the format {ID, display, colour}, where
# - ID is unique to each node
# - display is the name of the node - either the course code or "and"/"or". This is not necessarily unique
# - colour is the colour the node should be - white for courses, blue for "and" and red for "or"
#
# Edges have the format {from, to, colour}, where
# - from is the unique ID of the node the edge is outgoing from
# - to is the unique ID of the node the edge is ingoing to
# - colour is the colour the the edge should be - white for single dependencies, blue for "and", red for "or" and black for prohibitions

def calculate_graph():
    nodes = []
    for id, node in Dependency.nodes.items():
        if isinstance(node, Course):
            display = node.code
            colour = "white"
        else:
            display = node.logic
            colour = "blue" if display == "and" else "red"

        nodes.append({"ID": id, "display": display, "colour": colour})

    edges = []
    for node in Dependency.nodes.values():
        if isinstance(node, Course):
            if node.pre_req != None:
                edges.append({"from": node.pre_req.id, "to": node.id, "colour": "white"})

            for e in node.prohibitions:
                edges.append({"from": e.id, "to": node.id, "colour": "black"})
        else:
            colour = "blue" if node.logic == "and" else "red"
            edges.append({"from": node.children_id[0], "to": node.id, "colour": colour})
            edges.append({"from": node.children_id[1], "to": node.id, "colour": colour})

    return {"nodes": nodes, "edges": edges}

@app.route('/get_all', methods=['POST'])
def send_all():
    return str(calculate_graph()), 200


#### Given the courses taken, calculate which course requirements are:
# Can take now - all requirements (if any) are satisfied, can enrol in the course right now
# Can potentially take - some requirements are not yet satisfied, but as long as they're completed, the user can take this course in the future
# Can never take - there is a prohibition which stops the user from selecting the subject

def calculate_categories(courses_taken):
    can_take_now = []
    for code, course in courses.items():
        if course.almost_satisfied(courses_taken) and not course.is_satisfied(courses_taken):
            can_take_now.append(code)

    can_never_take = []
    for code, course in courses.items():
        if not course.can_satisfy(courses_taken) and not course.is_satisfied(courses_taken):
            can_never_take.append(code)

    can_potentially_take = list(x for x in courses.keys() if not x in (courses_taken + can_take_now + can_never_take))

    return {"Can take": can_take_now, "Can potentially take": can_potentially_take, "Can never take": can_never_take}

@app.route('/unit_category', methods=['POST'])
def send_categories():
    data_in = request.get_json()
    return str(calculate_categories(data_in['units_taken'])), 200

#### Given the courses taken and a desired course, calculate which courses need to be taken to satisfy the requirements

def parse_requirements(requirements, courses_taken):
    if type(requirements) == Course:
        if requirements.code in courses_taken:
            return None
        else:
            return requirements

    c1 = parse_requirements(requirements.children[0], courses_taken)
    c2 = parse_requirements(requirements.children[1], courses_taken)

    if requirements.logic == "and":
        if c1 == None and c2 == None:
            return None
        elif c1 == None:
            return c2
        elif c2 == None:
            return c1

        return requirements

    elif requirements.logic == "or":
        if c1 == None or c2 == None:
            return None
        return requirements

def calculate_necessary(courses_taken, desired_course):
    desired_course = courses[desired_course]

    if type(desired_course) == Course and desired_course.code in courses_taken:
        return "already_completed"

    if not desired_course.can_satisfy(courses_taken) and not desired_course.is_satisfied(courses_taken):
        return "cannot_take"

    if desired_course.pre_req == None:
        return ""

    requirements = parse_requirements(desired_course.pre_req, courses_taken)
    return requirements.__repr__() if requirements != None else ""

@app.route('/must_take', methods=['POST'])
def send_necessary():
    data_in = request.get_json()
    courses = data_in['units_taken']
    target = data_in['target_unit']

    return calculate_necessary(courses, target), 200

if __name__ == "__main__":
    server = False

    if server:
        app.run(debug=True, port=5000, host='0.0.0.0')

    else:
        # for c in courses.values():
        #     c.check()

        # ==== Make sure graph is calculated ====
        vals = calculate_graph()
        print(*vals["nodes"], '\n', sep='\n')
        print(*vals["edges"], '\n', sep='\n')

        # ==== Calculate units they can take based on what they've already taken ====

        courses_taken = ["COMP2129", "INFO1110"]

        print("You've taken: {}".format(", ".join(courses_taken)))
        print()

        vals = calculate_categories(courses_taken)
        print("You can currently take: {}\n".format(", ".join(vals["Can take"])))
        print("In the future, you can potentially take: {}\n".format(", ".join(vals["Can potentially take"])))
        print("You can never take: {}\n".format(", ".join(vals["Can never take"])))

        # ==== Calculate what other courses they need to do to be eligible for another course ====

        target = "INFO2222"

        print("You've taken: {}".format(", ".join(courses_taken)))
        print("If you want to take {}:".format(target))
        units_to_take = calculate_necessary(courses_taken, target)
        if units_to_take == 'already_completed':
            print("You've already completed that course")
        elif units_to_take == 'cannot_take':
            print("You're prohibited from taking that course")
        elif units_to_take == '':
            print("You can already take that course")
        else:
            print("You should take {}".format(units_to_take))
