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

    def is_satisfied(self):
        if self.logic == "and":
            return child_1.is_satisfied() and child_2.is_satisfied()
        else:
            return child_1.is_satisfied() or child_2.is_satisfied()

    def __repr__(self):
        sign = "&" if self.logic == "and" else "|"
        return f"({self.children[0].__repr__()} {sign} {self.children[1].__repr__()})"

class Course(Dependency):
    def __init__(self, code, prohib=[], pre_req=[]):
        super().__init__()

        self.code = code
        self.pre_req_ls = pre_req

        # self.prohibited_by = []
        # self.prohibits = prohib


    # Set up all prohibitions
    # def find_prohib(self, ls, courses):
    #     for c in ls:
    #         self.prohibited_by.append(courses[c])
    #         courses[c].prohibits.append(self)

    def find_dependencies(self, courses):
        self.pre_req = Dependency.make_dependency(self.pre_req_ls, courses)

        if self.pre_req != None:
            self.pre_req.necessary_for.append(self)

    def is_satisfied(self):
        if 

    def check(self):
        print(self.code)
        print("Necessary for: {}".format(self.necessary_for))
        print("Sufficient for: {}".format(self.sufficient_for))
        print()

    def __repr__(self):
        return self.code

def create_courses(darius_and_monicas_json):
    # (Use monica and darius's json)

    courses = {"A": Course("A"),
            "B": Course("B"),
            "C": Course("C"),
            "D": Course("D"),
            "E": Course("E", ["F"], ["and", "A", ["or", "B", "C"]]),
            "F": Course("F", [], "D"),}

    for c in courses.values():
        c.find_dependencies(courses)

    return courses
