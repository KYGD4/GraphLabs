"""
Gestionnaire d'import/export de graphes
"""

import json
from pathlib import Path
from typing import Optional
from graphlabs.core.graph import Graph, Node, Edge

class FileHandler:
    """Gère l'enregistrement et le chargement de graphes"""
    
    @staticmethod
    def save_graph(graph: Graph, filepath: str) -> bool:
        """
        Sauvegarde un graphe au format JSON
        
        Args:
            graph: Le graphe à sauvegarder
            filepath: Chemin du fichier de sortie
            
        Returns:
            True si succès, False sinon
        """
        try:
            data = {
                "directed": graph.directed,
                "next_id": graph.next_id,
                "nodes": [
                    {
                        "id": node.id,
                        "x": node.x,
                        "y": node.y,
                        "label": node.label,
                        "color": node.color
                    }
                    for node in graph.nodes.values()
                ],
                "edges": [
                    {
                        "source": edge.source,
                        "target": edge.target,
                        "weight": edge.weight,
                        "directed": edge.directed,
                        "color": edge.color
                    }
                    for edge in graph.edges
                ]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    @staticmethod
    def load_graph(filepath: str) -> Optional[Graph]:
        """
        Charge un graphe depuis un fichier JSON
        
        Args:
            filepath: Chemin du fichier à charger
            
        Returns:
            Le graphe chargé ou None en cas d'erreur
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            graph = Graph(directed=data.get("directed", False))
            graph.next_id = data.get("next_id", 0)
            
            # Recréer les nœuds
            for node_data in data.get("nodes", []):
                node = Node(
                    id=node_data["id"],
                    x=node_data["x"],
                    y=node_data["y"],
                    label=node_data["label"],
                    color=node_data.get("color", "#4A90E2")
                )
                graph.nodes[node.id] = node
            
            # Recréer les arêtes
            for edge_data in data.get("edges", []):
                edge = Edge(
                    source=edge_data["source"],
                    target=edge_data["target"],
                    weight=edge_data.get("weight", 1),
                    directed=edge_data.get("directed", graph.directed),
                    color=edge_data.get("color", "#333333")
                )
                graph.edges.append(edge)
            
            return graph
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return None
    
    @staticmethod
    def export_to_graphml(graph: Graph, filepath: str) -> bool:
        """
        Exporte un graphe au format GraphML (compatible avec Gephi, yEd, etc.)
        
        Args:
            graph: Le graphe à exporter
            filepath: Chemin du fichier de sortie
            
        Returns:
            True si succès, False sinon
        """
        try:
            xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
            xml_content.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
            xml_content.append('  <key id="label" for="node" attr.name="label" attr.type="string"/>')
            xml_content.append('  <key id="weight" for="edge" attr.name="weight" attr.type="int"/>')
            xml_content.append('  <key id="x" for="node" attr.name="x" attr.type="double"/>')
            xml_content.append('  <key id="y" for="node" attr.name="y" attr.type="double"/>')
            
            graph_type = "directed" if graph.directed else "undirected"
            xml_content.append(f'  <graph id="G" edgedefault="{graph_type}">')
            
            # Nodes
            for node in graph.nodes.values():
                xml_content.append(f'    <node id="n{node.id}">')
                xml_content.append(f'      <data key="label">{node.label}</data>')
                xml_content.append(f'      <data key="x">{node.x}</data>')
                xml_content.append(f'      <data key="y">{node.y}</data>')
                xml_content.append('    </node>')
            
            # Edges
            for i, edge in enumerate(graph.edges):
                xml_content.append(f'    <edge id="e{i}" source="n{edge.source}" target="n{edge.target}">')
                xml_content.append(f'      <data key="weight">{edge.weight}</data>')
                xml_content.append('    </edge>')
            
            xml_content.append('  </graph>')
            xml_content.append('</graphml>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(xml_content))
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'export GraphML: {e}")
            return False
