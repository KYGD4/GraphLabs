"""
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
