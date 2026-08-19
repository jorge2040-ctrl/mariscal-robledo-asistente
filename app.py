import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# 1. CONFIGURACIÓN BÁSICA DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Sistema de Convivencia - Mariscal Robledo", 
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS PERSONALIZADO - DISEÑO ACADÉMICO PROFESIONAL
# ==========================================
st.markdown("""
    <style>
    /* Importar fuentes profesionales */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
    
    /* Variables de color institucional */
    :root {
        --primary: #7B1E38;
        --primary-dark: #5A1528;
        --primary-light: #9B2E48;
        --accent: #C9A24B;
        --dark: #0F172A;
        --slate: #1E293B;
        --slate-light: #334155;
        --text-light: #F8FAFC;
        --border: #475569;
    }
    
    /* Fondo general con textura sutil */
    .stApp {
        background: linear-gradient(135deg, #0B0E14 0%, #1E293B 100%);
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 2.5rem 3rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(123, 30, 56, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.4;
    }
    
    .main-header h1 {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
        font-weight: 400 !important;
        position: relative;
        z-index: 1;
    }
    
    .institution-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.2rem;
        border-radius: 24px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #FFF;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Tarjeta de instrucciones mejorada */
    .info-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-left: 4px solid var(--accent);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        border: 1px solid var(--border);
    }
    
    .info-card h3 {
        color: var(--accent) !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.8rem !important;
        font-weight: 600 !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-card p {
        color: var(--text-light) !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    
    /* Sección de registro con diseño mejorado */
    .registro-section {
        background: linear-gradient(135deg, var(--slate) 0%, var(--dark) 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: #F8FAFC !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin-bottom: 1.5rem !important;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border);
    }
    
    /* Textarea mejorado */
    .stTextArea textarea {
        background: #0F172A !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(123, 30, 56, 0.2) !important;
        outline: none !important;
    }
    
    .stTextArea label {
        color: var(--text-light) !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Botón principal rediseñado */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.9rem 2.5rem !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(123, 30, 56, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%) !important;
        box-shadow: 0 6px 24px rgba(123, 30, 56, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Tarjeta de resultados */
    .resultado-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        margin-top: 2rem;
    }
    
    .resultado-card h3 {
        color: var(--accent) !important;
        border-bottom: 2px solid var(--border);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem !important;
    }
    
    /* Alertas y mensajes mejorados */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #065f46 0%, #064e3b 100%) !important;
        color: #d1fae5 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #92400e 0%, #78350f 100%) !important;
        color: #fef3c7 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #991b1b 0%, #7f1d1d 100%) !important;
        color: #fecaca !important;
    }
    
    /* Sidebar mejorado */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--slate) 0%, var(--dark) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem !important;
    }
    
    /* Texto del modelo activo */
    .model-info {
        background: rgba(201, 162, 75, 0.1);
        border: 1px solid var(--accent);
        color: var(--accent) !important;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-family: 'IBM Plex Sans', monospace;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Spinner personalizado */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }
    
    /* Markdown en resultados */
    .resultado-card p, .resultado-card ul, .resultado-card ol {
        color: var(--text-light) !important;
        line-height: 1.8 !important;
    }
    
    .resultado-card strong {
        color: var(--accent) !important;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--slate-light);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--border);
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-header, .info-card, .registro-section {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER PRINCIPAL
# ==========================================
st.markdown("""
    <div class="main-header">
        <h1>🏫 Sistema Experto de Convivencia Escolar</h1>
        <p>Institución Educativa Mariscal Robledo - Medellín, Colombia</p>
        <div class="institution-badge">Manual de Convivencia 2024</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR CON INFORMACIÓN
# ==========================================
with st.sidebar:
    st.markdown("### 📚 Acerca del Sistema")
    st.markdown("""
    Este sistema experto analiza incidentes disciplinarios basándose en el **Manual de Convivencia** oficial de la Institución.
    
    **Categorías de Faltas:**
    - 🟡 Prohibiciones Disciplinarias
    - 🟠 Situaciones Tipo I
    - 🟠 Situaciones Tipo II  
    - 🔴 Situaciones Tipo III
    
    ---
    
    **Conducto Regular:**
    1. Docente que presencia
    2. Director de grupo
    3. Orientador escolar
    4. Rector(a)
    
    ---
    
    **Soporte Técnico:**
    📧 sistemas@mariscalrobledo.edu.co
    """)
    
    st.markdown("---")
    st.markdown("**Versión 2.0** | Enero 2025")

# ==========================================
# 5. TARJETA DE INSTRUCCIONES
# ==========================================
st.markdown("""
    <div class="info-card">
        <h3>💡 Instrucciones de Uso</h3>
        <p>Describa de forma clara y detallada el incidente presenciado. El sistema analizará la situación conforme a la normativa legal del Manual de Convivencia vigente y proporcionará la clasificación, acción inmediata y protocolo institucional correspondiente.</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 6. CONTROL DE TASA DE USO
# ==========================================
if 'ultimo_uso' not in st.session_state:
    st.session_state.ultimo_uso = None
if 'contador_consultas' not in st.session_state:
    st.session_state.contador_consultas = 0

def puede_hacer_consulta():
    if st.session_state.ultimo_uso is None:
        return True
    tiempo_transcurrido = time.time() - st.session_state.ultimo_uso
    if tiempo_transcurrido < 10:
        return False
    return True

# ==========================================
# 7. CONEXIÓN A GOOGLE GEMINI
# ==========================================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    generation_config = {"temperature": 0.1}
    
    modelos_preferidos = [
        'models/gemini-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest', 
        'models/gemini-1.5-pro',
        'models/gemini-2.0-flash-exp',
        'models/gemini-pro'
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
        st.error("❌ No se encontró ningún modelo compatible.")
        st.stop()
    
    model = modelo_encontrado
    
    # Mostrar info del modelo de forma elegante
    st.markdown(f"""
        <div class="model-info">
            🤖 Modelo: {nombre_modelo.split('/')[-1]} | Consultas: {st.session_state.contador_consultas}
        </div>
    """, unsafe_allow_html=True)

    prompt_sistema = """
    Eres el Sistema Experto Legal y Disciplinario de la Institución Educativa Mariscal Robledo.
    Tu tarea EXCLUSIVA es leer el reporte del docente, buscar en tu base de datos la falta exacta, clasificarla y determinar el protocolo y la acción inmediata del docente.
    REGLA DE ORO: NO inventes reglas, no asumas protocolos externos, no resumas. Basa tus respuestas ÚNICA Y LITERALMENTE en el siguiente texto oficial del manual de convivencia:

    === ROL Y ACCIÓN INMEDIATA DEL DOCENTE (CONDUCTO REGULAR) ===
    - Para PROHIBICIONES y TIPO I: El primer responsable de dar manejo a la situación o conflicto será el docente que acompaña la actividad académica y que presencia la situación, por lo que deberá generar un espacio de diálogo, mediación y negociación y, de ser necesario, hacer la respectiva anotación en el observador del estudiante tipificando la falta.
    - Para TIPO II y TIPO III: Inmediatamente ocurran los hechos, el docente diligenciará el formato de remisión a orientación escolar, el cual debe ser firmado por el estudiante, y poner los hechos en conocimiento del acudiente/Rectoría.

    === CLASIFICACIÓN DE FALTAS Y PROTOCOLOS ===

    🔴 1. PROHIBICIONES DISCIPLINARIAS
    - FALTAS LITERALES: Dejar de asistir a clases/actos sin excusa válida, llegadas tarde (retardos), mentir para justificar inasistencia, permanecer en lugares no permitidos, uso inadecuado de espacios (templo, restaurante, laboratorios, aulas, etc.), interrumpir con juguetes/aparatos/audífonos/celulares, salirse de clase sin permiso, mal comportamiento en salidas pedagógicas, interrumpir con charlas/risas/burlas/juegos, ingresar mascotas sin autorización, negarse a hacer aseo, consumir alimentos/bebidas/chicles en clase o espacios no permitidos, rayar sillas/paredes/prendas, incumplir actividades, copiar tareas, botar basura mal, entrar sin autorización a oficinas/salones, salir al baño/tienda sin permiso, compras por ventanas, ingresar/salir saltando rejas/muros, falta de cuidado y limpieza, uso inadecuado del tablero, desorden en cambio de clase, perder tiempo, gritos/ruidos que interrumpan, faltar con implementos de clase, atentar contra derechos de autor, portar llaves sin permiso, no informar citaciones, desacatar orientaciones, levantar la voz imponiendo ideas, proselitismo político/religioso, usar o esconder útiles ajenos, usar balones fuera de canchas, permanencia en cantinas/bares portando el uniforme.
    - PROTOCOLO INSTITUCIONAL: 
      1. Seguir conducto regular (1. Docente, 2. Director de grupo, 3. Docente orientador, 4. Rector).
      2. Aplicar medidas formativas: Reflexión guiada, compromiso escrito, citación a padres, extrañamiento temporal o matrícula condicional.
      3. (Específico para retardos): Si acumula 3 o más llegadas tarde en el período, realizará actividades de limpieza por una hora, finalizada la jornada.

    🔴 2. SITUACIONES TIPO I (Conflictos manejados inadecuadamente sin daños a la salud)
    - FALTAS LITERALES: Arrojar piedras/objetos (sin daño), uso inadecuado de baños/recursos/mobiliario, llamados de atención constantes en actos, celebrar inadecuadamente (huevos, harina), daño a bienes institucionales o de compañeros (irrespeto propiedad ajena), actos de cariño en el aula (besos, abrazos, sentarse en piernas), recolectar dinero/rifas sin permiso, vocabulario vulgar/irrespetuoso para humillar, situaciones excluyentes/discriminatorias, rumores para dañar imagen, insultos/apodos/amenazas/burlas morbosas, desórdenes/saboteo, burlas por raza/orientación sexual/físico/credo, enfrentamientos agresivos verbales esporádicos, incitación a enfrentamientos/faltas, manifestaciones de irrespeto arrojando útiles/textos, mensajes obscenos en paredes/pupitres, desórdenes en la calle con uniforme (disturbios), estigmatización/sobrenombres, hechicería/magia/esoterismo, falsas alarmas (fulminantes, pánico), ingreso a viviendas/negocios en tiempo escolar sin permiso, desórdenes en transporte y restaurante, relaciones que exceden confianza estudiante-docente (besos, tocamientos).
    - PROTOCOLO INSTITUCIONAL:
      1. Reunir inmediatamente a las partes involucradas en el conflicto y mediar de manera pedagógica.
      2. Escuchar descargos por escrito.
      3. Fijar forma de solución imparcial (reparar daños, restablecer derechos, reconciliación).
      4. Dejar constancia por escrito en el observador.
      5. Realizar seguimiento del caso.

    🔴 3. SITUACIONES TIPO II (Agresión escolar, bullying, ciberacoso y daños sin incapacidad)
    - FALTAS LITERALES: Reincidir en Tipo I, agresión escolar/Bullying y ciberacoso que no sean delito, Bullying por orientación sexual/identidad de género, agresiones físicas esporádicas sin daño, peleas/lesiones sin incapacidad, atropellar/empujar intencionalmente, juegos bruscos que causen lesiones, uso de elementos peligrosos, tatuajes/perforaciones dentro de la Institución, trifulcas/escándalos dentro o fuera, mensajes sexuales ofensivos en espacios públicos, complicidad para ocultar hechos/mentir, porte/consumo o inducir a energizantes/medicamentos sin receta, salida del establecimiento sin autorización (fuga), consumo de estupefacientes/SPA (drogas, alcohol, vapeadores, etc.) al interior o alrededores, presentarse en estado de embriaguez o bajo SPA.
    - PROTOCOLO INSTITUCIONAL:
      1. Informar inmediatamente a acudientes de los involucrados (constancia escrita).
      2. Si hay daño, garantizar atención inmediata en salud física/mental.
      3. Remitir a autoridades administrativas (Comisaría, ICBF) si se requiere restablecimiento de derechos.
      4. Proteger a los involucrados.
      5. Remitir al Comité de Convivencia para determinar acciones restaurativas y/o pedagógicas (Matrícula Condicional o Extrañamiento temporal).
      6. Reportar obligatoriamente en SIUCE.

    🔴 4. SITUACIONES TIPO III (Presuntos delitos)
    - FALTAS LITERALES: Reincidencia en Tipo II, Homicidio, Hurto/robo comprobado, Acoso Sexual, Violación, Extorsión, Relaciones sexo-genitales dentro de la institución (exhibicionismo/masturbación), corrupción de menores, instrumentalización, porte de explosivos, pandillas/bandas, expendio/distribución de SPA, porte de dispositivos para consumo de SPA (vapeadores, pipas, cigarrillo, candelas), inducir al consumo/venta de SPA, comprar SPA, amenaza de muerte, atentado contra la vida/dignidad, apoyo en bandas de terceros para solucionar conflictos, acoso que revista delito, complicidad en tocamientos sexuales, exhibición sexual por medios, delitos informáticos, agresión física con daño a la salud considerable, porte de pólvora/químicos, secuestro/sicariato/terrorismo, maltrato animal, protestas violentas, grabación no autorizada, explotación sexual, uso de armas (fuego, cortopunzantes, traumáticas, navajas, bisturí), ciberacoso reiterado por homofobia/transfobia, comisión de fraude académico (copia en exámenes, plagio, alteración de notas), falsificar firmas, adulteración de planillas, soborno, suplantación, pornografía infantil (posesión, distribución), calumnia al buen nombre.
    - PROTOCOLO INSTITUCIONAL:
      1. Informar inmediatamente a los acudientes (constancia escrita).
      2. Garantizar atención en salud si hay daño físico/mental.
      3. El presidente del Comité informará INMEDIATAMENTE a la Policía Nacional.
      4. Citar al Comité de Convivencia Escolar para tomar medidas propias e iniciar Proceso Reeducativo.
      5. Reportar en SIUCE.
      6. Sugerir Cambio de Institución por parte del Consejo Directivo (si aplica).

    === FORMATO ESTRICTO DE RESPUESTA ===
    
    CLASIFICACION: [Tipo de falta]
    
    ACCION INMEDIATA DEL DOCENTE: [Qué debe hacer]
    
    PROTOCOLO INSTITUCIONAL: [Pasos a seguir]
    """

    # ==========================================
    # 8. FORMULARIO DE REGISTRO
    # ==========================================
    st.markdown('<div class="registro-section">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📝 Registro del Incidente</p>', unsafe_allow_html=True)
    
    incidente = st.text_area(
        "Describa los hechos ocurridos con el estudiante:",
        height=150,
        placeholder="Ejemplo: El estudiante llegó 15 minutos tarde a la clase de matemáticas sin justificación médica ni autorización previa..."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analizar_btn = st.button("🔍 Analizar Protocolo Legal")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 9. PROCESAMIENTO Y RESULTADOS
    # ==========================================
    if analizar_btn:
        if not puede_hacer_consulta():
            tiempo_restante = 10 - int(time.time() - st.session_state.ultimo_uso)
            st.warning(f"⏳ Por favor espere {tiempo_restante} segundos antes de realizar otra consulta.")
        elif incidente.strip():
            with st.spinner("⚖️ Consultando el Manual de Convivencia..."):
                try:
                    prompt_completo = f"{prompt_sistema}\n\nIncidente: {incidente}\n\nRespuesta:"
                    respuesta = model.generate_content(prompt_completo)
                    
                    if respuesta and respuesta.text:
                        st.success("✅ Análisis completado con base en la normativa vigente.")
                        
                        # Formatear respuesta
                        texto = respuesta.text.strip()
                        texto = texto.replace("CLASIFICACION:", "🔴 **CLASIFICACIÓN:**")
                        texto = texto.replace("ACCION INMEDIATA DEL DOCENTE:", "\n\n👩‍🏫 **ACCIÓN INMEDIATA DEL DOCENTE:**")
                        texto = texto.replace("PROTOCOLO INSTITUCIONAL:", "\n\n📋 **PROTOCOLO INSTITUCIONAL A SEGUIR:**")
                        
                        # Mostrar en tarjeta de resultados
                        st.markdown('<div class="resultado-card">', unsafe_allow_html=True)
                        st.markdown("### Resultado del Análisis")
                        st.markdown(texto)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Actualizar contadores
                        st.session_state.ultimo_uso = time.time()
                        st.session_state.contador_consultas += 1
                    else:
                        st.warning("⚠️ No se pudo generar respuesta. Intente reformular el incidente.")
                        
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        st.error("⚠️ **Límite de cuota alcanzado**")
                        st.info("Por favor espere unos minutos o contacte al administrador del sistema para actualizar el plan de la API.")
                    else:
                        st.error("⚠️ Error al procesar la respuesta.")
                        with st.expander("Ver detalles técnicos"):
                            st.code(str(e)[:300])
        else:
            st.warning("⚠️ Por favor, describa el incidente antes de realizar la consulta.")

except Exception as e:
    st.error("⚠️ Error de configuración del sistema.")
    st.caption(f"Detalle técnico: {e}")

# ==========================================
# 10. FOOTER
# ==========================================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📧 Contacto:** sistemas@mariscalrobledo.edu.co")
with col2:
    st.markdown("**🏫 Sede:** Medellín, Antioquia")
with col3:
    st.markdown("**📅 Versión:** 2.0 - Enero 2025")
