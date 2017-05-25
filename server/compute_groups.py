'''
Compute a set of groups with the highest diversity score
'''
from __future__ import print_function
import csv
import math
import copy
import numpy as np
import pandas
import statistics
import logging
from random import randrange

from person import person
from group import group

rootlogger = logging.getLogger()
rootlogger.setLevel(logging.INFO)
FORMAT = '%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)

target_group_size = 4
num_mutations = 10000

people_file = "tmp/beta-testers.csv"
all_people = []
last_group_set = []
current_group_set = []


def print_set(groups_set, print_groups = False):
  set_score = 0
  set_score_avg = 0
  scores = []
  for g in groups_set:
    g.score_group()
    set_score += g.get_group_score()
    scores.append( g.get_group_score() )
    if print_groups:
      logging.info(g)

  set_variance = statistics.variance(scores)

  logging.info("Total score for this set: {:n}  Var: {:n}".format(set_score, set_variance))

def save_set(groups_set):
  for g in groups_set:
    for p in g.get_members():
      print(p.get_attributes()['email'], end='')
      print(", ", end='')
    print("\n", end='')

with open(people_file, newline='') as f:
    reader = csv.reader(f)
    logging.debug("Openend CSV file {:s}".format(people_file))

    # First row is headers
    headers = next(reader)
    
    for row in reader:
      m = {}
      for i in range(len(headers)):
        m[headers[i]] = row[i]

      p = person(m)
      all_people.append(p)

num_people = len(all_people)
logging.info("Read in {:n} people from {:s}".format(num_people, people_file))

# Read in group history and assemble history factors for everyone
#history_files = ["tmp/history1.csv", "tmp/history2.csv", "tmp/history3.csv"]
history_files = []
p_email_list = []
history_sets = []

for filename in history_files:
  groups = []
  with open(filename, newline='') as f:
      reader = csv.reader(f)
      logging.debug("Openend CSV file {:s}".format(filename))

      for row in reader:
        groups.append(row)
        for p in row:
          if p not in p_email_list:
            p_email_list.append(p)
  # add these groups as a set to history_sets
  history_sets.append(groups)

# If we don't have any history, then just init the email list with the current group
if len(p_email_list) == 0:
  for p in all_people:
    p_email_list.append( p.get_attributes()['email'] )

num_history_people = len(p_email_list)

S = np.zeros((num_history_people, num_history_people))

history_df = pandas.DataFrame(S, columns=p_email_list, index=p_email_list)

group_mate_factor = 2.0
for set in history_sets:
  group_mate_factor = group_mate_factor / 2.0
  for g in set:
    g_size = len(g)
    for i in range(g_size): 
      p1 = g.pop()
      for j in range(len(g)):
        p2 = g[j]
        print("{:s}:{:s} = {:n}".format(p1, p2, group_mate_factor))
        # increment both people's grouping factor with each other
        history_df.set_value(p1, p2, history_df.loc[p1, p2] + group_mate_factor)
        history_df.set_value(p2, p1, history_df.loc[p2, p1] + group_mate_factor)

# Create Groups
logging.info("## Initial Group Placements")

num_groups = math.floor( num_people / target_group_size )
logging.info("Making {:n} groups".format(num_groups))

# Make the groups
for i in range(num_groups):
  new_g = group(history_df)
  current_group_set.append(new_g)

people_to_place = all_people
"""
For however many people there are to place, loop through the groups 
and put a random person in each group until there are no more people
to place.
"""
logging.info( "{:n} people to place".format(len(people_to_place)) )
for i in range(num_people):
  current_g = current_group_set[ i % num_groups ]
  # Pick a random person and remove them from people_to_place
  p_rand = randrange( len(people_to_place) )
  p = people_to_place.pop(p_rand)
  # Add them to the current group
  current_g.addPerson(p)
  logging.debug( "{:n} more people to place".format(len(people_to_place)) )

# Now begin mutating the sets to see if we can arrive at a less similar (more diverse) set
last_group_set = copy.deepcopy(current_group_set)

last_set_score = 10000
for i in range(num_mutations):
  current_set_score = 0
  
  # Pick Two Groups to swap people from
  group_indexes_to_pick_from = list(range(len(current_group_set)))
  swap_g1_idx = group_indexes_to_pick_from.pop( randrange( len(group_indexes_to_pick_from) ) )
  swap_g2_idx = group_indexes_to_pick_from.pop( randrange( len(group_indexes_to_pick_from) ) )
  g1 = current_group_set[swap_g1_idx]
  g2 = current_group_set[swap_g2_idx]
  
  # Remove a random person from each of the groups
  p1 = g1.remove_random_person()
  p2 = g2.remove_random_person()
  
  # And put them back in the other group
  g1.addPerson(p2)
  g2.addPerson(p1)

  for g in current_group_set:
    g.score_group()
    current_set_score += g.get_group_score()
  
  # If this mutation resulted in a better score, keep this set as the last set, otherwise
  # ignore this and keep going
  if current_set_score < last_set_score:
    logging.info("Found better score in itteration #{:n}. {:n} -> {:n}".format(i, last_set_score, current_set_score))
    last_group_set = copy.deepcopy(current_group_set)
    last_set_score = current_set_score
  
  # logging.info("Current Group Set:")
  # print_set(current_group_set)

# Final Set
logging.info("Best set after {:n} mutations:".format(num_mutations) )
print_set(last_group_set, True)
save_set(last_group_set)

