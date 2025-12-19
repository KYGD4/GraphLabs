"""
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
        
        # Si start_node est None, prendre le premier sommet
        if start_node is None:
            start = next(iter(self.graph.nodes))
        else:
            start = start_node
            
        # Vérifier que le sommet de départ existe
        if start not in self.graph.nodes:
            return f"Erreur : Le sommet de départ {start} n'existe pas dans le graphe"
        
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
                                     (not self.graph.directed and e.target == curr and e.source == neighbor)), 1)
                distance = curr_dist + edge_weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = curr
                    heapq.heappush(pq, (distance, neighbor))
        
        # Obtenir les labels des sommets
        def get_label(node_id):
            return self.graph.nodes[node_id].label if node_id in self.graph.nodes else str(node_id)
        
        # Si end_node spécifié et existe dans le graphe
        if end_node is not None and end_node in self.graph.nodes:
            if distances[end_node] == float('inf'):
                return f"Aucun chemin trouvé entre {get_label(start)} et {get_label(end_node)}"
            
            # Reconstruire le chemin
            path = []
            curr = end_node
            while curr in previous or curr == start:
                path.append(curr)
                if curr == start:
                    break
                curr = previous.get(curr)
                if curr is None:
                    break
            
            if not path or path[-1] != start:
                return f"Aucun chemin trouvé entre {get_label(start)} et {get_label(end_node)}"
            
            path.reverse()
            
            # Surbrillance du chemin
            self.canvas.highlight_nodes(set(path))
            
            # Créer les arêtes du chemin pour la surbrillance
            path_edges = set()
            for i in range(len(path) - 1):
                path_edges.add((path[i], path[i+1]))
            self.canvas.highlight_edges(path_edges)
            
            # Formatter le résultat avec labels
            path_labels = [get_label(node) for node in path]
            
            return (f"Plus court chemin de {get_label(start)} à {get_label(end_node)} :\n\n"
                   f"Chemin : {' → '.join(path_labels)}\n"
                   f"Distance totale : {distances[end_node]:.0f}\n"
                   f"Nombre de sommets : {len(path)}")
        
        # Sinon, afficher toutes les distances depuis start
        result = f"Distances depuis le sommet {get_label(start)} :\n\n"
        
        # Trier par distance puis par ID
        sorted_distances = sorted(distances.items(), key=lambda x: (x[1], x[0]))
        
        for node_id, dist in sorted_distances:
            dist_str = f"{dist:.0f}" if dist != float('inf') else "∞"
            label = get_label(node_id)
            
            # Afficher aussi le chemin si accessible
            if dist != float('inf') and node_id != start:
                # Reconstruire le chemin
                path = []
                curr = node_id
                while curr in previous or curr == start:
                    path.append(curr)
                    if curr == start:
                        break
                    curr = previous.get(curr)
                    if curr is None:
                        break
                path.reverse()
                path_labels = [get_label(n) for n in path]
                result += f"  {label:10} : {dist_str:>6} via {' → '.join(path_labels)}\n"
            else:
                result += f"  {label:10} : {dist_str:>6}\n"
        
        # NE PAS surbriller tous les sommets, juste le sommet de départ
        self.canvas.highlight_nodes({start})
        self.canvas.highlight_edges(set())
        
        return result.strip()
        
    def get_description(self) -> str:
        return ("Algorithme de Dijkstra :\n\n"
                "Trouve le plus court chemin dans un graphe pondéré avec poids positifs. "
                "Utilise une file de priorité pour explorer les sommets par ordre de distance croissante.\n\n"
                "• Sélectionnez un sommet de départ dans la liste\n"
                "• Optionnel : Sélectionnez un sommet d'arrivée pour voir le chemin\n"
                "• Si pas d'arrivée : affiche toutes les distances depuis le départ\n\n"
                "Limitation : Ne fonctionne pas avec des poids négatifs.")
    
    def get_complexity(self) -> str:
        return "Temps : O((V + E) log V) | Espace : O(V)"