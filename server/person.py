'''
A person class
'''
import logging
import json

class person:
    
  def __init__(self, init_data):
    '''
    Init a new person object.
    Take in a map of key/value pairs and just adds those to a data dictionary
    '''
    self.att = {}
    self.sim_score = 0
    self.sim_index = 0
    
    for k,v in init_data.items():
      # print( "{:s}, {:s}".format(k,v) )
      self.att[k] = v
    
    logging.debug("New Person: {:s}".format( repr(self) ))

  def get_similarity_score(self):
    return self.sim_score

  def get_similarity_index(self):
    return self.sim_index
  
  def get_attributes(self):
    return self.att

  @property
  def name(self):
    return self.att['name']

  def __repr__(self):
    '''
    Print out a basic representation of a person object
    '''
    return json.dumps( self.att )
