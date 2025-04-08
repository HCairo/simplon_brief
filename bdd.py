import sqlite3
import os

os.makedirs('data', exist_ok=True)

cnx = sqlite3.connect('data/brief.db')
cursor = cnx.cursor()

# Liste des requêtes SQL pour créer les tables
queries = [
    '''
    CREATE TABLE IF NOT EXISTS Magasins (
        id INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        nb_salariés INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Produits (
        id TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prix DECIMAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Ventes (
        date TEXT NOT NULL,
        id_ref_prod TEXT NOT NULL,
        quantité INTEGER NOT NULL,
        id_magasin INTEGER NOT NULL,
        UNIQUE (date, id_ref_prod, id_magasin),
        FOREIGN KEY(id_ref_prod) REFERENCES Produits(id),
        FOREIGN KEY(id_magasin) REFERENCES Magasins(id)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Résultats_CA (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total DECIMAL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Résultats_Magasins (
        id INTEGER PRIMARY KEY,
        id_magasin INTEGER NOT NULL,
        ventes DECIMAL,
        FOREIGN KEY(id_magasin) REFERENCES Magasins(id)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Résultats_Produits (
        id INTEGER PRIMARY KEY,
        id_produit TEXT,
        ventes DECIMAL,
        FOREIGN KEY(id_produit) REFERENCES Produits(id)
    )
    '''
]

# Exécution des requêtes pour créer les tables
for query in queries:
    cursor.execute(query)

# Création des indices pour les clés étrangères dans la table Ventes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_id_ref_prod ON Ventes(id_ref_prod);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_id_magasin ON Ventes(id_magasin);')

# Commit pour sauvegarder les changements
cnx.commit()

# Vérification de la validité des données dans la table Ventes
cursor.execute('''
    SELECT v.date, v.id_ref_prod, p.nom AS produit, v.id_magasin, m.ville AS magasin
    FROM Ventes v
    JOIN Produits p ON v.id_ref_prod = p.id
    JOIN Magasins m ON v.id_magasin = m.id
''')
valid_ventes = cursor.fetchall()

if valid_ventes:
    print("✅ Données valides dans la table Ventes :")
    for vente in valid_ventes:
        print(vente)
else:
    print("❌ Aucune donnée valide dans la table Ventes.")

# Sauvegarde du schéma dans un fichier schema.sql
with open('data/db.sql', 'w') as f:
    for query in queries:
        f.write(query.strip() + ';\n\n')

print("✅ Base de données créée avec succès.")
print("📄 Fichier db.sql généré dans le dossier data/")

# Fermeture de la connexion à la base de données
cnx.close()