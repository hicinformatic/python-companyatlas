# Setup python-companyatlas

Ce document récapitule la structure et la configuration du projet python-companyatlas.

## 📁 Structure du projet

```
python-companyatlas/
├── .cursor/
│   └── rules/
│       └── assistant-guidelines.md   # Règles pour l'assistant AI
├── src/
│   └── python_companyatlas/
│       ├── __init__.py               # Point d'entrée du package
│       └── client.py                 # Client CompanyAtlas principal
├── tests/
│   ├── __init__.py
│   └── test_client.py                # Tests unitaires
├── dev.py                            # Script de développement
├── pyproject.toml                    # Configuration du projet
├── requirements-dev.txt              # Dépendances de développement
├── README.md                         # Documentation principale
├── CONTRIBUTING.md                   # Guide de contribution
├── LICENSE                           # Licence MIT
├── .gitignore                        # Fichiers à ignorer
└── env.example                       # Exemple de variables d'environnement
```

## 🚀 Quick Start

```bash
# Installation
cd /home/charl/Projects/python-companyatlas
python dev.py venv           # Créer l'environnement virtuel
python dev.py install-dev    # Installer en mode développement

# Tests
python dev.py test           # Exécuter les tests
python dev.py coverage       # Tests avec rapport de couverture

# Qualité du code
python dev.py lint           # Vérifier le code (ruff + mypy)
python dev.py format         # Formater le code
python dev.py check          # Vérifications complètes

# Utilisation
python -c "from python_companyatlas import CompanyAtlas; atlas = CompanyAtlas(); print(atlas.lookup('example.com'))"
```

## ✅ Fonctionnalités actuelles

- ✅ Client CompanyAtlas de base
- ✅ Méthode `lookup(domain)` pour rechercher une entreprise
- ✅ Méthode `enrich(company_data)` pour enrichir les données
- ✅ Tests unitaires avec 100% de couverture
- ✅ Type hints complets
- ✅ Docstrings Google-style
- ✅ Script dev.py complet
- ✅ Configuration linting (ruff, mypy)
- ✅ Règles Cursor AI

## 📋 Commandes dev.py disponibles

### Environnement
- `venv` - Créer l'environnement virtuel
- `install` - Installation production
- `install-dev` - Installation développement avec dépendances dev
- `venv-clean` - Recréer l'environnement virtuel

### Tests & Qualité
- `test` - Exécuter pytest
- `test-verbose` - Tests avec sortie détaillée
- `coverage` - Tests avec rapport de couverture HTML
- `lint` - Vérifier le code (ruff + mypy)
- `format` - Formater le code avec ruff
- `check` - Vérifications lint + format

### Nettoyage
- `clean` - Nettoyer tous les artefacts
- `clean-build` - Nettoyer les artefacts de build
- `clean-pyc` - Nettoyer les fichiers bytecode Python
- `clean-test` - Nettoyer les artefacts de tests

### Packaging
- `build` - Construire sdist et wheel
- `upload-test` - Upload vers TestPyPI
- `upload` - Upload vers PyPI

### Utilitaires
- `show-version` - Afficher la version du projet
- `help` - Afficher l'aide

## 🎯 Prochaines étapes

1. **Implémenter la logique métier**
   - Ajouter des providers pour différentes sources de données
   - Implémenter l'enrichissement des données d'entreprise
   - Gérer le cache et les rate limits

2. **Ajouter des tests**
   - Tests d'intégration avec des API réelles (mockées)
   - Tests de validation des données
   - Tests de gestion d'erreurs

3. **Documentation**
   - Exemples d'utilisation dans le README
   - Documentation des API
   - Guide de configuration

4. **CI/CD**
   - GitHub Actions pour les tests automatiques
   - Publication automatique sur PyPI
   - Vérification de qualité du code

## 🔧 Configuration

### Variables d'environnement (`.env`)

Copier `env.example` vers `.env` et configurer :

```bash
# API Keys (selon les providers utilisés)
COMPANYATLAS_API_KEY=your_api_key_here

# Configuration
COMPANYATLAS_BASE_URL=https://api.example.com
COMPANYATLAS_TIMEOUT=30
```

### Règles Cursor AI

Les règles pour l'assistant AI sont dans `.cursor/rules/assistant-guidelines.md` :
- Utiliser `python dev.py` pour toutes les opérations
- Code en anglais (commentaires, docstrings, etc.)
- Type hints obligatoires
- Docstrings Google-style
- Pas de dépendances Django
- Validation des données avant appels API
- Gestion des erreurs avec exceptions personnalisées

## 📊 Statut actuel

- **Version**: 0.1.0
- **Tests**: 5/5 passent ✅
- **Couverture**: 100% ✅
- **Linting**: Configuré (ruff, mypy) ✅
- **Documentation**: README, CONTRIBUTING ✅
- **Licence**: MIT ✅

## 📚 Resources

- [Projet python-missive](../python-missive) - Projet similaire comme référence
- [pytest documentation](https://docs.pytest.org/)
- [ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)

