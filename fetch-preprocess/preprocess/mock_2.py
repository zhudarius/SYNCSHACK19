from mock import Dependency, Course, create_courses
from flask import request

if __name__ == "__main__":
    # TODO give it a json file
    courses = create_courses(None)
    # for c in courses.values():
    #     c.check()


    completed = [False] * len(courses)

    @app.route('/get_all', methods=['GET'])
    def send_all():
        data_in = request.get_json()
        return ""

    @app.route('/can_take', methods=['GET'])
    def send_sufficient():
        data_in = request.get_json()
        course_codes = data_in['courses_taken']

        can_take = []
        potentially_take = []

        for c in course_codes:



        return "TEST1234,SYNC0000"

    @app.route('/must_take', methods=['GET'])
    def send_necessary():
        data_in = request.get_json()
        return "USYD1234,HACK0000"
