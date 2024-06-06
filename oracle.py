import requetes as rqt

def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True

def start(nom_data) :
    hollywood = rqt.json_vers_nx(nom_data)
    print("♦------------------------------------------------------♦")
    print("|               Bienvenue à Hollywood !                |")
    print("♦------------------------------------------------------♦")
    print("  ")
    print("♦ Options ---------------------------------------------♦")
    print("| A- Quel est l'acteur central d'Hollywood ?           |")
    print("| C- Trouver des collaborateurs communs à deux acteurs |")
    print("| T- Trouver les collaborateurs proches d'un acteur    |")
    print("| E- Quelle est la distance d'éloignement maximale ?   |")
    print("| U- Trouver la distance entre deux acteurs            |")
    print("| R- Trouver la centralité d'un acteur                 |")
    print("| S- Stopper l'application                             |")
    print("♦------------------------------------------------------♦")
    stop = False
    while not stop :
        reponse = input("Choisissez une option : ")
        while reponse not in ["A", "C", "T", "E", "U", "R","S", "a", "c", "t", "e", "u", "r","s"] :
            reponse = input("Cela ne fait pas partie des options proposées. Choisissez-en une autre : ")
        if reponse in {"S", "s"} :
            stop = True
        elif reponse in {"A", "a"} :
            centre = rqt.centre_hollywood(hollywood)
            print(f"L'acteur le plus central d'Hollywood est {centre}")
        elif reponse in {"C", "c"} :
            acteur1 = input("Choisissez un·e premier·ère acteur·rice : ")
            acteur2 = input("Choisissez un·e deuxième acteur·rice : ")
            collabs = rqt.collaborateurs_communs(hollywood, acteur1, acteur2)
            if "inconnu" in collabs :
                print(collabs)
            else :
                print(f"Les collaborateurs communs à {acteur1} et {acteur2} sont {collabs}")
        elif reponse in {"T", "t"} :
            acteur = input("Choisissez un·e acteur·rice : ")
            dist = input("Choisissez la distance maximale des collaborateurs : ")
            while not is_integer(dist) :
                dist = input("La distance doit être un nombre entier. Recommencez : ")
            distance = int(dist)
            proches = rqt.collaborateurs_proches(hollywood, acteur, distance)
            if proches is None :
                print("Cet·te acteur·ice est inconnu·e au bataillon")
            else :
                print(f"Les collaborateurs proches de {acteur} sont {proches}")
        elif reponse in {"E", "e"} :
            loin = rqt.eloignement_max(hollywood)
            print(f"Les deux acteurs·rices les plus éloignés sont séparés·es de {loin} personnes")
        elif reponse in {"U", "u"} :
            acteur3 = input("Choisissez un·e premier·ère acteur·rice : ")
            acteur4 = input("Choisissez un·e deuxième acteur·rice : ")
            entre_deux = rqt.distance(hollywood, acteur3, acteur4)
            if not is_integer(entre_deux) :
                print(entre_deux)
            else :
                print(f"{acteur3} et {acteur4} sont éloignés de {entre_deux}")
        elif reponse in {"R", "r"} :
            actor = input("Choisissez un·e acteur·rice : ")
            plus_loin = rqt.centralite(hollywood, actor)
            print(f"La personne la plus éloignée de {actor} est éloignée de {plus_loin} personnes")
    return "Bonne journée à vous !"

start('data_10000.txt')
