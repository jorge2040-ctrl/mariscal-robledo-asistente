import streamlit as st
import google.generativeai as genai

# 1. Configuración visual
st.set_page_config(page_title="Asistente de Convivencia - Mariscal Robledo", page_icon="🏫")
st.title("🏫 Buscador Rápido: Manual de Convivencia")
st.markdown("Ingresa el incidente y la IA te dirá el protocolo exacto a seguir.")

# 2. Casilla de API Key
api_key = st.text_input("Pega tu API Key de Gemini aquí (solo tú la ves):", type="password")

if api_key:
    # 3. Conexión con el modelo actualizado exacto que pide el sistema
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel('gemini-3.6-flash')

        # 4. Base de Conocimiento (El Manual)
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

        # 5. Buscador
        incidente = st.text_area("Describe el incidente de forma breve (ej. 'tiró piedras' o 'usó el celular en clase'):")

        if st.button("Buscar Protocolo"):
            if incidente:
                with st.spinner("Buscando en el manual..."):
                    prompt_completo = f"{prompt_sistema}\n\nIncidente reportado: {incidente}\n\nRespuesta:"
                    respuesta = model.generate_content(prompt_completo)
                    st.success("¡Resultado encontrado!")
                    st.markdown(respuesta.text)
            else:
                st.warning("Por favor, describe un incidente primero.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")