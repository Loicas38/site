from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from backend import Utilisateur, Lieu
from bdd import recup_lieux_par_nom


app = Flask(__name__)
app.secret_key = "75066eb0307741709f7ec435386af599ddefe6ea57a715f2bf26f2af830a2387"

def recherche_utilisateur(username, password) -> Utilisateur:
    """ cherche si un utilisateur avec ce mdp existe,
    retourne l'objet utilisateur si mot de passe et nom d'utilisateur corrects, sinon None"""
    con = sqlite3.connect('data_2.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM UTILISATEURS WHERE nom_utilisateur=? AND mot_de_passe=?", (username, password))
    utilisateur = cur.fetchall()
    cur.close()

    if len(utilisateur) == 0:
        return False
    else:
        return Utilisateur(utilisateur[0][0], utilisateur[0][1], utilisateur[0][3], utilisateur[0][4])



def obtenir_lieux():
    """lieux = liste des lieux à rechercher dans la base de donnée et à afficher
    retourne une liste d'objets contenant les lieux trouvés, une liste vide si aucun lieu n'est trouvé """
    con = sqlite3.connect('data_2.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM LIEUX")
    lieux = cur.fetchall()
    cur.close()
    con.close()

    liste_lieux = []
    for lieu in lieux:
        liste_lieux.append(Lieu(lieu[1], lieu[2], lieu[3], lieu[4], lieu[5], lieu[6], lieu[7], lieu[8]))

    return liste_lieux



def ajout_lieu_bdd_backend(nom, telephone, mail, horaires, createur, type_lieu, adresse, note=None):
    con = sqlite3.connect('data_2.db')
    cur = con.cursor()
    cur.execute("INSERT INTO LIEUX(nom, adresse, telephone, mail, horaires, createur, type, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nom, adresse, telephone, mail, horaires, createur, type_lieu, note))
    con.commit()
    cur.close()
    con.close()



def creation_utilisateur(username, password, mail, telephone) -> str:
    """ crée un compte et retoune une chaine de charactères pour dire si ca a fonctionné ou non, et pourquoi """
    con = sqlite3.connect('data_2.db')
    cur = con.cursor()
    cur.execute("SELECT nom_utilisateur FROM UTILISATEURS")

    all_users = cur.fetchall()

    all_usernames = []
    for user in all_users:
        all_usernames.append(user[0])


    if username not in all_usernames:
        try:
            cur.execute("INSERT INTO UTILISATEURS (nom_utilisateur, mail, mot_de_passe, telephone, est_admin) VALUES (?, ?, ?, ?, 'False')", (username, mail, password, telephone))
            con.commit()

            cur.close()
            con.close()

            return "Compte créé avec succès !"

        except:
            cur.close()
            con.close()
            return "une erreur est survenue"

    else:
        cur.close()
        con.close()
        return "ce nom d'utilisateur existe déjà !"

    cur.close()
    con.close()


@app.route("/")
def index():
    lieux = obtenir_lieux()
    return render_template("index.html", lieux=lieux)



@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        username = request.form.get("nom")
        password = request.form.get("mdp")

        utilisateur = recherche_utilisateur(username, password)

        if not utilisateur:
            return redirect(request.url)

        else:
            session["nom_utilisateur"] = utilisateur.USERNAME
            return redirect(url_for("index"))

    else:
        if "nom_utilisateur" in session:
            return redirect(url_for('index'))
        return render_template("connexion.html")








@app.route("/creation", methods=["GET", "POST"])
def creation():
    if request.method == "POST":
        username = request.form.get("nom")
        password = request.form.get("mdp")
        mail = request.form.get("mail")
        telephone = request.form.get("telephone")

        creation_compte = creation_utilisateur(username, password, mail, telephone)


        if creation_compte == "Compte créé avec succès !":
            utilisateur = recherche_utilisateur(username, password)

            session["nom_utilisateur"] = utilisateur.USERNAME
            return redirect(url_for("index"))

        else:
            return render_template("creer_compte.html", erreur=creation_compte)

    return render_template("creer_compte.html", erreur=None)




@app.route("/deconnexion")
def deconnexion():
    session.pop('nom_utilisateur', None)
    return redirect(url_for('index'))



@app.route("/affichage_lieux", methods=['GET', 'POST'])
def affichage_lieux():
    # récupère les lieux passés s'il y en a, None, si pas de lieux, et donc pas de recherche
    if request.method == "POST":
        #si le formulaire est envoyé
        donnees = request.form
        nom_lieux = donnees.get("lieux")
        liste_lieux = recup_lieux_par_nom(nom_lieux)
    else :
        #méthode GET
        liste_lieux = None
    return render_template("affichage_lieux.html")



@app.route("/ajout_lieu")
def ajout_lieu():
    # recherche = request.form.get("lieux")
    # lieux = recherche_lieux(recherche)
    # return render_template("ajout_lieu.html", lieu = recherche)
    if session.get("nom_utilisateur") == None:
        return redirect(url_for("connexion"))

    return render_template("ajout_lieu.html")


@app.route("/ajout_lieu_bdd", methods=["GET", "POST"])
def ajout_lieu_bdd():
    if request.method == "POST":
        nom = request.form.get("nom_lieu")
        type_lieu = request.form.get("type_lieu")

        horraire_matin = request.form.get("horraire_mat")
        horraire_apres_midi = request.form.get("horraire_aprem")

        horraires = horraire_matin + " " + horraire_apres_midi

        mail = request.form.get("mail")
        telephone = request.form.get("tel_lieu")
        utilisateur = session.get("nom_utilisateur")
        adresse = request.form.get("adresse")

        ajout_lieu_bdd_backend(nom, telephone, mail, horraires, utilisateur, type_lieu, adresse)

        return redirect(url_for("index"))





if __name__ == "__main__":
    app.run(debug=False)


