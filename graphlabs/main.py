"""
Point d'entrée principal de GraphLabs
"""

import sys
from PyQt6.QtWidgets import QApplication
from graphlabs.ui.main_window import GraphLabsWindow

def main():
    """Lance l'application GraphLabs"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = GraphLabsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
