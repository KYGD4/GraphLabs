"""
Détection de cycles dans un graphe
"""

from graphlabs.algorithms.base import AlgorithmModule
from typing import Set, List, Optional, Tuple

class CycleDetectionModule(AlgorithmModule):
    """
    Détecte la présence de cycles dans un graphe
    Algorithme différent selon graphe orienté ou non
    """
    
    def run(self, start_node: int = None) -> str:
        """
        Détecte les cycles dans le graphe
        
        Returns:
            Information sur les cycles trouvés
        """
        if not self.graph.nodes:
            return "Graphe vide"
        
        if self.graph.directed:
            return self._detect_directed()
        else:
            return self._detect_undirected()
    
    def _detect_undirected(self) -> str:
        """Détection de tous les cycles dans graphe non-orienté"""
        all_cycles: List[List[int]] = []
        
        # Pour chaque sommet comme point de départ
        for start in sorted(self.graph.nodes.keys()):
            # Trouver tous les cycles simples passant par start
            cycles_from_start = self._find_cycles_undirected_from_node(start)
            
            for cycle in cycles_from_start:
                # Normaliser le cycle
                normalized = self._normalize_cycle(cycle)
                
                # Vérifier si on n'a pas déjà ce cycle
                if not any(self._normalize_cycle(existing) == normalized for existing in all_cycles):
                    all_cycles.append(cycle + [cycle[0]])  # Ajouter retour au début
        
        return self._format_cycles_result(all_cycles, False)
    
    def _find_cycles_undirected_from_node(self, start: int) -> List[List[int]]:
        """Trouve tous les cycles élémentaires contenant start (non-orienté)"""
        cycles = []
        
        def dfs(current: int, path: List[int], parent: Optional[int]):
            # Explorer tous les voisins
            for neighbor in sorted(self.graph.get_neighbors(current)):
                if neighbor == parent:
                    continue
                    
                if neighbor == start and len(path) >= 3:
                    # On compare le premier nœud après start (path[1]) 
                    # avec le nœud actuel (current) qui va fermer la boucle.
                    # Cela force un sens unique de parcours.
                    if path[1] < current:
                        cycles.append(path[:])
                    
                elif neighbor not in path and neighbor > start:
                    dfs(neighbor, path + [neighbor], current)
        
        # Commencer DFS depuis start
        dfs(start, [start], None)
        return cycles
    
    def _detect_directed(self) -> str:
        """Détection de tous les cycles dans graphe orienté (algorithme de Johnson simplifié)"""
        all_cycles: List[List[int]] = []
        
        # Pour chaque sommet comme point de départ potentiel
        for start in sorted(self.graph.nodes.keys()):
            # Trouver tous les cycles simples passant par start
            cycles_from_start = self._find_cycles_from_node(start)
            
            for cycle in cycles_from_start:
                # Normaliser le cycle (rotation pour commencer par le plus petit ID)
                normalized = self._normalize_cycle(cycle)
                
                # Vérifier si on n'a pas déjà ce cycle
                if not any(self._normalize_cycle(existing) == normalized for existing in all_cycles):
                    all_cycles.append(cycle + [cycle[0]])  # Ajouter retour au début
        
        return self._format_cycles_result(all_cycles, True)
    
    def _find_cycles_from_node(self, start: int) -> List[List[int]]:
        """Trouve tous les cycles élémentaires contenant start comme plus petit élément"""
        cycles = []
        blocked = set()
        block_map = {node: set() for node in self.graph.nodes}
        
        def unblock(node: int):
            blocked.discard(node)
            for w in list(block_map[node]):
                block_map[node].discard(w)
                if w in blocked:
                    unblock(w)
        
        def dfs(current: int, path: List[int]) -> bool:
            found_cycle = False
            blocked.add(current)
            
            for neighbor in self.graph.get_neighbors(current):
                if neighbor == start:
                    # Cycle trouvé !
                    cycles.append(path[:])
                    found_cycle = True
                elif neighbor not in blocked and neighbor > start:  # Condition > start évite doublons
                    if dfs(neighbor, path + [neighbor]):
                        found_cycle = True
            
            if found_cycle:
                unblock(current)
            else:
                for neighbor in self.graph.get_neighbors(current):
                    block_map[neighbor].add(current)
            
            return found_cycle
        
        dfs(start, [start])
        return cycles
    
    def _normalize_cycle(self, cycle: List[int]) -> Tuple[int, ...]:
        """Normalise un cycle pour éviter les doublons (rotation pour commencer par min)"""
        if not cycle:
            return tuple()
        min_val = min(cycle)
        min_idx = cycle.index(min_val)
        return tuple(cycle[min_idx:] + cycle[:min_idx])
    
    def _format_cycles_result(self, cycles: List[List[int]], is_directed: bool) -> str:
        """Formate le résultat avec tous les cycles"""
        def get_label(node_id):
            return self.graph.nodes[node_id].label if node_id in self.graph.nodes else str(node_id)
        
        if cycles:
            # Surbrillance de tous les sommets dans des cycles
            all_cycle_nodes = set()
            all_cycle_edges = set()
            
            for cycle in cycles:
                all_cycle_nodes.update(cycle[:-1])  # Sans dernier (répétition)
                for i in range(len(cycle) - 1):
                    if is_directed:
                        all_cycle_edges.add((cycle[i], cycle[i+1]))
                    else:
                        all_cycle_edges.add((min(cycle[i], cycle[i+1]), max(cycle[i], cycle[i+1])))
            
            self.canvas.highlight_nodes(all_cycle_nodes)
            self.canvas.highlight_edges(all_cycle_edges)
            
            result = f"🔴 {len(cycles)} CYCLE{'S' if len(cycles) > 1 else ''} DÉTECTÉ{'S' if len(cycles) > 1 else ''} !\n\n"
            
            # Afficher chaque cycle
            for i, cycle in enumerate(cycles, 1):
                labels = [get_label(n) for n in cycle]
                result += f"Cycle {i} ({len(cycle)-1} sommets) :\n"
                result += f"   {' → '.join(labels)}\n\n"
            
            # Statistiques
            result += "📊 Statistiques :\n"
            cycle_sizes = [len(c) - 1 for c in cycles]
            result += f"   • Nombre total de cycles : {len(cycles)}\n"
            result += f"   • Plus petit cycle : {min(cycle_sizes)} sommets\n"
            result += f"   • Plus grand cycle : {max(cycle_sizes)} sommets\n"
            result += f"   • Sommets dans des cycles : {len(all_cycle_nodes)}\n\n"
            
            result += "💡 Implications :\n"
            result += "   • Le graphe contient des boucles\n"
            result += "   • Ce n'est PAS un arbre\n"
            
            if is_directed:
                result += "   • Ce n'est PAS un DAG\n"
                result += "   • Tri topologique impossible\n"
        else:
            self.canvas.clear_highlights()
            
            result = "✅ AUCUN CYCLE\n\n"
            result += "Le graphe est ACYCLIQUE.\n\n"
            
            # Vérifier si c'est un arbre/DAG
            num_nodes = len(self.graph.nodes)
            num_edges = len(self.graph.edges)
            
            if is_directed:
                result += "🎯 C'est un DAG (Directed Acyclic Graph) !\n\n"
                result += "Propriétés utiles :\n"
                result += "   ✅ Tri topologique possible\n"
                result += "   ✅ Ordonnancement de tâches OK\n"
                result += "   ✅ Pas de dépendances circulaires\n\n"
                result += "💡 Applications :\n"
                result += "   • Compilation (dépendances)\n"
                result += "   • Gestion de projet\n"
                result += "   • Makefiles\n"
            else:
                if num_edges == num_nodes - 1:
                    result += "🌳 C'est un ARBRE !\n"
                    result += f"   • {num_nodes} sommets\n"
                    result += f"   • {num_edges} arêtes\n"
                    result += f"   • Formule vérifiée : E = V - 1\n"
                else:
                    result += "📊 Statistiques :\n"
                    result += f"   • {num_nodes} sommets\n"
                    result += f"   • {num_edges} arêtes\n"
                    if num_edges < num_nodes - 1:
                        result += "   • Forêt (plusieurs arbres)\n"
        
        return result
        
    def get_description(self) -> str:
        return ("Détection de Cycles :\n\n"
                "Trouve TOUS les cycles dans le graphe.\n\n"
                "Algorithmes :\n"
                "• Graphe NON-ORIENTÉ : DFS exhaustif\n"
                "• Graphe ORIENTÉ : DFS avec 3 couleurs\n\n"
                "Affiche :\n"
                "• Tous les cycles trouvés\n"
                "• Taille de chaque cycle\n"
                "• Statistiques (nombre, min/max)\n\n"
                "Applications :\n"
                "- Détection de deadlocks\n"
                "- Dépendances circulaires\n"
                "- Validation de DAG")
    
    def get_complexity(self) -> str:
        return "Temps : O(V + E) | Espace : O(V)"