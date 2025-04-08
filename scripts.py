# VERSION FICHIERS LOCAUX
# import sqlite3
# import csv
# import os

# print("✅ Script démarré")

# # Connexion à la base de données avec gestion d'erreur
# db_path = 'data/brief.db'
# try:
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     print("✅ Connexion réussie à la base de données.")
# except sqlite3.Error as e:
#     print(f"❌ Erreur lors de la connexion à la base de données: {e}")
#     exit()  # Terminer le programme si la connexion échoue

# # Fonction générique d'insertion avec vérification des doublons
# def insert_csv_data(file_path, table, columns, csv_columns):
#     row_added = 0
#     row_ignored = 0
    
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         print(f"Colonnes dans {file_path}: {reader.fieldnames}")
#         for row in reader:
#             values = tuple(row[csv_col] for csv_col in csv_columns)
#             placeholders = ','.join(['?'] * len(csv_columns))
#             columns_with_quotes = [f'"{col}"' for col in columns]
            
#             # Pas besoin de vérifier les doublons manuellement, INSERT OR IGNORE le fait
#             query = f'INSERT OR IGNORE INTO {table} ({",".join(columns_with_quotes)}) VALUES ({placeholders})'
#             cursor.execute(query, values)
            
#             if cursor.rowcount > 0:  # Si une ligne a été insérée
#                 row_added += 1
#             else:  # Si une ligne a été ignorée
#                 row_ignored += 1
    
#     print(f"✅ Données insérées dans {table} depuis {file_path}")
#     print(f"📊 Lignes ajoutées : {row_added}")
#     print(f"📊 Lignes ignorées (doublons) : {row_ignored}")

# # Insertion des données
# insert_csv_data('data/csv/data_magasins.csv', 'Magasins', ['id', 'ville', 'nb_salariés'], ['ID Magasin', 'Ville', 'Nombre de salariés'])
# insert_csv_data('data/csv/data_produits.csv', 'Produits', ['id', 'nom', 'prix', 'stock'], ['ID Référence produit', 'Nom', 'Prix', 'Stock'])
# insert_csv_data('data/csv/data_ventes.csv', 'Ventes', ['date', 'id_ref_prod', 'quantité', 'id_magasin'], ['Date','ID Référence produit', 'Quantité', 'ID Magasin'])



# VERSION HTTP
import sqlite3
import csv
import requests
import io
import os

print("✅ Script démarré")

# Créer le dossier s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

# Connexion à la base de données
db_path = 'data/brief.db'
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("✅ Connexion réussie à la base de données.")
except sqlite3.Error as e:
    print(f"❌ Erreur BDD: {e}")
    exit()

# Fonction de lecture robuste avec encodage et correction de colonnes
def read_csv_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8-sig')
    except UnicodeDecodeError:
        content = response.content.decode('latin1')
    
    csvfile = io.StringIO(content)
    reader = csv.DictReader(csvfile)
    
    # Corriger colonnes mal encodées
    reader.fieldnames = [col.encode('latin1').decode('utf-8') if 'Ã' in col else col for col in reader.fieldnames]
    
    return list(reader), reader.fieldnames

# Fonction d'insertion générique
def insert_csv_from_url(csv_url, table, db_columns, csv_columns):
    row_added = 0
    row_ignored = 0

    try:
        rows, fieldnames = read_csv_from_url(csv_url)
        print(f"📥 Lecture depuis : {csv_url}")
        print(f"🧾 Colonnes détectées : {fieldnames}")

        for col in csv_columns:
            if col not in fieldnames:
                raise ValueError(f"❌ Colonne manquante : {col}")

        for row in rows:
            values = tuple(row[c] for c in csv_columns)
            placeholders = ','.join(['?'] * len(csv_columns))
            columns_str = ','.join(f'"{col}"' for col in db_columns)
            query = f'INSERT OR IGNORE INTO {table} ({columns_str}) VALUES ({placeholders})'
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                row_added += 1
            else:
                row_ignored += 1

        print(f"✅ Insertion dans {table}")
        print(f"📊 Lignes ajoutées : {row_added}")
        print(f"📊 Ignorées (doublons) : {row_ignored}")

    except Exception as e:
        print(f"❌ Erreur traitement {table} : {e}")

# URLs CSV
url_magasins = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
url_produits = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
url_ventes   = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"

# Insertion
insert_csv_from_url(url_magasins, 'Magasins', ['id', 'ville', 'nb_salariés'], ['ID Magasin', 'Ville', 'Nombre de salariés'])
insert_csv_from_url(url_produits, 'Produits', ['id', 'nom', 'prix', 'stock'], ['ID Référence produit', 'Nom', 'Prix', 'Stock'])
insert_csv_from_url(url_ventes, 'Ventes', ['date', 'id_ref_prod', 'quantité', 'id_magasin'], ['Date','ID Référence produit', 'Quantité', 'ID Magasin'])

# Calcul du CA
def calculate_revenue():
    print("\n📊 Calcul du chiffre d'affaires en cours...")

    # Produit
    cursor.execute('''
        SELECT v.id_ref_prod, SUM(v.quantité * p.prix) 
        FROM Ventes v
        JOIN Produits p ON v.id_ref_prod = p.id
        GROUP BY v.id_ref_prod
    ''')
    product_revenue = cursor.fetchall()
    print("-" * 40)
    print("✅ CA par produit :")
    for id_ref, ca in product_revenue:
        print(f"{id_ref:<20} {ca:,.2f} €")
        try:
            cursor.execute("INSERT INTO Résultats_Produits (id_produit, ventes) VALUES (?, ?)", (id_ref, ca))
        except Exception as e:
            print(f"❌ Insertion CA produit {id_ref} : {e}")
    print("-" * 40)
    # Magasin
    cursor.execute('''
        SELECT v.id_magasin, SUM(v.quantité * p.prix) 
        FROM Ventes v
        JOIN Produits p ON v.id_ref_prod = p.id
        GROUP BY v.id_magasin
    ''')
    store_revenue = cursor.fetchall()
    print("-" * 40)
    print("✅ CA par magasin :")
    for id_mag, ca in store_revenue:
        print(f"{id_mag:<12} {ca:,.2f} €")
        try:
            cursor.execute("INSERT INTO Résultats_Magasins (id_magasin, ventes) VALUES (?, ?)", (id_mag, ca))
        except Exception as e:
            print(f"❌ Insertion CA magasin {id_mag} : {e}")
    print("-" * 40)
    # Global
    cursor.execute('''
        SELECT SUM(v.quantité * p.prix) 
        FROM Ventes v
        JOIN Produits p ON v.id_ref_prod = p.id
    ''')
    total_ca = cursor.fetchone()[0]
    if total_ca is not None:
        try:
            cursor.execute("INSERT INTO Résultats_CA (total) VALUES (?)", (total_ca,))
            print(f"✅ Insertion CA global : {total_ca:,.2f} €")
        except Exception as e:
            print(f"❌ Insertion CA global : {e}")
    else:
        print("❌ Aucun CA global trouvé. Table vide ?")

    conn.commit()
    print("✅ Tous les résultats ont été enregistrés.")

calculate_revenue()
conn.close()
print("✅ Script terminé.")