# https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v3
import requests
import json

import functions

""" 
    Retrieve GraphQL mid prices for uniswap
    API result sample: [
        {
        "id": "0x277667eb3e34f134adf870be9550e9f323d0dc24",
        "totalValueLockedETH": "834419413.0127326409251168468344917",
        "token0Price": "10201983.52821130596040573863212092",
        "token1Price": "0.00000009802015433907763482013950488687576",
        "feeTier": "100",
        "token0": {
          "id": "0x160de4468586b6b2f8a92feb0c260fc6cfc743b1",
          "symbol": "ease.org",
          "name": "Ease Fun Token",
          "decimals": "18"
        },
        "token1": {
          "id": "0xea5edef1c6ed1be1bcba4617a1c5a994e9018a43",
          "symbol": "ez-cvxsteCRV",
          "name": "cvxsteCRV Ease Vault",
          "decimals": "18"
        }
      }
      ...
    ] 
"""
def retrieve_uniswap_information():
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    query = """query {
        pools(orderBy: totalValueLockedETH, orderDirection: desc, first: 500) {
            id totalValueLockedETH token0Price token1Price feeTier
            token0 { id symbol name decimals }
            token1 { id symbol name decimals }
        }
    }"""

    req = requests.post(url, json={'query': query})
    json_dictionary = json.loads(req.text)
    return json_dictionary


if __name__ == '__main__':
    pairs = retrieve_uniswap_information()['data']['pools']
    structured_pairs = functions.structure_trading_pairs(pairs, limit=500)

    # Get surface rates
    surface_rate_list = []
    for t_pair in structured_pairs:
        surface_rate = functions.calculate_triangular_arbitrage_surface_rate(t_pair, min_rate=1.5)
        if len(surface_rate) > 0:
            surface_rate_list.append(surface_rate)

    # Save to JSON file
    if len(surface_rate_list) > 0:
        with open('uniswap_surface_rates.json', 'w') as fp:
            json.dump(surface_rate_list, fp)
            print('file saved')
