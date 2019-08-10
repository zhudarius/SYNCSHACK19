from mock import Dependency, Course, create_courses
from flask import request

if __name__ == "__main__":
    # TODO give it a json file
    courses = create_courses(None)
    # for c in courses.values():
    #     c.check()

    #
    # @app.route('/get_all', methods=['GET'])
    # def send_all():
    #     data_in = request.get_json()
    #     return ""
    #
    # @app.route('/can_take', methods=['GET'])
    # def send_sufficient():
    #     data_in = request.get_json()
    #     courses_taken = data_in['courses_taken']
    #
    #     can_take_now = []
    #
    #     for code, course in courses.items():
    #         if course.is_satisfied(courses_taken) and not (code in courses_taken):
    #             can_take_now.append(code)
    #
    #     return "{}".format(",".join(can_take_now))
    #
    # @app.route('/must_take', methods=['GET'])
    # def send_necessary():
    #     data_in = request.get_json()
    #     return "USYD1234,HACK0000"


    courses_taken = ["C", "D"]

    can_take_now = []

    for code, course in courses.items():
        if course.is_satisfied(courses_taken) and not (code in courses_taken):
            can_take_now.append(code)

    can_never_take = []
    for code, course in courses.items():
        if not course.can_satisfy(courses_taken) and not (code in courses_taken):
            can_never_take.append(code)

    print("{}".format(",".join(can_take_now)))
    print("{}".format(",".join(can_never_take)))
