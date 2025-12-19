"""
Fenêtre principale de GraphLabs
"""

import math
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QGroupBox, QComboBox, QSpinBox, 
                             QCheckBox, QPushButton, QTextEdit, QLabel,
                             QMessageBox, QStatusBar, QFileDialog, QMenuBar, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from graphlabs.core.graph import Graph
from graphlabs.core.constants import *
from graphlabs.ui.canvas import GraphCanvas
from graphlabs.algorithms.traversal.dfs import DFSModule
from graphlabs.algorithms.traversal.bfs import BFSModule
from graphlabs.algorithms.shortest_path.dijkstra import DijkstraModule
from graphlabs.utils.file_handler import FileHandler
from graphlabs.utils.graph_library import GraphLibrary

class GraphLabsWindow(QMainWindow):
    """Fenêtre principale de GraphLabs"""
    
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.current_file = None
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Menu bar
        self._create_menu_bar()
        
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
    
    def _create_menu_bar(self):
        """Crée la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("📁 Fichier")
        
        new_action = QAction("🆕 Nouveau graphe", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_graph)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        open_action = QAction("📂 Ouvrir...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_graph)
        file_menu.addAction(open_action)
        
        save_action = QAction("💾 Enregistrer", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("💾 Enregistrer sous...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_graph_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("📤 Exporter en GraphML...", self)
        export_action.triggered.connect(self.export_graphml)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("❌ Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("❓ Aide")
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
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
        self.spin_edge_weight.setMaximum(999)
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
            lambda v: self.canvas.set_edge_weight(int(v))
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
        
        # Paramètres - COMBOBOX au lieu de SPINBOX
        params_layout = QVBoxLayout()
        
        # Départ
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Sommet départ:"))
        self.combo_start = QComboBox()
        self.combo_start.setMinimumWidth(100)
        start_layout.addWidget(self.combo_start)
        start_layout.addStretch()
        params_layout.addLayout(start_layout)
        
        # Arrivée
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Sommet arrivée:"))
        self.combo_end = QComboBox()
        self.combo_end.setMinimumWidth(100)
        end_layout.addWidget(self.combo_end)
        end_layout.addStretch()
        params_layout.addLayout(end_layout)
        
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
        
        # Exemples - avec scroll
        examples_group = QGroupBox("Graphes Exemples")
        examples_main_layout = QVBoxLayout()
        
        # Zone scrollable
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(400)  # Limiter la hauteur
        
        # Widget contenant les boutons
        examples_widget = QWidget()
        examples_layout = QVBoxLayout(examples_widget)
        examples_layout.setContentsMargins(5, 5, 5, 5)
        
        # Créer le menu hiérarchique à partir de la bibliothèque
        all_graphs = GraphLibrary.get_all_graphs()
        
        for category, graphs in all_graphs.items():
            # Label de catégorie
            category_label = QLabel(f"<b>{category}</b>")
            examples_layout.addWidget(category_label)
            
            # Boutons pour chaque graphe
            for graph_name, graph_func in graphs.items():
                btn = QPushButton(f"  {graph_name}")
                btn.setMaximumHeight(30)
                btn.clicked.connect(lambda checked, f=graph_func, n=graph_name: 
                                  self.load_from_library(f, n))
                examples_layout.addWidget(btn)
            
            # Séparateur
            examples_layout.addSpacing(5)
        
        examples_layout.addStretch()
        
        scroll.setWidget(examples_widget)
        examples_main_layout.addWidget(scroll)
        examples_group.setLayout(examples_main_layout)
        layout.addWidget(examples_group)
        
        layout.addStretch()
        return panel
    
    def update_node_combos(self):
        """Met à jour les combobox avec les labels des sommets"""
        # Sauvegarder les sélections actuelles
        current_start = self.combo_start.currentData()
        current_end = self.combo_end.currentData()
        
        self.combo_start.clear()
        self.combo_end.clear()
        
        if self.graph.nodes:
            # Ajouter option "Auto" pour le premier sommet
            self.combo_start.addItem("(Auto)", None)
            self.combo_end.addItem("(Aucun)", None)
            
            # Ajouter tous les sommets avec leur label
            for node_id in sorted(self.graph.nodes.keys()):
                node = self.graph.nodes[node_id]
                display_text = f"{node.label} (id: {node_id})"
                self.combo_start.addItem(display_text, node_id)
                self.combo_end.addItem(display_text, node_id)
            
            # Restaurer les sélections si possible
            if current_start is not None:
                index = self.combo_start.findData(current_start)
                if index >= 0:
                    self.combo_start.setCurrentIndex(index)
            
            if current_end is not None:
                index = self.combo_end.findData(current_end)
                if index >= 0:
                    self.combo_end.setCurrentIndex(index)
    
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
            self.update_node_combos()
            self.current_file = None
            self.setWindowTitle(WINDOW_TITLE)
            
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
            
            # Récupérer les valeurs des combos
            start = self.combo_start.currentData()
            end = self.combo_end.currentData()
            
            try:
                if "Dijkstra" in algo_name:
                    result = module.run(start_node=start, end_node=end)
                else:
                    result = module.run(start_node=start)
                self.result_text.setText(result)
            except Exception as e:
                import traceback
                error_msg = f"Erreur lors de l'exécution:\n{str(e)}\n\n{traceback.format_exc()}"
                QMessageBox.critical(self, "Erreur", error_msg)
                print(error_msg)
                
    def load_from_library(self, graph_func, graph_name: str):
        """Charge un graphe depuis la bibliothèque"""
        try:
            # Charger le nouveau graphe
            new_graph = graph_func()
            
            # Remplacer le graphe actuel
            self.graph.clear()
            self.graph.nodes = new_graph.nodes
            self.graph.edges = new_graph.edges
            self.graph.directed = new_graph.directed
            self.graph.next_id = new_graph.next_id
            
            # Mettre à jour l'interface
            self.chk_directed.setChecked(self.graph.directed)
            self.canvas.graph = self.graph
            self.canvas.clear_highlights()
            self.canvas.update()
            self.update_node_combos()
            
            # Message de succès
            node_count = len(self.graph.nodes)
            edge_count = len(self.graph.edges)
            self.result_text.setText(
                f"✅ {graph_name}\n\n"
                f"Chargé avec succès !\n"
                f"• {node_count} sommets\n"
                f"• {edge_count} arêtes\n"
                f"• {'Orienté' if self.graph.directed else 'Non-orienté'}"
            )
            self.statusBar.showMessage(f"Graphe chargé: {graph_name}")
            self.current_file = None
            self.setWindowTitle(WINDOW_TITLE)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", 
                               f"Impossible de charger le graphe:\n{str(e)}")
    
    def load_example(self, example_id: int):
        """DEPRECATED: Ancienne méthode, gardée pour compatibilité"""
        # Rediriger vers les nouveaux graphes de la bibliothèque
        if example_id == 1:
            self.load_from_library(GraphLibrary.create_cycle, "Cycle (5 sommets)")
        elif example_id == 2:
            self.load_from_library(GraphLibrary.create_grid, "Grille")
        elif example_id == 3:
            self.load_from_library(GraphLibrary.create_dijkstra_example, "Dijkstra")
    
    # ========== GESTION DES FICHIERS ==========
    
    def new_graph(self):
        """Crée un nouveau graphe"""
        if self.graph.nodes:
            reply = QMessageBox.question(
                self, "Nouveau graphe",
                "Voulez-vous sauvegarder le graphe actuel ?",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                if not self.save_graph():
                    return
        
        self.graph.clear()
        self.canvas.clear_highlights()
        self.canvas.update()
        self.result_text.clear()
        self.update_node_combos()
        self.current_file = None
        self.setWindowTitle(WINDOW_TITLE)
        self.statusBar.showMessage("Nouveau graphe créé")
    
    def open_graph(self):
        """Ouvre un graphe depuis un fichier"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un graphe",
            "",
            "Fichiers GraphLabs (*.json);;Tous les fichiers (*)"
        )
        
        if filename:
            loaded_graph = FileHandler.load_graph(filename)
            if loaded_graph:
                self.graph = loaded_graph
                self.canvas.graph = self.graph
                self.canvas.clear_highlights()
                self.canvas.update()
                self.update_node_combos()
                self.current_file = filename
                self.setWindowTitle(f"{WINDOW_TITLE} - {Path(filename).name}")
                self.statusBar.showMessage(f"Graphe chargé: {filename}")
                self.result_text.setText(f"Graphe chargé avec succès!\n{len(self.graph.nodes)} sommets, {len(self.graph.edges)} arêtes")
            else:
                QMessageBox.critical(self, "Erreur", "Impossible de charger le graphe!")
    
    def save_graph(self) -> bool:
        """Enregistre le graphe (utilise save_as si pas de fichier actuel)"""
        if self.current_file:
            if FileHandler.save_graph(self.graph, self.current_file):
                self.statusBar.showMessage(f"Graphe enregistré: {self.current_file}")
                return True
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer le graphe!")
                return False
        else:
            return self.save_graph_as()
    
    def save_graph_as(self) -> bool:
        """Enregistre le graphe sous un nouveau nom"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le graphe",
            "mon_graphe.json",
            "Fichiers GraphLabs (*.json);;Tous les fichiers (*)"
        )
        
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
            
            if FileHandler.save_graph(self.graph, filename):
                self.current_file = filename
                self.setWindowTitle(f"{WINDOW_TITLE} - {Path(filename).name}")
                self.statusBar.showMessage(f"Graphe enregistré: {filename}")
                return True
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer le graphe!")
                return False
        return False
    
    def export_graphml(self):
        """Exporte le graphe au format GraphML"""
        if not self.graph.nodes:
            QMessageBox.warning(self, "Attention", "Le graphe est vide!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter en GraphML",
            "graphe.graphml",
            "Fichiers GraphML (*.graphml);;Tous les fichiers (*)"
        )
        
        if filename:
            if not filename.endswith('.graphml'):
                filename += '.graphml'
            
            if FileHandler.export_to_graphml(self.graph, filename):
                self.statusBar.showMessage(f"Graphe exporté: {filename}")
                QMessageBox.information(self, "Succès", 
                    f"Graphe exporté avec succès!\n\n"
                    f"Compatible avec: Gephi, yEd, Cytoscape, etc.")
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'exporter le graphe!")
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        QMessageBox.about(
            self,
            "À propos de GraphLabs",
            "<h2>GraphLabs v1.0</h2>"
            "<p>Application didactique pour l'apprentissage de la théorie des graphes.</p>"
            "<p><b>Fonctionnalités:</b></p>"
            "<ul>"
            "<li>Création interactive de graphes</li>"
            "<li>Algorithmes de parcours (DFS, BFS)</li>"
            "<li>Plus courts chemins (Dijkstra)</li>"
            "<li>Enregistrement et chargement de graphes</li>"
            "<li>Export GraphML</li>"
            "</ul>"
            "<p><i>Développé pour les étudiants en informatique</i></p>"
        )
    
    def closeEvent(self, event):
        """Gère la fermeture de la fenêtre"""
        if self.graph.nodes:
            reply = QMessageBox.question(
                self,
                "Quitter",
                "Voulez-vous enregistrer le graphe avant de quitter ?",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif reply == QMessageBox.StandardButton.Yes:
                if not self.save_graph():
                    event.ignore()
                    return
        
        event.accept()