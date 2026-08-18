import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página (Diseño y cabecera)
st.set_page_config(
    page_title="Asistente de Convivencia - Mariscal Robledo", 
    page_icon="🏫",
    layout="centered"
)

# Estilos CSS personalizados para mejorar el aspecto visual
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #1e3d59;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #cbd5e1;
    }
    .stButton button {
        background-color: #17b978;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        padding: 0.5rem;
        border: none;
    }
    .stButton button:hover {
        background-color: #149a65;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado visual llamativo
st.markdown("<h1>🏫 Asistente de Convivencia Escolar</h1>", unsafe_allow_html=True)
st.markdown("### Institución Educativa Mariscal Robledo")
st.markdown("---")
st.info("💡 **Instrucciones:** Describe de forma breve el incidente reportado por el estudiante y la IA te indicará la clasificación exacta y el protocolo a seguir según el manual.")

# 2. Conexión automática con la llave oculta en la nube
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Base de Conocimiento (El Manual)
    prompt_sistema = """
    Eres el asistente disciplinario legal de la Institución Educativa Mariscal Robledo.
    Tu tarea es leer el reporte del docente, clasificar la falta y dar el protocolo exacto. 
    NO inventes reglas. Basa tus respuestas ÚNICAMENTE en esto:

    1. PROHIBICIONES DISCIPLINARIAS: Llegadas tarde, inasistencias sin excusa. Comportamiento: celulares en clase, salir sin permiso, comer en clase, ruidos/burlas, actos de cariño en el aula, alterar uniforme.
    Protocolo: 1. Docente, 2. Director de grupo, 3. Orientador, 4. Rectoría. Llamado de atención, registro en observador. Retener objetos no permitidos y entregar a acudiente. 3 retardos = 1 hora de limpieza.

    2. SITUACIONES TIPO I (Conflictos mal manejados): Agresiones verbales esporádicas, burlas físicas/raza/género, arrojar objetos sin daño, daño a bienes, vocabulario vulgar.
    Protocolo: Reunir partes, mediar descargos escritos, fijar solución imparcial (reparar daño, restablecer derechos con constancia), seguimiento.

    3. SITUACIONES TIPO II (Acoso o daño sin incapacidad): Reincidir en Tipo I, Bullying, ciberacoso, peleas/agresiones físicas sin incapacidad, consumo de drogas/alcohol en la institución, fugarse.
    Protocolo: Informar acudientes (constancia), remitir a salud si hay daño, Comité de Convivencia define medida (Extrañamiento o Matrícula Condicional), reportar en SIUCE.

    4. SITUACIONES TIPO III (Presuntos delitos): Venta de drogas, porte de armas, hurto comprobado, violencia sexual, extorsión, amenazas de muerte, relaciones sexo-genitales.
    Protocolo: Informar acudientes, Presidente Comité Convivencia informa a Policía Nacional INMEDIATAMENTE, citar Comité, reportar en SIUCE, posible cambio de institución.

    Responde SIEMPRE en este formato estricto:
    🔴 CLASIFICACIÓN: [Tipo de falta]
    📋 PROTOCOLO A SEGUIR: [Lista de pasos]
    """

    # 5. Área de entrada de texto
    st.markdown("#### 📝 Reporte del Incidente")
    incidente = st.text_area("", placeholder="Ej. El estudiante llegó tarde a la clase por tercera vez o usó el celular en horario académico...")

    if st.button("🔍 Consultar Protocolo en el Manual"):
        if incidente:
            with st.spinner("Analizando el caso con el manual de convivencia..."):
                prompt_completo = f"{prompt_sistema}\n\nIncidente reportado: {incidente}\n\nRespuesta:"
                respuesta = model.generate_content(prompt_completo)
                
                st.markdown("---")
                st.success("¡Protocolo generado con éxito!")
                
                # Contenedor con mejor presentación para el resultado
                with st.container():
                    st.markdown(respuesta.text)
        else:
            st.warning("Por favor, escribe una descripción del incidente antes de consultar.")

except Exception as e:
    st.error("⚠️ Error de configuración: Asegúrate de haber guardado correctamente tu `GEMINI_API_KEY` en la sección de 'Secrets' de Streamlit Cloud.")
