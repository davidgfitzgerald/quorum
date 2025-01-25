/**
 * The file contains the client-side state object that
 * is updated whenever new state is retrieved from the 
 * backend.
 */
export const graphState = $state(
  {
    "options": {
      "type": "mixed",
      "multi": false,
      "allowSelfLoops": true
    },
    "attributes": {},
    "nodes": [
      {
        "key": "1",
        "attributes": {
          "label": "Node 1",
          "x": 0,
          "y": 0,
          "size": 10,
          "color": "blue"
        }
      },
      {
        "key": "2",
        "attributes": {
          "label": "Node 2",
          "x": 1,
          "y": 1,
          "size": 20,
          "color": "red"
        }
      }
    ],
    "edges": [
      {
        "key": "geid_192_0",
        "source": "1",
        "target": "2",
        "attributes": {
          "size": 5,
          "color": "purple"
        }
      }
    ]
  }  
)