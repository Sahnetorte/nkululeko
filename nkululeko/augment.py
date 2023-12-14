# augment.py
# augment the training sets

from nkululeko.experiment import Experiment
import configparser
from nkululeko.util import Util
from nkululeko.constants import VERSION
import argparse
import os


def main(src_dir):
    parser = argparse.ArgumentParser(description="Call the nkululeko framework.")
    parser.add_argument("--config", default="exp.ini", help="The base configuration")
    args = parser.parse_args()
    if args.config is not None:
        config_file = args.config
    else:
        config_file = f"{src_dir}/exp.ini"

    # test if the configuration file exists
    if not os.path.isfile(config_file):
        print(f"ERROR: no such file: {config_file}")
        exit()

    # load one configuration per experiment
    config = configparser.ConfigParser()
    config.read(config_file)
    # create a new experiment
    expr = Experiment(config)
    util = Util("augment")
    util.debug(
        f"running {expr.name} from config {config_file}, nkululeko version"
        f" {VERSION}"
    )

    if util.config_val("EXP", "no_warnings", False):
        import warnings

        warnings.filterwarnings("ignore")

    # load the data
    expr.load_datasets()

    # split into train and test
    expr.fill_train_and_tests()
    util.debug(f"train shape : {expr.df_train.shape}, test shape:{expr.df_test.shape}")

    # augment
    augmenting = util.config_val("AUGMENT", "augment", False)
    if augmenting:
        df_ret = expr.augment()

    random_splicing = util.config_val("AUGMENT", "random_splice", False)
    if random_splicing:
        df_ret = expr.random_splice()

    if (not augmenting) and (not random_splicing):
        util.error("no augmentation selected")

    # remove encoded labels
    target = util.config_val("DATA", "target", "emotion")
    if "class_label" in df_ret.columns:
        df_ret = df_ret.drop(columns=[target])
        df_ret = df_ret.rename(columns={"class_label": target})
    # save file
    filename = util.config_val("AUGMENT", "result", "augmented.csv")

    df_ret.to_csv(f"{expr.data_dir}/{filename}")
    util.debug(f"saved augmentation table to {filename} to {expr.data_dir}")
    print("DONE")


if __name__ == "__main__":
    cwd = os.path.dirname(os.path.abspath(__file__))
    main(cwd)  # use this if you want to state the config file path on command line
