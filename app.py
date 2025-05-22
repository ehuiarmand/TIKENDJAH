
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CaveManager Web", layout="wide")

menu = ["Accueil", "Ventes", "Stocks", "Dépenses", "Salaires"]
choix = st.sidebar.selectbox("Menu", menu)

def load_data(nom_fichier, colonnes):
    try:
        return pd.read_csv(nom_fichier)
    except FileNotFoundError:
        df = pd.DataFrame(columns=colonnes)
        df.to_csv(nom_fichier, index=False)
        return df

if choix == "Accueil":
    st.title("📊 Tableau de bord - CaveManager Web")
    ventes = load_data("ventes.csv", ["Produit", "Quantité", "Prix total", "Mode de paiement"])
    stocks = load_data("stocks.csv", ["Produit", "Quantité", "Prix achat", "Prix vente"])
    depenses = load_data("depenses.csv", ["Date", "Libellé", "Catégorie", "Montant"])
    salaires = load_data("salaires.csv", ["Employé", "Mois", "Montant"])

    st.metric("Total Ventes", f"{ventes['Prix total'].sum():,.0f} FCFA")
    st.metric("Dépenses", f"{depenses['Montant'].sum():,.0f} FCFA")
    st.metric("Salaires Payés", f"{salaires['Montant'].sum():,.0f} FCFA")

elif choix == "Ventes":
    st.title("🛒 Enregistrement des ventes")
    produits = load_data("stocks.csv", ["Produit", "Quantité", "Prix achat", "Prix vente"])
    ventes = load_data("ventes.csv", ["Produit", "Quantité", "Prix total", "Mode de paiement"])

    produit = st.selectbox("Produit", produits["Produit"].unique())
    quantite = st.number_input("Quantité", min_value=1, step=1)
    mode = st.selectbox("Mode de paiement", ["Espèce", "Mobile Money", "Crédit"])

    if st.button("Enregistrer la vente"):
        prix_vente = produits[produits["Produit"] == produit]["Prix vente"].values[0]
        total = prix_vente * quantite
        ventes = ventes.append({"Produit": produit, "Quantité": quantite, "Prix total": total, "Mode de paiement": mode}, ignore_index=True)
        ventes.to_csv("ventes.csv", index=False)
        st.success("Vente enregistrée !")

elif choix == "Stocks":
    st.title("📦 Gestion du stock")
    stocks = load_data("stocks.csv", ["Produit", "Quantité", "Prix achat", "Prix vente"])

    with st.form("form_stock"):
        produit = st.text_input("Nom du produit")
        quantite = st.number_input("Quantité", min_value=0, step=1)
        prix_achat = st.number_input("Prix d'achat", min_value=0.0)
        prix_vente = st.number_input("Prix de vente", min_value=0.0)
        submit = st.form_submit_button("Ajouter / Modifier")

        if submit:
            stocks = stocks[stocks["Produit"] != produit]
            stocks = stocks.append({"Produit": produit, "Quantité": quantite, "Prix achat": prix_achat, "Prix vente": prix_vente}, ignore_index=True)
            stocks.to_csv("stocks.csv", index=False)
            st.success("Stock mis à jour !")

    st.dataframe(stocks)

elif choix == "Dépenses":
    st.title("💸 Dépenses")
    depenses = load_data("depenses.csv", ["Date", "Libellé", "Catégorie", "Montant"])

    with st.form("form_depense"):
        date = st.date_input("Date")
        libelle = st.text_input("Libellé")
        categorie = st.selectbox("Catégorie", ["Approvisionnement", "Facture", "Autre"])
        montant = st.number_input("Montant", min_value=0.0)
        submit = st.form_submit_button("Ajouter")

        if submit:
            depenses = depenses.append({"Date": date, "Libellé": libelle, "Catégorie": categorie, "Montant": montant}, ignore_index=True)
            depenses.to_csv("depenses.csv", index=False)
            st.success("Dépense enregistrée.")

    st.dataframe(depenses)

elif choix == "Salaires":
    st.title("👤 Paiement des salaires")
    salaires = load_data("salaires.csv", ["Employé", "Mois", "Montant"])

    with st.form("form_salaire"):
        employe = st.text_input("Nom de l'employé")
        mois = st.selectbox("Mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
        montant = st.number_input("Montant", min_value=0.0)
        submit = st.form_submit_button("Payer")

        if submit:
            salaires = salaires.append({"Employé": employe, "Mois": mois, "Montant": montant}, ignore_index=True)
            salaires.to_csv("salaires.csv", index=False)
            st.success("Salaire payé !")

    st.dataframe(salaires)
