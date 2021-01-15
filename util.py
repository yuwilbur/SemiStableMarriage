import random
import ast

# Creates a unique random. Once a random is used, it won't be produced again.
class UniqueRandom:
    def __init__(self, total):
        self.numbers = []
        for i in range(0, total):
            self.numbers.append(i)

    def rand(self):
        if len(self.numbers) == 0:
            print("rand error")
            return -1
        result = self.numbers[random.randint(0, len(self.numbers) - 1)]
        self.numbers.remove(result)
        return result

# Creates a list of unique random numbers
def random_list(count, total):
    result = []
    if count > total:
        print("random_list error")
        return result
    random_gen = UniqueRandom(total)
    while len(result) < count:
        randomized = random_gen.rand()
        if not randomized in result:
            result.append(randomized)
    return result

# A people (This can be assumed to be a group of mentors or students)
class Person:
    def __init__(self, index, ranking, matches = 1):
        self.index = index
        self.ranking = ranking
        self.matches = matches
        self.likedBy = []
        self.matched = []

# Group of persons
class Group:
    def __init__(self, name):
        self.name = name
        self.list = []

def sort_by_id(person):
  return person.index

def sort_by_matched(person):
  return len(person.matched)

def serialize_group_list(group_list):
  group_list.sort(key=sort_by_id)
  result = ""
  for item in group_list:
    result += str(item.index) + str(item.matched)
  return result;

def serialize_group(group):
  result = {}
  result['name'] = group.name
  group_list = []
  for person in group.list:
    person_serialized = {}
    person_serialized['index'] = person.index
    person_serialized['ranking'] = person.ranking
    person_serialized['matches'] = person.matches
    group_list.append(person_serialized)
  result['list'] = group_list
  return str(result)

def deserialize_group(serialized):
  deserialized = ast.literal_eval(serialized)
  result = Group(deserialized['name'])
  group_list = []
  for person in deserialized['list']:
    person_deserialized = Person(person['index'], person['ranking'], person['matches'])
    group_list.append(person_deserialized)
  result.list = group_list
  return result

# Create a random group of persons
def create_random_group(group_name, group_count, rank_count, rank_total, matches=1):
    group = Group(group_name)
    for i in range(0, group_count):
        person = Person(i, random_list(rank_count, rank_total))
        person.matches = matches
        group.list.append(person)
    return group

# Print the index, and the person's rankings
def print_group(group):
    print(group.name)
    print_group_list(group.list)

def print_group_list(group_list):
  for person in group_list:
        print("Team " + str(person.index) + " | Preferences: " + str(person.ranking))