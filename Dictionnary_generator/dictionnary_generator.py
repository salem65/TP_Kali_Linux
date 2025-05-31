import subprocess
import sys

def generate(output_file, min_len, max_len, charset=None):

    if not charset:
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # j'utilise l'outils crunch pour genere des mot de passe
    command = [
        "crunch",
        str(min_len),
        str(max_len),
        charset,
        "-o", output_file
    ]

    try:
        print("[+] Génération du dictionnaire en cours...")
        subprocess.run(command, check=True)
        print(f"[✔] Dictionnaire généré avec succès : {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[✘] Erreur lors de l'exécution de Crunch : {e}")
    except FileNotFoundError:
        print("[✘] Crunch n'est pas installé.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)

    output_file = sys.argv[1]
    min_len = int(sys.argv[2])
    max_len = int(sys.argv[3])

    custom_charset = "abcdefghijklmnopqrstuvwxyz0123456789"

    generate(output_file, min_len, max_len, custom_charset)
