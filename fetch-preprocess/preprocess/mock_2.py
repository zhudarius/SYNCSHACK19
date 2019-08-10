from mock import Dependency, Course, create_courses

import sys
import json

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# TODO give it a json file
# with open(sys.argv[0]) as f:
#     x = json.loads(f.readline())
#     courses = create_courses(None)
courses = create_courses(None)



# for c in courses.values():
#     c.check()


@app.route('/get_all', methods=['GET'])
def send_all():
    data_in = request.get_json()
    return ""


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
    print("HERE")
    data_in = request.get_json()
    print(data_in)
    return str(calculate_categories(data_in['units_taken'])), 200

def calculate_necessary(courses_taken, desired_course):


    pass

@app.route('/must_take', methods=['GET'])
def send_necessary():
    data_in = request.get_json()
    return calculate_necessary(data_in).__repr__()

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

    # x, y, z = calculate_categories(["C", "D"])
    # print("{}\n{}\n{}".format(",".join(x), ",".join(y), ",".join(z)))
