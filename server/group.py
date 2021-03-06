'''
A group class
'''
import logging
import json
import numpy as np
import pandas
import copy
from random import randrange

class group:
  
  def __init__(self, df):
    '''
    Init a new group object.
    
    df: A Pandas data_frame containing scores for group history, indexed by emails
    '''
    # List to hold the members of thi group (Person objects)
    self.members = []
    
    # The ultimate similarity score of this group (Higher is more similar)
    self.group_score = 0
    self.group_index = 0
    self.score_average = 0
    self.history_df = df
    
    # Attribute Counts data structure for the group
    self.att_counts = {}
    self.att_freq = {}

    # Total Sum of all Frequency
    self.att_freq_total = 0
    
    logging.debug("New Group: {:s}".format( repr(self) ))

  def addPerson(self, p):
    self.members.append(p)
  
  def score_group(self):
    self.compute_stats()
    
    self.group_score += self.compute_history_score()
    
    if self.num_women == 1:
      self.group_score += 2
          
    for p in self.members:
      self.group_score += p.get_similarity_score()
      self.group_index += p.get_similarity_index()
      self.score_average = self.group_score / len(self.members)

  def get_group_score(self):
    return self.group_score


  def get_attr_counts(self):
    return self.att_counts


  def get_members(self):
    return self.members
  

  def compute_stats(self):
    # Reset Everything
    self.group_score = 0
    self.group_index = 0
    self.score_average = 0
    self.att_counts = {}
    self.att_freq = {}
    self.att_freq_total = 0
    self.num_women = 0

    num_people = len(self.members)

    # First we need to count up how many attributes are held by what people
    for p in self.members:
      atts = p.get_attributes()
      # The following creates a multi-demential map, with attributes at the first
      # level, and values for the next level.  The ultimate value for a [att][val] 
      # index is the count of times that value was used for that attribute.
      for k,v in atts.items():
        if k not in self.att_counts:
          self.att_counts[k] = {}
        if v not in self.att_counts[k]:
          self.att_counts[k][v] = 0
        self.att_counts[k][v] += 1
      # Also count up the number of women in the group
      if atts['gender'] == 'F':
        self.num_women += 1

    
    # Next we need to get the sum of the frequency of each attribute
    # In the same loop, sum up the frequencies for each person
    for p in self.members:
      sim_score = 0
      attrs = p.get_attributes()
      for attr in attrs:
        p_freq = self.att_counts[attr][ attrs[attr] ]
        sim_score += p_freq
        
        if attr not in self.att_freq:
          self.att_freq[attr] = {}
          self.att_freq[attr]['sum'] = 0
        
        self.att_freq[attr]['sum'] += p_freq
        self.att_freq_total += p_freq
      p.sim_score = sim_score
    
    # Next compute the avg frequency for each attribute
    for attr,stats in self.att_freq.items():
      self.att_freq[attr]['avg'] = self.att_freq[attr]['sum'] / num_people
      logging.debug("{:12s}  Sum:{:5n}  Avg:{:5n}".format(attr, stats['sum'], stats['avg']) )
    
    logging.debug("att_freq_total: {:5n}".format(self.att_freq_total) )
  
    for p in self.members:
      p.sim_index = p.sim_score / self.att_freq_total * 100
      logging.debug("{:25s}  Sim Score: {:5n}    Sim Index: {:5n}".format(p.name, p.sim_score, p.sim_index) )


  def compute_history_score(self):
    history_score = 0
    temp_members = copy.deepcopy(self.members)
    for i in range(len(temp_members)):
      p1 = temp_members.pop()
      p1email = p1.get_attributes()['email']
      for j in range(len(temp_members)):
        p2 = temp_members[j]
        p2email = p2.get_attributes()['email']
        p1p2_factor = self.history_df.loc[p1email, p2email]
        history_score += p1p2_factor
    return history_score

  
  def remove_random_person(self):
    '''
    Pick a random person from our group and remove them.  Return the removed person
    '''
    p_index = randrange( len(self.members) )
    return self.members.pop(p_index)

  def __repr__(self):
    '''
    Print out a basic representation of a group object
    '''
    names = []
    for m in self.members:
      names.append( m.name )
    names_string = ", ".join(names)
    return_string = "[ {:s} ] Score: {:n}   Index: {:n}".format(names_string, self.group_score, self.score_average)
      
    return return_string

