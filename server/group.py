'''
A group class
'''
import logging
import json

class group:
  
  def __init__(self):
    '''
    Init a new group object.
    '''
    self.group_score = 0
    self.group_index = 0
    self.members = []
    logging.debug("New Group: {:s}".format( repr(self) ))

  def addPerson(self, p):
    self.members.append(p)
  
  def score_group(self):
    for p in self.members:
      self.group_score += p.get_similarity_score()
      self.group_index += p.get_similarity_index()

  def get_group_score(self):
    return self.group_score

  def __repr__(self):
    '''
    Print out a basic representation of a person object
    '''
    names = []
    for m in self.members:
      names.append( m.name )
    names_string = ", ".join(names)
    return_string = "[ {:s} ] Score: {:n}   Index: {:n}".format(names_string, self.group_score, self.group_index)
      
    return return_string

