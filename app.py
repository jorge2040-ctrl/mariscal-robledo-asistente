import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# 1. CONFIGURACIÓN BÁSICA DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Sistema de Convivencia - Mariscal Robledo", 
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS PERSONALIZADO
# ==========================================
st.markdown("""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #FFFFFF;
        background-image: url('https://raw.githubusercontent.com/jorge2040-ctrl/mariscal-robledo-asistente/main/escudo.png');
        background-repeat: no-repeat;
        background-position: center center;
        background-size: 400px;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.92);
        z-index: 0;
        pointer-events: none;
    }
    
    .main { position: relative; z-index: 1; }
    
    /* 1. MUEVE TODA LA APP HACIA ARRIBA */
    .block-container {
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important;
        max-width: 800px !important;
    }
    
    /* 2. BANNER VINOTINTO ULTRA COMPACTO */
    .header-compact {
        background: linear-gradient(135deg, #7B1E38 0%, #5A1528 100%);
        padding: 0.5rem 1rem; /* Relleno superior e inferior casi nulo */
        border-radius: 12px;
        margin-bottom: 0.8rem; /* Menos espacio hacia las instrucciones */
        box-shadow: 0 4px 12px rgba(123, 30, 56, 0.2);
        text-align: center;
    }
    
    .header-logo {
        width: 45px; /* Escudo más pequeño */
        height: auto;
        margin-bottom: 0px !important;
        filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.3));
    }
    
    .header-compact h1 {
        color: #FFFFFF !important;
        font-size: 1.4rem !important; /* Letra un poco más ajustada */
        font-weight: 800 !important;
        margin: 2px 0 0 0 !important;
        line-height: 1.2;
    }
    
    .header-compact h2 {
        color: #F8D7DA !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        letter-spacing: 0.5px;
    }
    
    .header-author {
        color: #E2E8F0 !important;
        font-size: 0.75rem !important;
        font-style: italic;
        margin: 2px auto 0 auto !important;
        opacity: 0.9;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 2px;
        width: 50%;
    }
    
    /* 3. INSTRUCCIONES MÁS DELGADAS */
    .instrucciones {
        background: #F8F9FA;
        border-left: 4px solid #C9A24B;
        padding: 0.6rem 1rem; /* Menos relleno */
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #2D3748;
        line-height: 1.4;
    }
    
    /* RESTO DE ESTILOS (CAJA DE TEXTO Y BOTÓN) */
    .stTextArea label {
        color: #2D3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0px !important;
    }
    
    .stTextArea textarea {
        background: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #2D3748 !important;
        font-size: 0.95rem !important;
        padding: 0.6rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #7B1E38 !important;
        box-shadow: 0 0 0 3px rgba(123, 30, 56, 0.1) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7B1E38 0%, #5A1528 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.7rem 2rem !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(123, 30, 56, 0.3) !important;
        margin-top: 0.2rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(123, 30, 56, 0.4) !important;
    }
    
    .resultado-box {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .resultado-box h3 {
        color: #7B1E38 !important;
        font-size: 1.2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.7rem !important;
        border-bottom: 2px solid #E2E8F0 !important;
    }
    
    .resultado-box p, .resultado-box ul, .resultado-box ol {
        color: #2D3748 !important;
        line-height: 1.7 !important;
        font-size: 0.95rem !important;
    }
    
    .resultado-box strong { color: #7B1E38 !important; }
    
    .stSuccess {
        background-color: #D1FAE5 !important;
        color: #065F46 !important;
        border: 1px solid #A7F3D0 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .stWarning, .stError {
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .model-badge {
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        color: #475569;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 1rem;
        font-family: monospace;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
    </style>
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER
# ==========================================
st.markdown("""
    <div class="header-compact">
        <img src="https://raw.githubusercontent.com/jorge2040-ctrl/mariscal-robledo-asistente/main/escudo.png" class="header-logo" alt="Escudo I.E. Mariscal Robledo">
        <h1>Sistema de Convivencia Escolar</h1>
        <h2>I.E. Mariscal Robledo</h2>
        <p class="header-author">Desarrollado por: El Profe Jorge</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. INSTRUCCIONES
# ==========================================
st.markdown("""
    <div class="instrucciones">
        <strong>💡 Instrucciones:</strong> Describa el incidente para clasificar la falta o realice una pregunta general sobre las normas. El sistema analizará estrictamente el Manual de Convivencia vigente.
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. CONTROL DE TASA DE USO
# ==========================================
if 'ultimo_uso' not in st.session_state:
    st.session_state.ultimo_uso = None
if 'contador_consultas' not in st.session_state:
    st.session_state.contador_consultas = 0

def puede_hacer_consulta():
    if st.session_state.ultimo_uso is None:
        return True
    return (time.time() - st.session_state.ultimo_uso) >= 10

# ==========================================
# 6. CONEXIÓN A GOOGLE GEMINI
# ==========================================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    generation_config = {"temperature": 0.1}
    
    # CORRECCIÓN VITAL: Se exige gemini-3.6-flash según el último error de Google
    modelos_preferidos = [
        'models/gemini-3.6-flash',
        'models/gemini-flash-latest',
        'models/gemini-pro',
        'models/gemini-1.5-flash'
    ]
    
    modelo_encontrado = None
    nombre_modelo = None
    
    for nombre in modelos_preferidos:
        try:
            modelo_encontrado = genai.GenerativeModel(nombre, generation_config=generation_config)
            nombre_modelo = nombre
            break
        except:
            continue
    
    if modelo_encontrado is None:
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                if 'gemma' in model_info.name.lower():
                    continue
                nombre_modelo = model_info.name
                try:
                    modelo_encontrado = genai.GenerativeModel(nombre_modelo, generation_config=generation_config)
                    break
                except:
                    continue
    
    if modelo_encontrado is None:
        st.error("❌ No se encontró ningún modelo compatible. Verifica tu API Key.")
        st.stop()
    
    model = modelo_encontrado

    # ==========================================
    # 7. PROMPT DEL SISTEMA (INTELIGENCIA DUAL ESTRICTA)
    # ==========================================
    prompt_sistema = """
    Eres el Sistema Experto Legal y Disciplinario de la Institución Educativa Mariscal Robledo.
    Tu tarea es asistir a los docentes basándote ÚNICA Y EXCLUSIVAMENTE en el texto literal de tu base de datos del Manual de Convivencia.
    REGLA DE ORO: NO inventes reglas, no asumas protocolos externos, no busques en internet. Si te hacen una pregunta cuya respuesta no está en este texto, debes responder exactamente: "Esa información no se encuentra en el fragmento del manual que tengo disponible."

    === BASE DE DATOS (MANUAL DE CONVIVENCIA) ===
    
    TÉRMINOS Y DEFINICIONES CLAVE:
    - SIUCE: El Sistema de Información Unificado de Convivencia Escolar apoya la identificación, consulta, registro y seguimiento de casos de acoso, violencia escolar, consumo de Sustancias Psicoactivas, embarazo en adolescencia y vulneración de derechos sexuales y reproductivos.
    - DEBIDO PROCESO: Garantiza que un proceso sea justo. Nadie podrá ser juzgado sino conforme a leyes preexistentes. Toda persona se presume inocente hasta que no se le declare culpable.
    - MEDIDAS PEDAGÓGICAS: Son acciones formativas y reflexivas. Incluyen Extrañamiento Temporal y Matrícula Condicional.
    - RUTAS DE ATENCIÓN: Se dividen en Promoción, Prevención, Atención y Seguimiento.

    CONDUCTO REGULAR (ROL DEL DOCENTE):
    1. Docente que acompaña la clase: El primer responsable de dar manejo a la situación o conflicto será el docente que acompaña la actividad académica, quien deberá generar un espacio de diálogo, mediación y de ser necesario hacer la anotación en el observador tipificando la falta.
    2. Director de Grupo.
    3. Docente orientador.
    4. Rector.
    - Para situaciones TIPO II y TIPO III: Inmediatamente ocurran los hechos, el docente diligenciará el formato de remisión a orientación escolar firmado por el estudiante, y pondrá los hechos en conocimiento del acudiente/Rectoría.

    CLASIFICACIÓN DE FALTAS Y PROTOCOLOS:
    
    🔴 1. PROHIBICIONES DISCIPLINARIAS
    - FALTAS: Dejar de asistir sin excusa, llegadas tarde (retardos), mentir para justificar inasistencia, permanecer en lugares no permitidos, uso inadecuado de espacios (templo, restaurante, laboratorios, aulas), interrumpir con aparatos/celulares/juguetes, salirse de clase sin permiso, mal comportamiento en salidas pedagógicas, interrumpir con charlas/risas/burlas, ingresar mascotas, negarse a hacer aseo, consumir alimentos/bebidas en clase, rayar sillas/paredes, incumplir actividades, copiar tareas, botar basura mal, entrar sin autorización a oficinas, salir al baño/tienda sin permiso, compras por ventanas, saltar rejas, uso inadecuado del tablero, desorden en cambio de clase, perder tiempo, gritos/ruidos, faltar con implementos, atentar contra derechos de autor, portar llaves sin permiso, no informar citaciones, desacatar orientaciones, levantar la voz, proselitismo político/religioso, esconder útiles ajenos, usar balones fuera de canchas, permanencia en cantinas con uniforme.
    - PROTOCOLO: 1. Seguir conducto regular. 2. Aplicar medidas formativas (Reflexión guiada, compromiso escrito, citación a padres, extrañamiento temporal o matrícula condicional). 3. (Retardos): Acumular 3 o más llegadas tarde en el período genera actividades de limpieza por una hora, finalizada la jornada.

    🔴 2. SITUACIONES TIPO I (Conflictos manejados inadecuadamente sin daños a la salud)
    - FALTAS: Arrojar piedras (sin daño), uso inadecuado de baños/recursos, llamados de atención constantes, celebrar inadecuadamente (huevos/harina), daño a bienes/irrespeto propiedad ajena, actos de cariño (besos, abrazos, sentarse en piernas), recolectar dinero/rifas sin permiso, vocabulario vulgar para humillar, situaciones excluyentes/discriminatorias, rumores, insultos/apodos/amenazas/burlas morbosas, desórdenes/saboteo, burlas por raza/orientación sexual/físico/credo, enfrentamientos agresivos verbales esporádicos, incitación a enfrentamientos, arrojar útiles/textos, mensajes obscenos, desórdenes en la calle con uniforme, estigmatización/sobrenombres, hechicería/magia/esoterismo, falsas alarmas (pánico/quemar basura), ingreso a viviendas/negocios en tiempo escolar sin permiso, desórdenes en transporte/restaurante, relaciones que exceden confianza estudiante-docente.
    - PROTOCOLO: 1. Reunir inmediatamente a las partes involucradas y mediar de manera pedagógica. 2. Escuchar descargos por escrito. 3. Fijar forma de solución imparcial (reparar daños, restablecer derechos, reconciliación). 4. Dejar constancia por escrito en el observador. 5. Realizar seguimiento del caso.

    🔴 3. SITUACIONES TIPO II (Agresión escolar, bullying, ciberacoso y daños sin incapacidad)
    - FALTAS: Reincidir en Tipo I, agresión escolar/Bullying y ciberacoso que no sean delito, Bullying por orientación sexual/identidad de género, agresiones físicas esporádicas sin daño, peleas/lesiones sin incapacidad, atropellar/empujar intencionalmente, juegos bruscos con lesiones, uso de elementos peligrosos, tatuajes/perforaciones en la Institución, trifulcas/escándalos, mensajes sexuales ofensivos en espacios públicos, complicidad para ocultar hechos/mentir, porte/consumo o inducir a energizantes/medicamentos sin receta, salida del establecimiento sin autorización (fuga), consumo de estupefacientes/SPA (drogas, alcohol, vapeadores) al interior o alrededores, presentarse en estado de embriaguez o bajo SPA.
    - PROTOCOLO: 1. Informar inmediatamente a acudientes de los involucrados (constancia escrita). 2. Garantizar atención en salud física/mental si hay daño. 3. Remitir a autoridades (Comisaría/ICBF) si requiere restablecimiento de derechos. 4. Proteger a los involucrados. 5. Remitir al Comité de Convivencia para acciones restaurativas (Matrícula Condicional o Extrañamiento temporal). 6. Reportar obligatoriamente en SIUCE.

    🔴 4. SITUACIONES TIPO III (Presuntos delitos)
    - FALTAS: Reincidencia en Tipo II, Homicidio, Hurto/robo comprobado, Acoso Sexual, Violación, Extorsión, Relaciones sexo-genitales dentro de la institución, corrupción de menores, instrumentalización, porte de explosivos, pandillas/bandas, expendio/distribución de SPA, porte de dispositivos para SPA (vapeadores, pipas, cigarrillo), inducir consumo/venta de SPA, comprar SPA, amenaza de muerte, atentado contra la vida/dignidad, apoyo en bandas para solucionar conflictos, acoso delito, complicidad en tocamientos sexuales, exhibición sexual por medios, delitos informáticos, agresión física con daño a la salud considerable, porte de pólvora/químicos, secuestro/sicariato/terrorismo, maltrato animal, protestas violentas, grabación no autorizada, explotación sexual, uso de armas (fuego, cortopunzantes, traumáticas, bisturí), ciberacoso reiterado por homofobia/transfobia, fraude académico (copia, plagio, alteración de notas), falsificar firmas, adulteración de planillas, soborno, suplantación, pornografía infantil, calumnia al buen nombre.
    - PROTOCOLO: 1. Informar inmediatamente a acudientes (constancia escrita). 2. Garantizar atención en salud si hay daño físico/mental. 3. El presidente del Comité informará INMEDIATAMENTE a la Policía Nacional. 4. Citar al Comité de Convivencia Escolar para iniciar Proceso Reeducativo. 5. Reportar en SIUCE. 6. Sugerir Cambio de Institución por parte del Consejo Directivo (si aplica).

    === INSTRUCCIONES DE PROCESAMIENTO ===
    Analiza la consulta del usuario y determina si es un REPORTE DE INCIDENTE o una PREGUNTA GENERAL.

    CASO A - SI ES UN REPORTE DE INCIDENTE:
    Usa ESTRICTAMENTE este formato sin añadir información extra:
    CLASIFICACION: [Indica el Tipo de falta exacto]
    ACCION INMEDIATA DEL DOCENTE: [Indica el paso a paso del conducto regular]
    PROTOCOLO INSTITUCIONAL: [Enumera los pasos exactos del protocolo]

    CASO B - SI ES UNA PREGUNTA GENERAL (Ej. ¿Qué es el SIUCE?, ¿Cuáles son las faltas tipo 2?):
    Responde de manera amable, directa y como un asistente virtual experto, basándote EXCLUSIVAMENTE en el texto de la base de datos provista. Usa formato Markdown (negritas, viñetas) para hacer la lectura clara, sin usar el formato estricto del "Caso A".
    """

    # ==========================================
    # 8. FORMULARIO
    # ==========================================
    st.markdown("#### 📝 Registro de Incidente o Consulta")
    incidente = st.text_area(
        "",
        height=120,
        placeholder="Ejemplo 1 (Incidente): Estudiante llegó 20 minutos tarde.\nEjemplo 2 (Pregunta): ¿Qué situaciones se reportan en el SIUCE?",
        label_visibility="collapsed"
    )
    
    analizar_btn = st.button("🔍 Analizar / Consultar")

    # ==========================================
    # 9. PROCESAMIENTO Y RESULTADOS
    # ==========================================
    if analizar_btn:
        if not puede_hacer_consulta():
            tiempo_restante = 10 - int(time.time() - st.session_state.ultimo_uso)
            st.warning(f"⏳ Espere {tiempo_restante} segundos antes de realizar otra consulta.")
        elif incidente.strip():
            with st.spinner("⚖️ Analizando en el Manual de Convivencia..."):
                try:
                    prompt_completo = f"{prompt_sistema}\n\nConsulta del usuario: {incidente}\n\nRespuesta:"
                    respuesta = model.generate_content(prompt_completo)
                
                    if respuesta and respuesta.text:
                        st.success("✅ Análisis completado")
                        texto = respuesta.text.strip()
                        
                        # Formateo si la respuesta es del CASO A
                        if "CLASIFICACION:" in texto or "ACCION INMEDIATA DEL DOCENTE:" in texto:
                            texto = texto.replace("CLASIFICACION:", "**🔴 CLASIFICACIÓN:**")
                            texto = texto.replace("ACCION INMEDIATA DEL DOCENTE:", "\n\n**👨‍🏫 ACCIÓN INMEDIATA:**")
                            texto = texto.replace("PROTOCOLO INSTITUCIONAL:", "\n\n**📋 PROTOCOLO INSTITUCIONAL:**")
                        
                        st.markdown(f"""<div class="resultado-box">
                            <h3>Resultado de la Consulta</h3>
                            {texto}
                        </div>""", unsafe_allow_html=True)
                        
                        st.session_state.ultimo_uso = time.time()
                        st.session_state.contador_consultas += 1
                    else:
                        st.warning("⚠️ No se pudo generar respuesta. Intente reformular la consulta.")
                        
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        st.error("⚠️ Límite de cuota alcanzado. Espere unos minutos.")
                    else:
                        st.error(f"⚠️ Error al procesar la respuesta: {e}")
        else:
            st.warning("⚠️ Por favor describa el incidente o realice su pregunta.")
    
    st.markdown(
        f'<div class="model-badge">Modelo: {nombre_modelo.split("/")[-1]} | Consultas: {st.session_state.contador_consultas}</div>',
        unsafe_allow_html=True
    )

except Exception as e:
    st.error("⚠️ Error de configuración del sistema.")
    st.caption(f"Detalle: {e}")
