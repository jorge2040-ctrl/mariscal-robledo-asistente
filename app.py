import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Diagnóstico API", page_icon="🔍")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    st.title("🔍 Modelos disponibles en tu API Key")
    
    modelos_disponibles = []
    for model_info in genai.list_models():
        if 'generateContent' in model_info.supported_generation_methods:
            modelos_disponibles.append(model_info.name)
            st.success(f"✅ {model_info.name}")
    
    if not modelos_disponibles:
        st.error("❌ No se encontraron modelos disponibles")
    else:
        st.info(f"Total de modelos: {len(modelos_disponibles)}")
        
except Exception as e:
    st.error(f"Error: {e}")
