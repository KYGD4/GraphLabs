"""
Algorithme de détection des composantes connexes
"""

from graphlabs.algorithms.base import AlgorithmModule
from typing import Dict, Set, List

class ConnectedComponentsModule(AlgorithmModule):
    """
    Trouve toutes les composantes connexes d'un graphe
    Une composante connexe = ensemble de sommets mutuellement accessibles
    """
    
    def run(self, start_node: int = None) -> str:
        """
        Identifie toutes les composantes connexes
        
        Returns:
            Description des composantes trouvées
        """
        if not self.graph.nodes:
            return "Graphe vide"
        
        # Dictionnaire : sommet -> numéro de composante
        components: Dict[int, int] = {}
        component_num = 0
        
        # DFS pour marquer une composante
        def dfs(node: int, comp_id: int):
            components[node] = comp_id
            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in components:
                    dfs(neighbor, comp_id)
        
        # Parcourir tous les sommets
        for node_id in self.graph.nodes:
            if node_id not in components:
                dfs(node_id, component_num)
                component_num += 1
        
        # Regrouper par composante
        comp_groups: Dict[int, List[int]] = {}
        for node_id, comp_id in components.items():
            if comp_id not in comp_groups:
                comp_groups[comp_id] = []
            comp_groups[comp_id].append(node_id)
        
        # Obtenir labels
        def get_label(node_id):
            return self.graph.nodes[node_id].label if node_id in self.graph.nodes else str(node_id)
        
        # Colorier les composantes différemment
        colors = [
            ("#FF6B6B", "Rouge"),
            ("#4ECDC4", "Turquoise"),
            ("#45B7D1", "Bleu ciel"),
            ("#FFA07A", "Saumon"),
            ("#98D8C8", "Vert d'eau"),
            ("#F7DC6F", "Jaune"),
            ("#BB8FCE", "Violet"),
            ("#85C1E2", "Bleu clair"),
            ("#F8B739", "Orange"),
            ("#52B788", "Vert")
        ]
        
        for comp_id, nodes in comp_groups.items():
            color_hex, color_name = colors[comp_id % len(colors)]
            for node_id in nodes:
                if node_id in self.graph.nodes:
                    self.graph.nodes[node_id].color = color_hex
        
        # Mettre à jour le canvas
        self.canvas.clear_highlights()
        self.canvas.update()
        
        # Construire le résultat
        num_components = len(comp_groups)
        
        if num_components == 1:
            result = "✅ Le graphe est CONNEXE\n\n"
            result += f"Tous les {len(self.graph.nodes)} sommets sont dans la même composante.\n"
        else:
            result = f"❌ Le graphe est DÉCONNECTÉ\n\n"
            result += f"Nombre de composantes connexes : {num_components}\n\n"
            
            for comp_id in sorted(comp_groups.keys()):
                nodes = comp_groups[comp_id]
                labels = [get_label(n) for n in sorted(nodes)]
                color_hex, color_name = colors[comp_id % len(colors)]
                
                result += f"📍 Composante {comp_id + 1} ({len(nodes)} sommets) - {color_name}\n"
                result += f"   Sommets : {', '.join(labels)}\n\n"
        
        # Statistiques
        sizes = [len(comp_groups[i]) for i in comp_groups]
        result += "📊 Statistiques :\n"
        result += f"   Plus grande composante : {max(sizes)} sommets\n"
        result += f"   Plus petite composante : {min(sizes)} sommets\n"
        result += f"   Taille moyenne : {sum(sizes) / len(sizes):.1f} sommets\n"
        
        return result
        
    def get_description(self) -> str:
        return ("Composantes Connexes :\n\n"
                "Identifie les groupes de sommets mutuellement accessibles. "
                "Deux sommets sont dans la même composante s'il existe un chemin entre eux.\n\n"
                "• Graphe CONNEXE : 1 seule composante\n"
                "• Graphe DÉCONNECTÉ : Plusieurs composantes\n\n"
                "Algorithme : DFS depuis chaque sommet non visité.\n\n"
                "Applications :\n"
                "- Réseaux sociaux : groupes d'amis\n"
                "- Réseaux routiers : zones accessibles\n"
                "- Réseaux électriques : sous-réseaux")
    
    def get_complexity(self) -> str:
        return "Temps : O(V + E) | Espace : O(V)"