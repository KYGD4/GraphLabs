"""Tests pour la classe Graph"""

import pytest
from graphlabs.core.graph import Graph, Node, Edge

def test_add_node():
    g = Graph()
    node_id = g.add_node(100, 200, "A")
    assert node_id == 0
    assert len(g.nodes) == 1
    assert g.nodes[0].label == "A"

def test_add_edge():
    g = Graph()
    n1 = g.add_node(0, 0)
    n2 = g.add_node(100, 100)
    g.add_edge(n1, n2, 5.0)
    assert len(g.edges) == 1
    assert g.edges[0].weight == 5.0

def test_get_neighbors():
    g = Graph()
    n1 = g.add_node(0, 0)
    n2 = g.add_node(100, 100)
    n3 = g.add_node(200, 200)
    g.add_edge(n1, n2)
    g.add_edge(n1, n3)
    neighbors = g.get_neighbors(n1)
    assert len(neighbors) == 2
    assert n2 in neighbors
    assert n3 in neighbors
