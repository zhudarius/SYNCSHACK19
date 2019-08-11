# Encodes boolean expressions like "((A and B) or C) or D"
# Has a tree-like structure
class Dependency:
    # Keep track of all the Dependency objects that have been created so far, and give each a unique node ID
    nodes = {}

    # Recursively parse a dependency so that each node has 0 or 2 children
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

    def __init__(self, give_id=True):
        if give_id:
            self.id = len(Dependency.nodes)
            Dependency.nodes[self.id] = self

        # Deprecated
        self.necessary_for = []
        self.sufficient_for = []

    # Children only need to be added to "Dependency" objects which are not "Course"s
    def add_children(self, logic, child_1, child_2, find_children_id=True):
        self.logic = "and" if logic == "&" else "or"
        self.children = (child_1, child_2)

        if find_children_id:
            self.children_id = (child_1.id, child_2.id)

        if self.logic.lower() == "and":
            child_1.necessary_for.append(self)
            child_2.necessary_for.append(self)
        elif self.logic.lower() == "or":
            child_1.sufficient_for.append(self)
            child_2.sufficient_for.append(self)

    # Calculates whether or not a dependency is satisfied - depends on whether the node is an "and" or an "or"
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

    # MaKe iT LoOK FAncY (TM)
    def __repr__(self):
        sign = "&" if self.logic == "and" else "|"
        return f"({self.children[0].__repr__()} {sign} {self.children[1].__repr__()})"

# A leaf in the course dependency tree. Is also a dependency itself
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

    # Returns True if the course has been satisfied
    def is_satisfied(self, courses_taken):
        return self.code in courses_taken

    # Returns True if all the courses' PREREQS have been satisfied
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

    # Returns True if the unit's prerequisits can EVER be satisfied, given that a certain set of courses have already been taken
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

    # Some more pretty printing stuff
    def __repr__(self):
        return self.code

# Extract all course names - even the ones which are in the "prereq" list but aren't explicitly mentioned as a uos
def unpack(ls):
    if type(ls) == list:
        if len(ls) == 0:
            return []
        elif len(ls) == 1:
            return ls
        else:
            return (unpack(ls[1]) + unpack(ls[2]))
    return [ls]

# Read the json string given, and extract the relevant information
def create_courses(course_json):

    # Get a list of all the courses, including ones that aren't mentioned explicitly
    all_course_names = []
    for course in course_json:
        all_course_names.append(course["uos_code"])
        all_course_names.extend(course["prohibitions"])
        all_course_names.extend(unpack(course["prereqs"]))
    all_course_names = list(set(all_course_names))

    prohib_dict = {}
    prereq_dict = {}

    # Figure out the relationships between courses
    for course_info in course_json:
        uos = course_info["uos_code"]
        prohib_dict[uos] = course_info["prohibitions"]
        prereq_dict[uos] = course_info["prereqs"]

    # Create a bunch of Course objects
    courses = {}
    for course_name in all_course_names:
        if course_name in prohib_dict:
            courses[course_name] = Course(course_name, prohib_dict[course_name], prereq_dict[course_name])
        else:
            courses[course_name] = Course(course_name)

    # Set up dependencies
    for c in courses.values():
        c.find_dependencies(courses)
        c.find_prohib(courses)

    return courses
