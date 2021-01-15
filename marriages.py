import random
from util import serialize_group_list, sort_by_matched

# Adds the adder into receiver's list in priority order
def insert_ranked(adder, receiver):
  # assume adder is end of the list
  adder_position = len(receiver.ranking)
  # if adder is part of the ranking, assign new position
  if adder.index in receiver.ranking:
    adder_position = receiver.ranking.index(adder.index)
  index = len(receiver.matched)
  for matched in receiver.matched:
    matched_position = receiver.ranking.index(matched)
    if adder_position < matched_position:
      index = matched_position
      break
  receiver.matched.insert(index, adder.index)
  while len(receiver.matched) > receiver.matches:
    receiver.matched.pop()

def find_person(group_list, index):
  for person in group_list:
    if person.index == index:
      return person
  print(person.index)
  print("Impossible")

# Perform stable marriage on unmatched proposers
# This algorithm ensures people who rank each other highly get paired up and does best-effort to pair up the rest.
#
# This works by having all proposers propose to their most desired and available person (receiver).
# Then the receiver looks at all their proposals (including current partners) and pick the best proposer (this might include breaking up with current partner!).
# The remaining or new single proposers will now repeat the process with single receivers.
# Continue this loop until no more matches are possible.
def stable_marriage(proposers, receivers):
    # Keep matchin until no more movement
    previous_proposers = ""
    while not previous_proposers == serialize_group_list(proposers):
        previous_proposers = serialize_group_list(proposers)
        # sort by least matched so they have a higher chance of being matched
        proposers.sort(key=sort_by_matched)
        receivers.sort(key=sort_by_matched)
        for proposer in proposers:
            # if proposer is already matched, skip
            if len(proposer.matched) >= proposer.matches:
                continue
            # propose if the receiver is available according to preference
            for receiver_index in proposer.ranking:
                receiver = find_person(receivers, receiver_index)
                # if the receiver is no longer accepting proposals, skip
                if len(receiver.matched) >= receiver.matches:
                  continue
                if not proposer.index in receiver.matched:
                    receiver.likedBy.append(proposer.index)
                    break
        for receiver in receivers:
            # go through the receiver's rank and see if potential is one of the proposers
            for proposer_index in receiver.ranking:
              proposer = find_person(proposers, proposer_index)
              # potential is a proposer!
              if proposer.index in receiver.likedBy:
                  insert_ranked(proposer, receiver)
                  if proposer.index in receiver.matched:
                    proposer.matched.append(receiver.index)
                  # break after adding one. only accept 1 proposal
            receiver.likedBy = []

# Perform unstable marriage on unmatched proposers
# This algorithm will have all proposers propose to their most desired and available person (1 proposal).
# If a receiver has multiple proposals, they will randomly pick one partner.
# Single proposers continue this loop until none of their preferences are left.
def unstable_marriage(proposers, receivers):
    previous_proposers = ""
    while not previous_proposers == serialize_group_list(proposers):
        previous_proposers = serialize_group_list(proposers)
        proposers.sort(key=sort_by_matched)
        receivers.sort(key=sort_by_matched)
        for proposer in proposers:
            # if proposer is already matched, skip
            if len(proposer.matched) >= proposer.matches:
                continue
            # propose to first receiver is available according to preference
            for receiver_index in proposer.ranking:
                receiver = find_person(receivers, receiver_index)
                if not len(receiver.matched) >= receiver.matches:
                    receiver.likedBy.append(proposer.index)
                    break
        for receiver in receivers:
            # if receiver is already matched, skip
            if len(receiver.matched) >= receiver.matches:
                continue
            # randomly select a proposer if a proposer exist
            num_likes = len(receiver.likedBy)
            if num_likes == 0:
                continue
            selected = 0 if num_likes == 1 else random.randint(
                0, num_likes - 1)
            proposer = find_person(proposers, receiver.likedBy[selected])
            receiver.matched.append(proposer.index)
            proposer.matched.append(receiver.index)
            # Add 1 proposer and finish
            receiver.likedBy = []

# Perform random marriages on unmatched proposers
# Randomly match up proposers with receivers.
def random_marriage(proposers, receivers):
  remaining_proposers = []
  for proposer in proposers:
    if proposer.matched == []:
      remaining_proposers.append(proposer)
  # grab all the available receivers
  remaining_receivers = []
  for receiver in receivers:
    if len(receiver.matched) < receiver.matches:
      remaining_receivers.append(receiver)
  for receiver in remaining_receivers:
    while len(receiver.matched) < receiver.matches:
      if len(remaining_proposers) == 0:
        break
      proposer = remaining_proposers[0]
      # randomly have a receiver accept the proposer
      if len(remaining_proposers) > 1:
        proposer = remaining_proposers[random.randint(0, len(remaining_proposers) - 1)]
      proposer.matched.append(receiver.index)
      receiver.matched.append(proposer.index)
      remaining_proposers.remove(proposer)