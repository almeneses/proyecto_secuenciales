import streamlit as st
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

st.set_page_config(
    page_title="Traducción con Transformer Encoder-Decoder",
    page_icon="🌐",
    layout="centered",
)

MODELOS = {
    "Español → Inglés": "Helsinki-NLP/opus-mt-es-en",
    "Inglés → Español": "Helsinki-NLP/opus-mt-en-es",
}


@st.cache_resource(show_spinner="Descargando y cargando el modelo (solo la primera vez)...")
def cargar_modelo(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    model.eval()
    return tokenizer, model


def traducir(texto, tokenizer, model, max_new_tokens=256):
    inputs = tokenizer(
        texto,
        return_tensors="pt",
        truncation=True,
        padding=True,
    )
    with torch.no_grad():
        salida_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_beams=4,
            early_stopping=True,
        )
    return tokenizer.batch_decode(salida_ids, skip_special_tokens=True)[0]


st.title("🌐 Traducción con un Transformer Encoder-Decoder")
st.caption(
    "Réplica basada en **Democratizing Neural Machine Translation with "
    "OPUS-MT** (Tiedemann et al., 2022) — "
    "[paper](https://huggingface.co/papers/2212.01936) · "
    "[código oficial](https://github.com/Helsinki-NLP/OPUS-MT-train)"
)

with st.sidebar:
    st.header("Configuración")
    direccion = st.selectbox("Dirección de traducción", list(MODELOS.keys()))
    modelo_id = MODELOS[direccion]

    st.markdown("---")
    st.markdown(
        "*¿Cómo funciona la arquitectura?*\n\n"
        "1. El *tokenizador* (SentencePiece) parte el texto en subpalabras.\n"
        "2. El *encoder* procesa toda la secuencia de entrada y genera "
        "representaciones contextuales bidireccionales.\n"
        "3. El *decoder* genera la traducción token a token, atendiendo "
        "mediante cross-attention a la salida del encoder.\n"
        "4. Se usa beam search (4 haces) para elegir la mejor secuencia "
        "de salida completa."
    )

texto = st.text_area(
    "Texto a traducir",
    height=200,
    placeholder="Escribe o pega el texto en el idioma de origen...",
)

traducir_btn = st.button("Traducir", type="primary", use_container_width=True)

if traducir_btn:
    if not texto.strip():
        st.warning("Escribe un texto primero.")
    else:
        tokenizer, model = cargar_modelo(modelo_id)
        with st.spinner("Traduciendo..."):
            resultado = traducir(texto, tokenizer, model)

        st.subheader("Traducción")
        st.success(resultado)

st.markdown("---")
st.caption(
    "Modelo cargado con AutoModelForSeq2SeqLM + AutoTokenizer (Transformers), "
    "compatible con transformers v4 y v5. Arquitectura: Transformer "
    "encoder-decoder entrenado con Marian NMT (proyecto OPUS-MT, "
    "Universidad de Helsinki)."
)