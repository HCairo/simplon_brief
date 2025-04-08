CREATE TABLE IF NOT EXISTS Magasins (
        id INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        nb_salariés INTEGER NOT NULL
    );

CREATE TABLE IF NOT EXISTS Produits (
        id TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prix DECIMAL NOT NULL,
        stock INTEGER NOT NULL
    );

CREATE TABLE IF NOT EXISTS Ventes (
        date TEXT NOT NULL,
        id_ref_prod TEXT NOT NULL,
        quantité INTEGER NOT NULL,
        id_magasin INTEGER NOT NULL,
        UNIQUE (date, id_ref_prod, id_magasin),
        FOREIGN KEY(id_ref_prod) REFERENCES Produits(id),
        FOREIGN KEY(id_magasin) REFERENCES Magasins(id)
    );

CREATE TABLE IF NOT EXISTS Résultats_CA (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total DECIMAL
    );

CREATE TABLE IF NOT EXISTS Résultats_Magasins (
        id INTEGER PRIMARY KEY,
        id_magasin INTEGER NOT NULL,
        ventes DECIMAL,
        FOREIGN KEY(id_magasin) REFERENCES Magasins(id)
    );

CREATE TABLE IF NOT EXISTS Résultats_Produits (
        id INTEGER PRIMARY KEY,
        id_produit TEXT,
        ventes DECIMAL,
        FOREIGN KEY(id_produit) REFERENCES Produits(id)
    );

