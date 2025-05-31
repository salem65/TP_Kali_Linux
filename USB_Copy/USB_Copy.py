#!/usr/bin/env python3
import os
import shutil
import argparse
import time
from datetime import datetime

def copy_usb_content(usb_path, dest_dir):
    """
    Copie récursivement le contenu de la clé USB vers le répertoire de destination.
    Crée un sous-dossier avec la date et l'heure pour éviter les écrasements.
    """
    try:
        # Vérification des chemins
        if not os.path.exists(usb_path):
            raise FileNotFoundError(f"Le chemin USB '{usb_path}' n'existe pas.")
        
        if not os.path.isdir(usb_path):
            raise NotADirectoryError(f"'{usb_path}' n'est pas un répertoire.")

        # Création du dossier de destination (avec timestamp)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_dir = os.path.join(dest_dir, f"usb_backup_{timestamp}")
        
        os.makedirs(backup_dir, exist_ok=True)
        print(f"\n📁 Début de la copie : {usb_path} → {backup_dir}")

        # Copie récursive
        for item in os.listdir(usb_path):
            src = os.path.join(usb_path, item)
            dst = os.path.join(backup_dir, item)
            
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)  # Préserve les métadonnées
                print(f"✅ {item}")
            except Exception as e:
                print(f"❌ Erreur sur {item} : {str(e)}")

        print(f"\n✔️ Copie terminée ! Données sauvegardées dans : {backup_dir}")

    except Exception as e:
        print(f"\n⚠️ Erreur critique : {str(e)}")
        exit(1)

if __name__ == "__main__":
    # Configuration des arguments en ligne de commande
    parser = argparse.ArgumentParser(
        description="Copie le contenu d'une clé USB vers un répertoire de destination."
    )
    parser.add_argument(
        "-u", "--usb", 
        required=True,
        help="Chemin de la clé USB (ex: /media/user/USB_KEY)"
    )
    parser.add_argument(
        "-d", "--dest", 
        required=True,
        help="Répertoire de destination (ex: ~/backups)"
    )
    args = parser.parse_args()

    # Normalisation des chemins (supprime les / redondants)
    usb_path = os.path.normpath(args.usb)
    dest_dir = os.path.normpath(os.path.expanduser(args.dest))  # Gère le ~

    # Lancement
    print(f"\n🔍 Vérification des chemins...")
    print(f"  - Source USB : {usb_path}")
    print(f"  - Destination : {dest_dir}")
    
    copy_usb_content(usb_path, dest_dir)