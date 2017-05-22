from __future__ import print_function
import numpy as np
import pandas
import csv
import logging

from person import person
from group import group

rootlogger = logging.getLogger()
rootlogger.setLevel(logging.INFO)
FORMAT = '%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)

history_files = ["tmp/history1.csv", "tmp/history2.csv"]
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

num_people = len(p_email_list)

S = np.zeros((num_people, num_people))

df = pandas.DataFrame(S, columns=p_email_list, index=p_email_list)

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
        df.set_value(p1, p2, df.loc[p1, p2] + group_mate_factor)
        df.set_value(p2, p1, df.loc[p2, p1] + group_mate_factor)

print(df)
