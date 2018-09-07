from Le_cube_core import Valeurs, Choisir, Test_edit, Fenetre_de_jeu, Elements, Input
from tkinter import Toplevel, Tk, Button, Label, Canvas, PhotoImage
from time import sleep, time

# Afficher la texture des blocs dans le choix de bloc

# ---------- initialisation ---------- #
Globals = open("Elements_globaux.config", "r", encoding="Utf-8")
temps_pause, coul_cube, version, commandes, Librairies, Taille = eval(Globals.read())
Globals.close()
cliquant = False
# Test de la version du fichier de configurations
indication = []
elements, position, mode = [], 0, 1
if int(1/temps_pause) < 1/temps_pause - 0.5:
    T_pause = int(1/temps_pause) + 1
else:
    T_pause = int(1/temps_pause)
Texte = [str(T_pause), coul_cube]
# Need to be reloadable
AddTxt = []
coul_obstacles = []
nombre_elements = []
Texte.append([])
Texte.append(AddTxt)
Texte.append(coul_obstacles)
lequel = 0
value = 0
ech = 10

def Edit_declic(a=0):
    global cliquant
    cliquant = False

def Edit_Clic(vide=0, a=True):
    global cliquant, can, level, elements, position, mode, coul_obstacles, temps_pause, ech
    if a:
        cliquant = True
    px = fen.winfo_pointerx()-can.winfo_rootx()
    py = fen.winfo_pointery()-can.winfo_rooty()
    try:
        level[px//ech+position][py//ech] = 0
        elements.append(can.create_rectangle(px//ech*ech, py//ech*ech+2, px//ech*ech+ech, py//ech*ech+ech+2, fill="light yellow"))
    except IndexError:
        pass
    if cliquant:
        sleep(temps_pause)
        can.update()
        Edit_Clic(a=False)

def Edit_clic(vide=0, a=True):
    global cliquant, can, level, elements, position, mode, Elements, portail, texturiser, ech
    if a:
        cliquant = True
    px = fen.winfo_pointerx()-can.winfo_rootx()
    py = fen.winfo_pointery()-can.winfo_rooty()
    try:
        level[px//ech+position][py//ech] = mode
    except IndexError:
        print("Out of level zone")
    if mode in portail:    # affiche portail créé
        elements.append(can.create_image(px//ech*ech+ech/2, py//ech*ech+ech*3/2+2, image=texturiser[mode-1]))
    elif mode < len(Elements.elements)+1 and mode > 0:          # affiche bloc créé
        elements.append(can.create_image(px//ech*ech+ech/2, py//ech*ech+ech/2+2, image=texturiser[mode-1]))
    else:
        elements.append(can.create_rectangle(px//ech*ech, py//ech*ech+2, px//ech*ech+ech, py//ech*ech+ech+2, fill="light yellow"))
        level[px//ech+position][py//ech] = 0
    if cliquant:
        sleep(temps_pause*2)
        can.update()
        Edit_clic(a=False)

def Droite1(a=0):
    global position
    position = position + 1
    deplacer()

def Droite2(a=0):
    global position
    position = position + 20
    deplacer()

def Gauche1(a=0):
    global position
    position = position - 1
    deplacer()

def Gauche2(a=0):
    global position, everything
    position = position - 20
    deplacer()

def recolorer():
    global Colorer, Elements, parametrage, portail, lequel, ech, col
    if ech == 10:
        e = ""
    elif ech == 16:
        e = "big_"
    try:
        col = PhotoImage(file=e+"textures/"+Elements.elements[lequel][1]+".gif", master=parametrage)
    except:
        col = PhotoImage(file=e+"textures/default.gif", master=parametrage)
    Colorer.config(image=col)

def frappe(x):
    global lequel, value, Texte, l1, l2, l3, l4, l5
    touche = x.keysym
    if value < 2:
        if len(touche) == 1:
            Texte[value] = Texte[value] + touche
        elif touche == "BackSpace":
            Texte[value] = Texte[value][0:-1]
        elif touche == "space":
            Texte[value] = Texte[value] + " "
        elif touche == "Left":
            if lequel > 0:
                lequel = lequel - 1
            else:
                lequel = len(Texte[2]) - 1
            l3.configure(text="Nom : "+Texte[2][lequel])
            l4.configure(text="Nombre max : "+Texte[3][lequel])
            l5.configure(text="Texture (GIF) : "+Texte[4][lequel])
            recolorer()
        elif touche == "Right":
            lequel = lequel + 1
            if lequel == len(Texte[2]):
                lequel = 0
            l3.configure(text="Nom : "+Texte[2][lequel])
            l4.configure(text="Nombre max : "+Texte[3][lequel])
            l5.configure(text="Texture (GIF) : "+Texte[4][lequel])
            recolorer()
        l1.configure(text="Vitesse (en fps) : "+Texte[0])
        l2.configure(text="Texture du cube (format GIF) : "+Texte[1])
    elif value < 5:
        if len(touche) == 1:
            Texte[value][lequel] = Texte[value][lequel] + touche
        elif touche == "BackSpace":
            Texte[value][lequel] = Texte[value][lequel][0:-1]
        elif touche == "space":
            Texte[value][lequel] = Texte[value][lequel] + " "
        elif touche == "Left":
            if lequel > 0:
                lequel = lequel - 1
            else:
                lequel = len(Texte[2]) - 1
            recolorer()
        elif touche == "Right":
            lequel = lequel + 1
            if lequel == len(Texte[2]):
                lequel = 0
            recolorer()
        l3.configure(text="Nom : "+Texte[2][lequel])
        l4.configure(text="Nombre max : "+Texte[3][lequel])
        l5.configure(text="Texture (GIF) : "+Texte[4][lequel])
        if value == 4:
            recolorer()
    elif value == 5:
        if len(touche) == 1:
            commandes[0] = "<Key-" + touche + ">"
        else:
            commandes[0] = "<" + touche + ">"
        commandes[1] = "<KeyRelease-" + touche + ">"
        c1.configure(text="Sauter ou activer sphère : "+commandes[0])
    else:
        if len(touche) == 1:
            commandes[value-4] = "<Key-" + touche + ">"
        else:
            commandes[value-4] = "<" + touche + ">"
        c2.configure(text="Changer de mode : "+commandes[2])
        c3.configure(text="Supprimer point de retour practice : "+commandes[3])
        c4.configure(text="Mettre en pause : "+commandes[4])
    parametrage.update()

def L1(a=0):
    global value
    value = 0
    LIPIDES()

def L2(a=0):
    global value
    value = 1
    LIPIDES()

def L3(a=0):
    global value
    value = 2
    LIPIDES()

def L4(a=0):
    global value
    value = 3
    LIPIDES()

def L5(a=0):
    global value
    value = 4
    LIPIDES()

def LIPIDES():
    "Colore de façon à indiquer le paramètre sélectionné"
    global value, l1, l2, l3, l4, l5
    a = 0
    b = ["black", "black", "black", "black", "black"]
    c=[l1, l2, l3, l4, l5]
    if value < 5:
        b.insert(value, "red")
    while a < 5:
        c[a].config(foreground=b[a])
        a=a+1

def C1(a=0):
    global value
    value = 5

def C2(a=0):
    global value
    value = 6

def C3(a=0):
    global value
    value = 7

def C4(a=0):
    global value
    value = 8

def Default(a=0):
    "parametres - réinitialise la couleur d'un type d'élément"
    global lequel, Texte, Colorer, Elements, portail, l5, ech
    Texte[4][lequel] = Elements.elements[lequel][1]
    l5.configure(text="Texture (GIF) : "+Texte[4][lequel])
    recolorer()

# ------------------------------ Fenêtre des paramètres globaux ------------------------------ #

def parametres(a=0):
    global indication2, parametrage, Texte, indication, coul_obstacles, nombre_elements, librairies, Elements, Colorer
    parametrage = Tk(className="Paramètres")
    parametrage.bind("<Key>",frappe)
    Parametres()
    parametrage.mainloop()
    try:
        parametrage.destroy()
    except:
        pass
    indication2 = ["vide"] + Texte[2]
    # enregistrement des paramètres globaux
    temps_pause, coul_cube, indication, coul_obstacles = 1/int(Texte[0]), Texte[1], Texte[2], Texte[4]
    nombre_elements = []
    while len(Texte[3]) > len(nombre_elements):
        nombre_elements.append(int(Texte[3][len(nombre_elements)]))
    Elements.elements = []
    a = 0
    c = 0
    while c < len(librairies):
        blocs = []
        Lib = open(librairies[c] + ".lib", "r", encoding="Utf-8")
        lib = eval(Lib.read())
        Lib.close()
        try:
            b = 0
            while b < len(lib):
                Elements.elements.append([nombre_elements[a], coul_obstacles[a], indication[a]])
                blocs.append(lib[b][0:3] + Elements.elements[-1])
                b += 1
                a += 1
            Lib = open(librairies[c] + ".lib", "w", encoding="Utf-8")
            Lib.write(str(blocs))
            Lib.close()
        except:
            print("Rechargez le niveau pour accéder aux paramètres de la librairie", librairies[c], "nouvellement ajoutée.")
        c += 1
    try:
        Globals = open("Elements_globaux.config", "w", encoding="Utf-8")
        Globals.write(str((temps_pause, coul_cube, version, commandes, librairies, Taille)))
        Globals.close()
    except:
        print("Impossible d'enregistrer les nouveaux paramètres globaux.")

def LIB():
    global librairies, Librairies, Elements
    a = Input("Entrez le nom de la librairie")
    if a in Librairies and not a in librairies:
        librairies.append(a)
        Elements.init(librairies)
    else:
        print("Veuillez importer cette librairie (dans le dans le menu de choix du niveau) avant de l'utiliser dans un niveau.")

def Parametres():
    global Texte, l1, l2, l3, l4, l5, Colorer, indication2, parametrage, B3, B2, B1, B0, c1, c2, c3, c4, oK, value, Elements
    try:
        c1.destroy()
        c2.destroy()
        c3.destroy()
        c4.destroy()
        oK.destroy()
    except:
        pass
    l1 = Label(parametrage, text="Vitesse (en fps) : "+Texte[0])
    l1.bind("<Button-1>", L1)
    l1.pack()
    l2 = Label(parametrage, text="Texture du cube (format GIF) : "+Texte[1])
    l2.bind("<Button-1>", L2)
    l2.pack()
    Colorer = Label(parametrage, text="L'image devrait s'afficher ici")
    Colorer.pack()
    recolorer()
    l3 = Label(parametrage, text="Nom : "+Texte[2][lequel])
    l3.bind("<Button-1>", L3)
    l3.pack()
    l4 = Label(parametrage, text="Nombre max : "+Texte[3][lequel])
    l4.bind("<Button-1>", L4)
    l4.pack()
    l5 = Label(parametrage, text="Texture (GIF) : "+Texte[4][lequel])
    l5.bind("<Button-1>", L5)
    l5.bind("<Button-3>", Default)
    l5.pack()
    B3 = Button(parametrage, text="Commandes", command=Commandes)
    B3.pack()
    B2 = Button(parametrage, text="Importer une librairie", command=LIB)
    B2.pack()
    B1 = Button(parametrage, text="Raffraichir", command=fenêtre)
    B1.pack()
    B0 = Button(parametrage, text="OK", command=parametrage.quit)
    B0.pack()
    value = 0

def Commandes():
    global l1, l2, l3, l4, l5, Colorer, parametrage, B3, B2, B1, B0, commandes, c1, c2, c3, c4, oK, value
    l1.destroy()
    l2.destroy()
    l3.destroy()
    l4.destroy()
    l5.destroy()
    Colorer.destroy()
    B3.destroy()
    B2.destroy()
    B1.destroy()
    B0.destroy()
    c1 = Label(parametrage, text="Sauter ou activer sphère : "+commandes[0])
    c1.bind("<Button-1>", C1)
    c1.pack()
    c2 = Label(parametrage, text="Changer de mode : "+commandes[2])
    c2.bind("<Button-1>", C2)
    c2.pack()
    c3 = Label(parametrage, text="Supprimer point de retour practice : "+commandes[3])
    c3.bind("<Button-1>", C3)
    c3.pack()
    c4 = Label(parametrage, text="Mettre en pause : "+commandes[4])
    c4.bind("<Button-1>", C4)
    c4.pack()
    oK = Button(parametrage, text="OK", command=Parametres)
    oK.pack()
    Tk.update(parametrage)
    value = 5

def plus(a=0):
    global mode, indication2
    mode = mode + 1
    if mode > len(indication2)-1:
        mode = 0
    lab.configure(text=indication2[mode])

def moins(a=0):
    global mode, indication2
    mode = mode - 1
    if mode < 0:
        mode = len(indication2)-1
    lab.configure(text=indication2[mode])

def deplacer():
    global level, position, elements, Elements, Haut, portail, texturiser, ech
    if position < 0:
        position = 0
    while position+30 > len(level):
        level.append(eval("[0" + ",0"*(Haut-1) + "]"))
    for a in elements:
        can.delete(a)
    elements = []
    a = position
    while len(level) > a:
        b = 0
        while len(level[0]) > b:
            if level[a][b] in portail: # affiche les portails
                elements.append(can.create_image((a-position+0.5)*ech, (b+1.5)*ech+2, image=texturiser[level[a][b]-1]))
            elif level[a][b] < len(Elements.elements)+1 and level[a][b] > 0:# affiche les autres blocs
                elements.append(can.create_image((a-position+0.5)*ech, (b+0.5)*ech+2, image=texturiser[level[a][b]-1]))
            b = b + 1
        a = a + 1

# ---------- Chargement du niveau ---------- # (remarque : 'version' concerne la version du niveau chargé)
def choisir(x):
    global mode, indication2
    mode = x
    lab.configure(text=indication2[x])

texturiser = ["pyimage1"]

def fenêtre():
    global fen, lab, can, top, parametrage, Hauteur, Haut, ligne_sol, ligne_plafond, Elements, texturiser, ech
    try:
        fen.quit()
        fen.destroy()
    except:
        try:
            fen.destroy()
        except:
            pass
    try:
        parametrage.quit()
        parametrage.destroy()
    except:
        pass
    fen = Tk(className="Editeur de niveau")
    fen.bind("<Up>", plus)
    fen.bind("<Down>", moins)
    fen.bind("<Right>", Droite1)
    fen.bind("<Left>", Gauche1)
    fen.bind("<Key-a>", Crash_analyser)
    lab = Label(fen, text="sol")
    lab.pack()
    can = Canvas(fen, width = 30*ech, height=Haut*ech)
    can.bind("<Button-1>", Edit_clic)
    can.bind("<Button-3>", Edit_Clic)
    can.bind("<ButtonRelease-1>", Edit_declic)
    can.bind("<ButtonRelease-3>", Edit_declic)
    can.pack()
    droite2 = Button(fen, text="Grand droite", command=Droite2).pack(side="right")
    droite1 = Button(fen, text="Droite", command=Droite1).pack(side="right")
    gauche2 = Button(fen, text="Grand gauche", command=Gauche2).pack(side="left")
    gauche1 = Button(fen, text="Gauche", command=Gauche1).pack(side="left")
    test = Button(fen, text="Tester", command=Tester).pack()
    param = Button(fen, text="Paramètres", command=parametres).pack()
    quitter = Button(fen, text="Quitter", command=fen.destroy).pack()
    ligne_avant = can.create_line(4*ech, 0, 4*ech, Haut*ech+1, fill="light grey")
    sol = can.create_line(0, Haut*ech+1, 30*ech+1, Haut*ech+1)
    plafond = can.create_line(0, 2, 30*ech+1, 2)
    ligne_sol = can.create_line(3*ech, Hauteur+2, 4*ech, Hauteur+2, fill='red')
    ligne_plafond = can.create_line(3*ech, Hauteur-8, 4*ech, Hauteur-8, fill='red')
    texturiser.clear()
    if ech == 10:
        e = ""
    elif ech == 16:
        e = "big_"
    liste = []
    top = Toplevel(fen)
    a = 0
    while a < len(Elements.elements):
        try:
            texturiser.append(PhotoImage(file=e+"textures/"+Elements.elements[a][1] + ".gif"))
        except:
            texturiser.append(PhotoImage(file=e+"textures/default.gif"))
        a=a+1
    z = [None]+texturiser
    b = len(texturiser)
    c = 0
    Cl=[]
    while c < b:
        c = len(liste)
        if c == 0:
            liste.append(Label(top, text=indication2[c]))
        else:
            liste.append(Label(top, image=z[c]))
        def cl(x, a=c):
            choisir(a)
        Cl.append(cl)
        del cl
        liste[-1].bind("<Button-1>", Cl[c])
        liste[-1].grid(row=c%10, column=c//10, sticky="w")
    deplacer()
    top.focus()
    fen.focus()
    fen.mainloop()

inv = False
def Inv(a):
    global inv, inv_ou_pas
    inv = not inv
    inv_ou_pas.configure(text="Gravité inversée : "+str(inv))

def Monter_cube():
    global Hauteur, ligne_sol, ligne_plafond, ech
    Hauteur = Hauteur - ech
    can.coords(ligne_sol, 3*ech, Hauteur+2, 4*ech, Hauteur+2)
    can.coords(ligne_plafond, 3*ech, Hauteur-ech+2, 4*ech, Hauteur-ech+2)

def Descendre_cube():
    global Hauteur, ligne_sol, ligne_plafond, ech
    Hauteur = Hauteur + ech
    can.coords(ligne_sol, 3*ech, Hauteur+2, 4*ech, Hauteur+2)
    can.coords(ligne_plafond, 3*ech, Hauteur-ech+2, 4*ech, Hauteur-ech+2)

def Tester(): # -----------------------------------------------< TEST DU NIVEAU
    global position, inv, Hauteur, inv_ou_pas
    tps = position*10+300
    Choisirs = Tk(className = "Options de lancement")
    inv_ou_pas = Label(Choisirs, text="Gravité inversée : "+str(inv))
    inv_ou_pas.bind("<Button-1>", Inv)
    inv_ou_pas.pack()
    m_cube = Button(Choisirs, text="Monter cube", command=Monter_cube).pack(side="right")
    d_cube = Button(Choisirs, text="Descendre cube", command=Descendre_cube).pack(side="left")
    Vali = Button(Choisirs, text="Lancer", command=Choisirs.quit).pack()
    Choisirs.mainloop()
    try:
        Choisirs.destroy()
    except:
        pass
    Test_edit(level, p_prac = [(tps, (Hauteur*10)//ech, 0, inv, False, 1, False, False, False, 0, 0, 0, 0)])
    Fenetre_de_jeu()

def Sauvegarder():
    global level, void_add, niv, version, librairies
    # Retrait des colonnes inutiles (après le dernier bloc)
    while level[-1] == void_add:
        level = level[0:-1]
    
    # enregistrement du niveau
    fichier_secours = open(niv+".cubelvl", "r", encoding="Utf-8")
    level_save = fichier_secours.read()
    fichier_secours.close()
    try: # tenter d'enregistrer le niveau normalement
        fichier2 = open(niv+".cubelvl", "w", encoding="Utf-8")
        fichier2.write(str(level) + ", " + str(version) + ", " + str(librairies))
        fichier2.close()
    except:
        ### RECUPERATION DU NIVEAU ### (en cas de crash imprévu)
        try:    # tenter de réc(upérer le niveau avant modification (qui est une source d'erreur possible)
            try:
                fichier2.close()
            except:
                pass
            recuperation = open(niv+".cubelvl", "w", encoding="Utf-8")
            recuperation.write(level_save)
            recuperation.close()
            print("Une erreur est survenue lors de la sauvegarde.\nLe niveau a été restauré avec succès.")
        except: # si c'est impossible, INFORMER l'utilisateur de la situation, et donner sous format texte le contenu du niveau avec print()
            print("Fatal Error !\nLe niveau que vous avez ouvert est perdu !\nVoici le contenu de votre niveau (un message dira que le niveau est complet) :")
            print(level, end=", ")  # tenter d'afficher le contenu du niveau (Ex : [[0, 0, 1], [0, 2, 0], [0, 1, 0]])
            print(version, end=", ")# tenter d'afficher la version du niveau (à la suite, ce qui permet de pouvoir avoir le niveau en entier)
            print(librairies)       # tenter d'afficher les librairies du niveau
            print("----- Le niveau a été affiché avec succès -----\nRécupérez le niveau, il n'existe qu'ici à présent !")

def Crash_analyser(a):
    bouh = Tk()
    bouh.focusmodel("active")
    inf = Label(bouh, text="Enregistre les valeurs dans un fichier")
    inf.pack()
    mince = Button(bouh, text="Analyser le bug actuel", command=Report)
    mince.pack()
    place = Label(bouh, text="\n")
    place.pack()
    malade = Button(bouh, text="Analyse COMPLETE (difficile à exploiter)", command=Report_X)
    malade.pack()
    bouh.mainloop()

def Report():
    "Enregistre la valeur de toutes les variables\nCommande d'invocation : <Key-a>"
    global level, Elements, texturiser, Texte
    file = open(str(int(time())) + " crash report", "w", encoding="Utf-8")
    file.write("level, Elements, texturiser, Texte = "+str((level, Elements.__dict__, texturiser, Texte)))
    file.close()

def Report_X():
    print("Report complet en cours...")
    file = open(str(int(time())) + " big crash report", "w", encoding="Utf-8")
    file.write("fenêtre, parametres, Edit_clic, frappe" + str(fenêtre.__globals__) + ", " + str(parametres.__globals__) + ", " + str(Edit_clic.__globals__) + ", " + str(frappe.__globals__))
    file.close()
    print("Report terminé.")

while True:
    Haut, level, version, niv, total, librairies, ech, mode_jouer = Choisir()
    if not Valeurs.encore:
        break
    if mode_jouer:
        Fenetre_de_jeu()
    else:
        void_add = eval("[0" + ",0"*(Haut-1) + "]")
        Hauteur = Haut*ech
        portail = []
        a = 0
        while a < len(Elements.Type_prioritaire):
            if Elements.Type_prioritaire[a][0]:
                portail.append(Elements.Type_prioritaire[a][1]+1)
            a=a+1
        while len(AddTxt) < len(Elements.elements):
            nombre_elements.append(Elements.elements[len(AddTxt)][0])
            coul_obstacles.append(Elements.elements[len(AddTxt)][1])
            indication.append(Elements.elements[len(AddTxt)][2])
            AddTxt.append(str(nombre_elements[-1]))
        indication2 = ["vide"] + indication
        Texte[2] = indication
        Texte[3] = AddTxt
        Texte[4] = coul_obstacles
        if Valeurs.encore:
            fenêtre() # Ben, on lance, non ?
            Sauvegarder()
