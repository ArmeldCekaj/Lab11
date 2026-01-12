from dataclasses import dataclass
from model.nodes import Prodotti
@dataclass
class Edges:
    node1: Prodotti
    node2: Prodotti
    weight: int

