from util import create_random_group, serialize_group

class GeneratorData:
    total = 0
    rankings_count = 1
    matches_count = 1

def generate(studentsData, mentorsData):
    data = {}
    data["students"] = serialize_group(create_random_group(
        "Students", studentsData.total, studentsData.rankings_count,
        mentorsData.total, studentsData.matches_count))
    data["mentors"] = serialize_group(create_random_group("Mentors", mentorsData.total,
                                  mentorsData.rankings_count,
                                  studentsData.total, mentorsData.matches_count))
    return data
