import json
from pathlib import Path
import random
from typing import Any
from uuid import uuid4

from pydantic import BaseModel


# This is a json representation of a graph in a format usable by sigma.js
# It exists in lieu of a database
STATEFILE = Path(__file__).parent / "state.json"
STATE = json.load(STATEFILE.open())
 
COLORS=["red", "blue", "green", "yellow", "black", "pink", "purple", "orange"]


NodeKey = str


class NodeAttributes(BaseModel):
    label: str
    x: float  # TODO maybe use Decimal but need to include seraliser
    y: float
    size: int
    color: str


class Node(BaseModel):
    key: NodeKey
    attributes: NodeAttributes


class EdgeAttributes(BaseModel):
    size: int
    color: str


class Edge(BaseModel):
    key: str
    source: NodeKey
    target: NodeKey
    attributes: EdgeAttributes


class Graph(BaseModel):
    options: dict[str, Any]  # TODO
    attributes: dict[str, Any]  # TODO
    nodes: list[Node]
    edges: list[Edge]
    
    def add_node(self, x, y):
        # Inject some random data for the time being
        key = str(uuid4())
        size = random.randint(3, 30)
        color = random.choice(COLORS)
        
        node = Node(
            key=key,
            attributes=NodeAttributes(
                label=f"Node-{key}-{size}-{color}",
                x=x,
                y=y,
                size=size,
                color=color
            )
        )
        self.nodes.append(node)


graph = Graph(**STATE)