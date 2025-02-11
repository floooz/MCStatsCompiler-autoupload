import json
import os
import pandas as pd
import configparser


# 1. Import each json file and store it
# 2. Import a names.csv config file with translations from UUID to username
# 3. Based on a category and sub-category of stats, return the leaderboard 


def loadData(csvtoggle, csvpath):
    df = pd.DataFrame()
    names = pd.read_csv('names.csv')
    for filename in os.listdir('stats'):
        print("Now processing", filename)
        file = open('stats/' + filename)
        data = json.load(file)
        # Import the JSON to a Pandas DF
        temp_df = pd.json_normalize(data, meta_prefix=True)
        temp_name = names.loc[names['uuid'] == filename[:-5]]['name']
        temp_df = temp_df.transpose().iloc[1:].rename({0: temp_name.iloc[0]}, axis=1)
        # Split the index (stats.blabla.blabla) into 3 indexes (stats, blabla, blabla)
        temp_df.index = temp_df.index.str.split('.', expand=True)
        if df.empty:
            df = temp_df
        else:
            df = df.join(temp_df, how="outer")
    if csvtoggle:
        df.to_csv(csvpath)
    return df
    
def getLeaderboard(df, cat, subcat):
    row = df.loc['stats'].loc[cat].loc[subcat].fillna(0).sort_values()
    print("Leaderboard of", cat, subcat, ":")
    print(row)


# Read config
config = configparser.ConfigParser()
config.read('config.ini')

# Load the data
df = loadData(config['LEADERBOARD']['CreateCSV'], config['LEADERBOARD']['CSVPath'])

# First leaderboard testing
getLeaderboard(df, config['LEADERBOARD']['Category'], config['LEADERBOARD']['Subcategory'])