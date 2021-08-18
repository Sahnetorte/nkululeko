# scaler.py


from sklearn.preprocessing import StandardScaler, RobustScaler
import pandas as pd
from util import Util

class Scaler:
    # class to normalize speech parameters

    def __init__(self, config, train_data_df, test_data_df, train_feats, test_feats):
        self.util = Util(config)
        scaler_type = config['FEATS']['scale'] 
        if scaler_type == 'standard':
            self.scaler = StandardScaler()
        elif scaler_type == 'robust':
            self.scaler = RobustScaler()
        else:
            self.util.error('unknown scaler: '+scaler_type)

        self.feats_train = train_feats.df
        self.data_train = train_data_df
        self.feats_test = test_feats.df
        self.data_test = test_data_df

    def scale(self):
        self.scaler.fit(self.feats_train.values)
        self.feats_train = self.scale_df(self.feats_train)
        self.feats_test = self.scale_df(self.feats_test)
        return self.feats_train, self.feats_test

    def scale_df(self, df):
        scaled_features = self.scaler.fit_transform(df.values)
        df = pd.DataFrame(scaled_features, index=df.index, columns=df.columns)
        return df 