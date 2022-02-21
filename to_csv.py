#!/usr/bin/env python3
import csv
import json

import pandas as pd
from datetime import datetime, timedelta
import requests

# the endpoint of GraphQL API
url = 'https://api.cloudflare.com/client/v4/graphql/'

# Customize these variables.
file_dir = ''  # Must include trailing slash. If left blank,
# csv will be created in the current directory.
api_token = 'j9BUHyhAWfmtSbIhu1Qz3xmR7k_ybQTi3kuDs81X'
api_zone = input("Enter Zone ID of domain: ")
# Set most recent day as yesterday by default.
offset_days = 1
# How many days worth of data do we want? By default, 7.
historical_days = 2


def get_past_date(num_days):
    today = datetime.utcnow().date()
    return today - timedelta(days=num_days)


def get_cf_graphql(start_date, end_date):
    assert (start_date <= end_date)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    # The GQL query we would like to use:
    payload = f'''{{"query":
      "query ListFirewallEvents($zonetag: string, $filter: FirewallEventsAdaptiveFilter_InputObject) {{
        viewer {{
          zones(
            filter: {{ zoneTag: $zoneTag }}
          ) {{
            firewallEventsAdaptive(
              filter: $filter
              limit: 10000
              orderBy: [datetime_DESC]
            ) {{
                action
                clientASNDescription
                clientAsn
                clientCountryName
                clientIP
                clientRequestHTTPHost
                clientRequestHTTPMethodName
                clientRequestHTTPProtocol
                clientRequestPath
                clientRequestQuery
                datetime
                rayName
                ruleId
                rulesetId
                source
                userAgent
                metadata
        {{
                key
                value
        }}
                sampleInterval
              }}
            }}
        
        }}
      }}",
      "variables": {{
        "zoneTag": "{api_zone}",
        "filter": {{
          "AND":[
            {{
              "date_geq": "{start_date}"
            }},
            {{
              "date_leq": "{end_date}"
            }}
          ]
        }}
      }}
    }}'''

    r = requests.post(url, data=payload.replace('\n', ''), headers=headers)
    return r


#
# def convert_to_csv(raw_data, start_date, end_date):
#     data = pd.read_json(raw_data, dtype=False)['data']
#     errors = pd.read_json(raw_data, dtype=False)['errors']
#
#     # Check if we got any errors
#     if errors.notna().any() or not 'viewer' in data or not 'accounts' in data['viewer']:
#         print('Failed to retrieve data: GraphQL API responded with error:')
#         print(raw_data)
#         return
#
#     # Flatten nested JSON data first
#     network_analytics_normalized = pd.json_normalize(data['viewer']['accounts'], 'ipFlows1mAttacksGroups')
#
#     if len(network_analytics_normalized) == 0:
#         print('We got empty response')
#         return
#
#     network_analytics_abridged = network_analytics_normalized[[
#         'dimensions.attackId',
#         'min.datetimeMinute',
#         'max.datetimeMinute',
#         'dimensions.attackMitigationType',
#         'dimensions.attackType',
#         'dimensions.attackDestinationIP',
#         'max.packetsPerSecond',
#         'avg.packetsPerSecond']]
#     # Rename the columns to get friendly names
#     network_analytics_abridged.columns = [
#         'Attack ID',
#         'Started at',
#         'Ended at',
#         'Action taken',
#         'Attack type',
#         'Destination IP',
#         'Max packets/second',
#         'Avg packets/second']
#     file = "{}network-analytics-{}-{}.csv".format(file_dir, start_date, end_date)
#     network_analytics_abridged.to_csv(file)
#     print("Successfully exported to {}".format(file))
#
#
start_date = input("Enter start date and time in format of 2022-02-20T15:00:00Z ")
end_date = input("Enter start date and time in format of 2022-02-21T14:59:59Z ")

req = get_cf_graphql(start_date, end_date)
# raw_data = req.text
# print(raw_data)
raw_data = json.loads(req.text)
data = raw_data["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]
# if req.status_code == 200:
#     convert_to_csv(req.text, start_date, end_date)
# else:
#     print("Failed to retrieve data: GraphQL API responded with {} status code".format(req.status_code))

with open(f"firewall_activities.csv", newline='', mode='w') as file:
    output = csv.writer(file)
    output.writerow(data[0].keys())
    for row in data:
        output.writerow(row.values())
