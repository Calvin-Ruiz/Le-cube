from tkinter import Tk, Label, Button, Canvas, Scale, PhotoImage, Entry
from time import sleep, time
module = False
try:
    from Lib_editor import Fenit
    module = True
except:
    pass

# Erreur lors d'interaction avec un bloc Special
# Erreur d'initialiation dans demarrer à la suite d'un test

### Modification de la gestion des éléments : les informations seront à présent dans les librairies de blocs
### La couleur par défaut sera la couleur avant modification
"""La gestion des blocs est une grille (pour l'instant en tout cas)
Les éléments sont gérés par 'types' d'objet. Il existe 5 types d'éléments :
Sol, Plafond (pour passages étroits), Portail,
Orbe (sphère que l'on active en sautant) et Special qui est customisable.
Special servira par la suite pour la création de blocs complexes par les utilisateurs.
Les objets sont rangés comme objet[numero du TYPE d'objet][0 = objet, 1 = coordonnée x, 2 = coordonnée y][numero de l'objet parmis tous ceux de son type]"""
# ------------ Chargement des paramètres globaux ------------ #
try:
    Globals = open("Elements_globaux.config", "r", encoding="Utf-8")
    temps_pause, coul_cube, version, commandes, Librairies, Taille = eval(Globals.read())
    Globals.close()
except:
    try:
        Globals = open("Elements_globaux.config", "r", encoding="Utf-8")
        Tout = Globals.read()
        Globals.close()
        print("Une erreur est survenue lors du chargement des paramètres globaux.")
        print(Tout)
        version = eval(Tout)[2]
    except:
        temps_pause, coul_cube, version, commandes, Librairies, Taille = (0.01, "skin default", 6.0, ["<space>", "<KeyRelease-space>", "<Key-p>", "<Key-r>", "<Escape>"], ["Blocs"], False)
        Globals = open("Elements_globaux.config", "w", encoding="Utf-8")
        Globals.write(str((temps_pause, coul_cube, version, commandes, Librairies, Taille)))
        Globals.close()

if version == 6.0:
    pass # Cas principal donc testé en premier, donne rien en retour, mais il faut remplir avec quelque-chose...
elif version < 6.0: # si la version est ultérieure
    version = 6.0
    Globals = open("Elements_globaux.config", "w", encoding="Utf-8")
    Globals.write(str((temps_pause, coul_cube, version, commandes, Librairies, Taille)))
    Globals.close()
else:
    print("La version de la librairie 'Le_cube_lib' est trop ancienne (version 6.0)\n",
          "Il est possible que cela provoque des bugs, ou d'autres problèmes.\n",
          "Veuillez prendre la version ", version, " ou une version supérieure.", sep="")
    temps_pause, coul_cube, version, commandes, Librairies, Taille = (0.01, "skin default", 6.0, ["<space>", "<KeyRelease-space>", "<Key-p>", "<Key-r>", "<Escape>"], ["Blocs"], False)
    if Input("Vos paramètres personnels ne peuvent pas être chargé pour cette version.\nVoulez-vous les réinitialiser ?") in ["oui", "o", "Oui", "O"]:
        Globals = open("Elements_globaux.config", "w", encoding="Utf-8")
        Globals.write(str((temps_pause, coul_cube, version, commandes, Librairies, Taille)))
        Globals.close()
    else:
        print("Les valeurs par défaut seront utilisés pour ces paramètres.\nPour conserver vos anciens paramètres globaux, ne touchez pas aux boutons 'paramètres', 'Librairies' et 'petit'.")
if Taille:
    ech = 1.6
else:
    ech = 1
# ------------------------------------------------------------------------- #

# ---------- Classes des éléments ---------- #
# renvoie True si contact (ET activation pour Orbe()) et False sinon (SAUF 'Special')

def Sol(num, a):
    "Sol du niveau pour les blocs, bloc principal"
    global speed, objets, inverse, hauteur, saut, vie, can, ech
    # importe vitesse, objets, nombre d'éléments, si inversé ou pas, hauteur du cube, mouvement du cube, si en vie, fenêtre de jeu
    objets[num][1][a] = objets[num][1][a] - speed   # déplace l'objet
    can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+5)*ech+2)
    # redéfinit les nouvelle coordonnées de l'objet
    # ----- Test interaction ----- #
    if objets[num][1][a] < 40 and objets[num][1][a] > 20:               # si l'objet est dans la même "colonne" que le cube :
        if hauteur > objets[num][2][a] and hauteur-20 < objets[num][2][a]:# si le cube traverse l'objet
            if inverse:                                                     # si la gravité est inversée
                if hauteur - 20 - saut >= objets[num][2][a]:                  # si le cube ne traversait pas l'objet avant d'être affecté par la gravité
                    if saut < 0:                                                # si on descendait :
                        hauteur = objets[num][2][a] + 20                          # définir la hauteur pour que le cube soit sur l'objet
                        saut = 0                                                  # le mouvement vertical est 0
                        return True                                               # faire l'action spécifique à l'objet
            else:                                                           # si la gravité est normale
                if hauteur + saut <= objets[num][2][a]:                       # si le cube ne traversait pas l'objet avant d'être affecté par la gravité
                    if saut < 0:                                                # si on descendait (ou montait, comme on veux...) :
                        hauteur = objets[num][2][a]                               # définir la hauteur pour que le cube soit sous l'objet
                        saut = 0                                                  # le mouvement vertical est 0
                        return True                                               # faire l'action spécifique à l'objet
            vie = False                                                     # Perdu si le cube traversait l'objet avant d'être affecté par la gravité
    return False                                                        # ne pas faire l'action spécifique à l'objet (= pas de changement)

def Plafond(num, a):
    "Plafond, peut être utilisé pour des passages étoits"
    global speed, objets, inverse, hauteur, saut, vie, can, ech
    objets[num][1][a] = objets[num][1][a] - speed
    can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+5)*ech+2)
    if objets[num][1][a] < 40 and objets[num][1][a] > 20:
        if hauteur > objets[num][2][a] and hauteur-20 < objets[num][2][a]:
            if inverse:
                if hauteur - saut-0.1 <= objets[num][2][a]:
                    hauteur = objets[num][2][a]
                    saut = 0
                    return True
            else:
                if hauteur - 20 + saut+0.1 >= objets[num][2][a]:
                    hauteur = objets[num][2][a] + 20
                    saut = 0
                    return True
            vie = False
    return False

def Portail(num, a):
    "Portails, donnent des effets divers.\nDisparais après utilisation"
    global objets, speed, hauteur, can, ech
    objets[num][1][a] = objets[num][1][a] - speed
    if objets[num][1][a] < 40 and objets[num][1][a] > 20:
        if hauteur > objets[num][2][a] and hauteur < objets[num][2][a]+40:
            objets[num][2][a] = -50 # déplace le portail hors de la zone visible
            can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+15)*ech+2)
            return True
    can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+15)*ech+2)
    return False

def Orbe(num, a):
    "Outil particulier, qui demande 'sphère' en entrée et donne True si activé.\nDisparais après utilisation"
    global objets, speed, hauteur, can, sautons, ech
    objets[num][1][a] = objets[num][1][a] - speed
    if sautons:
        if objets[num][1][a] < 40 and objets[num][1][a] > 20:
            if hauteur > objets[num][2][a] and hauteur < objets[num][2][a]+20:
                objets[num][2][a] = -50
                can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+5)*ech+2)
                return True
    can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+5)*ech+2)
    return False

def Special(num, a, parametre):
    """Permet la création de bloc complexes et renvoie :
0 si aucune interaction
1 si utilisé comme sol
2 si utilisé comme plafond
3 si utilisé comme sol (en inversé)
4 si utilisé comme plafond (en inversé)
5 si DANS le bloc"""
    global inverse, objets, speed, hauteur, saut, vie, can, Elements, ech
    # Pour la création de blocs personnalisés
    objets[num][1][a] = objets[num][1][a] - speed
    if Elements.action[num][-1](objets[num][1][a]):
        can.coords(objets[num][0][a], (objets[num][1][a]+5)*ech, (objets[num][2][a]+5)*ech+2)
        if objets[num][1][a] < 40 and objets[num][1][a] > 20:
            if hauteur > objets[num][2][a] and hauteur-20 < objets[num][2][a]:
                if inverse:
                    if saut <= 0:
                        if parametre[2]:
                            if hauteur - 20 - saut >= objets[num][2][a]:
                                hauteur = objets[num][2][a] + 20
                                saut = 0
                                return 3
                    else:
                        if parametre[3]:
                            if hauteur - saut-0.1 <= objets[num][2][a]:
                                hauteur = objets[num][2][a]
                                saut = 0
                                return 4
                else:
                    if saut <= 0:
                        if parametre[0]:
                            if hauteur + saut <= objets[num][2][a]:
                                hauteur = objets[num][2][a]
                                saut = 0
                                return 1
                    else:
                        if parametre[1]:
                            if hauteur - 20 + saut+0.1 >= objets[num][2][a]:
                                hauteur = objets[num][2][a] + 20
                                saut = 0
                                return 2
                return 5
    else:
        can.coords(objets[num][0][a], -50, -50)
    return 0

# ------------------------------------------ #

def lancer():
    global hauteur, saut, level, joue, air, inverse, scie, sautons, practice, pos_practice, temps_pause, vie, infini, speed, s_pause, marche, Score, objets, attente, can, fen, cube, sol, plafond, texte, Scor, Elements, fuse, toggle1, toggle2, var1, var2, var3, var4, tps, ech, deformation
    # initialisation des éléments
    debut = True
    air = False
    deformation = 0
    if practice:
        tps, hauteur, saut, inverse, scie, speed, fuse, toggle1, toggle2, var1, var2, var3, var4 = pos_practice[-1]
        tps = tps - 270
    else:
        hauteur, saut, tps, speed, var1, var2, var3, var4 = haut, 0, 0, 1, 0, 0, 0, 0
        inverse, scie, fuse, toggle1, toggle2 = False, False, False, False, False
    attente = 270
    while tps == 0 and level[0][hauteur//10-1] != 0:
        hauteur = hauteur - 10

    # initalisation
    vie, sautons = True, False
    marche = False
    can.coords(cube, 35*ech, (hauteur-5)*ech+2)
    if hauteur in [10, haut]:
        air = True

    # boucle de jeu
    while vie or not marche:
        temps_calculs = time()
        ### definition du sol du cube et de son mouvement ============================== #
        if marche:
            if inverse:
                if hauteur > 10 or saut > 0:
                    hauteur = hauteur + saut
                    saut = saut - 0.1
                elif hauteur < 10:
                    hauteur, saut = 10, 0
                    air = True
                elif saut != 0:
                    saut = 0
                    air = True
            else:
                if hauteur < haut or saut > 0:
                    hauteur = hauteur - saut
                    saut = saut - 0.1
                elif hauteur > haut:
                    hauteur, saut = haut, 0
                    air = True
                elif saut != 0:
                    saut = 0
                    air = True
        else:
            if attente > 0:
                attente = attente - speed
            elif debut:
                debut = False
                Pause()
            else:
                marche = True
                if practice:
                    try:
                        saut, inverse, scie, speed, fuse, toggle1, toggle2, var1, var2, var3, var4 = pos_practice[-1][2:13]
                    except:
                        pass
        b = 0

        ### Blocs spéciaux -+-+-+-+-+-+-+-+-+-+-+
        while b < len(Elements.Special):
            a = 0
            Inf, Iden = Elements.Special[b]
            while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                c = Special(Iden, a, Inf)
                Elements.action[Iden][c]()
                a=a+1
            b=b+1
        b = 0

        ### Prioritaire  -+-+-+-+-+-+-+-+-+-+-+-+
        while b < len(Elements.Prioritaire):
            a=0
            Iden = Elements.Prioritaire[b][1]
            if not Elements.Prioritaire[b][0]:
                while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                    if Sol(Iden, a):
                        Elements.action[Iden]()
                    a=a+1
            else:
                while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                    if Plafond(Iden, a):
                        Elements.action[Iden]()
                    a=a+1
            b=b+1
        b = 0

        ### Autres -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        while b < len(Elements.Autre):
            a=0
            Iden = Elements.Autre[b][1]
            if not Elements.Autre[b][0]:
                while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                    if Sol(Iden, a):
                        Elements.action[Iden]()
                    a=a+1
            else:
                while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                    if Plafond(Iden, a):
                        Elements.action[Iden]()
                    a=a+1
            b=b+1
        b = 0

        ### Type_prioritaire -+-+-+-+-+-+-+-+-+-+
        while b < len(Elements.Type_prioritaire):
            a=0
            Iden = Elements.Type_prioritaire[b][1]
            if Elements.Type_prioritaire[b][0]:
                while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                    if Portail(Iden, a):
                        Elements.action[Iden]()
                    a=a+1
            else:
                while a < Elements.elements[Iden][0] and objets[Iden][1][a] > -10:
                    if Orbe(Iden, a):
                        Elements.action[Iden]()
                    a=a+1
            b=b+1
        b = 0

        ### Si action ("<espace>" par défaut) -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        if sautons and marche:
            if air and saut in [-0.1, 0]:
                if scie:
                    inverse = not inverse
                    saut = -saut-0.1
                    hauteur = hauteur + saut
                elif not fuse:
                    saut = 2.3
                air = False
            if fuse:
                saut = saut/1.2 + 0.3
                if hauteur < 10:
                    hauteur, saut = 0, 0
        can.coords(cube, 35*ech, (hauteur-5)*ech+2)
        if tps%10 < speed:
            if len(level) > int(tps//10):
                tour = 0
                while tour < info_haut:
                    if not level[int(tps//10)][tour] == 0:
                        v = level[int(tps//10)][tour]-1
                        try:
                            objets[v][1] = [300-tps%10] + objets[v][1][0:-1]
                            objets[v][2] = [tour*10] + objets[v][2][0:-1]
                        except IndexError:
                            print("Le bloc d'ID", v, "n'a pas pu être placé.")
                            print("Nombre d'objets :", len(objets))
                            print(end="Infos sur l'objet :")
                            if v < len(Elements.elements):
                                print("Nombre de blocs maximum :", Elements.elements[v][0])
                                print("Texture attribuée :", Elements.elements[v][1])
                                print("Nom du bloc :", Elements.elements[v][2])
                                print(end="Image chargée : ")
                                if len(Elements.elements) > 3:
                                    print("oui")
                                else:
                                    print("NON")
                            else:
                                print("L'ID n'est attribué à aucun des blocs chargés.\nL'erreur peut être liée à un problème de librairie.")
                    tour=tour+1
                if tps%50 < speed and marche and practice and pos_practice[-1][0] < tps-10:
                    if deformation == 0:
                        pos_practice.append((tps, hauteur, saut, inverse, scie, speed, fuse, toggle1, toggle2, var1, var2, var3, var4))
                    else:
                        deformation += -1
            elif tps/10-28 > len(level):
                vie, infini = False, False
                pos_practice.clear()
            score = int(tps*10-2600)//(len(level)+3)
            Sco.itemconfig(Scor, text=str(score)+"%")
        tps=tps+speed
        Sco.coords(Score, 2, 2, (int((tps*10-2600)/len(level))+1), 11)
        can.update()
        a = temps_pause+temps_calculs-time()
        if a > 0 and marche:
            sleep(a)
    inverse = True
    hauteur, saut, s_pause = haut, 0, 0
    score = (tps*10-2600)//len(level)
    if score > 100:
        print("100%")
        a = 35*ech
        b = 300*ech
        c = can.coords(cube)[1]
        while a < b:
            can.coords(cube, a, c)
            can.update()
            sleep(temps_pause)
            a=a+3
        if practice:
            practice_mode(None)
        try:
            fen.destroy()
        except:
            pass
    else:
        print(int(score), "%", sep="")

texte = None

def Fenetre_de_jeu():
    global fen, can, bouton, sol, plafond, haut, Score, Sco, commandes, texte, Scor, practice, coul_cube, Elements, librairies, ech, img_cube
    fen = Tk(className="Le cube")
    fen.bind(commandes[0], clic)            # barre d'espace enfoncée
    fen.bind(commandes[1], declic)          # barre d'espace relachée
    fen.bind(commandes[2], practice_mode)   # passe en mode practice
    fen.bind(commandes[3], retrait_point)   # retire un point de retour practice
    fen.bind(commandes[4], Pause)           # mettre en pause
    fen.bind("<Key-a>", Crash_analyser)     # ouvrir l'analyseur de crash
    fen.bind("<Button-2>", force_demarrer)
    Sco = Canvas(fen, width=100, height=10, bg="light yellow")
    Sco.pack()
    if practice:
        Score = Sco.create_rectangle(0, 0, 0, 0, fill="cyan")
    else:
        Score = Sco.create_rectangle(0, 0, 0, 0, fill="light green")
    Scor = Sco.create_text(51, 6, text="0%")
    can = Canvas(fen, width = 300*ech, height=haut*ech)
    can.bind("<Button-1>", demarrer)
    can.pack()
    Quitter = Button(fen, text="Quitter", command=retour_menu)
    Quitter.pack(side="bottom")
    sol = can.create_line(0, haut*ech+1, 300*ech+1, haut*ech+1)
    plafond = can.create_line(0, 2, 300*ech+1, 2)
    a = 0
    if ech == 1:
        e=""
    elif ech == 1.6:
        e="big_"
    if len(Elements.elements[0]) == 3:
        while a < len(Elements.elements):
            try:
                Elements.elements[a].append(PhotoImage(file=e+"textures/"+Elements.elements[a][1] + ".gif", master=fen))
            except:
                Elements.elements[a].append(PhotoImage(file=e+"textures/default.gif", master=fen))
            a=a+1
    else:
        while a < len(Elements.elements):
            try:
                Elements.elements[a][3] = PhotoImage(file=e+"textures/"+Elements.elements[a][1] + ".gif", master=fen)
            except IndexError:
                try:
                    Elements.elements[a].append(PhotoImage(file=e+"textures/"+Elements.elements[a][1] + ".gif", master=fen))
                except:
                    Elements.elements[a].append(PhotoImage(file=e+"textures/default.gif", master=fen))
            except:
                Elements.elements[a][3] = PhotoImage(file=e+"textures/default.gif", master=fen)
            a=a+1
    try:
        img_cube = PhotoImage(file=e+"textures/"+coul_cube+".gif", master=fen)
    except:
        img_cube = PhotoImage(file=e+"textures/skin default.gif", master=fen)
    texte = can.create_text(150*ech, haut*ech/2, text="Cliquez sur la zone de jeu pour initialiser")
    fen.focus()
    fen.mainloop()

def initialisation(num, init=False):
    global Elements, can, fen, objets
    a=0
    while a < Elements.elements[num][0]:
        if init:
            objets[num][1].append(-10)
            objets[num][2].append(10)
            objets[num][0].append(can.create_image(-35, 15, image=Elements.elements[num][3]))
        else:
            objets[num][1][a] = -10
            objets[num][2][a] = 10
            can.coords(objets[num][0][a], -35, 15)
        a=a+1

def Sortie(x=0):
    global menu, Valeurs
    Valeurs.encore = False
    menu.quit()

def force_demarrer(x):
    global perdu, fen, texte, can, objets, Elements
    can.coords(texte, 0, -20)
    objets = []
    while len(objets) < Elements.Nbr_types:
        objets.append([[], [], []])
    print("Initialisation")
    a=0
    while a < Elements.Nbr_types:
        initialisation(a, True)
        a = a + 1
    print("Lancement")
    b = lancer()

def demarrer(x):
    global perdu, fen, texte, can, objets, Elements, cube, img_cube
    if perdu:
        perdu = False
        can.coords(texte, 0, -20)
        objets = []
        while len(objets) < Elements.Nbr_types:
            objets.append([[], [], []])
        c = True
        while not perdu:
            a = 0
            while a < Elements.Nbr_types:
                initialisation(a, c)
                a = a + 1
            cube = can.create_image(35*ech, (haut-5)*ech+2, image = img_cube)
            try:
                lancer()
            except:
                break
            c = False
            try:
                can.delete(cube)
            except:
                break
        perdu = True

def retour_menu(x=0):
    global fen, temps_pause, vie, perdu
    perdu = True
    if vie:
        vie = False
        fen.quit()
        try:
            fen.destroy()
        except:
            pass
    else:
        try:
            fen.quit()
            fen.destroy()
        except:
            try:
                fen.destroy()
            except:
                pass

def clic(souris):
    global sautons
    sautons = True

def declic(souris):
    global sautons
    sautons = False

def retrait_point(a=None):
    global pos_practice, marche, practice, vie
    if len(pos_practice) > 1:
        del pos_practice[-1]
        print("Point practice retiré")
    else:
        print("Il n'y a pas de point practice à retirer")
    if practice:
        vie = False
        if not marche:
            Pause()
            marche = True

def Pause(a=None):
    global speed, s_pause, marche, attente
    if attente < 1:
        print("Pause")
        marche = False
        attente = 1
        speed, s_pause = s_pause, speed
    elif attente == 1:
        print("Play")
        marche = True
        attente = 0
        speed, s_pause = s_pause, speed
    else:
        print("Vous ne pouvez pas mettre en pause pendant l'initialisation")

def practice_mode(p):
    global practice, vie, pos_practice, marche, Score, Sco, haut
    if practice:
        Sco.itemconfig(Score, fill="light green")
        practice = False
        print("Mode normal - Relance le niveau")
        vie = False
        if not marche:
            Pause()
    else:
        Sco.itemconfig(Score, fill="cyan")
        practice = True
        pos_practice = [[270, haut, 0, False, False, 1, False, False, False, 0, 0, 0, 0]]
        print("Mode practice")

def New_level(a=0):
    global level, all_levels, max_liste_levels
    aff = Input("Entrez le nom du niveau : ")
    try:
        fix = open(aff+".cubelvl", "r", encoding="Utf-8")
        fix.close()
        all_levels.append(aff)
        ajout = open("Levels.txt", "w", encoding="Utf-8")
        ajout.write(str(all_levels))
        ajout.close()
    except:
        if Input("Le niveau '" + str(aff) + "' est inexistant.\nVoulez-vous l'ajouter à la liste (pour le créer) ?") in ["oui", "Oui"]:
            all_levels.append(aff)
            ajout = open("Levels.txt", "w", encoding="Utf-8")
            ajout.write(str(all_levels))
            ajout.close()
    max_liste_levels = len(all_levels)//5
    if len(all_levels)%5 == 0:
        max_liste_levels = max_liste_levels - 1
    raffraichir()

def Retrait():
    global aff, all_levels, Sup
    del all_levels[aff]
    fichier_niveaux = open("Levels.txt", "w", encoding="Utf-8")
    fichier_niveaux.write(str(all_levels))
    fichier_niveaux.close()
    raffraichir()
    Sup.destroy()

def updateLabel(x):
    global level_up, montrer, Sup
    level_up = int(x)
    montrer.destroy()
    montrer = Canvas(Sup, width=300, height=10*level_up, bg="light yellow")
    montrer.pack(side="top")
    regarde = []
    while len(regarde) < level_up:
        regarde.append(montrer.create_rectangle(len(regarde)%2*10, len(regarde)*10, len(regarde)%2*10+10, len(regarde)*10+10, fill="red"))

def Créer_niv():
    global Sup, lab, ligne_1, ligne_2, Oui, Non, Créer, scal, montrer
    ligne_1.destroy()
    ligne_2.destroy()
    Oui.destroy()
    Créer.destroy()
    Non.destroy()
    valid = Button(Sup, text="Créer le niveau", command=Valider_nouveau_niveau)
    Maximum = (Sup.winfo_vrootheight() // 10) - 5
    scal = Scale(Sup, length=360, orient="horizontal", label ='Hauteur du niveau en cubes :',
      troughcolor ='dark grey', sliderlength = 20,
      showvalue =10, from_=10, to=100,
      command=updateLabel)
    scal.pack(side="top")
    montrer = Canvas(Sup, width=300, height=100, bg="light yellow")
    montrer.pack()
    valid.pack(side="bottom")

def Valider_nouveau_niveau():
    global Sup, level_up, level, aff
    level_up = eval("[0" + ",0"*(level_up-1) + "]")
    level = [level_up, level_up]
    while len(level) < 30:
        level.append(level_up)
    Haut=len(level_up)
    Sup.destroy()
    Sauv = open(all_levels[aff]+".cubelvl", "w", encoding="Utf-8")
    Sauv.write(str(level) + ", " + str(version) + ", ['Blocs']")
    Sauv.close()

def ouvre_fichier(a):
    global level, all_levels, classe_levels, aff, Sup, niv, ligne_1, ligne_2, Oui, Non, Créer, librairies, Elements
    try:
        aff = classe_levels*5 + a
        fix = open(all_levels[aff]+".cubelvl", "r", encoding="Utf-8")
        level = eval(fix.read())
        fix.close()
        menu.quit()
    except:
        if len(all_levels) > aff:
            Sup = Tk(className="Niveau introuvable")
            ligne_1 = Label(Sup, text="Ce niveau est introuvable")
            ligne_1.pack()
            ligne_2 = Label(Sup, text="Voulez-vous le retirer de la liste ?")
            ligne_2.pack()
            Oui = Button(Sup, text="Oui", command=Retrait)
            Oui.pack(side="left")
            Non = Button(Sup, text="Non", command=Sup.destroy)
            Non.pack(side="right")
            Créer = Button(Sup, text="Créer", command=Créer_niv)
            Créer.pack()
            Sup.mainloop()
    try:
        level, version, librairies = level
    except ValueError:
        level, version = level
        librairies = ["Blocs"]
    niv = all_levels[aff]
    if version > 6.0:
        Warn = Tk(className="Warning")
        Ligne_1 = Label(Warn, text="Veuillez utiliser la version " + version + " ou supérieure pour ce niveau.").pack()
        Ligne_2 = Label(Warn, text="La version que vous utilisez est la version 6.0").pack()
        Ok = Button(Warn, text="Ok", commant=Warn.destroy).pack()
        Warn.mainloop()

def supprime_fichier(a):
    global all_levels, classe_levels, aff, Sup
    aff = classe_levels*5+a
    Sup = Tk(className="Suppresion d'un niveau")
    ligne_1 = Label(Sup, text="Voulez-vous supprimer ce niveau ?")
    ligne_1.pack()
    ligne_2 = Label(Sup, text=("Il s'agit seulement de l'entrée '"+all_levels[aff]+"', pas du fichier."))
    ligne_2.pack()
    Oui = Button(Sup, text="Oui", command=Retrait)
    Oui.pack(side="left")
    Non = Button(Sup, text="Non", command=Sup.destroy)
    Non.pack(side="right")
    Sup.mainloop()

def raffraichir():
    global liste_niveaux, classe_levels, all_levels
    id_niveaux = classe_levels*5
    a = 0
    while a < 5 and len(all_levels) > id_niveaux+a:
        liste_niveaux[a].configure(text=all_levels[id_niveaux+a])
        a = a + 1
    while a < 5:
        liste_niveaux[a].configure(text="")
        a = a + 1

def left(a=0):
    global classe_levels, all_levels, max_liste_levels
    classe_levels = classe_levels - 1
    if classe_levels < 0:
        classe_levels = max_liste_levels
    raffraichir()

def right(a=0):
    global classe_levels, all_levels, max_liste_levels
    classe_levels = classe_levels + 1
    if classe_levels > max_liste_levels:
        classe_levels = 0
    raffraichir()

# ----- initialisation des variables ----- #
perdu = True
hauteur, saut, s_pause, speed = 100, 0, 0, 1
inverse, scie, sautons, practice = False, True, False, False
air, sautons, vie, mode_jouer = True, False, False, True
try:
    fichier_niveaux = open("Levels.txt", "r", encoding="Utf-8")
    all_levels = eval(fichier_niveaux.read())
    fichier_niveaux.close()
except:
    all_levels = []
max_liste_levels = len(all_levels)//5
if len(all_levels)%5 == 0:
    max_liste_levels = max_liste_levels - 1
classe_levels = 0
aff = 0
cl = list()
CL = list()
b = 0
while b < 5:
    def cl0(a=0, c=b):
        ouvre_fichier(c)
    def CL0(a=0, c=b):
        supprime_fichier(c)
    cl.append(cl0)
    CL.append(CL0)
    del cl0, CL0
    b = b + 1

# ----- boucle principale ----- #
def Choisir():
    "Combiner avec while Valeurs.encore:"
    global menu, all_levels, liste_niveaux, level, haut, info_haut, practice, pos_practice, niv, librairies, Elements, ech, Debug, mode_jouer, Modder, lib_edit
    menu = Tk("Menu") # menu est la fenêtre où l'on choisit le niveau
    menu.bind("<Left>", left)
    menu.bind("<Right>", right)
    liste_niveaux = []
    ZZaZZ_bu=0
    while ZZaZZ_bu < 5: # changer par un 'for'
        try:
            liste_niveaux.append(Label(menu, text=all_levels[ZZaZZ_bu]))
        except:
            liste_niveaux.append(Label(menu, text=""))
        liste_niveaux[-1].bind("<Button-1>", cl[ZZaZZ_bu])
        liste_niveaux[-1].bind("<Button-3>", CL[ZZaZZ_bu])
        liste_niveaux[-1].pack()
        ZZaZZ_bu = ZZaZZ_bu + 1
    if lib_edit:
        Modder = Button(menu, text="Mode jouer", command=Switcher)
        Modder.pack(side="top")
    Au_revoir = Button(menu, text="Quitter", command=Sortie)
    Au_revoir.pack(side="bottom")
    Nouv = Button(menu, text="Nouveau", command=New_level)
    Nouv.pack(side="left")
    Libre = Button(menu, text="Librairies", command=LIBRE)
    Libre.pack(side="left")
    if ech == 1:
        TxT = "Petit"
    else:
        TxT="Grand"
    Debug = Button(menu, text=TxT, command=Retailler)
    Debug.pack(side="left")
    menu.mainloop()

    # --- fin de la fenêtre menu --- #
    try:
        menu.destroy()  # on s'assure que la fenêtre est bien fermée
    except:
        pass
    haut = len(level[0])*10
    info_haut = len(level[0])
    practice = False
    pos_practice = []
    Elements.init(librairies)
    if lib_edit:
        return info_haut, level, version, niv, Elements.Nbr_types, librairies, int(ech*10), mode_jouer

def Retailler():
    global Debug, ech
    if ech == 1:
        Debug.config(text="Grand")
        ech = 1.6
        T = True
    else:
        Debug.config(text="Petit")
        ech = 1
        T = False
    file = open("Elements_globaux.config", "r", encoding="Utf-8")
    tout = eval(file.read())
    tout = list(tout)
    tout[-1] = T
    file.close()
    file = open("Elements_globaux.config", "w", encoding="Utf-8")
    file.write(str(tout))
    file.close()

def Switcher():
    global mode_jouer, Modder
    if mode_jouer:
        Modder.config(text="Mode éditer")
    else:
        Modder.config(text="Mode jouer")
    mode_jouer = not mode_jouer

def Test_edit(level_edit, p_prac):
    "Dépendance de 'Le cube éditeur'\nIntéragit avec les valeurs interne de 'Le_cube_lib'."
    global level, practice, pos_practice
    practice = True
    level = level_edit
    pos_practice = p_prac

def LIBRE():
    global menu, fenlib, module, librairies_L, Libraires
    fenlib = Tk(className="Librairie")
    lab = Label(fenlib, text="Le redémarrage du jeu est nécessaire pour appliquer ces modifications.")
    lab.pack()
    a=1
    lb = Librairies[0]
    while a < len(Librairies):
        lb += "\n" + Librairies[a]
        a=a+1
    librairies_L = Label(fenlib, text=lb)
    librairies_L.bind("<Button-3>", retrait_lib)
    librairies_L.pack()
    ajout = Button(fenlib, text="Ajouter une librairie", command=add_lib)
    ajout.pack()
    if module:
        edit = Button(fenlib, text="Ouvrir l'éditeur de librairies", command=Fenit)
        edit.pack()
    retour = Button(fenlib, text="Retour", command=fenlib.destroy)
    retour.pack()
    fenlib.focus()
    fenlib.mainloop()

def add_lib():
    global temps_pause, coul_cube, version, commandes, Librairies, librairies_L, Taille
    a = Input("Entrez le nom de la librairie")
    try:
        file = open(a+".lib", 'r', encoding='Utf-8')
        file.close()
        Librairies.append(a)
        Globals = open("Elements_globaux.config", "w", encoding="Utf-8")
        Globals.write(str((temps_pause, coul_cube, version, commandes, Librairies, Taille)))
        Globals.close()
    except:
        print("Nom de librairie incorrect.")
    a=1
    lb = Librairies[0]
    while a < len(Librairies):
        lb += "\n" + Librairies[a]
        a=a+1
    librairies_L.config(text=lb)


def retrait_lib(a):
    global temps_pause, coul_cube, version, commandes, Librairies, librairies_L
    if (a.y-3)//15 > 0:
        try:
            del Librairies[(a.y-3)//15]
            Globals = open("Elements_globaux.config", "w", encoding="Utf-8")
            Globals.write(str((temps_pause, coul_cube, version, commandes, Librairies, Taille)))
            Globals.close()
        except:
            pass
    a=1
    lb = Librairies[0]
    while a < len(Librairies):
        lb += "\n" + Librairies[a]
        a=a+1
    librairies_L.config(text=lb)


def Input(raison):
    global tp, ent, Ent
    tp = Tk()
    l = Label(tp, text=raison)
    l.pack()
    ent = Entry(tp)
    ent.pack()
    valid = Button(tp, text="Ok", command=entry)
    valid.pack()
    tp.focus()
    tp.mainloop()
    try:
        tp.destroy()
    except:
        pass
    return Ent

def entry():
    global tp, ent, Ent
    Ent = ent.get()
    tp.quit()

def Crash_analyser(a=None):
    bouh = Tk()
    bouh.focusmodel("active")
    inf = Label(bouh, text="Enregistre les valeurs dans un fichier")
    inf.pack()
    mince = Button(bouh, text="Analyser le bug actuel", command=Report)
    mince.pack()
    place = Label(bouh, text="\n")
    place.pack()
    malade = Button(bouh, text="Analyse COMPLETE (Difficile à exploiter)", command=Report_X)
    malade.pack()
    bouh.mainloop()

def Report_X():
    print("Report complet en cours...")
    file = open(str(int(time())) + " big crash report", "w", encoding="Utf-8")
    file.write("lancer, Choisir, Fen = "+str(lancer.__globals__) + ", " + str(Choisir.__globals__) + ", " + str(Fenetre_de_jeu.__globals__))
    file.close()
    print("Report terminé.")

def Report():
    "Enregistre la valeur de toutes les variables"
    global Elements, objets, level
    file = open(str(int(time())) + " crash report", "w", encoding="Utf-8")
    file.write("Elements, objets, level = " + str(Elements.__dict__) + "," + str(objets) + "," + str(level))
    file.close()

### ----- Définition des classes ----- ###

class Valeurs:
    encore = True

# Les_blocs = Fichier.read() --> [[Type, si_prioritaire, action], [Type, si_prioritaire, action], ...]
# Elements.Type_prioritaire --> [[Type, pos], [Type, pos], ...]
# Portails : 0 puis True
# Sphères  : 1 puis False
# Sol      : 2 puis False
# Plafonds : 3 puis True
# Special  : 4 puis Propriétés (contenues à la place du booléen)

class Any_libs:
    global Librairies
    def Rien():
        pass
    a = 0
    blocs = []
    while a < len(Librairies):
        try:
            file = open(Librairies[a] + ".lib", "r", encoding="Utf-8")
            Content = file.read()
            file.close()
        except FileNotFoundError:
            if a == 0:
                file = open("Blocs.lib", "w", encoding="Utf-8")
                Content = [[2, False, 'global air\n    air = True', 40, "sol", "sol"],
                           [4, [False, False, False, False], ['pass', 'pass', 'pass', 'pass', 'global vie\n    vie = False', "return True"], 50, "obstacle", "obstacles"],
                           [2, True, 'global saut\n    saut = 3.2', 5, "sauteur", "sauteur"],
                           [3, False, 'pass', 40, "plafond", "plafond"],
                           [0, False, 'global inverse, saut\n    inverse = not inverse\n    saut = -saut', 4, "portail inverseur", "portail inverseur"],
                           [0, False, 'global speed\n    speed = speed * 1.2\n    if speed > 2:\n        speed = 2', 4, "portail accelerateur", "acélérateur"],
                           [0, False, 'global speed\n    speed = speed / 1.2\n    if speed > 0.7:\n        speed = 0.7', 4, "portail decelerateur", "ralentisseur"],
                           [0, False, 'global scie\n    scie = not scie', 4, "portail scie", "portail scie"],
                           [2, True, 'global inverse\n    inverse = not inverse', 10, "sauteur inverseur", "saut inverseur"],
                           [3, False, 'global sautons, saut\n    if not sautons:\n        saut = 0.2', 40, "plafond collant", "bloc collant"],
                           [0, False, 'global speed\n    speed = 1', 4, "portail vitesse normale", "vitesse normale"],
                           [0, False, 'global fuse, scie\n    fuse, scie = False, False', 4, "portail cube", "mode normal"],
                           [0, False, 'global fuse\n    fuse = not fuse', 4, "portail fusee", "portail fusée"],
                           [1, False, 'global inverse, saut\n    inverse = not inverse\n    saut = -saut', 10, "sphere inverseur", "sphere d'inversion"],
                           [1, False, 'global saut\n    saut = 3.2', 10, "sphere super saut", "sphere super-saut"],
                           [1, False, 'global saut\n    saut = 2.3', 10, "sphere saut", "sphere saut"],
                           [1, False, 'global saut\n    saut = -2.3', 10, "sphere anti saut", "sphere anti-saut"],
                           [4, [True, True, True, True], ['global air\n    air = True', 'pass', 'global air\n    air = True', 'pass', 'pass', "return True"], 20, "surface", "surface"]]
                Content = str(Content)
                file.write(Content)
                file.close()
            else:
                print("File '" + Librairies[a] + ".lib' is not readable.")
                print("Librairie ", a+1, "/", len(Librairies), " non chargée", sep='')
                continue
        if "(" in Content or "import" in Content:
            print("Unautorised syntax detected in '" + Librairies[a] + ".lib'\n'import' and '(' arguments was unautorised for library.")
            print("Librairie ", a+1, "/", len(Librairies), " non chargée", sep='')
            continue
        try:
            Content = eval(Content)
        except:
            print("FormatError : File '", Librairies[a], ".lib' is not in Le cube's library format.")
            print("Librairie ", a+1, "/", len(Librairies), " non chargée", sep='')
        Nb_types = len(Content)
        erreur=False
        Type_prioritaire = []
        Prioritaire = []
        Autre = []
        Special = []
        action = []
        elements = [] # [nombre_elements, apparence, nom]
        while len(action) < Nb_types:
            r = len(action)
            l = Content[r][0]
            elements.append(Content[r][3:6])
            if l == 0:
                Type_prioritaire.append([True, r])
            elif l == 1:
                Type_prioritaire.append([False, r])
            elif l in [2, 3]:
                if Content[r][1]:
                    Prioritaire.append([l-2, r])
                else:
                    Autre.append([l-2, r])
            try:
                if l == 4:
                    Special.append([Content[r][1], r])
                    exec("def Action1():\n    " + Content[r][2][0] + 
                         "\ndef Action2():\n    " + Content[r][2][1] +
                         "\ndef Action3():\n    " + Content[r][2][2] +
                         "\ndef Action4():\n    " + Content[r][2][3] +
                         "\ndef Action5():\n    " + Content[r][2][4] +
                         "\ndef Condition(pos):\n    " + Content[r][2][5])
                    action.append([Rien, Action1, Action2, Action3, Action4, Action5, Condition])
                    del Action1, Action2, Action3, Action4, Action5, Condition
                else:
                    exec("def Action():\n    " + Content[r][2])
                    action.append(Action)
                    del Action
            except:
                erreur = True
                break
            del r, l
        if erreur:
            print("SyntaxError : Invalid syntax in file '", Librairies[a], ".lib' in '", Content[r][5], "' script", sep='')
            if l == 4:
                print("def Action1():\n    " + Content[r][2][0] + 
                         "\ndef Action2():\n    " + Content[r][2][1] +
                         "\ndef Action3():\n    " + Content[r][2][2] +
                         "\ndef Action4():\n    " + Content[r][2][3] +
                         "\ndef Action5():\n    " + Content[r][2][4] +
                         "\ndef Condition(pos):\n    " + Content[r][2][5])
            else:
                print("def Action():\n    " + Content[r][2])
            print("Librairie ", a+1, "/", len(Librairies), " non chargée", sep='')
        else:
            blocs.append([Librairies[a], [Type_prioritaire, Prioritaire, Autre, Special, action, elements]])
            print("Librairie ", a+1, "/", len(Librairies), " chargée (", len(elements), " blocs)", sep='')
        a += 1
    blocs = dict(blocs)

class Elements:
    Nbr_types = 0
    Type_prioritaire = []
    Prioritaire = []
    Autre = []
    Special = []
    action = []
    elements = []
    def init(Librairies):
        global Elements, Any_libs
        Elements.Type_prioritaire.clear()
        Elements.Prioritaire.clear()
        Elements.Autre.clear()
        Elements.Special.clear()
        Elements.action.clear()
        Elements.elements.clear() # [nombre_elements, apparence, nom]
        l = 0
        while l < len(Librairies):
            ajout = len(Elements.action)
            try:
                T_p, P, A, S = eval(str(Any_libs.blocs[Librairies[l]][0:4]))
                a, e = Any_libs.blocs[Librairies[l]][4:6]
            except:
                print("Ce niveau requiert la librairie '", Librairies[l], ".lib'", sep='')
                l += 1
                continue
            b = 0
            while b < len(T_p):
                T_p[b][1] += ajout
                b=b+1
            b = 0
            while b < len(P):
                P[b][1] += ajout
                b=b+1
            b = 0
            while b < len(A):
                A[b][1] += ajout
                b=b+1
            b = 0
            while b < len(S):
                S[b][1] += ajout
                b=b+1
            Elements.Type_prioritaire   += T_p
            Elements.Prioritaire        += P
            Elements.Autre              += A
            Elements.Special            += S
            Elements.action             += a
            Elements.elements           += e
            l += 1
        Elements.Nbr_types = len(Elements.elements)

try:
    file = open("News.txt", "r", encoding="Utf-8")
    news = file.read()
    file.close()
except:
    news = """Déja, ce message s'affichera une seule fois.
Si vous cliquez sur la croix pour fermer ce message,
il s'affichera à nouveau quand vous relancerez Le cube.
- Un clic gauche sur un niveau permet d'y jouer ou de l'éditer -
- Un clic droit permet de retirer un niveau de la liste -
Les flèches gauche et droite permettent de passer d'une page à l'autre.
Certaines fonctionnalités comme l'éditeur de librairies requiert la présence d'une librairie pour apparaitre.
Le nombre maximum pour chaque élément est important, il peux affecter le temps de chargement.
Pour générer un rapport de bug, appuyez sur la touche 'a'.
Les autres commandes sont personnalisables dans l'éditeur.
"""
if news != "":
    def lu():
        global News
        file = open("News.txt", "w", encoding="Utf-8")
        file.write("")
        file.close()
        News.quit()
    News = Tk()
    Label(News, text="Information relative à Le cube :", font="Arial", foreground="red").pack()
    Label(News, text=news[0:-1], font="Arial").pack()
    OK = Button(News, text="OK", command=lu)
    OK.pack()
    News.focus()
    News.mainloop()
    try:
        News.destroy()
    except:
        pass

try:
    file = open("Le cube launcher.py", "r")
    file.close()
    lib_edit = True
except:
    lib_edit = False
    while True:
        Choisir()
        if Valeurs.encore:
            Fenetre_de_jeu()
        else:
            break
