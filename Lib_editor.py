from tkinter import Tk, Canvas, Toplevel, Button, Label, Entry
"""Ceci est l'éditeur de blocs de 'Le cube'.
IMPORTANT : déclarer avec global toute variable affectée ou récupérée !
Voici le système actuel de stockage des éléments :
[[ID_type, si_prioritaire, action], ...]
Voici le système plus optimisé du stockage des éléments :
[[ID_type, action, si_prioritaire], ...]
Pour le bloc spécial, on aura :
[[ID_type, [si_rien, a_sol, a_pla, a_inv_sol, a_inv_pla, a_saut_contact, traversant],
si_prioritaire, [si_sol, si_pla, si_inv_sol, si_inv_pla, cond_actif]], ...]"""
# fonctionnement                        - à faire
# mise en parallèle avec Le_cube_lib    - Compilation
# être facilement utilisable            - fait
# ajout du bloc spécial                 - fait
# ajout de la gestion des textures      - fait
# encodage special pour blocs.lib       - 
"Note : fenit = fen + edit"

var = ["Vrai", "Faux", "hauteur", "saut", "au_sol", "gravité_inversée", "mode_inversion", "vivant", "vitesse", "mode_propultion", "switch1", "switch2", "touche_action", "avancement", "var1", "var2", "var3", "var4"] # all autorized variables
fonc = ["attribuer valeur", "inverser", "Si ", "Sinon", "Fin condition", "Existe : "] # all functions who added line
# "+", "-", "*", "/", ".", ",", "=", "%" and numbers --> keypad entry
contenu = {'prog':[], 'type':[], 'nom':[], 'priorité':[]}
# "prog" pour code, "type" pour type, "nom" pour nom
ligne = 0
page = 0
mode = 0 # 0 inactif, 1 variable pour attribution, 2 variable pour inversion, 3 valeur/opérateur
changement = False
nom = ""

def clic_ligne(pos):
    global ligne, mode
    if mode in [3, 4]:
        mode = 0
    if mode == 0:
        ligne = (pos.y+7)//15

def supprime_ligne(pos):
    global contenu, mode, page
    if mode == 0:
        del contenu['prog'][page][pos.y//15]
        if page == len(contenu['nom']):
            page += -1
        raffraichir()

def raffraichir():
    global contenu, prog, page, Nom, Type, prioritaire
    a=1
    try:
        texte=contenu['prog'][page][0]
        while a < len(contenu['prog'][page]):
            texte+= "\n" + contenu['prog'][page][a]
            a=a+1
    except:
        texte = "Aucun code n'a été saisi pour ce bloc"
    prog.config(text=texte)
    Type.config(text=contenu['type'][page])
    Nom.config(text=contenu['nom'][page])
    if contenu['type'][page][2] != 'e':
        prioritaire.config(text="Prioritaire : "+{True:'oui', False:'non'}[contenu['priorité'][page]])
    elif contenu['type'][page][10] == 'c':
        prioritaire.config(text="Réagit pour ce contact : "+{True:'oui', False:'non'}[contenu['priorité'][page]])
    else:
        prioritaire.config(text="")

def frappe(lettre):
    global contenu, ligne, mode, page
    touche = lettre.keysym
    if mode == 3:
        if len(touche) == 1 and touche in ["1", "2", "3", "4", "5","6","7","8","9","0"]:
            contenu['prog'][page][ligne] += touche
        elif touche in ["plus", "equal", "minus", "asterisk", "slash", "percent", "period", "comma", "less", "greater"]:
            contenu['prog'][page][ligne] += {"plus":" + ", "equal":" = ", "minus":" - ", "asterisk":" * ", "slash":" / ", "period":".", "comma":".", "percent":" % ", "less":" < ", "greater":" > "}[touche]
        elif touche == "BackSpace":
            contenu['prog'][page][ligne] = contenu['prog'][page][ligne][0:-1]
        elif touche == "Return":
            mode = 0
            ligne+= 1
        raffraichir()
    elif mode == 4:
        if len(touche) == 1:
            contenu['nom'][page] += touche
        elif touche == "BackSpace":
            contenu['nom'][page] = contenu['nom'][page][0:-1]
        elif touche == "space":
            contenu['nom'][page] += " "
        elif touche == "Return":
            mode = 0
        raffraichir()
    elif mode == 0:
        if touche == "Left":
            Page_précédente()
        elif touche == "Right":
            Page_suivante()

def renommer(a):
    global mode
    if mode in [0, 3]:
        mode = 4

def really():
    global contenu, page, fen
    del contenu['nom'][page], contenu['type'][page], contenu['prog'][page], contenu['priorité'][page]
    raffraichir()
    fen.destroy()

def supprime_page(a):
    global fenit, fen
    fen = Toplevel(fenit)
    l = Label(fen, text="Voulez-vous vraiment supprimer ce bloc ?")
    b1 = Button(fen, text="Oui", command=really)
    b2 = Button(fen, text="Non", command=fen.destroy)
    l.pack()
    b1.pack(side="left")
    b2.pack(anchor="e")
    fen.focus()

def toggle(a):
    global contenu, page
    contenu['priorité'][page] = not contenu['priorité'][page]
    raffraichir()

def Fenit():
    global fenit, fonc, var, Ca, prog, Fonc, Var, Nom, Type, prioritaire
    fenit = Tk(className="Lib editor") # Scripts
    fenit.bind("<Key>", frappe)
    Nom = Label(fenit, text="Veuillez charger une librairie non-compilée")
    Nom.bind("<Button-1>", renommer)
    Nom.bind("<Button-3>", supprime_page)
    Nom.pack()
    Type = Label(fenit)
    Type.pack()
    prioritaire = Label(fenit)
    prioritaire.bind("<Button-1>", toggle)
    prioritaire.pack()
    prog = Label(fenit)
    prog.bind("<Button-1>", clic_ligne)
    prog.bind("<Button-3>", supprime_ligne)
    prog.pack(anchor="w")
    Add_page = Button(fenit, text="Ajouter un bloc", command=add_bloc)
    Add_page.pack(anchor="s")
    ouvre = Button(fenit, text="Charger", command=Ouvre)
    ouvre.pack(anchor="s")
    comp = Button(fenit, text="Compiler", command=Compiler)
    comp.pack(anchor="s")
    quitter = Button(fenit, text="Enregistrer et quitter", command=Sauve)
    quitter.pack(anchor="s")
    # fonctions
    texte = fonc[0]
    a = 1
    while a < len(fonc):
        texte += "\n" + fonc[a]
        a=a+1
    outils = Toplevel(fenit)
    outils.bind("<Key>", frappe)
    Fonc = Label(outils, text=texte)
    Fonc.bind("<Button-1>", add_fonc)
    Fonc.pack(anchor="nw", side="right")
    # variables
    texte = var[0]
    a = 1
    while a < len(var):
        texte += "\n" + var[a]
        a=a+1
    Var = Label(outils, text=texte)
    Var.bind("<Button-1>", add_var)
    Var.pack(anchor="nw")
    outils.focus()
    fenit.focus()
    fenit.mainloop()
    try:
        fenit.destroy()
    except:
        pass

def add_fonc(pos):
    global fonc, ligne, mode, contenu, page
    y = pos.y//15
    if mode == 0:
        if y > 1 and y < 5:
            if ligne >= len(contenu['prog'][page]):
                ligne = len(contenu['prog'][page])
                contenu['prog'][page].append(fonc[y])
            else:
                contenu['prog'][page].insert(ligne, fonc[y])
            if y == 2:
                mode = 3
            else:
                ligne += 1
        elif y < 2:
            mode=y+1
            if ligne >= len(contenu['prog'][page]):
                ligne = len(contenu['prog'][page])
                contenu['prog'][page].append("")
            else:
                contenu['prog'][page].insert(ligne, "")
        elif contenu['type'][page] == "Special - Condition pour exister":
            if ligne >= len(contenu['prog'][page]):
                ligne = len(contenu['prog'][page])
                contenu['prog'][page].append(fonc[y])
            else:
                contenu['prog'][page].insert(ligne, fonc[y])
            mode = 5 # Seul un booléen peut être recu
        raffraichir()

def add_var(pos):
    global var, ligne, mode, contenu, page
    y = (pos.y-4)//15
    if y < 0:
        y = 0
    if mode > 0:
        if mode == 3:
            contenu['prog'][page][ligne] += var[y]
        elif mode == 1:
            contenu['prog'][page][ligne] = var[y] + " prend pour valeur "
            mode = 3
        elif mode == 2:
            contenu['prog'][page][ligne] = "inverser " + var[y]
            mode = 0
            ligne += 1
        elif mode == 5:
            if y in [0, 1, 4, 5, 10, 11, 12]:
                contenu['prog'][page][ligne] += var[y]
                mode = 0
                ligne += 1
        raffraichir()

def add_bloc():
    global contenu, choix
    choix = Tk()
    Button(choix, text="Retour", command=choix.quit).pack(side="bottom")
    Button(choix, text="Sol", command=b1).pack(anchor="c", side="left")
    Button(choix, text="Plafond", command=b2).pack(side="left")
    Button(choix, text="Portail", command=b3).pack(side="left")
    Button(choix, text="Sphère", command=b4).pack(side="left")
    Button(choix, text="Bloc special", command=b5).pack(side="left")
    choix.focus()
    choix.mainloop()
    try:
        choix.destroy()
    except:
        pass

def b1():
    Add_bloc("sol")
def b2():
    Add_bloc("plafond")
def b3():
    Add_bloc("portail")
def b4():
    Add_bloc("sphère")
def b5():
    Add_bloc("special")

def Add_bloc(Type):
    global contenu, choix
    if Type == "special":
        contenu['prog'] += [[], [], [], [], [], []]
        contenu['type'] += ["Special - contact sol pour gravité normale",
                            "Special - contact plafond pour gravité normale",
                            "Special - contact sol pour gravité inversée",
                            "Special - contact plafond pour gravité inversée",
                            "Special - autre contact et contact désactivé",
                            "Special - Condition pour exister"]
        contenu['nom'] += ["wow", "", "", "", "", ""]
        contenu['priorité'] += [False, False, False, False, False, False]
    else:
        contenu['prog'].append([])
        contenu['type'].append(Type)
        contenu['nom'].append("CR")
        contenu['priorité'].append(False)
    raffraichir()
    choix.quit()

def Ouvre():
    "Charge une librairie non-compilée"
    global contenu, nom, page, mode, changement
    if mode == 0:
        Nommer()
        if changement:
            try:
                file = open(nom+".build", "r", encoding="Utf-8")
                contenu = eval(file.read())
                file.close()
            except:
                print("Une erreur est survenue lors du chargement de la librairie.")
            changement = False
    raffraichir()

def Sauve():
    "Enregistre les modifications apportées et quitte"
    global contenu, nom, changement, mode, fenit
    if mode == 0:
        if nom == "":
            Nommer()
            changement = False
        if nom != "":
            try:
                file = open(nom+".build", "w", encoding='Utf-8')
                file.write(str(contenu))
                file.close()
            except:
                print("Une erreur est survenue lors de l'enregistrement de la librairie.")
    fenit.quit()

def Compiler():
    "Compile la librairie sous le format des librairies de 'Le cube'"
    # Utiliser .replace
    global contenu, nom, mode, var
    Indexage = 0
    programme = []
    chercher = var[2:-1] + [var[-1]]
    recherche = ("au_sol", "gravité_inversée", "mode_inversion", "vivant", "vitesse", "mode_propultion", "switch1", "switch2", "touche_action", "avancement")
    remplacer = {"au_sol":"air", "gravité_inversée":"inverse", "mode_inversion":"scie", "vivant":"vie", "vitesse":"speed", "mode_propultion":"fuse", "switch1":"toggle1", "switch2":"toggle2", "touche_action":"sautons", "avancement":"tps"}
    if mode == 0:
        # Compilation des programmes générés
        a = 0
        while a < len(contenu['prog']):
            programme.append("")
            b=0
            while b < len(contenu['prog'][a]):
                if contenu['prog'][a][b] == "Sinon":
                    programme[a] += "\n    "+"    "*(Indexage-1) + "else:"
                elif contenu['prog'][a][b][0:2] == "Si":
                    programme[a] += "\n    "+"    "*Indexage + contenu['prog'][a][b]+":"
                    Indexage += 1
                    print("Indexage +1")
                elif contenu['prog'][a][b] == "Fin condition":
                    Indexage += -1
                    print("Indexage -1")
                elif contenu['prog'][a][b][0:5] == "inver":
                    c = contenu['prog'][a][b][9:-1] + contenu['prog'][a][b][-1]
                    programme[a] += "\n    "+"    "*Indexage + c + " prend pour valeur not " + c
                else:
                    programme[a] += "\n    "+"    "*Indexage + contenu['prog'][a][b]
                b=b+1
            if Indexage != 0:
                print("Nombre de 'Fin condition' incorrect pour la page", a)
                print("Script généré :")
                print(programme[a])
                break
            if programme[-1] == "":
                programme[-1] = "pass"
            else:
                programme[-1] = programme[-1].replace("=", "==").replace("prend pour valeur", "=").replace("Si", "if").replace("Existe :", "return").replace("Vrai", "True").replace("Faux", "False")
                variables = []
                c = 0
                while c < len(chercher):
                    if programme[-1].count(chercher[c]) > 0:
                        if chercher[c] in recherche:
                            programme[-1] = programme[-1].replace(chercher[c], remplacer[chercher[c]])
                            variables.append(remplacer[chercher[c]])
                        else:
                            variables.append(chercher[c])
                    c=c+1
                if len(variables) > 0:
                    if "tps" in variables:
                        programme[-1] = "    deformation = 6\n" + programme[-1]
                        variables.append("deformation")
                    programme[-1] = "global " + str(variables)[1:-1].replace("'", "") + programme[-1]
                else:
                    programme[-1] = programme[-1][5:-1] + programme[-1][-1]
            a+=1
            print("Page ",a, "/", len(contenu['prog']), " compilée", sep="")
        # Compilation de la librairie
        librairie = []
        try:
            file = open(nom+".lib", "r", encoding="Utf-8")
            toux = eval(file.read())
            file.close()
            recup = True
        except:
            print("Aucun paramère pré-existant")
            recup = False
        a = 0
        b = 0
        while a < len(programme):
            if contenu['type'][a][2] == "e":
                prog_part = programme[a:(a+6)]
                bool_part = contenu["priorité"][a:(a+4)]
                if recup:
                    try:
                        librairie.append([4, bool_part, prog_part, toux[b][3], toux[b][4], contenu['nom'][a]])
                    except:
                        print("Aucun paramètre pré-existant pour ce bloc")
                        librairie.append([4, bool_part, prog_part, 10, contenu['nom'][a], contenu['nom'][a]])
                else:
                    librairie.append([4, bool_part, prog_part, 10, contenu['nom'][a], contenu['nom'][a]])
                a=a+5
            else:
                if recup:
                    try:
                        librairie.append([['portail', 'sphère', 'sol', 'plafond'].index(contenu['type'][a]), contenu['priorité'][a], programme[a], toux[b][3], toux[b][4], contenu['nom'][a]])
                    except:
                        print("Aucun paramètre pré-existant pour ce bloc")
                        librairie.append([['portail', 'sphère', 'sol', 'plafond'].index(contenu['type'][a]), contenu['priorité'][a], programme[a], 10, contenu['nom'][a], contenu['nom'][a]])
                else:
                    librairie.append([['portail', 'sphère', 'sol', 'plafond'].index(contenu['type'][a]), contenu['priorité'][a], programme[a], 10, contenu['nom'][a], contenu['nom'][a]])
            a=a+1
            b=b+1
        print("La librairie a été compilée avec succès.")
        try:
            file = open(nom+".lib", "w", encoding='Utf-8')
            file.write(str(librairie))
            file.close()
        except:
            print("Cependant, elle n'a pas pu être enregistrée.")
        print("La librairie a été enregistrée avec succès.")

def Page_suivante():
    global page, contenu, mode, ligne
    if mode in [3, 4]:
        mode = 0
    if mode == 0:
        page += 1
        if page == len(contenu['nom']):
            page = 0
        raffraichir()
        ligne = 0

def Page_précédente():
    global page, contenu, mode, ligne
    if mode in [3, 4]:
        mode = 0
    if mode == 0:
        page+= -1
        if page == -1:
            page = len(contenu['nom']) - 1
        raffraichir()
        ligne = 0

def Nommer():
    global fenit, tp, ent
    tp = Toplevel(fenit)
    l = Label(tp, text="Entrez le nom de la libraire (annule si rien n'est saisi)")
    l.pack()
    ent = Entry(tp)
    ent.pack()
    valid = Button(tp, text="Ok", command=valider)
    valid.pack()
    tp.focus()
    tp.mainloop()
    try:
        tp.destroy()
    except:
        pass

def valider():
    global tp, ent, nom, changement
    if ent.get() != '':
        nom = ent.get()
        changement = True
    tp.quit()

"""On utilisera la position du clic pour savoir sur quelle ligne j'ai cliqué.
anchor=W pour le programme, pour tout aligner à gauche.
"""
