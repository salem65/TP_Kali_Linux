# FTP Brute Force Tool

Outil Python pour réaliser des attaques par dictionnaire sur des serveurs FTP.

## Fonctionnalités

- Attaque par dictionnaire sur le protocole FTP
- Supporte les fichiers d'utilisateurs ou un seul utilisateur
- Limitation configurable du taux de tentatives
- Multi-threading pour une exécution rapide
- Affichage en temps réel des tentatives
- Gestion propre de l'interruption clavier (Ctrl+C)

## Prérequis

- Python 3.x
- Bibliothèques standard (aucune installation supplémentaire requise)

## Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/votre-utilisateur/ftp-brute-force.git
cd ftp-brute-force

python ftp_attack.py <serveur> <utilisateur|fichier_utilisateurs> <fichier_mots_de_passe>
