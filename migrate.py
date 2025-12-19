#!/usr/bin/env python3
"""
Script de migration automatique pour GraphLabs
Réorganise le code monolithique en architecture modulaire
"""

import os
import shutil
from pathlib import Path

# Code source à diviser
GRAPH_CORE = '''"""
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
    
@dataclass
class Edge:
    """Représente une arête du graphe"""
    source: int
    target: int
    weight: float = 1.0
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
        self.nodes[node_id] = Node(node_id, x, y, label or str(node_id))
        self.next_id += 1
        return node_id
        
    def add_edge(self, source: int, target: int, weight: float = 1.0):
        """Ajoute une arête entre deux sommets"""
        if source in self.nodes and target in self.nodes:
            self.edges.append(Edge(source, target, weight, self.directed))
            
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
'''

CONSTANTS = '''"""
Constantes globales de l'application
"""

# Couleurs
COLOR_NODE_DEFAULT = "#4A90E2"
COLOR_NODE_SELECTED = "#FF9500"
COLOR_NODE_HIGHLIGHTED = "#50C878"
COLOR_EDGE_DEFAULT = "#333333"
COLOR_EDGE_HIGHLIGHTED = "#FF6B6B"

# Dimensions
NODE_RADIUS = 25
CANVAS_MIN_WIDTH = 600
CANVAS_MIN_HEIGHT = 400
TOOLBAR_HEIGHT = 40

# Interface
WINDOW_TITLE = "GraphLabs - Laboratoire de Théorie des Graphes"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
'''

ALGORITHM_BASE = '''"""
Classe de base pour tous les algorithmes
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphlabs.core.graph import Graph
    from graphlabs.ui.canvas import GraphCanvas

class AlgorithmModule:
    """Classe de base pour les modules d'algorithmes"""
    
    def __init__(self, graph: 'Graph', canvas: 'GraphCanvas'):
        self.graph = graph
        self.canvas = canvas
        
    def run(self, **kwargs) -> str:
        """
        Exécute l'algorithme et retourne le résultat
        
        Returns:
            str: Description textuelle du résultat
        """
        raise NotImplementedError
        
    def get_description(self) -> str:
        """
        Retourne une description pédagogique de l'algorithme
        
        Returns:
            str: Description de l'algorithme
        """
        raise NotImplementedError
    
    def get_complexity(self) -> str:
        """
        Retourne la complexité algorithmique
        
        Returns:
            str: Complexité temporelle et spatiale
        """
        return "Non spécifiée"
'''

DFS_MODULE = '''"""
Parcours en Profondeur (Depth-First Search)
"""

from graphlabs.algorithms.base import AlgorithmModule
from typing import Set, List

class DFSModule(AlgorithmModule):
    """Parcours en profondeur"""
    
    def run(self, start_node: int = None) -> str:
        """
        Exécute un parcours DFS depuis un sommet de départ
        
        Args:
            start_node: Sommet de départ (None = premier sommet)
            
        Returns:
            Résultat du parcours
        """
        if not self.graph.nodes:
            return "Graphe vide"
            
        start = start_node if start_node is not None else next(iter(self.graph.nodes))
        visited: Set[int] = set()
        order: List[int] = []
        
        def dfs(node: int):
            visited.add(node)
            order.append(node)
            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor)
        
        dfs(start)
        self.canvas.highlight_nodes(set(order))
        
        return (f"DFS depuis le sommet {start}:\\n"
                f"Ordre de visite: {' → '.join(map(str, order))}\\n"
                f"Sommets visités: {len(visited)}/{len(self.graph.nodes)}")
        
    def get_description(self) -> str:
        return ("Parcours en Profondeur (DFS):\\n\\n"
                "Explore un graphe en allant le plus loin possible sur chaque branche "
                "avant de revenir en arrière. Utilise une pile (ou la récursion).\\n\\n"
                "Applications: Détection de cycles, tri topologique, composantes connexes.")
    
    def get_complexity(self) -> str:
        return "Temps: O(V + E) | Espace: O(V)"
'''

BFS_MODULE = '''"""
Parcours en Largeur (Breadth-First Search)
"""

from collections import deque
from graphlabs.algorithms.base import AlgorithmModule
from typing import Set, List

class BFSModule(AlgorithmModule):
    """Parcours en largeur"""
    
    def run(self, start_node: int = None) -> str:
        """
        Exécute un parcours BFS depuis un sommet de départ
        
        Args:
            start_node: Sommet de départ (None = premier sommet)
            
        Returns:
            Résultat du parcours
        """
        if not self.graph.nodes:
            return "Graphe vide"
            
        start = start_node if start_node is not None else next(iter(self.graph.nodes))
        visited: Set[int] = {start}
        queue = deque([start])
        order: List[int] = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        self.canvas.highlight_nodes(set(order))
        
        return (f"BFS depuis le sommet {start}:\\n"
                f"Ordre de visite: {' → '.join(map(str, order))}\\n"
                f"Sommets visités: {len(visited)}/{len(self.graph.nodes)}")
        
    def get_description(self) -> str:
        return ("Parcours en Largeur (BFS):\\n\\n"
                "Explore un graphe niveau par niveau, visitant tous les voisins "
                "directs avant de passer aux voisins des voisins. Utilise une file.\\n\\n"
                "Applications: Plus court chemin (non pondéré), distance minimale.")
    
    def get_complexity(self) -> str:
        return "Temps: O(V + E) | Espace: O(V)"
'''

DIJKSTRA_MODULE = '''"""
Algorithme de Dijkstra pour le plus court chemin
"""

import heapq
from graphlabs.algorithms.base import AlgorithmModule
from typing import Dict, Optional

class DijkstraModule(AlgorithmModule):
    """Plus court chemin de Dijkstra"""
    
    def run(self, start_node: int = None, end_node: int = None) -> str:
        """
        Calcule le plus court chemin avec Dijkstra
        
        Args:
            start_node: Sommet de départ
            end_node: Sommet d'arrivée (optionnel)
            
        Returns:
            Résultat avec distances et chemin
        """
        if not self.graph.nodes:
            return "Graphe vide"
            
        start = start_node if start_node is not None else next(iter(self.graph.nodes))
        distances: Dict[int, float] = {node: float('inf') for node in self.graph.nodes}
        distances[start] = 0
        previous: Dict[int, int] = {}
        pq = [(0, start)]
        
        while pq:
            curr_dist, curr = heapq.heappop(pq)
            if curr_dist > distances[curr]:
                continue
                
            for neighbor in self.graph.get_neighbors(curr):
                edge_weight = next((e.weight for e in self.graph.edges 
                                  if (e.source == curr and e.target == neighbor) or
                                     (not self.graph.directed and e.target == curr and e.source == neighbor)), 1.0)
                distance = curr_dist + edge_weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = curr
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruire le chemin si end_node spécifié
        if end_node and end_node in previous:
            path = []
            curr = end_node
            while curr != start:
                path.append(curr)
                curr = previous.get(curr)
                if curr is None:
                    break
            path.append(start)
            path.reverse()
            self.canvas.highlight_nodes(set(path))
            
            return (f"Plus court chemin de {start} à {end_node}:\\n"
                   f"Chemin: {' → '.join(map(str, path))}\\n"
                   f"Distance totale: {distances[end_node]:.1f}")
        
        # Sinon, afficher toutes les distances
        result = f"Distances depuis le sommet {start}:\\n"
        for node in sorted(distances.keys()):
            dist_str = f"{distances[node]:.1f}" if distances[node] != float('inf') else "∞"
            result += f"  Sommet {node}: {dist_str}\\n"
        return result.strip()
        
    def get_description(self) -> str:
        return ("Algorithme de Dijkstra:\\n\\n"
                "Trouve le plus court chemin dans un graphe pondéré avec poids positifs. "
                "Utilise une file de priorité pour explorer les sommets par ordre de distance croissante.\\n\\n"
                "Limitation: Ne fonctionne pas avec des poids négatifs.")
    
    def get_complexity(self) -> str:
        return "Temps: O((V + E) log V) | Espace: O(V)"
'''

CANVAS = '''"""
Canvas de dessin interactif pour les graphes
"""

import math
from typing import Optional, Set, Tuple
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont

from graphlabs.core.graph import Graph
from graphlabs.core.constants import *

class GraphCanvas(QWidget):
    """Zone de dessin interactive pour le graphe"""
    
    def __init__(self, graph: Graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.selected_node: Optional[int] = None
        self.dragging_node: Optional[int] = None
        self.temp_edge_start: Optional[int] = None
        self.mode = "select"
        self.edge_weight = 1.0
        self.highlighted_nodes: Set[int] = set()
        self.highlighted_edges: Set[Tuple[int, int]] = set()
        self.setMinimumSize(CANVAS_MIN_WIDTH, CANVAS_MIN_HEIGHT)
        self.setMouseTracking(True)
        
    def set_mode(self, mode: str):
        """Change le mode d'interaction du canvas"""
        self.mode = mode
        self.temp_edge_start = None
        self.update()
    
    def set_edge_weight(self, weight: float):
        """Définit le poids pour les prochaines arêtes"""
        self.edge_weight = weight
        
    def paintEvent(self, event):
        """Dessine le graphe"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dessiner les arêtes
        for edge in self.graph.edges:
            if edge.source not in self.graph.nodes or edge.target not in self.graph.nodes:
                continue
                
            src = self.graph.nodes[edge.source]
            tgt = self.graph.nodes[edge.target]
            
            is_highlighted = (edge.source, edge.target) in self.highlighted_edges
            pen_color = QColor(COLOR_EDGE_HIGHLIGHTED if is_highlighted else edge.color)
            pen = QPen(pen_color, 3 if is_highlighted else 2)
            painter.setPen(pen)
            
            painter.drawLine(int(src.x), int(src.y), int(tgt.x), int(tgt.y))
            
            if edge.directed:
                self._draw_arrow(painter, src.x, src.y, tgt.x, tgt.y)
                
            if edge.weight != 1.0:
                mid_x, mid_y = (src.x + tgt.x) / 2, (src.y + tgt.y) / 2
                painter.setPen(QPen(QColor("#000000")))
                painter.drawText(int(mid_x), int(mid_y), f"{edge.weight:.1f}")
        
        # Dessiner les sommets
        for node_id, node in self.graph.nodes.items():
            is_highlighted = node_id in self.highlighted_nodes
            is_selected = node_id == self.selected_node
            
            if is_selected:
                brush = QBrush(QColor(COLOR_NODE_SELECTED))
            elif is_highlighted:
                brush = QBrush(QColor(COLOR_NODE_HIGHLIGHTED))
            else:
                brush = QBrush(QColor(node.color))
                
            painter.setBrush(brush)
            painter.setPen(QPen(QColor("#000000"), 2))
            
            painter.drawEllipse(int(node.x - NODE_RADIUS), int(node.y - NODE_RADIUS), 
                              NODE_RADIUS * 2, NODE_RADIUS * 2)
            
            painter.setPen(QPen(QColor("#FFFFFF")))
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            painter.drawText(QRectF(node.x - NODE_RADIUS, node.y - NODE_RADIUS, 
                                   NODE_RADIUS * 2, NODE_RADIUS * 2),
                           Qt.AlignmentFlag.AlignCenter, node.label)
        
        # Arête temporaire
        if self.temp_edge_start is not None and self.mode == "add_edge":
            painter.setPen(QPen(QColor("#999999"), 2, Qt.PenStyle.DashLine))
            start_node = self.graph.nodes[self.temp_edge_start]
            cursor_pos = self.mapFromGlobal(self.cursor().pos())
            painter.drawLine(int(start_node.x), int(start_node.y), 
                           cursor_pos.x(), cursor_pos.y())
                           
    def _draw_arrow(self, painter, x1, y1, x2, y2):
        """Dessine une flèche pour les graphes orientés"""
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_size = 15
        
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        ratio = (dist - NODE_RADIUS) / dist if dist > 0 else 0
        arrow_x = x1 + (x2 - x1) * ratio
        arrow_y = y1 + (y2 - y1) * ratio
        
        p1_x = arrow_x - arrow_size * math.cos(angle - math.pi / 6)
        p1_y = arrow_y - arrow_size * math.sin(angle - math.pi / 6)
        p2_x = arrow_x - arrow_size * math.cos(angle + math.pi / 6)
        p2_y = arrow_y - arrow_size * math.sin(angle + math.pi / 6)
        
        painter.drawLine(int(arrow_x), int(arrow_y), int(p1_x), int(p1_y))
        painter.drawLine(int(arrow_x), int(arrow_y), int(p2_x), int(p2_y))
        
    def mousePressEvent(self, event):
        """Gère les clics de souris"""
        x, y = event.position().x(), event.position().y()
        clicked_node = self._find_node_at(x, y)
        
        if self.mode == "add_node" and clicked_node is None:
            self.graph.add_node(x, y)
            self.update()
            
        elif self.mode == "add_edge":
            if clicked_node is not None:
                if self.temp_edge_start is None:
                    self.temp_edge_start = clicked_node
                else:
                    self.graph.add_edge(self.temp_edge_start, clicked_node, self.edge_weight)
                    self.temp_edge_start = None
                self.update()
                
        elif self.mode == "delete" and clicked_node is not None:
            self.graph.remove_node(clicked_node)
            self.update()
            
        elif self.mode == "select":
            if clicked_node is not None:
                self.selected_node = clicked_node
                self.dragging_node = clicked_node
            self.update()
            
    def mouseMoveEvent(self, event):
        """Gère le déplacement de la souris"""
        if self.dragging_node is not None and self.mode == "select":
            x, y = event.position().x(), event.position().y()
            if self.dragging_node in self.graph.nodes:
                self.graph.nodes[self.dragging_node].x = x
                self.graph.nodes[self.dragging_node].y = y
                self.update()
        elif self.mode == "add_edge" and self.temp_edge_start is not None:
            self.update()
            
    def mouseReleaseEvent(self, event):
        """Gère le relâchement de la souris"""
        self.dragging_node = None
        
    def _find_node_at(self, x: float, y: float) -> Optional[int]:
        """Trouve le sommet à une position donnée"""
        for node_id, node in self.graph.nodes.items():
            dist = math.sqrt((node.x - x)**2 + (node.y - y)**2)
            if dist <= NODE_RADIUS:
                return node_id
        return None
        
    def highlight_nodes(self, node_ids: Set[int]):
        """Met en surbrillance des sommets"""
        self.highlighted_nodes = node_ids
        self.update()
        
    def highlight_edges(self, edges: Set[Tuple[int, int]]):
        """Met en surbrillance des arêtes"""
        self.highlighted_edges = edges
        self.update()
        
    def clear_highlights(self):
        """Efface toutes les surbrillances"""
        self.highlighted_nodes.clear()
        self.highlighted_edges.clear()
        self.update()
'''

MAIN_WINDOW = '''"""
Fenêtre principale de GraphLabs
"""

import math
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QGroupBox, QComboBox, QSpinBox, 
                             QCheckBox, QPushButton, QTextEdit, QLabel,
                             QMessageBox, QStatusBar)
from PyQt6.QtCore import Qt

from graphlabs.core.graph import Graph
from graphlabs.core.constants import *
from graphlabs.ui.canvas import GraphCanvas
from graphlabs.algorithms.traversal.dfs import DFSModule
from graphlabs.algorithms.traversal.bfs import BFSModule
from graphlabs.algorithms.shortest_path.dijkstra import DijkstraModule

class GraphLabsWindow(QMainWindow):
    """Fenêtre principale de GraphLabs"""
    
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel gauche
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panel droit
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([700, 400])
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Prêt - Sélectionnez un mode pour commencer")
        
        self.update_description()
        
    def _create_left_panel(self):
        """Crée le panel gauche avec le canvas"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setMaximumHeight(TOOLBAR_HEIGHT)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        toolbar_layout.setSpacing(5)
        
        self.btn_select = QPushButton("✋ Sélect")
        self.btn_add_node = QPushButton("➕ Sommet")
        self.btn_add_edge = QPushButton("➡️ Arête")
        self.btn_delete = QPushButton("🗑️ Suppr")
        self.btn_clear = QPushButton("🔄 Effacer")
        
        for btn in [self.btn_select, self.btn_add_node, self.btn_add_edge, 
                    self.btn_delete, self.btn_clear]:
            btn.setMaximumHeight(30)
        
        self.btn_select.clicked.connect(lambda: self.set_canvas_mode("select"))
        self.btn_add_node.clicked.connect(lambda: self.set_canvas_mode("add_node"))
        self.btn_add_edge.clicked.connect(lambda: self.set_canvas_mode("add_edge"))
        self.btn_delete.clicked.connect(lambda: self.set_canvas_mode("delete"))
        self.btn_clear.clicked.connect(self.clear_graph)
        
        toolbar_layout.addWidget(self.btn_select)
        toolbar_layout.addWidget(self.btn_add_node)
        toolbar_layout.addWidget(self.btn_add_edge)
        toolbar_layout.addWidget(self.btn_delete)
        toolbar_layout.addWidget(self.btn_clear)
        toolbar_layout.addWidget(QLabel("|"))
        
        self.chk_directed = QCheckBox("Graphe orienté")
        self.chk_directed.stateChanged.connect(self.toggle_directed)
        toolbar_layout.addWidget(self.chk_directed)
        
        toolbar_layout.addWidget(QLabel("Poids:"))
        self.spin_edge_weight = QSpinBox()
        self.spin_edge_weight.setMinimum(1)
        self.spin_edge_weight.setMaximum(99)
        self.spin_edge_weight.setValue(1)
        self.spin_edge_weight.setMaximumWidth(60)
        self.spin_edge_weight.setMaximumHeight(30)
        toolbar_layout.addWidget(self.spin_edge_weight)
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar)
        
        # Canvas
        self.canvas = GraphCanvas(self.graph, self)
        layout.addWidget(self.canvas)
        
        self.spin_edge_weight.valueChanged.connect(
            lambda v: self.canvas.set_edge_weight(float(v))
        )
        
        return panel
        
    def _create_right_panel(self):
        """Crée le panel droit avec les algorithmes"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Sélection d'algorithme
        algo_group = QGroupBox("Algorithmes")
        algo_layout = QVBoxLayout()
        
        self.algo_combo = QComboBox()
        self.algorithms = {
            "DFS - Parcours en Profondeur": DFSModule,
            "BFS - Parcours en Largeur": BFSModule,
            "Dijkstra - Plus Court Chemin": DijkstraModule,
        }
        self.algo_combo.addItems(self.algorithms.keys())
        self.algo_combo.currentTextChanged.connect(self.update_description)
        algo_layout.addWidget(self.algo_combo)
        
        self.algo_description = QTextEdit()
        self.algo_description.setMaximumHeight(100)
        self.algo_description.setReadOnly(True)
        algo_layout.addWidget(QLabel("Description:"))
        algo_layout.addWidget(self.algo_description)
        
        # Paramètres
        params_layout = QHBoxLayout()
        params_layout.addWidget(QLabel("Sommet départ:"))
        self.spin_start = QSpinBox()
        self.spin_start.setMinimum(0)
        params_layout.addWidget(self.spin_start)
        params_layout.addWidget(QLabel("Arrivée:"))
        self.spin_end = QSpinBox()
        self.spin_end.setMinimum(0)
        params_layout.addWidget(self.spin_end)
        algo_layout.addLayout(params_layout)
        
        btn_layout = QHBoxLayout()
        self.btn_run = QPushButton("▶️ Exécuter")
        self.btn_run.clicked.connect(self.run_algorithm)
        self.btn_clear_highlight = QPushButton("Effacer surbrillance")
        self.btn_clear_highlight.clicked.connect(self.canvas.clear_highlights)
        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_clear_highlight)
        algo_layout.addLayout(btn_layout)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)
        
        # Résultats
        result_group = QGroupBox("Résultats")
        result_layout = QVBoxLayout()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # Exemples
        examples_group = QGroupBox("Graphes Exemples")
        examples_layout = QVBoxLayout()
        
        self.btn_example1 = QPushButton("Graphe simple (5 sommets)")
        self.btn_example2 = QPushButton("Graphe connexe (8 sommets)")
        self.btn_example3 = QPushButton("Graphe pondéré")
        
        self.btn_example1.clicked.connect(lambda: self.load_example(1))
        self.btn_example2.clicked.connect(lambda: self.load_example(2))
        self.btn_example3.clicked.connect(lambda: self.load_example(3))
        
        examples_layout.addWidget(self.btn_example1)
        examples_layout.addWidget(self.btn_example2)
        examples_layout.addWidget(self.btn_example3)
        examples_group.setLayout(examples_layout)
        layout.addWidget(examples_group)
        
        layout.addStretch()
        return panel
    
    def set_canvas_mode(self, mode: str):
        """Change le mode du canvas"""
        self.canvas.set_mode(mode)
        mode_names = {
            "select": "Sélection/Déplacement",
            "add_node": "Ajout de sommets",
            "add_edge": "Ajout d'arêtes",
            "delete": "Suppression"
        }
        self.statusBar.showMessage(f"Mode: {mode_names.get(mode, mode)}")
        
    def toggle_directed(self, state):
        """Bascule entre graphe orienté/non-orienté"""
        self.graph.directed = (state == Qt.CheckState.Checked.value)
        self.canvas.update()
        
    def clear_graph(self):
        """Efface tout le graphe avec confirmation"""
        reply = QMessageBox.question(self, "Confirmer", 
                                    "Effacer tout le graphe ?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.graph.clear()
            self.canvas.clear_highlights()
            self.canvas.update()
            self.result_text.clear()
            
    def update_description(self):
        """Met à jour la description de l'algorithme sélectionné"""
        algo_name = self.algo_combo.currentText()
        if algo_name in self.algorithms:
            module_class = self.algorithms[algo_name]
            module = module_class(self.graph, self.canvas)
            self.algo_description.setText(module.get_description())
            
    def run_algorithm(self):
        """Exécute l'algorithme sélectionné"""
        if not self.graph.nodes:
            QMessageBox.warning(self, "Erreur", "Le graphe est vide!")
            return
            
        algo_name = self.algo_combo.currentText()
        if algo_name in self.algorithms:
            module_class = self.algorithms[algo_name]
            module = module_class(self.graph, self.canvas)
            
            start = self.spin_start.value() if self.spin_start.value() in self.graph.nodes else None
            end = self.spin_end.value() if self.spin_end.value() in self.graph.nodes else None
            
            try:
                if "Dijkstra" in algo_name:
                    result = module.run(start, end)
                else:
                    result = module.run(start)
                self.result_text.setText(result)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exécution:\\n{str(e)}")
                
    def load_example(self, example_id: int):
        """Charge un graphe d'exemple"""
        self.graph.clear()
        
        if example_id == 1:
            n = 5
            radius = 150
            cx, cy = 300, 200
            for i in range(n):
                angle = 2 * math.pi * i / n
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                self.graph.add_node(x, y)
            for i in range(n):
                self.graph.add_edge(i, (i + 1) % n)
                
        elif example_id == 2:
            positions = [(150, 150), (300, 100), (450, 150), (150, 300),
                        (300, 250), (450, 300), (250, 200), (350, 200)]
            for x, y in positions:
                self.graph.add_node(x, y)
            edges = [(0, 1), (1, 2), (0, 3), (1, 6), (2, 7), (3, 4), 
                    (4, 5), (6, 7), (4, 6), (5, 7)]
            for s, t in edges:
                self.graph.add_edge(s, t)
                
        elif example_id == 3:
            positions = [(150, 200), (300, 100), (450, 200), (300, 300)]
            for x, y in positions:
                self.graph.add_node(x, y)
            edges = [(0, 1, 4), (0, 3, 2), (1, 2, 3), (1, 3, 5), (2, 3, 1)]
            for s, t, w in edges:
                self.graph.add_edge(s, t, w)
                
        self.canvas.update()
        self.result_text.setText(f"Graphe exemple {example_id} chargé avec succès!")
'''

MAIN_PY = '''"""
Point d'entrée principal de GraphLabs
"""

import sys
from PyQt6.QtWidgets import QApplication
from graphlabs.ui.main_window import GraphLabsWindow

def main():
    """Lance l'application GraphLabs"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = GraphLabsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
'''

REQUIREMENTS = '''PyQt6==6.7.0
numpy>=1.24.0
pytest>=7.4.0
pytest-qt>=4.2.0
black>=23.0.0
flake8>=6.0.0
'''

SETUP_PY = '''from setuptools import setup, find_packages

setup(
    name="graphlabs",
    version="1.0.0",
    description="Application didactique de théorie des graphes",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.7.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "graphlabs=graphlabs.main:main",
        ],
    },
    python_requires=">=3.9",
)
'''

README = '''# 🎓 GraphLabs

Application didactique pour l'apprentissage de la théorie des graphes.

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Installation en mode développement
pip install -e .
```

## Utilisation

```bash
# Lancer l'application
graphlabs

# Ou directement
python -m graphlabs.main
```

## Fonctionnalités

- ✅ Création interactive de graphes
- ✅ Parcours DFS et BFS
- ✅ Plus court chemin (Dijkstra)
- 🚧 Connexité et composantes
- 🚧 Arbres couvrants (Kruskal, Prim)
- 🚧 Détection de cycles
- 🚧 Flots et couplages
- 🚧 Coloration de graphes

## Structure du projet

```
graphlabs/
├── graphlabs/          # Code source
│   ├── core/          # Structures de données
│   ├── ui/            # Interface graphique
│   ├── algorithms/    # Algorithmes
│   └── utils/         # Utilitaires
├── tests/             # Tests unitaires
└── docs/              # Documentation
```

## Développement

```bash
# Tests
pytest

# Formatage
black graphlabs/

# Linter
flake8 graphlabs/
```
'''

GITIGNORE = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# Tests
.pytest_cache/
.coverage

# OS
.DS_Store
Thumbs.db
'''

def create_directory_structure():
    """Crée l'arborescence complète du projet"""
    
    base_dir = Path("graphlabs")
    
    # Structure des dossiers
    directories = [
        "graphlabs/core",
        "graphlabs/ui/widgets",
        "graphlabs/algorithms/traversal",
        "graphlabs/algorithms/shortest_path",
        "graphlabs/algorithms/connectivity",
        "graphlabs/algorithms/trees",
        "graphlabs/algorithms/cycles",
        "graphlabs/algorithms/flow",
        "graphlabs/algorithms/coloring",
        "graphlabs/algorithms/centrality",
        "graphlabs/algorithms/np_problems",
        "graphlabs/utils",
        "graphlabs/resources/styles",
        "graphlabs/resources/icons",
        "graphlabs/resources/examples",
        "tests/test_algorithms",
        "tests/test_ui",
        "docs",
        "scripts",
    ]
    
    print("🏗️  Création de la structure de dossiers...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Créer __init__.py dans les packages Python
        if directory.startswith("graphlabs") or directory.startswith("tests"):
            init_file = Path(directory) / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Module {}"""\n'.format(directory.replace("/", ".")))
    
    print("✅ Structure créée!")

def write_file(path: str, content: str):
    """Écrit un fichier avec le contenu donné"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n")
    print(f"  📝 {path}")

def migrate_code():
    """Migre le code vers la nouvelle structure"""
    
    print("\\n📦 Migration du code...")
    
    # Fichiers core
    write_file("graphlabs/core/graph.py", GRAPH_CORE)
    write_file("graphlabs/core/constants.py", CONSTANTS)
    
    # Fichiers algorithms
    write_file("graphlabs/algorithms/base.py", ALGORITHM_BASE)
    write_file("graphlabs/algorithms/traversal/dfs.py", DFS_MODULE)
    write_file("graphlabs/algorithms/traversal/bfs.py", BFS_MODULE)
    write_file("graphlabs/algorithms/shortest_path/dijkstra.py", DIJKSTRA_MODULE)
    
    # Fichiers UI
    write_file("graphlabs/ui/canvas.py", CANVAS)
    write_file("graphlabs/ui/main_window.py", MAIN_WINDOW)
    
    # Main
    write_file("graphlabs/main.py", MAIN_PY)
    
    # Configuration
    write_file("requirements.txt", REQUIREMENTS)
    write_file("setup.py", SETUP_PY)
    write_file("README.md", README)
    write_file(".gitignore", GITIGNORE)
    
    print("✅ Migration terminée!")

def create_template_files():
    """Crée des fichiers templates pour les futurs algorithmes"""
    
    print("\\n📄 Création de fichiers templates...")
    
    # Template pour nouveaux algorithmes
    algo_template = '''"""
TODO: Implémenter cet algorithme
"""

from graphlabs.algorithms.base import AlgorithmModule

class TemplateModule(AlgorithmModule):
    """Description de l'algorithme"""
    
    def run(self, **kwargs) -> str:
        # TODO: Implémenter
        return "Non implémenté"
        
    def get_description(self) -> str:
        return "Description TODO"
    
    def get_complexity(self) -> str:
        return "Complexité TODO"
'''
    
    templates = [
        "graphlabs/algorithms/shortest_path/bellman_ford.py",
        "graphlabs/algorithms/shortest_path/floyd_warshall.py",
        "graphlabs/algorithms/connectivity/connected_components.py",
        "graphlabs/algorithms/trees/mst_kruskal.py",
        "graphlabs/algorithms/trees/mst_prim.py",
    ]
    
    for template_path in templates:
        write_file(template_path, algo_template)
    
    print("✅ Templates créés!")

def create_test_files():
    """Crée des fichiers de tests basiques"""
    
    print("\\n🧪 Création de tests...")
    
    test_graph = '''"""Tests pour la classe Graph"""

import pytest
from graphlabs.core.graph import Graph, Node, Edge

def test_add_node():
    g = Graph()
    node_id = g.add_node(100, 200, "A")
    assert node_id == 0
    assert len(g.nodes) == 1
    assert g.nodes[0].label == "A"

def test_add_edge():
    g = Graph()
    n1 = g.add_node(0, 0)
    n2 = g.add_node(100, 100)
    g.add_edge(n1, n2, 5.0)
    assert len(g.edges) == 1
    assert g.edges[0].weight == 5.0

def test_get_neighbors():
    g = Graph()
    n1 = g.add_node(0, 0)
    n2 = g.add_node(100, 100)
    n3 = g.add_node(200, 200)
    g.add_edge(n1, n2)
    g.add_edge(n1, n3)
    neighbors = g.get_neighbors(n1)
    assert len(neighbors) == 2
    assert n2 in neighbors
    assert n3 in neighbors
'''
    
    write_file("tests/test_graph.py", test_graph)
    
    print("✅ Tests créés!")

def main():
    """Fonction principale de migration"""
    
    print("=" * 60)
    print("🚀 MIGRATION GRAPHLABS")
    print("=" * 60)
    
    # Vérifier si le dossier existe déjà
    if Path("graphlabs").exists():
        response = input("\\n⚠️  Le dossier 'graphlabs' existe déjà. Continuer? (o/N): ")
        if response.lower() != 'o':
            print("❌ Migration annulée")
            return
        print("🗑️  Suppression de l'ancien dossier...")
        shutil.rmtree("graphlabs")
    
    # Étapes de migration
    create_directory_structure()
    migrate_code()
    create_template_files()
    create_test_files()
    
    print("\\n" + "=" * 60)
    print("✨ MIGRATION RÉUSSIE!")
    print("=" * 60)
    print("\\n📋 Prochaines étapes:\\n")
    print("1. Créer l'environnement virtuel:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # Linux/Mac")
    print("   venv\\\\Scripts\\\\activate    # Windows")
    print("\\n2. Installer les dépendances:")
    print("   pip install -r requirements.txt")
    print("\\n3. Installer en mode dev:")
    print("   pip install -e .")
    print("\\n4. Lancer l'application:")
    print("   python -m graphlabs.main")
    print("   # ou")
    print("   graphlabs")
    print("\\n5. Lancer les tests:")
    print("   pytest")
    print("\\n" + "=" * 60)

if __name__ == "__main__":
    main()

    