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
              "date_geq": "2022-02-20"
              time: "17:30:15+05:30"
            }},
            {{
              "date_leq": "2022-02-21"
              time: "17:30:15+05:30"
            }}
          ]
        }}
      }}
    }}'''

    r = requests.post(url, data=payload.replace('\n', ''), headers=headers)
    return r


start_date = "2022-02-20T15:00:00.00"
end_date = "2022-02-21T15:00:00.00"

req = get_cf_graphql(start_date, end_date)

raw_data = json.loads(req.text)
print(raw_data)
data = raw_data["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]

with open(f"firewall_activities.csv", newline='', mode='w') as file:
    output = csv.writer(file)
    output.writerow(data[0].keys())
    for row in data:
        output.writerow(row.values())
