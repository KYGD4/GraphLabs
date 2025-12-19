"""
Canvas de dessin interactif pour les graphes
"""

import math
from typing import Optional, Set, Tuple
from PyQt6.QtWidgets import QWidget, QMenu, QInputDialog
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QAction

from graphlabs.core.graph import Graph
from graphlabs.core.constants import *

class GraphCanvas(QWidget):
    """Zone de dessin interactive pour le graphe"""
    
    def __init__(self, graph: Graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.selected_node: Optional[int] = None
        self.selected_edge: Optional[Tuple[int, int]] = None
        self.dragging_node: Optional[int] = None
        self.temp_edge_start: Optional[int] = None
        self.mode = "select"
        self.edge_weight = 1
        self.highlighted_nodes: Set[int] = set()
        self.highlighted_edges: Set[Tuple[int, int]] = set()
        self.setMinimumSize(CANVAS_MIN_WIDTH, CANVAS_MIN_HEIGHT)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def set_mode(self, mode: str):
        """Change le mode d'interaction du canvas"""
        self.mode = mode
        self.temp_edge_start = None
        self.selected_edge = None
        self.update()
    
    def set_edge_weight(self, weight: int):
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
                
            # Poids de l'arête (affichage amélioré)
            if edge.weight != 1:
                mid_x, mid_y = (src.x + tgt.x) / 2, (src.y + tgt.y) / 2
                painter.setPen(QPen(QColor("#000000")))
                painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                
                # Fond blanc pour meilleure lisibilité
                text = str(edge.weight)
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()
                
                painter.setBrush(QBrush(QColor("#FFFFFF")))
                painter.drawRect(int(mid_x - text_width/2 - 2), int(mid_y - text_height/2), 
                               text_width + 4, text_height)
                
                painter.setBrush(QBrush())
                painter.drawText(int(mid_x - text_width/2), int(mid_y + text_height/4), text)
        
        # Arête sélectionnée (afficher en orange)
        if self.selected_edge is not None:
            src_id, tgt_id = self.selected_edge
            if src_id in self.graph.nodes and tgt_id in self.graph.nodes:
                src = self.graph.nodes[src_id]
                tgt = self.graph.nodes[tgt_id]
                painter.setPen(QPen(QColor("#FF9500"), 4))
                painter.drawLine(int(src.x), int(src.y), int(tgt.x), int(tgt.y))
        
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
        clicked_edge = self._find_edge_at(x, y)
        
        if self.mode == "add_node" and clicked_node is None:
            self.graph.add_node(x, y)
            self._notify_graph_changed()
            self.update()
            
        elif self.mode == "add_edge":
            if clicked_node is not None:
                if self.temp_edge_start is None:
                    self.temp_edge_start = clicked_node
                else:
                    if self.temp_edge_start != clicked_node:
                        self.graph.add_edge(self.temp_edge_start, clicked_node, self.edge_weight)
                    self.temp_edge_start = None
                self.update()
                
        elif self.mode == "delete":
            if clicked_node is not None:
                self.graph.remove_node(clicked_node)
                self._notify_graph_changed()
                self.update()
            elif clicked_edge is not None:
                self.graph.remove_edge(clicked_edge[0], clicked_edge[1])
                self.update()
                
        elif self.mode == "select":
            if clicked_node is not None:
                self.selected_node = clicked_node
                self.selected_edge = None
                self.dragging_node = clicked_node
            elif clicked_edge is not None:
                self.selected_edge = clicked_edge
                self.selected_node = None
            else:
                self.selected_node = None
                self.selected_edge = None
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
    
    def _find_edge_at(self, x: float, y: float) -> Optional[Tuple[int, int]]:
        """Trouve une arête proche du point cliqué"""
        threshold = 10  # Distance maximale en pixels
        
        for edge in self.graph.edges:
            if edge.source not in self.graph.nodes or edge.target not in self.graph.nodes:
                continue
            
            src = self.graph.nodes[edge.source]
            tgt = self.graph.nodes[edge.target]
            
            # Distance point-à-ligne
            dist = self._point_to_line_distance(x, y, src.x, src.y, tgt.x, tgt.y)
            
            if dist < threshold:
                # Vérifier que le point est entre les deux sommets
                if self._is_between(x, y, src.x, src.y, tgt.x, tgt.y):
                    return (edge.source, edge.target)
        
        return None
    
    def _point_to_line_distance(self, px, py, x1, y1, x2, y2):
        """Calcule la distance d'un point à une ligne"""
        A = px - x1
        B = py - y1
        C = x2 - x1
        D = y2 - y1
        
        dot = A * C + B * D
        len_sq = C * C + D * D
        
        if len_sq == 0:
            return math.sqrt(A * A + B * B)
        
        param = dot / len_sq
        
        if param < 0:
            xx, yy = x1, y1
        elif param > 1:
            xx, yy = x2, y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D
        
        dx = px - xx
        dy = py - yy
        return math.sqrt(dx * dx + dy * dy)
    
    def _is_between(self, px, py, x1, y1, x2, y2):
        """Vérifie si un point est entre deux autres points"""
        margin = 30  # Marge en pixels
        min_x = min(x1, x2) - margin
        max_x = max(x1, x2) + margin
        min_y = min(y1, y2) - margin
        max_y = max(y1, y2) + margin
        
        return min_x <= px <= max_x and min_y <= py <= max_y
    
    def show_context_menu(self, position):
        """Affiche le menu contextuel (clic droit)"""
        menu = QMenu(self)
        
        clicked_node = self._find_node_at(position.x(), position.y())
        clicked_edge = self._find_edge_at(position.x(), position.y())
        
        if clicked_node is not None:
            # Menu pour sommet
            edit_label = QAction("✏️ Modifier le label", self)
            edit_label.triggered.connect(lambda: self._edit_node_label(clicked_node))
            menu.addAction(edit_label)
            
            delete_node = QAction("🗑️ Supprimer le sommet", self)
            delete_node.triggered.connect(lambda: self._delete_node(clicked_node))
            menu.addAction(delete_node)
            
        elif clicked_edge is not None:
            # Menu pour arête
            edge = self.graph.get_edge(clicked_edge[0], clicked_edge[1])
            if edge:
                edit_weight = QAction(f"✏️ Modifier le poids (actuel: {edge.weight})", self)
                edit_weight.triggered.connect(lambda: self._edit_edge_weight(clicked_edge))
                menu.addAction(edit_weight)
                
                delete_edge = QAction("🗑️ Supprimer l'arête", self)
                delete_edge.triggered.connect(lambda: self._delete_edge(clicked_edge))
                menu.addAction(delete_edge)
        
        if not menu.isEmpty():
            menu.exec(self.mapToGlobal(position))
    
    def _edit_node_label(self, node_id: int):
        """Édite le label d'un sommet"""
        if node_id in self.graph.nodes:
            current_label = self.graph.nodes[node_id].label
            text, ok = QInputDialog.getText(self, "Modifier le label", 
                                           "Nouveau label:", text=current_label)
            if ok and text:
                self.graph.update_node_label(node_id, text)
                self._notify_graph_changed()
                self.update()
    
    def _edit_edge_weight(self, edge_tuple: Tuple[int, int]):
        """Édite le poids d'une arête"""
        edge = self.graph.get_edge(edge_tuple[0], edge_tuple[1])
        if edge:
            value, ok = QInputDialog.getInt(self, "Modifier le poids", 
                                           "Nouveau poids:", edge.weight, 1, 999)
            if ok:
                self.graph.update_edge_weight(edge_tuple[0], edge_tuple[1], value)
                self.update()
    
    def _delete_node(self, node_id: int):
        """Supprime un sommet"""
        self.graph.remove_node(node_id)
        self.selected_node = None
        self._notify_graph_changed()
        self.update()
    
    def _delete_edge(self, edge_tuple: Tuple[int, int]):
        """Supprime une arête"""
        self.graph.remove_edge(edge_tuple[0], edge_tuple[1])
        self.selected_edge = None
        self.update()
        
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

    def _notify_graph_changed(self):
        """Notifie la fenêtre principale que le graphe a changé"""
        # Trouver la fenêtre parent et mettre à jour les combos
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'update_node_combos'):
                parent.update_node_combos()
                break
            parent = parent.parent()