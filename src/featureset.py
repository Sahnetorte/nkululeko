# featureset.py
import pandas as pd
from util import Util 

class Featureset:
    name = '' # designation
    config = None # Config file for statics
    df = None # pandas dataframe to store the features (and indexed with the data from the sets)
    data_df = None # dataframe to get audio paths


    def __init__(self, name, config, data_df):
        self.name = name
        self.config = config
        self.data_df = data_df
        self.util = Util(config)

    def extract(self):
        pass