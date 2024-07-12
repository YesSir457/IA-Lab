import math
import sys


class ArbreDecisionnel:

    def __init__(self, indice):
        self.indice = indice
        self.enfants = []
        self.classe = 'invalid' #initialisation d'une valeur par défaut"

    def ajouter_enfant(self, noeud):
        self.enfants.append(noeud)

    def definir_classe(self, classe):
        self.classe = classe

    def obtenir_indice(self):
        return self.indice

    def obtenir_enfant(self, index):
        return self.enfants[index]

    def obtenir_classe(self):
        return self.classe


def entropie(valeurs):
    total = sum(valeurs)
    if total == 0:
        return 0.0
    return -sum(v / total * math.log2(v / total) for v in valeurs if v > 0)


def calculer_frequence(DB, domaines, attr_index):
    compte = [0] * len(domaines[attr_index])
    idx_domaines = {val: idx for idx, val in enumerate(domaines[attr_index])}
    for enreg in DB:
        compte[idx_domaines[enreg[attr_index]]] += 1
    return compte


def construire_arbre(DB, attributs, verif_attributs, domaines):
    racine = ArbreDecisionnel(-1)
    compte_classe = calculer_frequence(DB, domaines, -1)
    entropie_totale = entropie(compte_classe)

    if entropie_totale == 0:
        racine.definir_classe(DB[0][-1])
        return racine

    gains = []
    for attr_index in range(len(attributs) - 1):
        if verif_attributs[attr_index]:
            gains.append(float('-inf'))
            continue

        entropie_attrib = 0.0
        for valeur in domaines[attr_index]:
            compte_cond = [0] * len(domaines[-1])
            idx_domaines = {}
            for enreg in DB:
                if enreg[attr_index] == valeur:
                    label = enreg[-1]
                    if label not in idx_domaines:
                        idx_domaines[label] = len(idx_domaines)
                    compte_cond[idx_domaines[label]] += 1

            entropie_attrib += entropie(compte_cond) * sum(compte_cond) / len(DB)

        gains.append(entropie_totale - entropie_attrib)

    indice_gain_max = gains.index(max(gains))
    racine.indice = indice_gain_max

    label_majoritaire = max(domaines[-1], key=lambda x: compte_classe[list(domaines[-1]).index(x)])

    for valeur in domaines[indice_gain_max]:
        sous_ensemble = [enreg for enreg in DB if enreg[indice_gain_max] == valeur]
        if not sous_ensemble:
            noeud = ArbreDecisionnel(-1)
            noeud.definir_classe(label_majoritaire)
            racine.ajouter_enfant(noeud)
            continue

        new_verif_attributs = verif_attributs[:]
        new_verif_attributs[indice_gain_max] = True
        sous_noeud = construire_arbre(sous_ensemble, attributs, new_verif_attributs, domaines)
        racine.ajouter_enfant(sous_noeud)

    return racine


def rechercher_classe(arbre, domaines, enreg):
    if arbre.indice == -1:
        return arbre.obtenir_classe()
    for i, valeur in enumerate(domaines[arbre.obtenir_indice()]):
        if valeur == enreg[arbre.obtenir_indice()]:
            return rechercher_classe(arbre.obtenir_enfant(i), domaines, enreg)
    return 'invalid'


def lire_fichier(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        lignes = f.readlines()
    attributs = lignes[0].strip().split()
    donnees = [ligne.strip().split() for ligne in lignes[1:]]
    return attributs, donnees


def ecrire_resultat(nom_sortie, attributs, donnees_test, resultat_test):
    with open(nom_sortie, 'w') as f:
        f.write('\t'.join(attributs) + '\n')
        for enreg, resultat in zip(donnees_test, resultat_test):
            f.write('\t'.join(enreg) + '\t' + resultat + '\n')


def executer():
    entree_train, entree_test, sortie = sys.argv[1:4]

    attributs, base_donnees = lire_fichier(entree_train)
    domaines = [set() for _ in attributs]
    for enreg in base_donnees:
        for i, valeur in enumerate(enreg):
            domaines[i].add(valeur)

    verif_attributs = [False] * len(attributs)
    racine_arbre = construire_arbre(base_donnees, attributs, verif_attributs, domaines)

    attributs_test, donnees_test = lire_fichier(entree_test)
    resultat_test = [rechercher_classe(racine_arbre, domaines, enreg) for enreg in donnees_test]

    ecrire_resultat(sortie, attributs, donnees_test, resultat_test)


if __name__ == '__main__':
    executer()