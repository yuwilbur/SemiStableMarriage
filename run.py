from util import print_group, sort_by_id, deserialize_group, serialize_group
from marriages import stable_marriage, unstable_marriage, random_marriage

def run(students, mentors):
    students = deserialize_group(students)
    mentors = deserialize_group(mentors)

    print('### SETUP (Preferences are ordered from High to Low) ###')
    print_group(students)
    print_group(mentors)
    print()

    paired = []

    def newlyPaired():
        newly_paired = {}
        for student in students.list:
            if student.matched == []:
                continue
            if student.index in paired:
                continue
            value = student.index
            if student.matched[0] in newly_paired:
                value = str(newly_paired[student.matched[0]]) + ", " + str(
                    student.index)
            newly_paired[student.matched[0]] = value
            paired.append(student.index)
        return newly_paired

    ### PERFORM STABLE MARRIAGE ###
    stable_marriage(students.list, mentors.list)
    well_paired = newlyPaired()

    ### PERFORM UNSTABLE MARRIAGES ###
    # have students propose to mentors (students have priority)
    unstable_marriage(students.list, mentors.list)
    students_priority_paired = newlyPaired()
    # have mentors propose to students
    unstable_marriage(mentors.list, students.list)
    mentors_priority_paired = newlyPaired()

    ### PERFORM RANDOM MARRIAGES ###
    random_marriage(students.list, mentors.list)
    randomly_paired = newlyPaired()

    mentors.list.sort(key=sort_by_id)
    students.list.sort(key=sort_by_id)

    ### PRINT RESULTS ###
    def printResult(result_list):
        for key, value in result_list.items():
            print(str(key) + " > " + str(value))

    debug = False
    if debug:
        print("### CALCULATIONS ###")
        print("WELL PAIRED")
        printResult(well_paired)
        print("ONE-SIDED PAIRED (students preference)")
        printResult(students_priority_paired)
        print("ONE-SIDED PAIRED (mentors preference)")
        printResult(mentors_priority_paired)
        print("RANDOMLY PAIRED")
        printResult(randomly_paired)
        print()
        print(serialize_group(students))
        print()
        print(serialize_group(mentors))
    print("### RESULTS ###")
    for mentor in mentors.list:
        print("Mentor Team " + str(mentor.index) + " -> " + "Student Teams " +
              str(mentor.matched))
