"""
Circuit et chemin eulériens
Problème historique des ponts de Königsberg (Euler, 1736)
"""

from graphlabs.algorithms.base import AlgorithmModule
from typing import List, Dict, Set, Tuple
from collections import defaultdict

class EulerianModule(AlgorithmModule):
    """
    Vérifie et construit des circuits/chemins eulériens
    Circuit eulérien : passe par chaque ARÊTE exactement une fois
    """
    
    def run(self, start_node: int = None) -> str:
        """
        Vérifie les conditions eulériennes et tente de construire un circuit
        
        Returns:
            Analyse eulérienne du graphe
        """
        if not self.graph.nodes:
            return "Graphe vide"
        
        if not self.graph.edges:
            return "Aucune arête dans le graphe"
        
        # Calculer les degrés
        degrees = self._compute_degrees()
        
        # Obtenir labels
        def get_label(node_id):
            return self.graph.nodes[node_id].label if node_id in self.graph.nodes else str(node_id)
        
        result = "🌉 ANALYSE EULÉRIENNE\n"
        result += "=" * 50 + "\n\n"
        
        if self.graph.directed:
            return self._analyze_directed(degrees, get_label)
        else:
            return self._analyze_undirected(degrees, get_label)
    
    def _analyze_undirected(self, degrees: Dict[int, int], get_label) -> str:
        """Analyse pour graphes non-orientés"""
        result = "📊 Degrés des sommets :\n"
        for node_id in sorted(degrees.keys()):
            label = get_label(node_id)
            deg = degrees[node_id]
            parity = "pair ✓" if deg % 2 == 0 else "impair ✗"
            result += f"   {label:10} : {deg:2} ({parity})\n"
        
        result += "\n📐 THÉORÈME D'EULER :\n\n"
        
        # Analyser les degrés
        odd_degree_nodes = [node for node, deg in degrees.items() if deg % 2 == 1]
        num_odd = len(odd_degree_nodes)
        
        if num_odd == 0:
            result += "✅ CIRCUIT EULÉRIEN EXISTE !\n\n"
            result += "Condition : Tous les sommets sont de degré PAIR\n"
            result += f"   → {len(degrees)} sommets pairs, 0 impair\n\n"
            
            # Tenter de construire le circuit
            start_node = next(iter(self.graph.nodes))  # Définir start_node ici
            
            circuit = self._find_eulerian_circuit(start_node)
            
            if circuit:
                result += "🎯 Circuit trouvé (algorithme de Hierholzer) :\n\n"
                labels = [get_label(n) for n in circuit]
                
                # Afficher par lignes de 8 sommets max
                line_length = 8
                for i in range(0, len(labels), line_length):
                    chunk = labels[i:i+line_length]
                    result += "   " + " → ".join(chunk)
                    if i + line_length < len(labels):
                        result += " →\n"
                    else:
                        result += "\n"
                
                result += f"\n   Longueur : {len(circuit) - 1} arêtes\n"
                result += f"   (Toutes les {len(self.graph.edges)} arêtes traversées !)\n\n"
                
                # Surbrillance
                self.canvas.highlight_nodes(set(circuit))
                path_edges = set()
                for i in range(len(circuit) - 1):
                    path_edges.add((circuit[i], circuit[i+1]))
                self.canvas.highlight_edges(path_edges)
            
        elif num_odd == 2:
            result += "✅ CHEMIN EULÉRIEN EXISTE !\n\n"
            result += "Condition : Exactement 2 sommets de degré IMPAIR\n"
            result += f"   → {len(degrees) - 2} sommets pairs, 2 impairs\n\n"
            result += "Sommets impairs (extrémités du chemin) :\n"
            for node in odd_degree_nodes:
                result += f"   • {get_label(node)} (degré {degrees[node]})\n"
            result += "\n"
            result += "💡 Il faut partir d'un sommet impair et arriver à l'autre.\n\n"
            
            # Construire chemin depuis premier sommet impair
            path = self._find_eulerian_path(odd_degree_nodes[0], odd_degree_nodes[1])
            
            if path:
                result += "🎯 Chemin trouvé :\n\n"
                labels = [get_label(n) for n in path]
                
                line_length = 8
                for i in range(0, len(labels), line_length):
                    chunk = labels[i:i+line_length]
                    result += "   " + " → ".join(chunk)
                    if i + line_length < len(labels):
                        result += " →\n"
                    else:
                        result += "\n"
                
                result += f"\n   Longueur : {len(path) - 1} arêtes\n\n"
                
                # Surbrillance
                self.canvas.highlight_nodes(set(path))
            
        else:
            result += "❌ NI CIRCUIT NI CHEMIN EULÉRIEN\n\n"
            result += f"Condition violée : {num_odd} sommets de degré impair\n"
            result += f"   (Il en faut 0 ou exactement 2)\n\n"
            result += "Sommets de degré impair :\n"
            for node in odd_degree_nodes:
                result += f"   • {get_label(node)} (degré {degrees[node]})\n"
            result += "\n"
            result += "💡 Pour rendre le graphe eulérien :\n"
            result += "   Il faudrait ajouter/supprimer des arêtes pour\n"
            result += "   que tous les sommets soient de degré pair.\n\n"
            
            # Surbrillance des problématiques
            self.canvas.highlight_nodes(set(odd_degree_nodes))
        return result
    
    def _analyze_directed(self, degrees: Dict[int, Tuple[int, int]], get_label) -> str:
        """Analyse pour graphes orientés"""
        result = "📊 Degrés entrants/sortants :\n"
        
        balanced_nodes = []
        start_candidates = []  # out - in = +1
        end_candidates = []    # out - in = -1
        other_unbalanced = []  # diff != 0, +1, -1
        
        for node_id in sorted(degrees.keys()):
            label = get_label(node_id)
            in_deg, out_deg = degrees[node_id]
            diff = out_deg - in_deg
            
            status = "✓" if diff == 0 else "✗"
            result += f"   {label:10} : in={in_deg}, out={out_deg}, diff={diff:+d} {status}\n"
            
            if diff == 0:
                balanced_nodes.append(node_id)
            elif diff == 1:
                start_candidates.append(node_id)
            elif diff == -1:
                end_candidates.append(node_id)
            else:
                other_unbalanced.append((node_id, diff))
        
        result += "\n📐 THÉORÈME D'EULER (graphe orienté) :\n\n"
        
        # Vérifier conditions
        has_circuit = (len(start_candidates) == 0 and len(end_candidates) == 0 and 
                      len(other_unbalanced) == 0)
        has_path = (len(start_candidates) == 1 and len(end_candidates) == 1 and 
                   len(other_unbalanced) == 0)
        
        if has_circuit:
            result += "✅ CIRCUIT EULÉRIEN EXISTE !\n\n"
            result += "Condition : in_degree = out_degree pour TOUS les sommets\n"
            result += f"   → {len(degrees)} sommets équilibrés\n\n"
            
            # Construire le circuit
            start = next(iter(self.graph.nodes))
            circuit = self._find_eulerian_circuit(start)
            
            if circuit:
                result += "🎯 Circuit trouvé :\n\n"
                labels = [get_label(n) for n in circuit]
                
                line_length = 8
                for i in range(0, len(labels), line_length):
                    chunk = labels[i:i+line_length]
                    result += "   " + " → ".join(chunk)
                    if i + line_length < len(labels):
                        result += " →\n"
                    else:
                        result += "\n"
                
                result += f"\n   Longueur : {len(circuit) - 1} arêtes\n\n"
                
                # Surbrillance
                self.canvas.highlight_nodes(set(circuit))
                path_edges = set()
                for i in range(len(circuit) - 1):
                    path_edges.add((circuit[i], circuit[i+1]))
                self.canvas.highlight_edges(path_edges)
                
        elif has_path:
            result += "✅ CHEMIN EULÉRIEN EXISTE !\n\n"
            result += "Conditions :\n"
            result += "  • 1 sommet avec out_degree - in_degree = +1 (départ)\n"
            result += "  • 1 sommet avec out_degree - in_degree = -1 (arrivée)\n"
            result += "  • Autres sommets équilibrés\n\n"
            
            start = start_candidates[0]
            end = end_candidates[0]
            
            result += f"Départ : {get_label(start)} (out={degrees[start][1]} > in={degrees[start][0]})\n"
            result += f"Arrivée : {get_label(end)} (in={degrees[end][0]} > out={degrees[end][1]})\n\n"
            
            # Construire chemin
            path = self._find_eulerian_circuit(start)
            
            if path:
                result += "🎯 Chemin trouvé :\n\n"
                labels = [get_label(n) for n in path]
                
                line_length = 8
                for i in range(0, len(labels), line_length):
                    chunk = labels[i:i+line_length]
                    result += "   " + " → ".join(chunk)
                    if i + line_length < len(labels):
                        result += " →\n"
                    else:
                        result += "\n"
                
                result += f"\n   Longueur : {len(path) - 1} arêtes\n\n"
                
                # Surbrillance
                self.canvas.highlight_nodes(set(path))
        else:
            result += "❌ NI CIRCUIT NI CHEMIN EULÉRIEN\n\n"
            
            total_unbalanced = len(start_candidates) + len(end_candidates) + len(other_unbalanced)
            result += f"Sommets déséquilibrés : {total_unbalanced}\n\n"
            
            result += "Conditions pour circuit eulérien orienté :\n"
            result += "  → in_degree = out_degree pour TOUS les sommets\n\n"
            
            result += "Conditions pour chemin eulérien orienté :\n"
            result += "  → Exactement 1 sommet avec out - in = +1 (départ)\n"
            result += "  → Exactement 1 sommet avec out - in = -1 (arrivée)\n"
            result += "  → Tous les autres sommets équilibrés (diff = 0)\n\n"
            
            result += "État actuel :\n"
            result += f"  • Sommets équilibrés (diff=0) : {len(balanced_nodes)}\n"
            result += f"  • Sommets avec diff=+1 : {len(start_candidates)}\n"
            result += f"  • Sommets avec diff=-1 : {len(end_candidates)}\n"
            result += f"  • Autres déséquilibrés : {len(other_unbalanced)}\n\n"
            
            if other_unbalanced:
                result += "Sommets très déséquilibrés :\n"
                for node_id, diff in other_unbalanced:
                    in_d, out_d = degrees[node_id]
                    result += f"   • {get_label(node_id)}: in={in_d}, out={out_d}, diff={diff:+d}\n"
                result += "\n"
            
            # Surbrillance des problématiques
            problem_nodes = ([s for s in start_candidates] + 
                           [e for e in end_candidates] + 
                           [n for n, _ in other_unbalanced])
            self.canvas.highlight_nodes(set(problem_nodes))
        
        result += "\n"
        result += "📚 HISTOIRE :\n"
        result += "Le problème des 7 ponts de Königsberg (1736) :\n"
        result += "Euler a prouvé qu'il est impossible de traverser\n"
        result += "tous les ponts exactement une fois car le graphe\n"
        result += "correspondant a 4 sommets de degré impair.\n\n"
        result += "Chargez 'Ponts de Königsberg' dans la bibliothèque\n"
        result += "pour voir le graphe historique !\n"
        
        return result
    
    def _compute_degrees(self) -> Dict[int, int]:
        """Calcule le degré de chaque sommet (ou in/out pour orienté)"""
        if self.graph.directed:
            # Pour graphe orienté : in-degree et out-degree
            in_deg = defaultdict(int)
            out_deg = defaultdict(int)
            
            for edge in self.graph.edges:
                out_deg[edge.source] += 1
                in_deg[edge.target] += 1
            
            # Pour eulérien orienté : in_degree doit égaler out_degree
            # On retourne la différence pour analyse
            degrees = {}
            all_nodes = set(self.graph.nodes.keys())
            for node in all_nodes:
                degrees[node] = (in_deg[node], out_deg[node])
            
            return degrees
        else:
            # Graphe non-orienté
            degrees = defaultdict(int)
            
            for edge in self.graph.edges:
                degrees[edge.source] += 1
                degrees[edge.target] += 1
            
            return dict(degrees)
    
    def _find_eulerian_circuit(self, start: int) -> List[int]:
        """
        Algorithme de Hierholzer pour circuit eulérien
        """
        # Copier les arêtes (pour les "consommer")
        edges_left = defaultdict(list)
        for edge in self.graph.edges:
            edges_left[edge.source].append(edge.target)
            if not self.graph.directed:
                edges_left[edge.target].append(edge.source)
        
        circuit = []
        stack = [start]
        current = start
        
        while stack:
            if edges_left[current]:
                next_node = edges_left[current].pop()
                # Supprimer arête reverse si non-orienté
                if not self.graph.directed and current in edges_left[next_node]:
                    edges_left[next_node].remove(current)
                stack.append(next_node)
                current = next_node
            else:
                circuit.append(current)
                current = stack.pop()
        
        circuit.reverse()
        return circuit if len(circuit) > 1 else []
    
    def _find_eulerian_path(self, start: int, end: int) -> List[int]:
        """Trouve un chemin eulérien (similaire au circuit)"""
        # Même algorithme mais commence au sommet impair
        return self._find_eulerian_circuit(start)
        
    def get_description(self) -> str:
        return ("Circuit Eulérien :\n\n"
                "Chemin qui traverse chaque ARÊTE exactement une fois.\n\n"
                "Théorème d'Euler (1736) :\n"
                "• Circuit eulérien existe ⟺ tous les sommets de degré pair\n"
                "• Chemin eulérien existe ⟺ exactement 2 sommets impairs\n\n"
                "Différence avec Hamiltonien :\n"
                "• Eulérien : passe par chaque ARÊTE une fois\n"
                "• Hamiltonien : passe par chaque SOMMET une fois\n\n"
                "Problème historique : Ponts de Königsberg (1736)\n"
                "Premier théorème de théorie des graphes !")
    
    def get_complexity(self) -> str:
        return "Temps : O(E) | Espace : O(E)"