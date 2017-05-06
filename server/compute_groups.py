'''
Compute a set of groups with the highest diversity score
'''
from __future__ import print_function
import csv
import math
import statistics
import logging
from random import randrange

from person import person
from group import group

rootlogger = logging.getLogger()
rootlogger.setLevel(logging.INFO)
FORMAT = '%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)

people_file = "people.csv"
all_people = []
all_groups = []

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

# Compute Stats for all people
person.compute_stats(all_people)

logging.info("############################")
logging.info("# Initial Group Placements #")
logging.info("############################")

num_groups = math.floor( num_people / 4 )
logging.info("Making {:n} groups".format(num_groups))

# Make the groups
for i in range(num_groups):
  new_g = group()
  all_groups.append(new_g)

people_to_place = all_people
"""
For however many people there are to place, loop through the groups 
and put a random person in each group until there are no more people
to place.
"""
logging.info( "{:n} people to place".format(len(people_to_place)) )
for i in range(num_people):
  current_g = all_groups[ i % num_groups ]
  # Pick a random person and remove them from the people_to_place
  p_rand = randrange( len(people_to_place) )
  p = people_to_place.pop(p_rand)
  # Add them to the current group
  current_g.addPerson(p)
  logging.debug( "{:n} more people to place".format(len(people_to_place)) )

set_score = 0
set_score_avg = 0
scores = []
for g in all_groups:
  g.score_group()
  set_score += g.get_group_score()
  scores.append( g.get_group_score() )
  logging.info(g)

set_variance = statistics.variance(scores)

logging.info("Total score for this set: {:n}  Var: {:n}".format(set_score, set_variance))

