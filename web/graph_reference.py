def graph_force_ref():
  graph = list()
  fe = { "adjacencies": [
              "fe", {
                "nodeTo": "c0",
                "nodeFrom": "fe",
                "data": {"$color": "#557EAA"}
              }, {
                "nodeTo": "c1",
                "nodeFrom": "fe",
                "data": {"$color": "#557EAA"}
              }
            ],
              "data" : {
                "$color" : "#83548B",
                "$type": "circle",
                "$dim": 10
              },
              "id": "fe",
              "name": "fe"
          }
  c0 = { "adjacencies": [
              "c0", {
                "nodeTo": "c1",
                "nodeFrom": "c0",
                "data": {"$color": "#557EAA"}
              }
              ],
              "data" : {
                "$color" : "#43548B",
                "$type": "circle",
                "$dim": 8
              },
              "id": "c0",
              "name": "c0"
          }
  c1 = { "adjacencies": [],
              "data" : {
                "$color" : "#43548B",
                "$type": "circle",
                "$dim": 8
              },
              "id": "c0",
              "name": "c0"
          }
  graph.append(fe)
  graph.append(c0)
  graph.append(c1)
  return graph
