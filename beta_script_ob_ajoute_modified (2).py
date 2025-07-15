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
        "Script - Extraire une partie d'une date (JJ/MM/AAAA)",
        "Script - Contrôle de cohérence entre un référentiel tiers et une métadonnée",
        "Script - Récupérer le nom (dossier ou tiers)",
        "Script - Contrôle de cohérence entre 3 métadonnées"
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

# Script 4 : Contrôle de cohérence entre un référentiel tiers et une métadonnée
elif script_type == "Script - Contrôle de cohérence entre un référentiel tiers et une métadonnée":
    st.subheader("Script : Contrôle de cohérence entre un référentiel tiers et une métadonnée")
    metadata_index = st.text_input("Quel est l'index de la métadonnée de référence ?", value="EMAIL_INDEX")
    thirdparty_index = st.text_input("Quel est l'index du référentiel tiers de référence ?", value="BPE_EMAIL_INDEX")
    value_if_equal = st.text_input("Que doit-on retourner si les deux valeurs sont identiques ?", value="OK")
    value_if_different = st.text_input("Que doit-on retourner si les deux valeurs sont différentes ?", value="NON")

    if metadata_index and thirdparty_index and value_if_equal and value_if_different:
        metadata_var = format_variable_name(metadata_index)
        thirdparty_var = format_variable_name(thirdparty_index)
        script_js = f"""// Récupération de la valeur de {metadata_index}
var {metadata_var} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, "{metadata_index}")).trim().toLowerCase();

// Fonction pour récupérer une variable de la troisième partie
var getThirdPartVariable = function(pID) {{
    for (var i = 0; i < THIRDPART.values.length; i++) {{
        if (THIRDPART.values[i].id == pID)
            return THIRDPART.values[i].rawValue;
    }}
    return "";
}};

// Récupération de la valeur de {thirdparty_index}
var {thirdparty_var} = getThirdPartVariable("{thirdparty_index}").trim().toLowerCase();

// Vérification de l'égalité entre les deux valeurs
if ({metadata_var} === {thirdparty_var}) {{
    return "{value_if_equal}";  // Les valeurs sont identiques
}} else {{
    return "{value_if_different}"; // Les valeurs sont différentes
}}"""

        st.markdown("### 📝 Script généré :")
        st.code(script_js, language="javascript")
        st.success("Script généré avec succès !")

# Script 5 : Contrôle de cohérence entre 3 métadonnées
elif script_type == "Script - Contrôle de cohérence entre 3 métadonnées":
    st.subheader("Script : Contrôle de cohérence entre 3 métadonnées")
    index1 = st.text_input("Quel est l'index de référence 1 ?", value="INDEX_1")
    index2 = st.text_input("Quel est l'index de référence 2 ?", value="INDEX_2")
    index3 = st.text_input("Quel est l'index de référence 3 ?", value="INDEX_3")
    value_if_all_ok = st.text_input("Que doit-on retourner si les trois valeurs sont 'OK' ?", value="CONTROLE OK")
    value_if_not_all_ok = st.text_input("Que doit-on retourner si au moins une valeur n'est pas 'OK' ?", value="CONTROLE NON OK")

    if index1 and index2 and index3 and value_if_all_ok and value_if_not_all_ok:
        var1 = format_variable_name(index1)
        var2 = format_variable_name(index2)
        var3 = format_variable_name(index3)
        script_js = f"""// Récupération des valeurs des trois index
var {var1} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, "{index1}"));
var {var2} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, "{index2}"));
var {var3} = getTextFromIndexInfo(getFirstIndexFromID(pParameters, "{index3}"));

// Vérification des trois valeurs
if (
    {var1} && {var1}.trim() === "OK" &&
    {var2} && {var2}.trim() === "OK" &&
    {var3} && {var3}.trim() === "OK"
) {{
    return "{value_if_all_ok}";  // Tous les index contiennent "OK"
}} else {{
    return "{value_if_not_all_ok}"; // Au moins un index n'est pas "OK"
}}"""

        st.markdown("### 📝 Script généré :")
        st.code(script_js, language="javascript")
        st.success("Script généré avec succès !")

# Script 6 : Récupérer le nom (dossier ou tiers)
elif script_type == "Script - Récupérer le nom (dossier ou tiers)":
    st.subheader("Script : Récupérer le nom (dossier ou tiers)")
    source = st.selectbox("Souhaitez-vous récupérer le nom depuis :", ["Le dossier", "Le tiers"])
    if source:
        source_var = "FOLDER" if source == "Le dossier" else "THIRDPART"
        source_label = "dossier" if source == "Le dossier" else "tiers"
        script_js = f"""// Récupération de la source : {source_label}
var nomDoss = [{source_var}];

// On extrait juste le champ "name"
var nom = nomDoss[0].name;

return nom;  // retourne le nom du {source_label} (ex: "konica")"""
        st.markdown("### 📝 Script généré :")
        st.code(script_js, language="javascript")
        st.success("Script généré avec succès !")
