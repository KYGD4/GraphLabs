"""
Structures de données de base pour les graphes
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional

@dataclass
class Node:
    """Représente un sommet du graphe"""
    id: int
    x: float
    y: float
    label: str = ""
    color: str = "#4A90E2"
    
    def __post_init__(self):
        # Générer un label alphabétique par défaut si vide
        if not self.label:
            self.label = self._int_to_letter(self.id)
    
    @staticmethod
    def _int_to_letter(n: int) -> str:
        """Convertit un entier en lettre(s) : 0->A, 1->B, ..., 26->AA"""
        result = ""
        n += 1  # Pour commencer à A (pas @)
        while n > 0:
            n -= 1
            result = chr(65 + (n % 26)) + result
            n //= 26
        return result
    
@dataclass
class Edge:
    """Représente une arête du graphe"""
    source: int
    target: int
    weight: int = 1  # Changé en int pour poids entiers
    directed: bool = False
    color: str = "#333333"

class Graph:
    """Modèle de graphe avec opérations de base"""
    def __init__(self, directed=False):
        self.nodes: Dict[int, Node] = {}
        self.edges: List[Edge] = []
        self.directed = directed
        self.next_id = 0
        
    def add_node(self, x: float, y: float, label: str = "") -> int:
        """Ajoute un sommet au graphe"""
        node_id = self.next_id
        node = Node(node_id, x, y, label)
        self.nodes[node_id] = node
        self.next_id += 1
        return node_id
        
    def add_edge(self, source: int, target: int, weight: int = 1):
        """Ajoute une arête entre deux sommets"""
        if source in self.nodes and target in self.nodes:
            self.edges.append(Edge(source, target, weight, self.directed))
    
    def update_node_label(self, node_id: int, label: str):
        """Met à jour le label d'un sommet"""
        if node_id in self.nodes:
            self.nodes[node_id].label = label
    
    def get_edge(self, source: int, target: int) -> Optional[Edge]:
        """Trouve une arête entre deux sommets"""
        for edge in self.edges:
            if edge.source == source and edge.target == target:
                return edge
            if not self.directed and edge.source == target and edge.target == source:
                return edge
        return None
    
    def update_edge_weight(self, source: int, target: int, weight: int):
        """Met à jour le poids d'une arête"""
        edge = self.get_edge(source, target)
        if edge:
            edge.weight = weight
            
    def remove_node(self, node_id: int):
        """Supprime un sommet et toutes ses arêtes"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.edges = [e for e in self.edges if e.source != node_id and e.target != node_id]
            
    def remove_edge(self, source: int, target: int):
        """Supprime une arête"""
        self.edges = [e for e in self.edges if not (e.source == source and e.target == target)]
        
    def get_neighbors(self, node_id: int) -> List[int]:
        """Retourne la liste des voisins d'un sommet"""
        neighbors = []
        for edge in self.edges:
            if edge.source == node_id:
                neighbors.append(edge.target)
            elif not self.directed and edge.target == node_id:
                neighbors.append(edge.source)
        return neighbors
        
    def get_adjacency_matrix(self) -> List[List[float]]:
        """Retourne la matrice d'adjacence"""
        n = len(self.nodes)
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        for edge in self.edges:
            matrix[edge.source][edge.target] = edge.weight
            if not self.directed:
                matrix[edge.target][edge.source] = edge.weight
        return matrix
        
    def clear(self):
        """Efface tout le graphe"""
        self.nodes.clear()
        self.edges.clear()
        self.next_id = 0