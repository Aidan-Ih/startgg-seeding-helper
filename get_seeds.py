from dotenv import dotenv_values
import requests

def get_seeds(token, id):
  url = "https://api.start.gg/gql/alpha"
  headers = {"Authorization": "Bearer " + token}
  query = """
  query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
    event(id: $eventId) {
      id
      name
      entrants(query: {
        page: $page
        perPage: $perPage
      }) {
        pageInfo {
          total
          totalPages
        }
        nodes {
          name
          initialSeedNum
          participants {
            player {
              id
            }
          }
        }
      }
    }
  }
  """  
  variables = {
  "eventId": id,
  "page": 1,
  "perPage": 50
  }
  to_send = {"query": query,
             "variables": variables}
  
  players = []
  curr_page = 0
  info = {"totalPages": 1}
  
  while(curr_page < info["totalPages"]):
    curr_page += 1
    variables["page"] = curr_page
    response = requests.post(url, json=to_send, headers=headers)
    data = response.json()["data"]["event"]["entrants"]
    info = data["pageInfo"]
    players += data["nodes"]
    
  players = [{"name": x["name"], "initialSeed": x["initialSeedNum"], "id": x["participants"][0]["player"]["id"]} for x in players]
  sorted_players = sorted(players, key=lambda x: x["initialSeed"])
  return sorted_players