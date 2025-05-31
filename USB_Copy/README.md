# USB to Directory Copier

Script Python pour copier automatiquement le contenu d'une clé USB vers un répertoire de destination sur Linux, avec gestion des erreurs et sauvegarde datée.

## 📝 Fonctionnalités
- Copie récursive de tous les fichiers/dossiers
- Création automatique d'un sous-dossier daté dans le répertoire de destination
- Gestion robuste des erreurs (permissions, fichiers corrompus, etc.)
- Préservation des métadonnées des fichiers
- Support des chemins avec `~` (dossier utilisateur)

## 🛠 Prérequis
- Python 3.x
- Bibliothèques standard (pas d'installation supplémentaire nécessaire)

## 🚀 Utilisation
```bash

./USB_Copy.py -u [CHEMIN_USB] -d [DESTINATION]
