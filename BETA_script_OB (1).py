import streamlit as st

# Configuration de la page
st.set_page_config(page_title="BETA Script OB", layout="centered")

# Titre principal
st.title("🧠 BETA Script OB")
st.markdown("Sélectionnez un type de script à générer dans le menu déroulant ci-dessous.")

# Fonction utilitaire pour convertir un nom d'index en camelCase
def format_variable_name(index: str) -> str:
    parts = index.lower().split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

# Menu déroulant pour choisir le type de script
script_type = st.selectbox(
    "Quel script voulez-vous générer ?",
    [
        "Script - Récupération depuis le référentiel tiers",
        "Script - Renseigner une valeur selon une autre métadonnée",
        "Script - Extraire une partie d'une date (JJ/MM/AAAA)"
    ]
)

# Script 1 : Récupération depuis le référentiel tiers
if script_type == "Script - Récupération depuis le référentiel tiers":
    st.subheader("Script : Récupération depuis le référentiel tiers")
    ref_index = st.text_input("Quel est l'index du référentiel tiers ?", value="MAIL_PARTAGE_INDEX")

    if ref_index:
        variable_name = format_variable_name(ref_index)
        script_js = f"""var getThirdPartVariable = function(pID) {{
    for (var i = 0; i < THIRDPART.values.length; i++) {{
        if (THIRDPART.values[i].id === pID)
            return THIRDPART.values[i].rawValue || "";
    }}
    return "";
}};

var {variable_name} = getThirdPartVariable("{ref_index}");
return {variable_name};"""

        st.markdown("### 📝 Script généré :")
        st.code(script_js, language="javascript")
        st.success("Script généré avec succès !")

# Script 2 : Renseigner une valeur selon une autre métadonnée
elif script_type == "Script - Renseigner une valeur selon une autre métadonnée":
    st.subheader("Script : Renseigner une valeur selon une autre métadonnée")
    index_name = st.text_input("Quel est le nom de l’index de référence ?", value="EMAIL_INDEX")
    value_if_exists = st.text_input("Que doit-on retourner si une valeur existe ?", value="DEMAT")
    value_if_not_exists = st.text_input("Que doit-on retourner si aucune valeur n'existe ?", value="NON DEMAT")

    if index_name and value_if_exists and value_if_not_exists:
        variable_name = format_variable_name(index_name)
        script_js = f"""// Récupération de la valeur de {index_name}
var {variable_name} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, "{index_name}"));

// Vérification de la présence d'une valeur dans {index_name}
if ({variable_name} && {variable_name}.trim() !== "") {{
    return "{value_if_exists}";  // Retourne "{value_if_exists}" si {variable_name} contient quelque chose
}} else {{
    return "{value_if_not_exists}"; // Retourne "{value_if_not_exists}" si {variable_name} est vide ou invalide
}}"""

        st.markdown("### 📝 Script généré :")
        st.code(script_js, language="javascript")
        st.success("Script généré avec succès !")

# Script 3 : Extraire une partie d'une date
elif script_type == "Script - Extraire une partie d'une date (JJ/MM/AAAA)":
    st.subheader("Script : Extraire une partie d'une date (JJ/MM/AAAA)")
    date_index = st.text_input("Quel est l'index de référence contenant la date ?", value="DATE_1_INDEX")
    date_part = st.selectbox("Quelle partie de la date souhaitez-vous extraire ?", ["Jour", "Mois", "Année"])

    if date_index and date_part:
        variable_name = format_variable_name(date_index)
        part_index = {"Jour": 0, "Mois": 1, "Année": 2}[date_part]
        part_label = date_part.lower()

        script_js = f"""// Récupération de la valeur de {date_index}
var {variable_name} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, "{date_index}"));

// Vérification que la valeur de {variable_name} n'est pas vide
if ({variable_name} && {variable_name}.trim() !== "") {{
    var dateParts = {variable_name}.split("/"); // Découpe la date au format JJ/MM/AAAA

    if (dateParts.length === 3) {{
        var extrait = dateParts[{part_index}]; // Extraction du {part_label}
        return extrait; // Retourne le {part_label}
    }}
}} 

// Si la date est invalide ou vide
return "Date invalide";"""

        st.markdown("### 📝 Script généré :")
        st.code(script_js, language="javascript")
        st.success("Script généré avec succès !")
