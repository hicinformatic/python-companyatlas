# Contributing to python-companyatlas

Merci de contribuer à python-companyatlas !

## Configuration de l'environnement de développement

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/python-companyatlas.git
cd python-companyatlas

# Créer l'environnement virtuel et installer les dépendances
python dev.py venv
python dev.py install-dev
```

## Workflow de développement

1. **Créer une branche** pour votre feature/fix
   ```bash
   git checkout -b feature/ma-nouvelle-feature
   ```

2. **Développer** votre code dans `src/python_companyatlas/`

3. **Écrire des tests** dans `tests/`
   ```bash
   python dev.py test
   python dev.py coverage
   ```

4. **Vérifier la qualité du code**
   ```bash
   python dev.py lint
   python dev.py format
   python dev.py check
   ```

5. **Committer et pousser**
   ```bash
   git add .
   git commit -m "feat: description de la feature"
   git push origin feature/ma-nouvelle-feature
   ```

## Commandes utiles

```bash
# Tests
python dev.py test              # Exécuter tous les tests
python dev.py test-verbose      # Tests avec sortie détaillée
python dev.py coverage          # Tests avec rapport de couverture

# Qualité du code
python dev.py lint              # Vérifier le code (ruff, mypy)
python dev.py format            # Formater le code
python dev.py check             # Vérifier lint + format

# Nettoyage
python dev.py clean             # Nettoyer tous les artefacts
python dev.py clean-test        # Nettoyer les artefacts de tests

# Build & release
python dev.py build             # Construire le package
python dev.py upload-test       # Upload vers TestPyPI
python dev.py upload            # Upload vers PyPI
```

## Standards de code

- **Python 3.10+** minimum
- **Type hints** pour toutes les fonctions publiques
- **Docstrings** style Google pour toutes les classes et fonctions publiques
- **Tests** pour toute nouvelle fonctionnalité
- **Couverture** > 80% minimum

## Format des commits

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` changements de documentation
- `test:` ajout/modification de tests
- `refactor:` refactoring du code
- `chore:` tâches de maintenance

## Questions ?

Ouvrez une issue sur GitHub !

