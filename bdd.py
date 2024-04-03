import sqlite3

def recup_lieux_par_nom(nom):
    conn = sqlite3.connect('data_2.db')
    cur = conn.cursor()
    res = cur.execute("SELECT nom FROM LIEUX WHERE nom LIKE %\"?\"%", (nom, ))
    lieux = res.fetchall() #on stocke les résultats pour les renvoyer
    cur.close()
    conn.close()
    return lieux #après avoir fermé !!