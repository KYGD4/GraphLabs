# 🤝 Guide de contribution - GraphLabs

Merci de votre intérêt pour contribuer à GraphLabs ! Ce document vous guidera dans le processus de contribution.

## 📋 Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Structure du projet](#structure-du-projet)
- [Configuration de l'environnement](#configuration-de-lenvironnement)
- [Standards de code](#standards-de-code)
- [Tests](#tests)
- [Soumettre une Pull Request](#soumettre-une-pull-request)

---

## 📜 Code de conduite

En participant à ce projet, vous acceptez de respecter notre [Code de conduite](CODE_OF_CONDUCT.md). Soyez respectueux, inclusif et constructif.

---

## 🚀 Comment contribuer

### Types de contributions

#### 1. 🐛 Reporter un bug

Si vous trouvez un bug :

1. Vérifiez qu'il n'est pas déjà [reporté](https://github.com/yourusername/graphlabs/issues)
2. Créez une nouvelle Issue avec le template "Bug Report"
3. Incluez :
   - Description du problème
   - Étapes pour reproduire
   - Comportement attendu vs réel
   - Captures d'écran si possible
   - Environnement (OS, version Python, etc.)

#### 2. ✨ Proposer une fonctionnalité

Pour suggérer une nouvelle fonctionnalité :

1. Créez une Issue avec le template "Feature Request"
2. Décrivez :
   - Le problème que ça résout
   - Votre solution proposée
   - Des alternatives envisagées
   - L'impact sur les utilisateurs

#### 3. 📚 Améliorer la documentation

La documentation est cruciale ! Vous pouvez :

- Corriger des fautes de frappe
- Clarifier des explications
- Ajouter des exemples
- Traduire en d'autres langues

#### 4. 💻 Coder une fonctionnalité

Voir la section [Soumettre une Pull Request](#soumettre-une-pull-request).

---

## 📁 Structure du projet

```
graphlabs/
├── graphlabs/              # Code source principal
│   ├── core/              # Structures de données (Graph, Node, Edge)
│   ├── ui/                # Interface graphique (Qt)
│   ├── algorithms/        # Algorithmes de graphes
│   │   ├── traversal/    # DFS, BFS, etc.
│   │   ├── shortest_path/ # Dijkstra, Bellman-Ford, etc.
│   │   └── ...
│   └── utils/             # Utilitaires (file_handler, graph_library)
├── tests/                  # Tests unitaires
├── docs/                   # Documentation
├── requirements.txt        # Dépendances
├── setup.py               # Configuration d'installation
└── README.md              # Readme principal
```

---

## ⚙️ Configuration de l'environnement

### 1. Fork et clone

```bash
# Fork sur GitHub, puis :
git clone https://github.com/VOTRE_USERNAME/graphlabs.git
cd graphlabs
```

### 2. Créer une branche

```bash
git checkout -b feature/nom-de-votre-feature
# ou
git checkout -b fix/nom-du-bug
```

### 3. Environnement virtuel

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
pip install -e .  # Installation en mode développement

# Dépendances de dev (tests, linting)
pip install pytest pytest-qt black flake8
```

### 5. Vérifier l'installation

```bash
python -m graphlabs.main
# L'application devrait se lancer
```

---

## 📐 Standards de code

### Style Python : PEP 8

Nous suivons [PEP 8](https://pep8.org/) avec quelques ajustements :

- **Longueur de ligne** : 100 caractères max
- **Indentation** : 4 espaces (pas de tabs)
- **Imports** : Groupés et triés (stdlib, third-party, local)
- **Docstrings** : Format Google

### Formatage automatique

Utilisez **Black** pour le formatage :

```bash
black graphlabs/
```

### Linting

Vérifiez avec **Flake8** :

```bash
flake8 graphlabs/ --max-line-length=100
```

### Type hints

Utilisez les type hints pour les fonctions publiques :

```python
def add_node(self, x: float, y: float, label: str = "") -> int:
    """Ajoute un sommet au graphe."""
    pass
```

### Docstrings

Format Google :

```python
def dijkstra(graph: Graph, start: int, end: int) -> Tuple[List[int], float]:
    """
    Calcule le plus court chemin avec l'algorithme de Dijkstra.
    
    Args:
        graph: Le graphe à analyser
        start: Sommet de départ
        end: Sommet d'arrivée
        
    Returns:
        Tuple contenant:
        - Liste des sommets du chemin
        - Distance totale
        
    Raises:
        ValueError: Si start ou end n'existe pas dans le graphe
        
    Example:
        >>> path, dist = dijkstra(graph, 0, 5)
        >>> print(path)
        [0, 2, 4, 5]
    """
    pass
```

---

## 🧪 Tests

### Écrire des tests

Chaque nouvelle fonctionnalité doit être testée :

```python
# tests/test_algorithms/test_dijkstra.py
import pytest
from graphlabs.core.graph import Graph
from graphlabs.algorithms.shortest_path.dijkstra import DijkstraModule

def test_dijkstra_simple():
    """Test Dijkstra sur un graphe simple."""
    graph = Graph()
    n1 = graph.add_node(0, 0, "A")
    n2 = graph.add_node(100, 0, "B")
    n3 = graph.add_node(200, 0, "C")
    
    graph.add_edge(n1, n2, 5)
    graph.add_edge(n2, n3, 3)
    graph.add_edge(n1, n3, 10)
    
    # Mock canvas
    from unittest.mock import Mock
    canvas = Mock()
    
    module = DijkstraModule(graph, canvas)
    result = module.run(start_node=n1, end_node=n3)
    
    assert "A → B → C" in result
    assert "8" in result  # Distance 5 + 3
```

### Lancer les tests

```bash
# Tous les tests
pytest

# Un fichier spécifique
pytest tests/test_algorithms/test_dijkstra.py

# Avec couverture
pytest --cov=graphlabs --cov-report=html
```

### Tests d'interface (PyQt6)

Utilisez `pytest-qt` :

```python
def test_add_node_button(qtbot):
    """Test du bouton d'ajout de sommet."""
    from graphlabs.ui.main_window import GraphLabsWindow
    
    window = GraphLabsWindow()
    qtbot.addWidget(window)
    
    # Simuler clic
    qtbot.mouseClick(window.btn_add_node, Qt.LeftButton)
    
    assert window.canvas.mode == "add_node"
```

---

## 📤 Soumettre une Pull Request

### 1. Commits

Messages de commit clairs et descriptifs :

```bash
# Format : type(scope): description

git commit -m "feat(algorithms): Add Bellman-Ford algorithm"
git commit -m "fix(ui): Fix combobox selection bug"
git commit -m "docs: Update installation guide"
git commit -m "test: Add tests for DFS module"
```

**Types** :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage (pas de changement de code)
- `refactor`: Refactoring
- `test`: Ajout/modification de tests
- `chore`: Maintenance (dépendances, config)

### 2. Push

```bash
git push origin feature/nom-de-votre-feature
```

### 3. Créer la Pull Request

Sur GitHub :

1. Cliquez sur "New Pull Request"
2. Sélectionnez votre branche
3. Remplissez le template :
   - **Description** : Qu'est-ce que ça fait ?
   - **Motivation** : Pourquoi c'est nécessaire ?
   - **Tests** : Comment l'avez-vous testé ?
   - **Screenshots** : Si changement UI
4. Cochez les cases de validation
5. Soumettez !

### 4. Review

Un mainteneur reviewera votre PR :

- ✅ **Approuvée** : Sera mergée
- 💬 **Commentaires** : Demandes de modifications
- ❌ **Changes requested** : À corriger avant merge

### 5. Après le merge

```bash
# Mettre à jour votre fork
git checkout main
git pull upstream main
git push origin main

# Supprimer la branche
git branch -d feature/nom-de-votre-feature
```

---

## 🎨 Contribuer à l'UI

### Design guidelines

- **Couleurs** : Suivre les constantes dans `core/constants.py`
- **Responsive** : Tester à différentes résolutions
- **Accessibilité** : Contraste, taille de police
- **Cohérence** : Respecter le style existant

### Ajouter un nouvel algorithme

1. **Créer le module** : `graphlabs/algorithms/category/my_algorithm.py`

```python
from graphlabs.algorithms.base import AlgorithmModule

class MyAlgorithmModule(AlgorithmModule):
    def run(self, **kwargs) -> str:
        # Votre algorithme ici
        return "Résultat"
    
    def get_description(self) -> str:
        return "Description pédagogique"
    
    def get_complexity(self) -> str:
        return "Temps: O(?) | Espace: O(?)"
```

2. **Ajouter des tests** : `tests/test_algorithms/test_my_algorithm.py`

3. **Intégrer à l'UI** : Dans `main_window.py`, ajouter à `self.algorithms`

4. **Documenter** : Ajouter dans `docs/algorithms/my_algorithm.md`

---

## 📚 Contribuer à la documentation

### Structure

```
docs/
├── guides/           # Guides utilisateurs
├── tutorials/        # Tutoriels pas-à-pas
├── technical/        # Documentation technique
└── algorithms/       # Explication des algorithmes
```

### Écrire un tutoriel

Format Markdown avec captures d'écran :

```markdown
# Titre du tutoriel

## Objectif

Ce que l'utilisateur va apprendre.

## Prérequis

- Notion X
- Avoir fait le tutoriel Y

## Étapes

### 1. Première étape

![Screenshot](../images/tutorial_step1.png)

Instructions claires...

### 2. Deuxième étape

...

## Conclusion

Récapitulatif et prochaines étapes.
```

---

## 🌍 Traductions

GraphLabs vise à être multilingue (v2.0).

### Ajouter une langue

1. Créer `graphlabs/locales/fr_FR.json` (exemple)

```json
{
  "menu": {
    "file": "Fichier",
    "new": "Nouveau",
    "open": "Ouvrir"
  },
  "algorithms": {
    "dfs": "Parcours en profondeur",
    "bfs": "Parcours en largeur"
  }
}
```

2. Traduire tous les strings de l'UI

3. Tester l'affichage

---

## 🐛 Débugger

### Logs

Utilisez le module `logging` :

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug info")
logger.info("Info message")
logger.error("Error occurred")
```

### Mode debug

Lancer avec traces :

```bash
python -m graphlabs.main --debug
```

### Profiling

Pour optimiser les performances :

```bash
python -m cProfile -o output.prof -m graphlabs.main
```

---

## ❓ Besoin d'aide ?

- **Questions** : [GitHub Discussions](https://github.com/yourusername/graphlabs/discussions)
- **Chat** : Discord (lien à venir)
- **Email** : contribute@graphlabs.dev

---

## 🙏 Merci !

Chaque contribution compte, qu'elle soit grande ou petite. Merci de faire de GraphLabs un meilleur outil éducatif ! ❤️

---

**Happy Coding! 🚀**
