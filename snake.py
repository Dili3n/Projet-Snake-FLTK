# -*- coding: utf-8 -*-

from fltk import *
from time import sleep
from random import *
import winsound
import doctest

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

# Création fenêtre de jeu.

cree_fenetre(taille_case * largeur_plateau,
             taille_case * hauteur_plateau)

################################################################ Les variables

boucle = True

# menus graphiques
menu = True
option = False
gameover = False
regles = False
regles1 = False
regles2 = False
regles3 = False

# mode de jeu
solo = False
duo = False
ordi = False


# options du jeu
obstacle = False # création d'obstacle.
difficulte = 1 # rapidité du jeu
flamme = False # une flamme qui apparaît pendant le jeu
acceleration = False # Accélération de la rapidité du jeu
sound = False # Activer ou non le son dans le jeu
pacman = False # Mode arène Pac-Man
buffet = False # Mode Buffet

################################################################ LES FONCTIONS


def case_vers_pixel(case):

    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    """

    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):

    """
    Cette fonction recoit les coordonnées de pommes pour ensuite
    les transformer en pixel et range la valeur x et y dans deux
    variables respectives.
    Ensutie la fonction trace un cercle et un rectangle aux
    coordonnées x, y pour y représenter une pomme.
    ----------
    pommes : coordonnées de la prochaine pomme
    -------

    """

    x, y = case_vers_pixel(pommes)

    cercle(x, y, taille_case/2,
           couleur='darkred', remplissage='red')
    rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
              couleur='darkgreen', remplissage='darkgreen')



def affiche_obstacles(obstacles):

    """
    Cette fonction à le même fonctionnement que "affiche_pommes",
    sauf que celle ci reçoit la coordonnées d'un obstacle.
    Ensuite la fonction trace un cercle gris aux coordonnées
    x, y pour y représenter une pierre (un obstacle)
    ----------
    obstacles : coordonnées de l'obstacle
    -------
    """

    for i in range(4):

        x, y = case_vers_pixel(obstacles[i-1])

        if pacman == True :
            chance_pacman = randint(1,5)
            if chance_pacman == 1:
                cercle(x, y, taille_case/randint(2,3),
                       couleur='black', remplissage='orange')
            elif chance_pacman == 2:
                cercle(x, y, taille_case/randint(2,3),
                       couleur='black', remplissage='white')
            elif chance_pacman == 3:
                cercle(x, y, taille_case/randint(2,3),
                       couleur='black', remplissage='yellow')
            elif chance_pacman == 4:
                cercle(x, y, taille_case/randint(2,3),
                       couleur='black', remplissage='green')
            elif chance_pacman == 5:
                cercle(x, y, taille_case/randint(2,3),
                       couleur='black', remplissage='blue')
        else :
             cercle(x, y, taille_case/2,
               couleur='black', remplissage='grey')


def affiche_flamme(flammes,indice):

    """
    Cette fonction à pour fonctionnalité d'afficher une ligne de flamme
    impassable quand l'option flamme est activé par l'utilisateur.
    Les paramètres de cette fonction sont flammes (les coordonnées des flammes)
    et indice (le nombre de tour de la boucle solo)
    C'est à dire que du tour 1 à 20 une simple ligne sera tracée, ensuite, de
    21 à 45 on aura une ligne grise pour nous prévenir que les flammes
    arrivent. De 46 à 100 le mur de flamme est mis en place (une ligne rouge)
    et pour finir on remet l'indice à 0 quand l'indice depasse 100
    ----------
    flammes : coordonnées des flammes
    indice : nombre de tour de la boucle solo (boucle de jeu)
    -------
    >>> affiche_flamme([30,25],7)
    8
    """

    x, y = case_vers_pixel(flammes)

    if indice <= 20:
        indice += 1
        rectangle(0,x,750,y,
                  couleur='grey', remplissage='black', epaisseur=2, tag='')
        return indice

    elif indice <= 45:
        indice += 1
        rectangle(0,x,750,y,
                  couleur='orange', remplissage='black', epaisseur=2, tag='')
        return indice

    elif indice <= 100:
        indice += 1
        rectangle(0,x,750,y,
                  couleur='darkred', remplissage='orange', epaisseur=10, tag='')
        return indice

    elif indice <= 101:
        indice = 0
        return indice



def affiche_serpent(serpent, joueur):

    """
    Cette fonction permet d'afficher le serpent. Pour ce faire la fonction
    reçoit deux paramètres; serpent (les coordonnées du serpent) et joueur
    (qui sert à différencier le joueur n°1 et le n°2 dans le mode DUO).
    Comme pour la fonction affiche_pommes et obstacles, cette fonction va
    convertir les coordonnées du serpent en pixel en envoyant serpent à la
    fonction case_vers_pixel. Ensuite selon le second paramètre de la fonction
    le serpent sera de couleur verte ou de couleur orange
    ----------
    serpent : coordonnées du serpent
    joueur : joueur1 ou joueur2.
    -------
    """

    x, y = case_vers_pixel(serpent)

    if joueur == 1 and pacman:
        cercle(x, y, taille_case/2 + 1,
                  couleur='darkgreen', remplissage='yellow')
    if joueur == 1 and pacman == False:
        cercle(x, y, taille_case/2 + 1,
                  couleur='darkgreen', remplissage='green')

    elif joueur == 2:
        cercle(x, y, taille_case/2 + 1,
                  couleur='darkred', remplissage='orange')

    elif joueur == 3:
        cercle(x, y, taille_case/2 + 1,
                  couleur='darkgrey', remplissage='grey')

def buffet_pommes(pospommes):
    """
    Même fonction que affiche_pommes mais spécialement utilisé pour le mode
    buffet.
    ----------
    pospommes : coordonnées pommes violette
    -------
    """

    x, y = case_vers_pixel(pospommes)

    cercle(x, y, taille_case/2,
              couleur='black', remplissage='purple')

    rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
             couleur='darkgreen', remplissage='darkgreen')




def change_direction1(direction1, touche): #joueur1

    """
    Cette fonction permet de renvoyer des coordonnées. Pour chacunes des
    touches de direction saisie, les coordonnées renvoyés seront différentes.
    Les coordonnées renvoyés sont utilisées ensuite pour faire avancer le
    serpent, et si aucune des touches n'est saisie, les coordonnées renvoyés
    restent les mêmes que les précedentes.
    Deplus cette fonction prend en compte deux paramètres : direction1
    (qui renvoie à la direction précedente) et touche (qui est un type
     d'évenement, ici c'est la saisie d'une touche)
    ----------
    direction1 : direction précédente
    touche: evenement, saisie d'une touche de clavier
    -------
    >>> change_direction1((1, 0), 'Up')
    (0, -1)
    """

    if touche == 'Up': # Touche haut pressée
        return (0, -1)
    elif touche == 'Down': # Touche bas pressée
        return (0, 1)
    elif touche == 'Left': # Touche gauche pressée
        return (-1, 0)
    elif touche == 'Right': # Touche droite pressée
        return (1, 0)
    else:
        return direction1

def change_direction2(direction1, touche): #joueur2

    """
    Cette fonction est la même que change_direction2 sauf que celle-ci est
    utilisé pour le mode DUO (un deuxième joueur). Les touches pouvants être
    saisies ne sont pas les mêmes " Z Q S D ".
    ----------
    direction1 : direction précédente
    touche: evenement, saisie d'une touche de clavier
    -------
    """

    if touche == 'z': # Touche haut pressée
        return (0, -1)
    elif touche == 's': # Touche bas pressée
        return (0, 1)
    elif touche == 'q': # Touche gauche pressée
        return (-1, 0)
    elif touche == 'd': # Touche droite pressée
        return (1, 0)
    else:
        return direction2

def deplacement_serpent(serpent,direction):

    """
    Cette fonction est séparé en deux parties, quand le paramètre serpent est
    égal à serpent1 (le serpent du joueur 1) et quand il est égal à serpent2
    (le serpent du joueur 2). Dans cette fonction on vient rajouter aux listes
    des "coordonnées" des serpents la liste direction contenant un liste de
    coordonnées, qui est le résultat de la fonction "change_direction".
    Ligne 2 pour les x, ligne 3 pour les y. On assemble tout ensuite dans la
    liste queue_serpent.
    Il faut ensuite retirer la dernière liste de la liste "serpent" pour
    pouvoir faire avancer le serpent.
    Pour finir on ajoute queue_serpent à la liste serpent pour pouvoir créé un
    nouveau cercle (représentant le corps) aux nouvelles coordonnées
    ----------
    serpent : coordonnées du serpent et serpent1 ou 2 (discernement des deux
    joueur)
    direction : la direction du serpent (sortie fonction change_direction)
    -------
    """

    if serpent == serpentordi:
        serpentordi[0][0] += directionordi[0]
        serpentordi[0][1] += directionordi[1]
        queue_serpentordi = [serpentordi[0][0], serpentordi[0][1]]
        serpentordi.pop()
        serpentordi.insert(0,queue_serpentordi)

    if serpent == serpent1:
        serpent1[0][0] += direction1[0]
        serpent1[0][1] += direction1[1]
        queue_serpent1 = [serpent1[0][0], serpent1[0][1]]
        serpent1.pop()
        serpent1.insert(0,queue_serpent1)

    elif serpent == serpent2:
        serpent2[0][0] += direction2[0]
        serpent2[0][1] += direction2[1]
        queue_serpent2 = [serpent2[0][0], serpent2[0][1]]
        serpent2.pop()
        serpent2.insert(0,queue_serpent2)

def play_sound(type_son, sound):

    """
    Fonction utilisée pour jouer du son. Pour cela on a deux paramètres :
    type_son (qui représente le son qu'il faut jouer) et le paramètre sound
    pour savoir si l'option son est activé ou non.
    ----------
    type_son : Chaine de caractère représentant le titre qu'il faut jouer
    sound : Booléen, savoir si l'option Son est activé
    -------
    """

    if sound:

        #Catégorie divers
        if type_son == "defaite":
            winsound.PlaySound('assets/divers/defaite.wav',
                                   winsound.SND_FILENAME)
        if type_son == "clic":
            winsound.PlaySound('assets/divers/clic.wav',
                                   winsound.SND_FILENAME)
        if type_son == "snack":
            winsound.PlaySound('assets/divers/snack.wav',
                                   winsound.SND_FILENAME)

        #catégorie manger
        if type_son == "rot":
            winsound.PlaySound('assets/manger/rot.wav',
                                   winsound.SND_FILENAME)
        if type_son == "manger":
            winsound.PlaySound('assets/manger/manger.wav',
                                   winsound.SND_FILENAME)

        #catégorie mort
        if type_son == "mort":
            winsound.PlaySound('assets/morts/mort.wav',
                                   winsound.SND_FILENAME)
        if type_son == "mortfire":
            winsound.PlaySound('assets/morts/mortfire.wav',
                                   winsound.SND_FILENAME)
        if type_son == "mortmur":
            winsound.PlaySound('assets/morts/mortmur.wav',
                                   winsound.SND_FILENAME)


######################################################### programme principal

#boucle principale
while boucle:

    # efface le contenu d'une fenêtre entre le changement de menu
    efface_tout()


    # initialisation du jeu
    score1 = 0
    score2 = 0
    scoreordi = 0
    # Pour savoir qui gagne entre le joueur 1 et 2
    gagnant1 = False
    gagnant2 = False
    gagnantordi = False
    # variable pour que l'ordinateur commence à joeur quand le joueur commence
    # à jouer
    depart = False
    # taux de rafraîchissement du jeu en images/s
    framerate = 10 * difficulte
    direction1 = [0, 0]  # direction initiale du serpent
    direction2 = [0, 0]
    directionordi = [0, 0]
    # création de 4 obstacles
    obstacles = [[randint(0, 39),randint(0, 29)],
                 [randint(0, 39),randint(0, 29)],
                 [randint(0, 39),randint(0, 29)],
                 [randint(0, 39),randint(0, 29)]]
    # liste des coordonnées des cases contenant des pommes
    pommes = [randint(0, 36),randint(0, 26)]
    pos_pommes = [[randint(0, 36),randint(0, 26)]]
    # liste des coordonnées de cases adjacentes décrivant le serpent
    serpent1 = [[20 ,10],[-1,-1]]
    serpent2 = [[20 ,20],[-1,-1]]
    serpentordi = [[20, 20],[-1,-1]]
    #variable pour le mode flamme
    indice = 0
    flamme_rouge = [0,0]
    flamme_coordonees = randint(1,30)
    flammes = [flamme_coordonees,flamme_coordonees]



# Menu principal

    while menu:

        # mise à jour graphique
        mise_a_jour()

        #ajout d'une image (un background)
        image(300.7,226.7,'assets/bgmenu.png', ancrage = "center")

        #création du bouton : option
        rectangle(203,369,405,415)
        texte(213, 375,"Ordinateur", police = 'benguiat')

        #création du bouton : Solo
        rectangle(100,293,250,342)
        texte(135,302,"Solo", police = 'benguiat')

        #création du bouton : Duo
        rectangle(360,293,510,342)
        texte(400,303,"Duo", police = 'benguiat')

        #création du bouton : Regles
        rectangle(429,17,589,71)
        texte(455,27,"Regles", police = 'benguiat')

        #création du bouton : ordinateur
        rectangle(40,14,233,67)
        texte(70, 23,"Options", police = 'benguiat')

        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)

        # Quand on quitte le jeu il se ferme, et ne crash pas
        if ty == 'Quitte':
            boucle = False
            break

        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            #Bouton Solo
            if 100 <= abscisse(ev) <= 250 and 300 <= ordonnee(ev) <= 350:
                solo = True
                menu = False

            #Bouton Duo
            elif 360 <= abscisse(ev) <= 510 and 300 <= ordonnee(ev) <= 350:
                solo = True
                duo = True
                menu = False

            #Bouton Option
            elif 205 <= abscisse(ev) <= 405 and 375 <= ordonnee(ev) <= 425:
                ordi = True
                solo = True
                menu = False

            elif 429 <= abscisse(ev) <= 579 and 21 <= ordonnee(ev) <= 71:
                regles = True
                menu = False

            elif 29 <= abscisse(ev) <= 211 and 21 <= ordonnee(ev) <= 71:
                menu = False
                option = True



### Menu regles ##############################################################

    while regles:

        image(299.7,226.7,'assets/bgregles.png', ancrage = "center")

        rectangle(425,393,555,440)
        texte(445, 403,("Menu"), taille = "25",
                 police = 'benguiat')

        mise_a_jour()

        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            boucle = False
            break
            # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            if 425 <= abscisse(ev) <= 555 and 393 <= ordonnee(ev) <= 440:
                regles = False
                menu = True

            if 325 <= abscisse(ev) <= 545 and 333 <= ordonnee(ev) <= 370:
                regles1 = True
                regles = False

    while regles1:

        image(299.7,226.7,'assets/bgregles1.png', ancrage = "center")

        rectangle(425,393,555,440)
        texte(445, 403,("Menu"), taille = "25",
                 police = 'benguiat')

        mise_a_jour()

        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            boucle = False
            break
        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            if 425 <= abscisse(ev) <= 555 and 393 <= ordonnee(ev) <= 440:
                regles1 = False
                menu = True

            if 325 <= abscisse(ev) <= 545 and 333 <= ordonnee(ev) <= 370:
                regles2 = True
                regles1 = False

    while regles2:

        image(299.7,226.7,'assets/bgregles2.png', ancrage = "center")

        rectangle(425,393,555,440)
        texte(445, 403,("Menu"), taille = "25",
                 police = 'benguiat')

        mise_a_jour()

        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            boucle = False
            break
        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            if 425 <= abscisse(ev) <= 555 and 393 <= ordonnee(ev) <= 440:
                regles2 = False
                menu = True

            if 325 <= abscisse(ev) <= 545 and 333 <= ordonnee(ev) <= 370:
                regles3 = True
                regles2 = False

    while regles3:

        image(299.7,226.7,'assets/bgregles3.png', ancrage = "center")

        rectangle(425,393,555,440)
        texte(445, 403,("Menu"), taille = "25",
                 police = 'benguiat')

        mise_a_jour()

        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            boucle = False
            break
        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            if 425 <= abscisse(ev) <= 555 and 393 <= ordonnee(ev) <= 440:
                regles3 = False
                menu = True




### Menu option ##############################################################

    while option:

        efface_tout()

        #ajout d'une image (un background)
        image(299.7,237.7,'assets/bgoption.png', ancrage = "center")

        #creation bouton : obstacle
        if obstacle == False:
            # en rouge quand il est désactivé
            rectangle(75,10,225,60,couleur = 'red')
            texte(85,20,"Obstacle", couleur = 'darkred', police = 'benguiat',
                  taille = "22")
        elif obstacle:
            # en vert quand il est activé
            rectangle(75,10,225,60,couleur = 'green')
            texte(85,20,"Obstacle", couleur = 'darkgreen',
                  police = 'benguiat', taille = "20")

        #creation bouton : difficulté
        if difficulte == 1:
            rectangle(75,75,250,125,couleur = 'green')
            texte(95,85,"Vitesse 1", couleur = 'darkgreen',taille = '20',
                  police = 'benguiat')
        elif difficulte == 2:
            rectangle(75,75,250,125,couleur = 'orange')
            texte(95,85,"Vitesse 2", couleur = 'orange',taille = '20',
                  police = 'benguiat')
        elif difficulte == 3:
            rectangle(75,75,250,125,couleur = 'red')
            texte(95,85,"Vitesse 3", couleur = 'darkred',taille = '20',
                  police = 'benguiat')
        elif difficulte == 10:
            rectangle(75,75,250,125,couleur = 'black')
            texte(81,87,"Vitesse Flash", couleur = 'black',taille = '18',
                  police = 'benguiat')

        #creation bouton : acceleration
        if acceleration == False:
            rectangle(75,140,260,190,couleur = 'red')
            texte(85,154,"Acceleration", couleur = 'darkred',
                  police = 'benguiat', taille = "18")
        elif acceleration:
            rectangle(75,140,260,190,couleur = 'green')
            texte(85,154,"Acceleration", couleur = 'darkgreen',
                  police = 'benguiat', taille = "18")

        #creation bouton : son
        if sound == False:
            rectangle(350,10,500,60,couleur = 'red')
            texte(360,20,"Son (FUN)", couleur = 'darkred', taille = '20',
                  police = 'benguiat')

        elif sound:
            rectangle(350,10,500,60,couleur = 'green')
            texte(360,20,"Son (FUN)", couleur = 'darkgreen', taille = '20',
                  police = 'benguiat')

        #creation bouton : flamme
        if flamme == False:
            rectangle(350,75,500,125,couleur = 'red')
            texte(372,85,"Flamme", couleur = 'darkred', taille = '20',
                  police = 'benguiat')
        elif flamme:
            rectangle(350,75,500,125,couleur = 'green')
            texte(372,85,"Flamme", couleur = 'darkgreen', taille = '20',
                  police = 'benguiat')

        #creation bouton : pacman
        if pacman == False:
            rectangle(350,140,500,190,couleur = 'red')
            texte(365,150,"Pac-Man", couleur = 'darkred', taille = '20',
                  police = 'benguiat')
        elif pacman:
            rectangle(350,140,500,190,couleur = 'green')
            texte(365,150,"Pac-Man", couleur = 'darkgreen', taille = '20',
                  police = 'benguiat')

        if buffet == False:
            # en rouge quand il est désactivé
            rectangle(212,212,380,262,couleur = 'red')
            texte(252,222,"Buffet", couleur = 'darkred', police = 'benguiat',
                  taille = "22")
        elif buffet:
            # en vert quand il est activé
            rectangle(212,212,380,262,couleur = 'green')
            texte(252,222,"Buffet", couleur = 'darkgreen',
                  police = 'benguiat', taille = "22")

        #creation bouton : Retour
        rectangle(350,340,500,390)
        texte(372,350,"Retour", police = 'benguiat')

        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            boucle = False
            break
        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            #Bouton Obstacle
            if 75 <= abscisse(ev) <= 225 and 10 <= ordonnee(ev) <= 60:

                play_sound("clic", sound)

                if obstacle == False:
                    obstacle = True
                else:
                    obstacle = False

            #Bouton Retour
            elif 350 <= abscisse(ev) <= 500 and 340 <= ordonnee(ev) <= 390:

                play_sound("clic", sound)
                option = False
                menu = True
                play_sound("snack", sound)
                continue

            #Bouton Difficulté
            elif 75 <= abscisse(ev) <= 250 and 75 <= ordonnee(ev) <= 125:
                play_sound("clic", sound)
                if difficulte == 1:
                    difficulte = 2
                elif difficulte == 2:
                    difficulte = 3
                elif difficulte == 3:
                    difficulte = 10
                elif difficulte == 10:
                    difficulte = 1

            #Bouton Acceleration
            elif 75 <= abscisse(ev) <= 250 and 140 <= ordonnee(ev) <= 190:
                play_sound("clic", sound)
                if acceleration == False:
                     acceleration = True
                else:
                     acceleration = False

            #Bouton Son
            elif 350 <= abscisse(ev) <= 500 and 10 <= ordonnee(ev) <= 60:
                play_sound("clic", sound)
                if sound == False:
                    sound = True
                else:
                    sound = False

            elif 350 <= abscisse(ev) <= 500 and 75 <= ordonnee(ev) <= 125:
                play_sound("clic", sound)
                if flamme == False:
                    flamme = True
                else:
                    flamme = False

            elif 350 <= abscisse(ev) <= 500 and 140 <= ordonnee(ev) <= 190:
                play_sound("clic", sound)
                if pacman == False:
                    pacman = True
                else:
                    pacman = False

            elif 220 <= abscisse(ev) <= 370 and 220 <= ordonnee(ev) <= 280:
                play_sound("clic", sound)
                if buffet == False:
                    buffet = True
                else:
                    buffet = False



### mode SOLO ################################################################

    while solo:

        efface_tout()

        # Si le mode ordi est activé désactivé toutes les options.
        if ordi:
            obstacle = False
            flamme = False
            sound = False
            buffet = False

### MODE PACMAN ##############################################################

        if pacman:
            obstacle = True

        #ajout d'une image (un background)
        if pacman:
            image(300.7,226.7,'assets/bgpacman.png', ancrage = "center")
        else :
            image(300.7,226.7,'assets/bgjeu.png', ancrage = "center")
        # Si le mode acceleration est True on accelère le rafraichissement
        if acceleration:
            framerate += 0.1


        # Affichage du score en haut à gauche
        if pacman:
            texte(10, 10,("Score", score1), taille = "16", couleur = "white",
              police = 'benguiat')
        else:
            texte(10, 10,("Score", score1), taille = "16", couleur = "green",
              police = 'benguiat')


        if buffet == False:
            affiche_pommes(pommes)

### MODE FLAMME ##############################################################

        #Si mode flamme activé
        if flamme:
            if indice == 0:
                indice += 1
                flamme_rouge = [0,0]
                flamme_coordonees = randint(1,30)
                flammes = [flamme_coordonees,flamme_coordonees]
            elif indice == 46:
                for i in range(0,100):
                    flamme_rouge.append([i,flamme_coordonees])
                indice = affiche_flamme(flammes,indice)


            else:
                indice = affiche_flamme(flammes,indice)



### DIVERS (Scores, affichage des serpents et direction) #####################


        # Si le mode obstacle est True on crée un obstacle qui se déplace
        chance_obstacle = randint (1,60)
        if chance_obstacle == 7:
            obstacles = [[randint(0, 39),randint(0, 29)],
                         [randint(0, 39),randint(0, 29)],
                         [randint(0, 39),randint(0, 29)],
                         [randint(0, 39),randint(0, 29)]]
        if obstacle:
            affiche_obstacles(obstacles)



        # Si mode ordinateur activé, mettre son score en haut à droite
        if ordi:
            texte(500, 10,("Score", scoreordi), taille = "16",
                  couleur = "grey", police = 'benguiat')

            # Affichage du serpent ordinateur
            for i in range(len(serpentordi)+1):
                affiche_serpent(serpentordi[i-1], 3)

        #Si mode duo activé, mettre le score du serpent 2
        if duo:
            texte(500, 10,("Score", score2), taille = "16",
                  couleur = "orange", police = 'benguiat')

            for i in range(len(serpent2)+1):
                affiche_serpent(serpent2[i-1], 2)

        # Permet d'afficher la tete du serpent et son corps
        for i in range(len(serpent1)+1):
            affiche_serpent(serpent1[i-1], 1)

        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)

        # Pour pouvoir quitter le jeu avec le croie en haut à droite
        if ty == 'Quitte':
            boucle = False
            break

        # Evenement gérant le déplacement du serpent
        elif ty == 'Touche':
            depart = True
            print(touche(ev))
            direction1 = change_direction1(direction1, touche(ev))
            if duo == True:
                direction2 = change_direction2(direction2, touche(ev))

        #Si les deux serpents ne se sont pas déplacer, afficher un message
        if (direction1 == [0, 0] and direction2 == [0, 0] and
            directionordi == [0, 0]):
            texte(70,200,"La partie peut commencer !", couleur = "white",
              police = 'benguiat')

        mise_a_jour()

### MANGER UNE POMME #########################################################

        # Quand le serpent mange une pomme (passe dessus avec sa tête)
        if serpent1[0] == pommes:
            score1 += 1
            if sound and score1%5 != 0:
                play_sound("manger", sound)
            elif sound and score1%5 == 0:
                play_sound("rot", sound)
            pommes = [randint(0,36), randint(0,26)]
            serpent1.append([serpent1[0][0], serpent1[0][1]])
        deplacement_serpent(serpent1,direction1)

        mise_a_jour()

        # quand le serpent n°2 mange une pomme
        if serpent2[0] == pommes and duo:
            score2 += 1
            if sound and score2%5 != 0:
                play_sound("manger", sound)
            elif sound and score2%5 == 0:
                play_sound("rot", sound)
            pommes = [randint(0,36), randint(0,26)]
            serpent2.append([serpent2[0][0], serpent2[0][1]])


        deplacement_serpent(serpent2,direction2)

        if pommes == obstacles[:]:
            pommes = [randint(0,36), randint(0,26)]



### LES DIFFERENTES MORTS DU SERPENT ! #######################################


# MORT AVEC OBSTRACLE

        # Si mode obstacle activé
        if obstacle:
            #création de la collision entre le serpent 2 et les obstacles
            if (serpent1[0] == obstacles[0] or serpent1[0] == obstacles[1] or
            serpent1[0] == obstacles[2] or serpent1[0] == obstacles[3]):
                play_sound("mortmur", sound)
                mise_a_jour()
                sleep(0.5)
                if duo:
                    gagnant2 = True
                if ordi:
                    gagnantordi = True
                gameover = True
                solo = False
                play_sound("defaite", sound)
                efface_tout()

            #Si mode duo activé
            if duo:
                #création de la collision entre le serpent 2 et les obstacles
                if (serpent2[0] == obstacles[0] or serpent2[0] == obstacles[1] or
                serpent2[0] == obstacles[2] or serpent2[0] == obstacles[3]
                and duo == True):
                    play_sound("mortmur", sound)
                    mise_a_jour()
                    sleep(0.5)
                    gagnant1 = True
                    gameover = True
                    solo = False
                    play_sound("defaite", sound)
                    efface_tout()

            #si mode ordi pour le mode pacman.
            if ordi:
                if (serpentordi[0] == obstacles[0] or serpentordi[0] == obstacles[1] or
            serpentordi[0] == obstacles[2] or serpentordi[0] == obstacles[3]):
                    play_sound("mortmur", sound)
                    mise_a_jour()
                    sleep(0.5)
                    gagnant1 = True
                    gameover = True
                    solo = False
                    play_sound("defaite", sound)
                    efface_tout()

# MORT QUAND LE SERPENT MANGE SE MANGE LA QUEUE OU SE RETOURNE SUR LUI MEME

        # Vérification que le serpent 1 ne se mangent pas la queue
        if serpent1[0] in serpent1[2:]:
            mise_a_jour()
            play_sound("mort", sound)
            sleep(0.5)
            if duo:
                    gagnant2 = True
            if ordi:
                    gagnantordi = True
            gameover = True
            solo = False
            efface_tout()
            play_sound("defaite", sound)
            continue

        # Si le serpent 2 se mange la queue
        if (serpent2[0] in serpent2[2:] and duo == True):
            mise_a_jour()
            play_sound("mort", sound)
            sleep(0.5)
            gagnant1 = True
            gameover = True
            solo = False
            efface_tout()
            play_sound("defaite", sound)
            continue

        # si le serpent ordi se mange lui même.
        if (serpentordi[0] in serpentordi[2:] and ordi == True):
            mise_a_jour()
            sleep(0.5)
            gagnant1 = True
            gameover = True
            solo = False
            efface_tout()
            continue

        # Si mode duo activé
        if duo == True:

            # Quand le serpent 1 rentre dans le serpent 2
            if serpent1[0] in serpent2[:]:
                mise_a_jour()
                play_sound("mort", sound)
                sleep(0.5)
                gagnant2 = True
                gameover = True
                solo = False
                efface_tout()
                play_sound("defaite", sound)
                continue

            # Quand le serpent 2 rentre dans le serpent 1
            elif serpent2[0] in serpent1[:]:
                mise_a_jour()
                play_sound("mort", sound)
                sleep(0.5)
                gagnant1 = True
                gameover = True
                solo = False
                play_sound("defaite", sound)
                efface_tout()

        #Si le mode ordinateur est activé
        if ordi == True:

            # Quand le serpent 1 rentre dans le serpent ordinateur
            if serpent1[0] in serpentordi[:]:
                mise_a_jour()
                sleep(0.5)
                gagnantordi = True
                gameover = True
                solo = False
                efface_tout()
                continue

            # Quand le serpent ordinateur rentre dans le serpent 1
            elif serpentordi[0] in serpent1[:]:
                mise_a_jour()
                sleep(0.5)
                gagnant1 = True
                gameover = True
                solo = False
                efface_tout()

        #Création des bordures de map si le mode pacman n'est pas activé
        if pacman == False:

            # Si le serpent 1 sort de la map
            if (serpent1[0][0] >= 40 or serpent1[0][0] <= -1 or
            serpent1[0][1] >= 30 or serpent1[0][1] <= -1):
                mise_a_jour()
                play_sound("mort", sound)
                sleep(0.5)
                if duo:
                    gagnant2 = True
                if ordi:
                    gagnantordi = True
                gameover = True
                solo = False
                efface_tout()
                play_sound("defaite", sound)
                continue

            # Si le serpent 2 sort de la map
            if (serpent2[0][0] >= 40 or serpent2[0][0] <= -1 or
            serpent2[0][1] >= 30 or serpent2[0][1] <= -1 and duo == True):
                mise_a_jour()
                play_sound("mort", sound)
                sleep(0.5)
                gagnant1 = True
                gameover = True
                solo = False
                efface_tout()
                play_sound("defaite", sound)
                continue

            # Si le serpent ordi sort de la map
            if (serpentordi[0][0] >= 40 or serpentordi[0][0] <= -1 or
            serpentordi[0][1] >= 30 or serpentordi[0][1] <= -1 and ordi == True):
                mise_a_jour()
                sleep(0.5)
                gagnant1 = True
                gameover = True
                solo = False
                efface_tout()
                continue



### MODE PACMAN ##############################################################

        if pacman:

            #Si le serpent 1 sort de la map le tp de l'autre coté
            if (serpent1[0][0] >= 40 or serpent1[0][0] <= -1 or
            serpent1[0][1] >= 30 or serpent1[0][1] <= -1):
                for i in range(0, len(serpent1)):
                    if serpent1[i][0] == 40:
                        serpent1[i][0] = 0
                    elif serpent1[i][0] == -1:
                        serpent1[i][0] = 40
                    elif serpent1[i][1] == 30:
                        serpent1[i][1] = 0
                    elif serpent1[i][1] == -1:
                        serpent1[i][1] = 30

            #Si le serpent 2 sort de la map le tp de l'autre coté
            if (serpent2[0][0] >= 40 or serpent2[0][0] <= -1 or
                serpent2[0][1] >= 30 or serpent2[0][1] <= -1 and duo == True):
                for i in range(0, len(serpent2)):
                    if serpent2[i][0] == 40:
                        serpent2[i][0] = 0
                    elif serpent2[i][0] == -1:
                        serpent2[i][0] = 40
                    elif serpent2[i][1] == 30:
                        serpent2[i][1] = 0
                    elif serpent2[i][1] == -1:
                        serpent2[i][1] = 30

            #Si le serpent ordi sort de la map le tp de l'autre coté
            if (serpentordi[0][0] >= 40 or serpentordi[0][0] <= -1 or
                serpentordi[0][1] >= 30 or serpentordi[0][1] <= -1 and
                ordi == True):
                for i in range(0, len(serpentordi)):
                    if serpentordi[i][0] == 40:
                        serpentordi[i][0] = 0
                    elif serpentordi[i][0] == -1:
                        serpentordi[i][0] = 40
                    elif serpentordi[i][1] == 30:
                        serpentordi[i][1] = 0
                    elif serpentordi[i][1] == -1:
                        serpentordi[i][1] = 30

        # Si le serpent 1 rentre dans la flamme
        if serpent1[1] in flamme_rouge[:]:
            mise_a_jour()
            play_sound("mortfire", sound)
            sleep(0.5)
            gagnant2 = True
            gameover = True
            solo = False
            efface_tout()
            play_sound("defaite", sound)

        # Si le serpent 2 rentre dans la flamme
        if serpent2[1] in flamme_rouge[:]:
            mise_a_jour()
            play_sound("mortfire", sound)
            sleep(0.5)
            gagnant1 = True
            gameover = True
            solo = False
            efface_tout()
            play_sound("defaite", sound)



### MODE BUFFET ##############################################################

        if buffet:

            # On limite le nombre de pomme sur la map
            if len(pos_pommes) <= 50:
                pos_pommes.append([randint(0, 36),randint(0, 26)])

                # on empeche le spawn de pomme sur le serpent
                while pos_pommes == serpent1[:] or pos_pommes == serpent2[:]:
                    pos_pommes.append([randint(0, 36),randint(0, 26)])

            # On fait spawn les pommes
            for i in range(len(pos_pommes)+1):
                buffet_pommes(pos_pommes[i-1])


            #si une pomme est mangé par le serpent 1
            if serpent1[0] in pos_pommes[:]:
                score1 += 1
                if sound and score1%5 != 0:
                    play_sound("manger", sound)
                elif sound and score1%5 == 0:
                    play_sound("rot", sound)
                pos_pommes.remove(serpent1[0])
                serpent1.append([serpent1[0][0], serpent1[0][1]])

            #si une pomme est mangé par le serpent 2
            if serpent2[0] in pos_pommes[:]:
                score2 += 1
                if sound and score2%5 != 0:
                    play_sound("manger", sound)
                elif sound and score2%5 == 0:
                    play_sound("rot", sound)
                pos_pommes.remove(serpent2[0])
                serpent2.append([serpent2[0][0], serpent2[0][1]])


            mise_a_jour()



### MODE ORDINATEUR   ########################################################

        if ordi == True and depart:

            # Si la pos x du serprent et de pomme sont les mêmes
            if serpentordi[0][0] == pommes[0]:
                # si la pos x du serpent est plus grande que celle de la pomme
                if serpentordi[0][1] > pommes[1]:
                    directionordi = (0, -1)
                # si la pos x du serpent est plus petite que celle de la pomme
                elif serpentordi[0][1] < pommes[1]:
                    directionordi = (0, 1)

            # Si la pos y du serprent et de pomme sont les mêmes
            elif serpentordi[0][1] == pommes[1]:
                # si la pos y du serpent est plus grande que celle de la pomme
                if serpentordi[0][0] > pommes[0]:
                    directionordi = (-1, 0)
                # si la pos y du serpent est plus petite que celle de la pomme
                elif serpentordi[0][0] < pommes[0]:
                    directionordi = (1, 0)

            # Si la pos x de la pomme est plus grande que celle du serpent
            elif pommes[0] - serpentordi[0][0] >= 1:
                directionordi = (1, 0)

            # Si la pos x de la pomme est plus petite que celle du serpent
            elif pommes[0] - serpentordi[0][0] <= -1:
                directionordi = (-1, 0)

            if i == 1:
                direction1 = directionordi

            # quand le serpent ordinateur mange une pomme.
            if serpentordi[0] == pommes and ordi:
                scoreordi += 1
                pommes = [randint(0,36), randint(0,26)]
                serpentordi.append([serpentordi[0][0], serpentordi[0][1]])

        deplacement_serpent(serpentordi,directionordi)


        # attente avant rafraîchissement
        sleep(1/framerate)


### Menu GAME OVER ###########################################################


    while gameover:

        #si les modes duo et ordi sont désactivés
        if duo == False and ordi == False:
            image(299.5,226.7,'assets/bggameover.png', ancrage = "center")
            texte(350, 10,(score1), taille = "30", couleur = 'white',
                  police = 'benguiat')
            rectangle(430,380,580,430,couleur = 'white')
            texte(457, 385,("Menu"), taille = "25", couleur = 'white',
                  police = 'benguiat')
            rectangle(30,380,210,430,couleur = 'white')
            texte(50, 385,("Rejouer"), taille = "25", couleur = 'white',
                  police = 'benguiat')

            mise_a_jour()

        #si les modes duo et ordi sont activés
        if duo == True or ordi == True:
            if duo:
                image(299.5,226.7,'assets/bggameoverduo.png', ancrage = "center")
                texte(165, 18,(score1), taille = "15", couleur = 'white',
                      police = 'benguiat')
                texte(540, 18,(score2), taille = "15", couleur = 'white',
                      police = 'benguiat')

            #si le mode ordi est activé
            if ordi:
                image(299.5,226.7,'assets/bggameoverordi.png', ancrage = "center")
                texte(165, 18,(score1), taille = "15", couleur = 'white',
                      police = 'benguiat')
                texte(540, 18,(scoreordi), taille = "15", couleur = 'white',
                      police = 'benguiat')

            # si le joueur 2 a gagné et mode duo activé
            if gagnant2 == True and duo == True:
                texte(200, 295,("Le joueur 2 gagne"), taille = "15",
                      couleur = 'white', police = 'benguiat')

            # si le joueur 1 a gagné
            elif gagnant1:
                texte(200, 295,("Le joueur 1 gagne"), taille = "15",
                      couleur = 'white', police = 'benguiat')

            # si l'ordinateur a gagné
            elif gagnantordi == True and ordi == True:
                texte(200, 295,("L'ordinateur gagne"), taille = "15",
                      couleur = 'white', police = 'benguiat')

            #BOUTONS MENU GAMEOVER
            rectangle(430,380,580,430,couleur = 'white')
            texte(457, 385,("Menu"), taille = "25", couleur = 'white',
                  police = 'benguiat')
            rectangle(30,380,210,430,couleur = 'white')
            texte(50, 385,("Rejouer"), taille = "25", couleur = 'white',
                  police = 'benguiat')

            mise_a_jour()

        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            boucle = False
            break

        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            #Bouton Retour
            if 430 <= abscisse(ev) <= 580 and 380 <= ordonnee(ev) <= 430:
                gameover = False
                menu = True
                ordi = False
                duo = False
                play_sound("clic", sound)
                continue

            #Bouton Rejouer MODE DUO
            elif (30 <= abscisse(ev) <= 210 and 380 <= ordonnee(ev) <= 430 and
                  duo == True):
                gameover = False
                solo = True
                duo = True
                continue

            #Bouton Rejouer MODE SOLO
            elif (30 <= abscisse(ev) <= 210 and 380 <= ordonnee(ev) <= 430 and
                  duo == False and ordi == False):
                gameover = False
                solo = True
                continue

            #Bouton Rejouer MODE ORDI
            elif (30 <= abscisse(ev) <= 210 and 380 <= ordonnee(ev) <= 430 and
                  ordi == True):
                gameover = False
                ordi = True
                solo = True
                continue

        mise_a_jour()


ferme_fenetre()
