import json
import os

# 1. Import each json file and store it
# 2. Import a names.csv config file with translations from UUID to username
# 3. Based on a category and sub-category of stats, return the leaderboard 

for filename in os.listdir('stats'):
    file = open('stats/' + filename)
    json_string = json.load(file)
    #print(json_string)