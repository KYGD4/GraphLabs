"""
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
        
        # Si start_node est None, prendre le premier sommet
        if start_node is None:
            start = next(iter(self.graph.nodes))
        else:
            start = start_node
            
        # Vérifier que le sommet existe
        if start not in self.graph.nodes:
            return f"Erreur : Le sommet {start} n'existe pas dans le graphe"
            
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
        
        # Obtenir les labels
        def get_label(node_id):
            return self.graph.nodes[node_id].label if node_id in self.graph.nodes else str(node_id)
        
        start_label = get_label(start)
        order_labels = [get_label(node) for node in order]
        
        return (f"DFS depuis le sommet {start_label} :\n\n"
                f"Ordre de visite : {' → '.join(order_labels)}\n"
                f"Sommets visités : {len(visited)} / {len(self.graph.nodes)}")
        
    def get_description(self) -> str:
        return ("Parcours en Profondeur (DFS) :\n\n"
                "Explore un graphe en allant le plus loin possible sur chaque branche "
                "avant de revenir en arrière. Utilise une pile (ou la récursion).\n\n"
                "• Sélectionnez un sommet de départ dans la liste\n"
                "• Ou laissez '(Auto)' pour démarrer du premier sommet\n\n"
                "Applications : Détection de cycles, tri topologique, composantes connexes.")
    
    def get_complexity(self) -> str:
        return "Temps : O(V + E) | Espace : O(V)"