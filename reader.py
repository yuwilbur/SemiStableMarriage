from util import Person, Group, serialize_group, print_group, deserialize_group

def read(name):
  group = Group(name)
  line = ''
  while True:
    line = input("Copy-paste " + name + " ([F/f] to finish): ") 
    if line == "F" or line == "f":
      break
    person = readLine(line)
    group.list.append(person)
  serialized = serialize_group(group)
  print()
  print_group(deserialize_group(serialized))
  return serialized


def readLine(line):
  separator = ','
  if ',' in line:
    separator = ','
  elif '\t' in line:
    separator = '\t'
  elif ' ' in line:
    separator = ' '
  index = int(line[0:line.find(separator)])
  line = line[line.find(separator)+1:]
  total_matches = int(line[0:line.find(separator)])
  line = line[line.find(separator)+1:]
  ranking = []
  while line.find(separator) >= 0:
    ranking.append(int(line[0:line.find(separator)]))
    line = line[line.find(separator)+1:]
  ranking.append(int(line))
  return Person(index, ranking, total_matches)