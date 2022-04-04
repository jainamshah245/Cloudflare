import csv, json, sys

# import pandas as pd

input = open(sys.argv[1])
raw_data = json.load(input)
data = raw_data["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]
# data = pd.read_json(input, dtype=False)['data']["viewer"]["zones"][0]["firewallEventsAdaptive"][0]
input.close()

with open(f'firewall_activities.csv', 'w', newline='') as file:
    output = csv.writer(file)

    output.writerow(data[0].keys())  # header row

    for row in data:
        output.writerow(row.values())
