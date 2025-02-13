import json
import os
import pandas as pd
import numpy as np
import configparser


# To get: table with columns for players and rows for pokemons


def loadData(csvtoggle, csvpath):
    df = pd.DataFrame()
    names = pd.read_csv('../data/names.csv')
    i = -1
    path = 'cobblemonplayerdata'
    root_dirnames = []
    for dirpath, dirnames, filenames in os.walk(path):
        if len(dirnames) > 0:
            root_dirnames = dirnames
        for filename in filenames:
            print("Now processing", filename)
            file = open(path + '/' + root_dirnames[i] + '/' + filename)
            data = json.load(file)['extraData']['cobbledex_discovery']['registers']
            # Import the JSON to a Pandas DF
            temp_df = pd.json_normalize(data, meta_prefix=True)
            temp_name = names.loc[names['uuid'] == filename[:-5]]['name']
            temp_df = temp_df.transpose().iloc[1:].rename({0: temp_name.iloc[0]}, axis=1)
            # Split the index (stats.blabla.blabla) into 3 indexes (stats, blabla, blabla)
            if not temp_df.empty:
                temp_df.index = temp_df.index.str.split('.', expand=True)
                if df.empty:
                    df = temp_df
                else:
                    df = df.join(temp_df, how="outer")
            else:
                df[temp_name] = np.nan
        # Replace missing values by 0 (the stat has simply not been initialized because the associated action was not performed)
        df = df.fillna(0)
        if csvtoggle == "true":
            df.to_csv(csvpath)
        i += 1
    return df


# Read config
config = configparser.ConfigParser()
config.read('cobblemon_config.ini')

# Load the data
df = loadData(config['GLOBALMATRIX']['CreateCSV'], config['GLOBALMATRIX']['CSVPath'])
count_df = df.drop(['caughtTimestamp', 'discoveredTimestamp', 'isShiny'], level=2)
print(count_df)
count_df['times_caught'] = count_df.apply(lambda row: (row == "CAUGHT").sum(), axis=1)
print(count_df['times_caught'].sort_values().to_string())