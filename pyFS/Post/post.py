# -*- coding: utf-8 -*-

class PostProcessor:
    
    def __init__(self, model_name):
        self.model_name = model_name
        self.results_sets = {}

    def read_results_set(self, set_number):
        with open(f'{self.model_name}.Q{set_number}', 'r') as rsf:
            s = [l.strip() for l in rsf.readlines()]
            rs = ResultsSet(s[0], [int(c) for c in s[1:]])
            print(rs.cases)
            
            
        
class ResultsSet:
    
    def __init__(self, name, cases = []):
        self.name = name
        self.cases = cases
    
pp = PostProcessor('model')
pp.read_results_set(1)