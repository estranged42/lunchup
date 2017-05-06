'''
A person class
'''
import logging
import json

class person:

  # Counts of each attribute
  att_counts = {}
  
  # Sum of each attribute frequency
  att_freq = {}
  
  # Total Sum of all Frequency
  att_freq_total = 0
  
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
      
      if k not in self.att_counts:
        self.att_counts[k] = {}
      
      if v not in self.att_counts[k]:
        self.att_counts[k][v] = 0
      
      self.att_counts[k][v] += 1
    
    logging.debug("New Person: {:s}".format( repr(self) ))

  def get_similarity_score(self):
    return self.sim_score

  def get_similarity_index(self):
    return self.sim_index

  @property
  def name(self):
    return self.att['name']

  @staticmethod
  def get_attr_counts():
    return person.att_counts
  
  @staticmethod
  def compute_stats(person_list):
    num_people = len(person_list)
    # First we need to get the sum of the frequency of each attribute
    # In the same loop, sum up the frequencies for each person
    for p in person_list:
      sim_score = 0
      for attr in p.att:
        p_freq = person.att_counts[attr][ p.att[attr] ]
        sim_score += p_freq
        
        if attr not in person.att_freq:
          person.att_freq[attr] = {}
          person.att_freq[attr]['sum'] = 0
        
        person.att_freq[attr]['sum'] += p_freq
        person.att_freq_total += p_freq
      p.sim_score = sim_score
    
    # Next compute the avg frequency for each attribute
    for attr,stats in person.att_freq.items():
      person.att_freq[attr]['avg'] = person.att_freq[attr]['sum'] / num_people
      logging.debug("{:12s}  Sum:{:5n}  Avg:{:5n}".format(attr, stats['sum'], stats['avg']) )
    
    logging.debug("att_freq_total: {:5n}".format(person.att_freq_total) )
  
    for p in person_list:
      p.sim_index = p.sim_score / person.att_freq_total * 100
      logging.debug("{:25s}  Sim Score: {:5n}    Sim Inex: {:5n}".format(p.name, p.sim_score, p.sim_index) )

  def __repr__(self):
    '''
    Print out a basic representation of a person object
    '''
    return json.dumps( self.att )
