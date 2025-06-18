
import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import io

# Titel und Hintergrund
st.set_page_config(page_title="Kayou Karten Scanner", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-image: url('https://i.imgur.com/YOUR_TSUNADE_BACKGROUND.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🃏 Naruto Kayou Karten Scanner")

# Uploadbereich
uploaded_files = st.file_uploader("📤 Lade deine Kartenbilder hoch", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Lokale Kartendatenbank
if "card_list" not in st.session_state:
    st.session_state.card_list = []

# OCR- und Kartenerkennung
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hochgeladene Karte", use_column_width=True)

        # Seriennummer-Bereich ausschneiden (rechts unten)
        width, height = image.size
        crop = image.crop((width*0.72, height*0.88, width*0.98, height*0.98))
        crop = crop.convert("L").resize((300, 80))
        text = pytesseract.image_to_string(crop)
        seriennummer = [line for line in text.split("\n") if "NR-" in line or "SR-" in line or "SSR" in line]
        seriennummer = seriennummer[0] if seriennummer else "Nicht erkannt"

        # Dummy-Werte (später Datenbankanbindung möglich)
        karte = {
            "Dateiname": uploaded_file.name,
            "Seriennummer": seriennummer,
            "Charakter": "– manuell ergänzen –",
            "ATK": None,
            "DEF": None,
            "Seltenheit": "?"
        }
        st.session_state.card_list.append(karte)

# Anzeige der Sammlung
if st.session_state.card_list:
    df = pd.DataFrame(st.session_state.card_list)
    df_sorted = df.sort_values(by="Seriennummer")
    st.markdown("### 📋 Deine aktuelle Sammlung:")
    st.dataframe(df_sorted)

    # Export-Option
    csv = df_sorted.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Als CSV exportieren", data=csv, file_name="kayou_sammlung.csv", mime="text/csv")
