import json

class Dependency:
    def make_dependency(prereqs, courses):
        if type(prereqs) == str:
            return courses[prereqs]
        elif type(prereqs) == list:
            if len(prereqs) == 0:
                return None
            else:
                logic = prereqs[0]
                temp = Dependency()
                temp.add_children(logic, Dependency.make_dependency(prereqs[1], courses), Dependency.make_dependency(prereqs[2], courses))
                return temp
        else:
            raise TypeError()

    def __init__(self):
        self.necessary_for = []
        self.sufficient_for = []

    def add_children(self, logic, child_1, child_2):
        self.logic = logic
        self.children = (child_1, child_2)

        if self.logic.lower() == "and":
            child_1.necessary_for.append(self)
            child_2.necessary_for.append(self)
        elif self.logic.lower() == "or":
            child_1.sufficient_for.append(self)
            child_2.sufficient_for.append(self)

    def is_satisfied(self, courses_taken):
        if self.logic == "and":
            return self.children[0].is_satisfied(courses_taken) and self.children[1].is_satisfied(courses_taken)
        else:
            return self.children[0].is_satisfied(courses_taken) or self.children[1].is_satisfied(courses_taken)

    def can_satisfy(self, courses_taken):
        if self.logic == "and":
            return self.children[0].can_satisfy(courses_taken) and self.children[1].can_satisfy(courses_taken)
        else:
            return self.children[0].can_satisfy(courses_taken) or self.children[1].can_satisfy(courses_taken)

    def __repr__(self):
        sign = "&" if self.logic == "and" else "|"
        return f"({self.children[0].__repr__()} {sign} {self.children[1].__repr__()})"

class Course(Dependency):
    def __init__(self, code, prohib=[], pre_req=[]):
        super().__init__()

        self.code = code
        self.pre_req_ls = pre_req
        self.prohibition_ls = prohib

    # Things that allow you to take courses
    def find_dependencies(self, courses):
        self.pre_req = Dependency.make_dependency(self.pre_req_ls, courses)

        if self.pre_req != None:
            self.pre_req.necessary_for.append(self)

    def is_satisfied(self, courses_taken):
        return self.can_satisfy(courses_taken) and (self.code in courese_taken)

    # Things that prohibit you from taking courses
    def find_prohib(self, courses):
        for c in self.prohibition_ls:
            self.prohibitions.append(courses[c])

    def can_satisfy(self, courses_taken):
        for c in courses_taken:
            if c in self.prohibition_ls:
                return False

        if self.pre_req == None:
            return True

        if self.pre_req.can_satisfy(courses_taken):
            return True

        return False

    def check(self):
        print(self.code)
        print("Necessary for: {}".format(self.necessary_for))
        print("Sufficient for: {}".format(self.sufficient_for))
        print()

    def __repr__(self):
        return self.code

def create_courses(darius_and_monicas_json):
    # (Use monica and darius's json)

    # courses = {"A": Course("A"),
    #         "B": Course("B"),
    #         "C": Course("C"),
    #         "D": Course("D"),
    #         "E": Course("E", ["F"], ["and", "A", ["or", "B", "C"]]),
    #         "F": Course("F", [], "D"),}

    courses = {"A": Course("A"),
            "B": Course("B"),
            "C": Course("C"),
            "D": Course("D"),
            "E": Course("E", ["D"]),
            "F": Course("F", [], "E"),
            "G": Course("G", [], ["and", "B", "C"]),
    }

    for c in courses.values():
        c.find_dependencies(courses)

    return courses
