# main.py
# Demonstration code to use the ML-experiment framework

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import numpy as np
import experiment as exp
import dataset as ds
import configparser
from emodb import Emodb
from util import Util

def main(config_file):
    # load one configuration per experiment
    config = configparser.ConfigParser()
    config.read(config_file)
    name = config['EXP']['name']
    print(f'running {name}')
    
    datasets = ['busim-spg', 'danish', 'emodb', 'emovo', 'polish', 'ravdess']
    dim = len(datasets)
    results = np.zeros(dim*dim).reshape([dim, dim])

    for i in range(dim):
        for j in range(dim):
            if i == j:
                dataset = datasets[i]
                print(f'running {dataset}')
                config['DATA']['strategy'] = 'train_test'
                config['DATA']['databases'] = f'[\'{dataset}\']'
            else:
                train = datasets[i]
                test = datasets[j]
                print(f'running {train}_vs_{test}')
                config['DATA']['strategy'] = 'cross_data'
                config['DATA']['databases'] = f'[\'{train}\', \'{test}\']'
                config['DATA']['tests'] = f'[\'{test}\']'
                config['DATA']['trains'] = f'[\'{train}\']'
                config['PLOT']['name'] = f'{train}_vs_{test}'
            expr = exp.Experiment(config)
            util = Util(config)
            # load the data
            expr.load_datasets()

            # split into train and test
            expr.fill_train_and_tests()
            util.debug(f'train shape : {expr.df_train.shape}, test shape:{expr.df_test.shape}')

            # extract features
            expr.extract_feats()
            util.debug(f'train feats shape : {expr.feats_train.df.shape}, test feats shape:{expr.feats_test.df.shape}')

            # initialize a run manager
            expr.init_runmanager()

            # run the experiment
            result = expr.run()
            results[i, j] = float(result)
    print(repr(results))
    plot_name = config['EXP']['name']+'_'+config['MODEL']['type']+'_'+config['FEATS']['type']+'_heatmap.png'
    plot_heatmap(results, datasets, plot_name)

def plot_heatmap(results, labels, name):
    df_cm = pd.DataFrame(results, index = [i for i in labels],
                    columns = [i for i in labels])
    plt.figure(figsize = (10,7))
    sn.heatmap(df_cm, annot=True, cmap=cm.gray)
    plt.savefig(name)
    plt.close()


if __name__ == "__main__":
    main('/home/felix/data/research/nkululeko/exp_emocomp.ini' )# sys.argv[1])
