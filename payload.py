payload = '{ "query":
  "query ListFirewallEvents($zoneTag: string, $filter: FirewallEventsAdaptiveFilter_InputObject) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          firewallEventsAdaptive(
            filter: $filter
            limit: 10
            orderBy: [datetime_DESC]
          ) {
            action
            clientAsn
            clientCountryName
            clientIP
            clientRequestPath
            clientRequestQuery
            datetime
            source
            userAgent
          }
        }
      }
    }",
    "variables": {
      "zoneTag": "CLOUDFLARE_ZONE_ID",
      "filter": {
        "datetime_geq": "2020-04-24T11:00:00Z",
        "datetime_leq": "2020-04-24T12:00:00Z"
      }
    }
  }'
