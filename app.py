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
# 2. CSS PERSONALIZADO - DISEÑO LIMPIO Y COMPACTO
# ==========================================
st.markdown("""
    <style>
    /* Importar fuente limpia */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Fondo blanco con escudo como marca de agua */
    .stApp {
        background-color: #FFFFFF;
        background-image: url('https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/escudo.png');
        background-repeat: no-repeat;
        background-position: center center;
        background-size: 400px;
        background-attachment: fixed;
        opacity: 1;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.92);
        z-index: 0;
        pointer-events: none;
    }
    
    /* Contenedor principal */
    .main {
        position: relative;
        z-index: 1;
    }
    
    /* Header compacto */
    .header-compact {
        background: linear-gradient(135deg, #7B1E38 0%, #5A1528 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(123, 30, 56, 0.2);
        text-align: center;
    }
    
    .header-compact h1 {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    
    .header-compact p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.95rem !important;
        margin: 0.3rem 0 0 0 !important;
    }
    
    /* Instrucciones compactas */
    .instrucciones {
        background: #F8F9FA;
        border-left: 4px solid #C9A24B;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        color: #2D3748;
        line-height: 1.5;
    }
    
    /* Formulario limpio */
    .stTextArea label {
        color: #2D3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextArea textarea {
        background: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #2D3748 !important;
        font-size: 0.95rem !important;
        padding: 0.8rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #7B1E38 !important;
        box-shadow: 0 0 0 3px rgba(123, 30, 56, 0.1) !important;
        outline: none !important;
    }
    
    /* Botón principal */
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
        margin-top: 0.5rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(123, 30, 56, 0.4) !important;
    }
    
    /* Resultados */
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
    
    .resultado-box strong {
        color: #7B1E38 !important;
    }
    
    /* Alertas limpias */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stSuccess {
        background-color: #D1FAE5 !important;
        color: #065F46 !important;
        border: 1px solid #A7F3D0 !important;
    }
    
    .stWarning {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
        border: 1px solid #FDE68A !important;
    }
    
    .stError {
        background-color: #FEE2E2 !important;
        color: #991B1B !important;
        border: 1px solid #FECACA !important;
    }
    
    /* Info del modelo - compacta */
    .model-badge {
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        color: #475569;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.8rem;
        text-align: center;
        margin: 0.8rem 0;
        font-family: monospace;
    }
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Eliminar padding excesivo */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 800px !important;
    }
    
    /* Scrollbar limpio */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER COMPACTO
# ==========================================
st.markdown("""
    <div class="header-compact">
        <h1>🏫 Sistema de Convivencia Escolar</h1>
        <p>I.E. Mariscal Robledo - Medellín</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. INSTRUCCIONES BREVES
# ==========================================
st.markdown("""
    <div class="instrucciones">
        <strong>💡 Instrucciones:</strong> Describa brevemente el incidente. El sistema determinará la clasificación y protocolo según el Manual de Convivencia vigente.
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
    tiempo_transcurrido = time.time() - st.session_state.ultimo_uso
    if tiempo_transcurrido < 10:
        return False
    return True

# ==========================================
# 6. CONEXIÓN A GOOGLE GEMINI
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
    - FALTAS LITERALES: Arrojar piedras/objetos (sin daño), uso inadecuado de baños/recursos/mobiliario, llamados de atención constantes en actos, celebrar inadecuadamente (huevos, harina), daño a bienes institucionales o de compañeros (irrespeto propiedad ajena), actos de cariño en el aula (besos, abrazos, sentarse en piernas), recolectar dinero/rifas sin permiso, vocabulario vulgar/irrespetuoso para humiliar, situaciones excluyentes/discriminatorias, rumores para dañar imagen, insultos/apodos/amenazas/burlas morbosas, desórdenes/saboteo, burlas por raza/orientación sexual/físico/credo, enfrentamientos agresivos verbales esporádicos, incitación a enfrentamientos/faltas, manifestaciones de irrespeto arrojando útiles/textos, mensajes obscenos en paredes/pupitres, desórdenes en la calle con uniforme (disturbios), estigmatización/sobrenombres, hechicería/magia/esoterismo, falsas alarmas (fulminantes, pánico), ingreso a viviendas/negocios en tiempo escolar sin permiso, desórdenes en transporte y restaurante, relaciones que exceden confianza estudiante-docente (besos, tocamientos).
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

    === FORMATO DE RESPUESTA ===
    
    CLASIFICACION: [Tipo de falta]
    
    ACCION INMEDIATA DEL DOCENTE: [Qué debe hacer]
    
    PROTOCOLO INSTITUCIONAL: [Pasos a seguir]
    """

    # ==========================================
    # 7. FORMULARIO COMPACTO
    # ==========================================
    incidente = st.text_area(
        "📝 Describa el incidente:",
        height=120,
        placeholder="Ejemplo: Estudiante llegó 20 minutos tarde sin justificación..."
    )
    
    analizar_btn = st.button("🔍 Analizar Protocolo")

    # ==========================================
    # 8. PROCESAMIENTO
    # ==========================================
    if analizar_btn:
        if not puede_hacer_consulta():
            tiempo_restante = 10 - int(time.time() - st.session_state.ultimo_uso)
            st.warning(f"⏳ Espere {tiempo_restante} segundos antes de realizar otra consulta.")
        elif incidente.strip():
            with st.spinner("⚖️ Analizando..."):
                try:
                    prompt_completo = f"{prompt_sistema}\n\nIncidente: {incidente}\n\nRespuesta:"
                    respuesta = model.generate_content(prompt_completo)
                    
                    if respuesta and respuesta.text:
                        st.success("✅ Análisis completado")
                        
                        texto = respuesta.text.strip()
                        texto = texto.replace("CLASIFICACION:", "**🔴 CLASIFICACIÓN:**")
                        texto = texto.replace("ACCION INMEDIATA DEL DOCENTE:", "\n\n**👨‍🏫 ACCIÓN INMEDIATA:**")
                        texto = texto.replace("PROTOCOLO INSTITUCIONAL:", "\n\n**📋 PROTOCOLO INSTITUCIONAL:**")
                        
                        st.markdown('<div class="resultado-box">', unsafe_allow_html=True)
                        st.markdown("### Resultado del Análisis")
                        st.markdown(texto)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.session_state.ultimo_uso = time.time()
                        st.session_state.contador_consultas += 1
                    else:
                        st.warning("⚠️ No se pudo generar respuesta.")
                        
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        st.error("⚠️ Límite de cuota alcanzado. Espere unos minutos.")
                    else:
                        st.error("⚠️ Error al procesar la respuesta.")
        else:
            st.warning("⚠️ Por favor describa el incidente.")
    
    # Info del modelo (compacta)
    st.markdown(f'<div class="model-badge">Modelo: {nombre_modelo.split("/")[-1]} | Consultas: {st.session_state.contador_consultas}</div>', unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Error de configuración del sistema.")
