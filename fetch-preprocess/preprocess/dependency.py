class Dependency:
    nodes = {}

    def make_dependency(prereqs, courses):
        if type(prereqs) == str:
            return courses[prereqs]
        elif type(prereqs) == list:
            if len(prereqs) == 0:
                return None
            if len(prereqs) == 1:
                return courses[prereqs[0]]
            else:
                logic = prereqs[0]
                temp = Dependency()
                temp.add_children(logic, Dependency.make_dependency(prereqs[1], courses), Dependency.make_dependency(prereqs[2], courses))
                return temp
        else:
            raise TypeError()

    def __init__(self):
        self.id = len(Dependency.nodes)
        Dependency.nodes[self.id] = self

        self.necessary_for = []
        self.sufficient_for = []

    def add_children(self, logic, child_1, child_2):
        self.logic = "and" if logic == "&" else "or"
        self.children = (child_1, child_2)
        self.children_id = (child_1.id, child_2.id)

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
        return self.code in courses_taken

    def almost_satisfied(self, courses_taken):
        if self.can_satisfy(courses_taken):
            if self.pre_req == None or self.pre_req.is_satisfied(courses_taken):
                return True

        return False

    # Things that prohibit you from taking courses
    def find_prohib(self, courses):
        self.prohibitions = []

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

# TODO fix this up :(
def unpack(ls):
    if type(ls) == list:
        if len(ls) == 0:
            return []
        elif len(ls) == 1:
            return ls
        else:
            return (unpack(ls[1]) + unpack(ls[2]))
    return [ls]

def create_courses(course_json):
    all_course_names = []

    for course in course_json:
        all_course_names.append(course["uos_code"])
        all_course_names.extend(course["prohibitions"])
        all_course_names.extend(unpack(course["prereqs"]))
    all_course_names = list(set(all_course_names))

    prohib_dict = {}
    prereq_dict = {}

    for course_info in course_json:
        uos = course_info["uos_code"]
        prohib_dict[uos] = course_info["prohibitions"]
        prereq_dict[uos] = course_info["prereqs"]

    courses = {}
    for course_name in all_course_names:
        if course_name in prohib_dict:
            courses[course_name] = Course(course_name, prohib_dict[course_name], prereq_dict[course_name])
        else:
            courses[course_name] = Course(course_name)

    for c in courses.values():
        c.find_dependencies(courses)
        c.find_prohib(courses)

    return courses
