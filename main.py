import json
import os
import pandas as pd
import configparser


# 1. Import each json file and store it
# 2. Import a names.csv config file with translations from UUID to username
# 3. Leaderboard feature: Based on a category and sub-category of stats, return the leaderboard 
# 4. Bestandworst feature: Based on a username, return their position in each leaderboard of each stat, ranked from their best stat to their worst stat


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
    # Replace missing values by 0 (the stat has simply not been initialized because the associated action was not performed)
    df = df.fillna(0)
    if csvtoggle == "true":
        df.to_csv(csvpath)
    return df
    
def getLeaderboard(df, cat, subcat):
    row = df.loc['stats'].loc[cat].loc[subcat].sort_values()
    print("Leaderboard of", cat, subcat, ":")
    print(row)

def getBestAndWorst(df, username):
    ranks = df.rank(axis=1, method='min', ascending=False)
    ranks.to_csv('temp.csv')

    #TODO: display all ranks for current player
    #TODO: add an option to ignore all stats where less than X players have a non-0 value
    #TODO: add an option to also display the number of players that have a non-0 value


# Read config
config = configparser.ConfigParser()
config.read('config.ini')

# Load the data
df = loadData(config['LEADERBOARD']['CreateCSV'], config['LEADERBOARD']['CSVPath'])

# First leaderboard testing
if config['LEADERBOARD']['Enable'] == "true":
    getLeaderboard(df, config['LEADERBOARD']['Category'], config['LEADERBOARD']['Subcategory'])

# First leaderboard testing
if config['BESTANDWORST']['Enable'] == "true":
    getBestAndWorst(df, config['BESTANDWORST']['Username'])