import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Script Extraction Date", layout="centered")

# Titre de l'application
st.title("📅 Script : Extraction d'une partie de date")
st.subheader("Format attendu : JJ/MM/AAAA")

# Entrée utilisateur : nom de l'index
index_name = st.text_input("Quel est l'index de référence ?", value="DATE_1_INDEX")

# Choix de la partie à extraire
part_to_extract = st.selectbox("Que souhaitez-vous extraire ?", ["jour", "mois", "année"])

# Fonction pour générer le script JavaScript
def generate_date_script(index, part):
    variable_name = index.lower().replace(" ", "").replace("-", "_")
    if part == "jour":
        part_index = 0
        label = "jour"
    elif part == "mois":
        part_index = 1
        label = "mois"
    else:
        part_index = 2
        label = "année"

    return f"""// Récupération de la valeur de {index}
var {variable_name} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, \"{index}\"));

// Vérification que la valeur de {variable_name} n'est pas vide
if ({variable_name} && {variable_name}.trim() !== "") {{
    var dateParts = {variable_name}.split("/"); // Découpe la date au format JJ/MM/AAAA

    if (dateParts.length === 3) {{
        var {label} = dateParts[{part_index}]; // Extraction du {label}
        return {label}; // Retourne le {label}
    }}
}} 

// Si la date est invalide ou vide
return "Date invalide";"""

# Affichage du script généré
if index_name and part_to_extract:
    script_js = generate_date_script(index_name, part_to_extract)
    st.markdown("### 📝 Script généré :")
    st.code(script_js, language="javascript")
    st.success("Script généré avec succès !")
