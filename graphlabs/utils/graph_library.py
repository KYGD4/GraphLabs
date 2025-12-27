"""
Bibliothèque de graphes classiques et d'exemples
"""

import math
from graphlabs.core.graph import Graph

class GraphLibrary:
    """Collection de graphes prédéfinis pour l'apprentissage"""
    
    # ==================== FORMES DE BASE ====================
    
    @staticmethod
    def create_chain(n: int = 5) -> Graph:
        """
        Chaîne simple : A-B-C-D-E
        Utile pour comprendre les parcours linéaires
        """
        graph = Graph(directed=False)
        
        # Disposition horizontale
        for i in range(n):
            x = 100 + i * 100
            y = 200
            graph.add_node(x, y)
        
        # Arêtes séquentielles
        for i in range(n - 1):
            graph.add_edge(i, i + 1, 1)
        
        return graph
    
    @staticmethod
    def create_cycle(n: int = 6) -> Graph:
        """
        Cycle : A-B-C-D-E-F-A
        Utile pour circuits eulériens
        """
        graph = Graph(directed=False)
        
        # Disposition en cercle
        radius = 150
        cx, cy = 300, 250
        
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2  # Commencer en haut
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            graph.add_node(x, y)
        
        # Arêtes cycliques
        for i in range(n):
            graph.add_edge(i, (i + 1) % n, 1)
        
        return graph
    
    @staticmethod
    def create_star(n: int = 6) -> Graph:
        """
        Étoile : Centre connecté à n branches
        Utile pour centralité
        """
        graph = Graph(directed=False)
        
        # Centre
        graph.add_node(300, 250, "Centre")
        
        # Branches en cercle
        radius = 150
        for i in range(n):
            angle = 2 * math.pi * i / n
            x = 300 + radius * math.cos(angle)
            y = 250 + radius * math.sin(angle)
            graph.add_node(x, y)
            graph.add_edge(0, i + 1, 1)
        
        return graph
    
    @staticmethod
    def create_complete(n: int = 5) -> Graph:
        """
        Graphe complet Kn : Tous les sommets connectés
        Utile pour coloration (nombre chromatique = n)
        """
        graph = Graph(directed=False)
        
        # Disposition en cercle
        radius = 150
        cx, cy = 300, 250
        
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            graph.add_node(x, y)
        
        # Toutes les arêtes possibles
        for i in range(n):
            for j in range(i + 1, n):
                graph.add_edge(i, j, 1)
        
        return graph
    
    @staticmethod
    def create_binary_tree(depth: int = 3) -> Graph:
        """
        Arbre binaire complet
        Utile pour parcours DFS/BFS
        """
        graph = Graph(directed=False)
        
        # Calculer positions niveau par niveau
        def add_tree_nodes(node_id, level, pos_x, width, max_depth):
            if level > max_depth:
                return node_id
            
            y = 80 + level * 80
            x = pos_x
            
            current_id = node_id
            graph.add_node(x, y)
            
            if level < max_depth:
                # Fils gauche
                left_id = add_tree_nodes(node_id + 1, level + 1, 
                                        pos_x - width // 2, width // 2, max_depth)
                graph.add_edge(current_id, node_id + 1, 1)
                
                # Fils droit
                right_id = add_tree_nodes(left_id, level + 1, 
                                         pos_x + width // 2, width // 2, max_depth)
                graph.add_edge(current_id, left_id, 1)
                
                return right_id
            
            return node_id + 1
        
        add_tree_nodes(0, 0, 300, 200, depth)
        return graph
    
    @staticmethod
    def create_grid(rows: int = 3, cols: int = 3) -> Graph:
        """
        Grille rectangulaire
        Utile pour plus courts chemins
        """
        graph = Graph(directed=False)
        
        spacing = 80
        offset_x = 150
        offset_y = 150
        
        # Créer tous les nœuds
        node_map = {}
        node_id = 0
        for i in range(rows):
            for j in range(cols):
                x = offset_x + j * spacing
                y = offset_y + i * spacing
                graph.add_node(x, y)
                node_map[(i, j)] = node_id
                node_id += 1
        
        # Arêtes horizontales et verticales
        for i in range(rows):
            for j in range(cols):
                current = node_map[(i, j)]
                
                # Droite
                if j < cols - 1:
                    graph.add_edge(current, node_map[(i, j + 1)], 1)
                
                # Bas
                if i < rows - 1:
                    graph.add_edge(current, node_map[(i + 1, j)], 1)
        
        return graph
    
    # ==================== GRAPHES HISTORIQUES ====================
    
    @staticmethod
    def create_konigsberg() -> Graph:
        """
        Les 7 ponts de Königsberg (Euler, 1736)
        Problème : Peut-on traverser tous les ponts une seule fois ?
        Réponse : NON (4 sommets de degré impair)
        """
        graph = Graph(directed=False)
        
        # 4 zones de la ville
        # A: Rive nord
        # B: Rive sud  
        # C: Île Kneiphof (centre)
        # D: Île est
        
        graph.add_node(300, 100, "Rive Nord")      # A
        graph.add_node(300, 400, "Rive Sud")       # B
        graph.add_node(300, 250, "Kneiphof")       # C (île centre)
        graph.add_node(500, 250, "Île Est")        # D
        
        # Les 7 ponts (arêtes)
        graph.add_edge(0, 2, 1)  # Nord → Kneiphof (pont 1)
        graph.add_edge(0, 2, 1)  # Nord → Kneiphof (pont 2)
        graph.add_edge(1, 2, 1)  # Sud → Kneiphof (pont 3)
        graph.add_edge(1, 2, 1)  # Sud → Kneiphof (pont 4)
        graph.add_edge(0, 3, 1)  # Nord → Est (pont 5)
        graph.add_edge(1, 3, 1)  # Sud → Est (pont 6)
        graph.add_edge(2, 3, 1)  # Kneiphof → Est (pont 7)
        
        return graph
    
    @staticmethod
    def create_utilities() -> Graph:
        """
        Problème des 3 maisons et 3 services (K3,3)
        3 maisons doivent être reliées à 3 services (eau, gaz, électricité)
        sans que les câbles se croisent. Impossible sur un plan !
        Graphe biparti, non planaire
        """
        graph = Graph(directed=False)
        
        # 3 maisons (gauche)
        graph.add_node(100, 100, "Maison 1")
        graph.add_node(100, 250, "Maison 2")
        graph.add_node(100, 400, "Maison 3")
        
        # 3 services (droite)
        graph.add_node(500, 100, "Eau")
        graph.add_node(500, 250, "Gaz")
        graph.add_node(500, 400, "Électricité")
        
        # Toutes les connexions (chaque maison → chaque service)
        for i in range(3):
            for j in range(3):
                graph.add_edge(i, 3 + j, 1)
        
        return graph
    
    @staticmethod
    def create_petersen() -> Graph:
        """
        Graphe de Petersen
        Célèbre contre-exemple en théorie des graphes
        Non-hamiltonien malgré de bonnes propriétés
        """
        graph = Graph(directed=False)
        
        # Pentagone extérieur
        radius_outer = 150
        cx, cy = 300, 250
        
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            x = cx + radius_outer * math.cos(angle)
            y = cy + radius_outer * math.sin(angle)
            graph.add_node(x, y)
        
        # Étoile intérieure (pentagramme)
        radius_inner = 70
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            x = cx + radius_inner * math.cos(angle)
            y = cy + radius_inner * math.sin(angle)
            graph.add_node(x, y)
        
        # Arêtes du pentagone extérieur
        for i in range(5):
            graph.add_edge(i, (i + 1) % 5, 1)
        
        # Arêtes de l'étoile intérieure
        for i in range(5):
            graph.add_edge(5 + i, 5 + ((i + 2) % 5), 1)
        
        # Arêtes radiales
        for i in range(5):
            graph.add_edge(i, 5 + i, 1)
        
        return graph
    
    # ==================== GRAPHES D'EXERCICE ====================
    
    @staticmethod
    def create_dijkstra_example() -> Graph:
        """
        Graphe pondéré pour Dijkstra
        Avec plusieurs chemins possibles
        """
        graph = Graph(directed=False)
        
        # Sommets en forme de losange
        graph.add_node(100, 250, "Départ")   # 0
        graph.add_node(250, 150, "B")        # 1
        graph.add_node(250, 350, "C")        # 2
        graph.add_node(400, 100, "D")        # 3
        graph.add_node(400, 250, "E")        # 4
        graph.add_node(400, 400, "F")        # 5
        graph.add_node(550, 250, "Arrivée")  # 6
        
        # Arêtes avec poids variés
        graph.add_edge(0, 1, 4)   # Départ → B
        graph.add_edge(0, 2, 2)   # Départ → C
        graph.add_edge(1, 3, 3)   # B → D
        graph.add_edge(1, 4, 5)   # B → E
        graph.add_edge(2, 4, 1)   # C → E
        graph.add_edge(2, 5, 8)   # C → F
        graph.add_edge(3, 6, 4)   # D → Arrivée
        graph.add_edge(4, 6, 3)   # E → Arrivée
        graph.add_edge(5, 6, 2)   # F → Arrivée
        
        return graph
    
    @staticmethod
    def create_mst_example() -> Graph:
        """
        Graphe pour MST (Kruskal/Prim)
        Réseau de villes à connecter au coût minimal
        """
        graph = Graph(directed=False)
        
        # 6 villes
        positions = [
            (150, 150, "Ville A"),
            (350, 100, "Ville B"),
            (500, 200, "Ville C"),
            (150, 350, "Ville D"),
            (350, 400, "Ville E"),
            (500, 350, "Ville F")
        ]
        
        for x, y, label in positions:
            graph.add_node(x, y, label)
        
        # Connexions avec coûts
        edges = [
            (0, 1, 7),   # A-B
            (0, 3, 5),   # A-D
            (1, 2, 8),   # B-C
            (1, 3, 9),   # B-D
            (1, 4, 7),   # B-E
            (2, 4, 5),   # C-E
            (2, 5, 6),   # C-F
            (3, 4, 15),  # D-E
            (4, 5, 8),   # E-F
        ]
        
        for src, tgt, weight in edges:
            graph.add_edge(src, tgt, weight)
        
        return graph
    
    @staticmethod
    def create_bipartite_example() -> Graph:
        """
        Graphe biparti clair
        Étudiants (gauche) et Stages (droite)
        """
        graph = Graph(directed=False)
        
        # 4 étudiants (gauche)
        for i in range(4):
            graph.add_node(100, 100 + i * 80, f"Étudiant {i+1}")
        
        # 4 stages (droite)
        for i in range(4):
            graph.add_node(400, 100 + i * 80, f"Stage {chr(65+i)}")
        
        # Connexions (préférences)
        edges = [
            (0, 4), (0, 5),           # Étudiant 1 → Stage A, B
            (1, 5), (1, 6),           # Étudiant 2 → Stage B, C
            (2, 4), (2, 6), (2, 7),   # Étudiant 3 → Stage A, C, D
            (3, 7),                   # Étudiant 4 → Stage D
        ]
        
        for src, tgt in edges:
            graph.add_edge(src, tgt, 1)
        
        return graph
    
    @staticmethod
    def create_coloring_example() -> Graph:
        """
        Graphe pour coloration
        Exemple : Emploi du temps (cours qui ne peuvent pas être simultanés)
        """
        graph = Graph(directed=False)
        
        # 7 cours en cercle
        courses = ["Maths", "Info", "Physique", "Anglais", "Sport", "Histoire", "Chimie"]
        radius = 150
        cx, cy = 300, 250
        
        for i, course in enumerate(courses):
            angle = 2 * math.pi * i / len(courses) - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            graph.add_node(x, y, course)
        
        # Conflits (même prof, même salle, etc.)
        conflicts = [
            (0, 1), (0, 2),  # Maths conflits
            (1, 2), (1, 4),  # Info conflits
            (2, 6),          # Physique-Chimie
            (3, 4),          # Anglais-Sport
            (4, 5),          # Sport-Histoire
            (5, 6),          # Histoire-Chimie
            (0, 3),          # Maths-Anglais
        ]
        
        for src, tgt in conflicts:
            graph.add_edge(src, tgt, 1)
        
        return graph
    
    @staticmethod
    def create_dag_example() -> Graph:
        """
        Graphe orienté acyclique (DAG)
        Pour tri topologique / ordonnancement de tâches
        """
        graph = Graph(directed=True)
        
        # Tâches d'un projet
        tasks = [
            (100, 100, "Cahier charges"),    # 0
            (250, 50, "Design UI"),          # 1
            (250, 150, "Base données"),      # 2
            (400, 100, "Backend"),           # 3
            (400, 200, "Frontend"),          # 4
            (550, 150, "Tests"),             # 5
            (700, 150, "Déploiement")        # 6
        ]
        
        for x, y, label in tasks:
            graph.add_node(x, y, label)
        
        # Dépendances (orientées)
        dependencies = [
            (0, 1), (0, 2),  # Cahier → Design & BDD
            (1, 4),          # Design → Frontend
            (2, 3),          # BDD → Backend
            (3, 4), (3, 5),  # Backend → Frontend & Tests
            (4, 5),          # Frontend → Tests
            (5, 6),          # Tests → Déploiement
        ]
        
        for src, tgt in dependencies:
            graph.add_edge(src, tgt, 1)
        
        return graph
    
    # ==================== ACCÈS CENTRALISÉ ====================
    
    @staticmethod
    def get_all_graphs():
        """
        Retourne un dictionnaire de tous les graphes disponibles
        Organisés par catégorie
        """
        return {
            "Formes de base": {
                "Chaîne (5 sommets)": GraphLibrary.create_chain,
                "Cycle (6 sommets)": GraphLibrary.create_cycle,
                "Étoile (centre + 6 branches)": GraphLibrary.create_star,
                "Complet K5": lambda: GraphLibrary.create_complete(5),
                "Arbre binaire": lambda: GraphLibrary.create_binary_tree(3),
                "Grille 3×3": lambda: GraphLibrary.create_grid(3, 3),
            },
            "Graphes historiques": {
                "🌉 Ponts de Königsberg": GraphLibrary.create_konigsberg,
                "🏠 3 maisons, 3 services (K3,3)": GraphLibrary.create_utilities,
                "⭐ Graphe de Petersen": GraphLibrary.create_petersen,
            },
            "Exercices types": {
                "Dijkstra (plus court chemin)": GraphLibrary.create_dijkstra_example,
                "MST (arbre couvrant)": GraphLibrary.create_mst_example,
                "Biparti (étudiants/stages)": GraphLibrary.create_bipartite_example,
                "Coloration (emploi du temps)": GraphLibrary.create_coloring_example,
                "DAG (ordonnancement tâches)": GraphLibrary.create_dag_example,
            },
            "Connexité & Cycles": {
                "Graphe déconnecté (3 composantes)": GraphLibrary.create_disconnected,
                "Avec cycle évident": GraphLibrary.create_with_cycle,
                "Arbre (sans cycle)": GraphLibrary.create_tree_no_cycle,
                "Circuit eulérien possible": GraphLibrary.create_eulerian_circuit,
                "Chemin eulérien seulement": GraphLibrary.create_eulerian_path_only,
            }
        }
    
    # ====================  ====================

    @staticmethod
    def create_disconnected() -> Graph:
        """
        Graphe déconnecté (3 composantes)
        Utile pour test des composantes connexes
        """
        graph = Graph(directed=False)
        
        # Composante 1 : Triangle
        graph.add_node(100, 150, "A")
        graph.add_node(200, 100, "B")
        graph.add_node(200, 200, "C")
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 0, 1)
        
        # Composante 2 : Chaîne
        graph.add_node(350, 150, "D")
        graph.add_node(450, 150, "E")
        graph.add_edge(3, 4, 1)
        
        # Composante 3 : Sommet isolé
        graph.add_node(300, 300, "F")
        
        return graph
    
    @staticmethod
    def create_with_cycle() -> Graph:
        """
        Graphe simple avec un cycle évident
        Utile pour détection de cycles
        """
        graph = Graph(directed=False)
        
        # Carré avec diagonale
        graph.add_node(150, 150, "A")
        graph.add_node(350, 150, "B")
        graph.add_node(350, 350, "C")
        graph.add_node(150, 350, "D")
        
        # Cycle : A-B-C-D-A
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)
        graph.add_edge(3, 0, 1)
        
        # Une arête supplémentaire
        graph.add_edge(0, 2, 2)  # Diagonale
        
        return graph
    
    @staticmethod
    def create_tree_no_cycle() -> Graph:
        """
        Arbre (pas de cycle)
        Utile pour vérifier détection
        """
        graph = Graph(directed=False)
        
        # Arbre simple
        graph.add_node(250, 100, "A")    # Racine
        graph.add_node(150, 200, "B")
        graph.add_node(350, 200, "C")
        graph.add_node(100, 300, "D")
        graph.add_node(200, 300, "E")
        graph.add_node(300, 300, "F")
        graph.add_node(400, 300, "G")
        
        graph.add_edge(0, 1, 1)  # A-B
        graph.add_edge(0, 2, 1)  # A-C
        graph.add_edge(1, 3, 1)  # B-D
        graph.add_edge(1, 4, 1)  # B-E
        graph.add_node(2, 5, 1)  # C-F
        graph.add_edge(2, 6, 1)  # C-G
        
        return graph
    
    @staticmethod
    def create_eulerian_circuit() -> Graph:
        """
        Graphe avec circuit eulérien
        Tous les sommets de degré pair
        """
        graph = Graph(directed=False)
        
        # Hexagone (tous les sommets degré 2)
        n = 6
        radius = 150
        cx, cy = 300, 250
        
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            graph.add_node(x, y)
        
        # Cycle
        for i in range(n):
            graph.add_edge(i, (i + 1) % n, 1)
        
        return graph
    
    @staticmethod
    def create_eulerian_path_only() -> Graph:
        """
        Graphe avec chemin eulérien mais pas circuit
        Exactement 2 sommets de degré impair
        """
        graph = Graph(directed=False)
        
        # Chaîne simple (extrémités = degré 1 impair)
        positions = [
            (100, 250, "A"),   # Degré 1 (impair)
            (200, 250, "B"),   # Degré 2
            (300, 250, "C"),   # Degré 2
            (400, 250, "D"),   # Degré 2
            (500, 250, "E"),   # Degré 1 (impair)
        ]
        
        for i, (x, y, label) in enumerate(positions):
            graph.add_node(x, y, label)
        
        for i in range(4):
            graph.add_edge(i, i + 1, 1)
        
        return graph
