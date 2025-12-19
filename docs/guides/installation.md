# 📦 Guide d'installation - GraphLabs

Guide détaillé pour installer GraphLabs sur différents systèmes d'exploitation.

---

## 📋 Prérequis

### Logiciels nécessaires

- **Python 3.9 ou supérieur**
- **pip** (gestionnaire de paquets Python)
- **git** (pour cloner le dépôt)

### Vérifier l'installation

```bash
# Vérifier Python
python3 --version  # ou python --version sur Windows
# Doit afficher : Python 3.9.x ou supérieur

# Vérifier pip
pip --version
# Doit afficher : pip 21.x.x ou supérieur

# Vérifier git
git --version
# Doit afficher : git version 2.x.x ou supérieur
```

---

## 🐧 Installation sur Linux

### Ubuntu / Debian

#### 1. Installer les prérequis

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

#### 2. Cloner le dépôt

```bash
cd ~
git clone https://github.com/yourusername/graphlabs.git
cd graphlabs
```

#### 3. Créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

Votre terminal devrait maintenant afficher `(venv)` au début de la ligne.

#### 4. Installer GraphLabs

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### 5. Lancer l'application

```bash
graphlabs
# ou
python -m graphlabs.main
```

#### 6. Créer un raccourci (optionnel)

Créer `~/.local/share/applications/graphlabs.desktop` :

```ini
[Desktop Entry]
Name=GraphLabs
Comment=Application de théorie des graphes
Exec=/home/VOTRE_USERNAME/graphlabs/venv/bin/python -m graphlabs.main
Icon=/home/VOTRE_USERNAME/graphlabs/docs/images/icon.png
Terminal=false
Type=Application
Categories=Education;Science;
```

Remplacer `VOTRE_USERNAME` par votre nom d'utilisateur.

### Fedora / RHEL / CentOS

```bash
# Installer prérequis
sudo dnf install python3 python3-pip git

# Puis suivre les étapes 2-5 d'Ubuntu
```

### Arch Linux

```bash
# Installer prérequis
sudo pacman -S python python-pip git

# Puis suivre les étapes 2-5 d'Ubuntu
```

---

## 🍎 Installation sur macOS

### Avec Homebrew (recommandé)

#### 1. Installer Homebrew

Si pas déjà installé :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Installer Python et git

```bash
brew install python git
```

#### 3. Cloner le dépôt

```bash
cd ~
git clone https://github.com/yourusername/graphlabs.git
cd graphlabs
```

#### 4. Créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Installer GraphLabs

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### 6. Lancer l'application

```bash
graphlabs
# ou
python -m graphlabs.main
```

### Créer une application macOS (optionnel)

Créer `GraphLabs.app` :

```bash
# Installer py2app
pip install py2app

# Créer le bundle
python setup.py py2app
```

L'application sera dans `dist/GraphLabs.app`.

---

## 🪟 Installation sur Windows

### Avec installateur Python officiel

#### 1. Installer Python

1. Télécharger depuis [python.org](https://www.python.org/downloads/)
2. Lancer l'installateur
3. ⚠️ **Cocher "Add Python to PATH"**
4. Cliquer "Install Now"

#### 2. Installer Git

1. Télécharger depuis [git-scm.com](https://git-scm.com/download/win)
2. Lancer l'installateur
3. Utiliser les options par défaut

#### 3. Ouvrir PowerShell

- Appuyer sur `Win + X`
- Choisir "Windows PowerShell" ou "Terminal"

#### 4. Cloner le dépôt

```powershell
cd ~
git clone https://github.com/yourusername/graphlabs.git
cd graphlabs
```

#### 5. Créer l'environnement virtuel

```powershell
python -m venv venv
venv\Scripts\activate
```

Vous devriez voir `(venv)` au début de la ligne.

#### 6. Installer GraphLabs

```powershell
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### 7. Lancer l'application

```powershell
graphlabs
# ou
python -m graphlabs.main
```

### Créer un raccourci Bureau

1. Créer un nouveau fichier `GraphLabs.bat` :

```batch
@echo off
cd C:\Users\VOTRE_USERNAME\graphlabs
call venv\Scripts\activate
python -m graphlabs.main
```

2. Créer un raccourci vers ce fichier sur le Bureau
3. Changer l'icône (propriétés → Changer l'icône)

### Alternative : Exécutable Windows (avancé)

Créer un `.exe` avec PyInstaller :

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name GraphLabs --icon=docs/images/icon.ico graphlabs/main.py
```

L'exécutable sera dans `dist/GraphLabs.exe`.

---

## 🐳 Installation avec Docker

Pour isoler complètement l'environnement :

### 1. Créer le Dockerfile

Créer `Dockerfile` à la racine :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    && rm -rf /var/lib/apt/lists/*

# Copier fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

CMD ["python", "-m", "graphlabs.main"]
```

### 2. Créer docker-compose.yml

```yaml
version: '3.8'

services:
  graphlabs:
    build: .
    environment:
      - DISPLAY=${DISPLAY}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - ~/.Xauthority:/root/.Xauthority
    network_mode: host
```

### 3. Lancer avec Docker

```bash
# Linux/Mac
xhost +local:docker
docker-compose up

# Windows (WSL2 requis)
# Configuration plus complexe, voir docs Docker
```

---

## 📦 Installation depuis PyPI (futur)

Quand GraphLabs sera publié sur PyPI :

```bash
# Simple installation globale
pip install graphlabs

# Avec environnement virtuel (recommandé)
python -m venv graphlabs-env
source graphlabs-env/bin/activate  # Linux/Mac
# ou
graphlabs-env\Scripts\activate  # Windows

pip install graphlabs
```

---

## 🔧 Résolution de problèmes

### Python non trouvé

**Erreur** : `python: command not found`

**Solution** :
- **Linux/Mac** : Essayez `python3` au lieu de `python`
- **Windows** : Réinstallez Python en cochant "Add to PATH"

### pip non trouvé

**Erreur** : `pip: command not found`

**Solution** :
```bash
# Linux/Mac
sudo apt install python3-pip  # Debian/Ubuntu
brew install python  # macOS

# Windows
python -m ensurepip --upgrade
```

### Erreur PyQt6

**Erreur** : `ModuleNotFoundError: No module named 'PyQt6'`

**Solution** :
```bash
pip install PyQt6==6.7.0
```

### Erreur de permissions

**Erreur** : `Permission denied`

**Solution** :
- **Ne jamais utiliser `sudo pip install`** sur Linux/Mac
- Utiliser un environnement virtuel
- Sur Windows, lancer PowerShell en administrateur si nécessaire

### Problèmes d'affichage Qt

**Erreur** : `qt.qpa.plugin: Could not load the Qt platform plugin`

**Solution Linux** :
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

**Solution macOS** :
```bash
brew install qt6
```

### Lenteur au démarrage

**Cause** : Premier lancement ou nombreux fichiers

**Solution** :
- Attendre quelques secondes
- Vérifier antivirus (peut ralentir)
- Utiliser SSD plutôt que HDD

---

## 🔄 Mise à jour

### Depuis Git

```bash
cd graphlabs
git pull origin main
pip install -r requirements.txt --upgrade
```

### Depuis PyPI (futur)

```bash
pip install --upgrade graphlabs
```

---

## 🗑️ Désinstallation

### Désinstallation complète

```bash
# Désactiver l'environnement virtuel
deactivate

# Supprimer le dossier
rm -rf ~/graphlabs  # Linux/Mac
rmdir /s graphlabs  # Windows

# Si installé globalement
pip uninstall graphlabs
```

### Désinstallation partielle (garder les données)

```bash
# Seulement désinstaller le package
pip uninstall graphlabs

# Garder le dossier avec vos graphes sauvegardés
```

---

## 🚀 Installation pour développeurs

Si vous voulez contribuer au projet :

```bash
# Cloner avec submodules (si applicable)
git clone --recursive https://github.com/yourusername/graphlabs.git

# Installer dépendances de dev
pip install -r requirements-dev.txt

# Installer pre-commit hooks
pre-commit install

# Vérifier installation
pytest
black --check graphlabs/
flake8 graphlabs/
```

Voir [CONTRIBUTING.md](../../CONTRIBUTING.md) pour plus de détails.

---

## 📞 Support

Si vous rencontrez des problèmes :

1. **Consulter** : [FAQ](faq.md)
2. **Chercher** : [Issues GitHub](https://github.com/yourusername/graphlabs/issues)
3. **Demander** : [Discussions GitHub](https://github.com/yourusername/graphlabs/discussions)
4. **Reporter** : Créer une nouvelle Issue avec tag "installation"

---

## ✅ Vérification de l'installation

Pour vérifier que tout fonctionne :

```bash
# Test rapide
python -c "import graphlabs; print('Installation OK!')"

# Lancer l'application
graphlabs

# Dans l'application :
# 1. Bibliothèque → Charger "Cycle (6 sommets)"
# 2. Algorithme → DFS
# 3. Cliquer ▶️ Exécuter
# ✓ Devrait afficher l'ordre de visite
```

Si vous voyez un graphe avec des sommets en vert, **félicitations !** 🎉

GraphLabs est correctement installé.

---

**Prêt à explorer la théorie des graphes ? 📊🎓**

[➡️ Guide de démarrage rapide](quickstart.md)
