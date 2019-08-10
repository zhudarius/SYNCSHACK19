from mock import Dependency, Course, create_courses

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

def calculate_necessary(courses_taken, desired_course):
    # TODO
    pass

@app.route('/must_take', methods=['POST'])
def send_necessary():
    data_in = request.get_json()
    return calculate_necessary(data_in).__repr__()

if __name__ == "__main__":
    server = False

    if server:
        app.run(debug=True, port=5000, host='0.0.0.0')

    else:
        # for c in courses.values():
        #     c.check()
        #
        # vals = calculate_graph()
        # print(*vals["nodes"], sep='\n')
        # print()
        # print(*vals["edges"], sep='\n')
        # print()

        vals = calculate_categories(["COMP2007"])
        print("Can take: \t\t{}".format(",".join(vals["Can take"])))
        print("Can potentially take: \t{}".format(",".join(vals["Can potentially take"])))
        print("Can never take: \t{}".format(",".join(vals["Can never take"])))
        print()
