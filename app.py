import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# 1. CONFIGURACIÓN BÁSICA DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Sistema de Convivencia - Mariscal Robledo", 
    page_icon="https://raw.githubusercontent.com/jorge2040-ctrl/mariscal-robledo-asistente/main/escudo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS PERSONALIZADO
# ==========================================
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
        background: rgba(255, 255, 255, 0.80);
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
    
    /* 2. BANNER VINOTINTO CORREGIDO */
    .header-compact {
        background: linear-gradient(135deg, #7B1E38 0%, #5A1528 100%);
        padding: 1.2rem 1rem 0.4rem 1rem; /* 👈 Le devolvemos el espacio arriba (1.2rem) para que NO se corte el escudo */
        border-radius: 12px;
        margin-bottom: 0.8rem; 
        box-shadow: 0 4px 12px rgba(123, 30, 56, 0.2);
        text-align: center;
    }
    
    .header-logo {
        width: 50px; 
        height: auto;
        margin-top: 0px !important;
        margin-bottom: -10px !important; /* 👈 Este margen negativo "jala" el título hacia el escudo */
        filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.3));
        position: relative;
        z-index: 3;
    }
    
    .header-compact h1 {
        color: #FFFFFF !important;
        font-size: 1.3rem !important; 
        font-weight: 800 !important;
        margin: 0 !important;
        line-height: 1.1;
        position: relative;
        z-index: 2;
    }
    
    .header-compact h2 {
        color: #F8D7DA !important;
        font-size: 0.9rem !important; 
        font-weight: 600 !important;
        margin: 2px 0 4px 0 !important;
        letter-spacing: 0.5px;
    }
    
    .header-author {
        color: #E2E8F0 !important;
        font-size: 0.7rem !important; 
        font-style: italic;
        margin: 0 auto 0 auto !important;
        opacity: 0.9;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 3px;
        width: 40%; 
    }
    
    /* 3. INSTRUCCIONES MÁS DELGADAS */
    .instrucciones {
        background: #F8F9FA;
        border-left: 4px solid #C9A24B;
        padding: 0.5rem 1rem; 
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #2D3748;
        line-height: 1.4;
    }
    
    /* RESTO DE ESTILOS */
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
        padding: 0.6rem 2rem !important;
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
        padding: 1.2rem;
        margin-top: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .resultado-box h3 {
        color: #7B1E38 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.8rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #E2E8F0 !important;
    }
    
    .resultado-box p, .resultado-box ul, .resultado-box ol {
        color: #2D3748 !important;
        line-height: 1.6 !important;
        font-size: 0.9rem !important;
    }
    
    .resultado-box strong { color: #7B1E38 !important; }
    
    .stSuccess, .stWarning, .stError {
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
# 6. CONEXIÓN SEGURA Y DIRECTA A GOOGLE GEMINI
# ==========================================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    generation_config = {"temperature": 0.1}
    
    # Hemos eliminado el ciclo automático que causaba el error 404.
    # Forzamos EXCLUSIVAMENTE el modelo más reciente exigido por Google:
    nombre_modelo = 'gemini-3.6-flash'
    model = genai.GenerativeModel(nombre_modelo, generation_config=generation_config)

    # ==========================================
    # 7. PROMPT DEL SISTEMA (BASE DE DATOS LITERAL OPTIMIZADA)
    # ==========================================
    prompt_sistema = """
    Eres el Asistente Experto Legal y Disciplinario de la Institución Educativa Mariscal Robledo.
    Tu tarea es responder EXCLUSIVAMENTE basándote en el texto proporcionado abajo.

    INSTRUCCIONES DE PROCESAMIENTO:
    Determina si el usuario está reportando un INCIDENTE o haciendo una PREGUNTA GENERAL.

    CASO A - REPORTE DE INCIDENTE:
    Usa ESTRICTAMENTE este formato:
    **🔴 CLASIFICACIÓN:** [Tipo de falta exacto]
    **👨‍🏫 ACCIÓN INMEDIATA:** [Conducto regular]
    **📋 PROTOCOLO INSTITUCIONAL:** [Pasos del protocolo]

    CASO B - PREGUNTA GENERAL (Ej. "¿Qué es el Consejo Directivo?"):
    Sigue estrictamente estos pasos:
    1. Identifica el concepto que pregunta el usuario.
    2. BUSCA detenidamente ese concepto en la sección "DICCIONARIO INSTITUCIONAL" o en las "FALTAS" que están abajo.
    3. Si la respuesta ESTÁ en el texto, extrae la definición y explícala de manera clara, amable y usando viñetas.
    4. SOLO si el concepto NO aparece en ninguna parte del texto de abajo, responde literalmente: "Esa información no se encuentra en el fragmento del manual que tengo disponible."

    === DICCIONARIO INSTITUCIONAL Y DEFINICIONES CLAVE ===
    ROLES:
    - RECTOR: Directivo docente que tiene la responsabilidad de dirigir, liderar y gestionar pedagógica y administrativamente el funcionamiento de un establecimiento educativo.
    - COORDINADOR: Lidera, participa y gestiona el trabajo de los docentes, bajo las orientaciones del rector y junto con éste, en los procesos académicos, pedagógicos y convivenciales.
    - DOCENTES: Personas que desarrollan labores académicas directa y personalmente con los alumnos en su proceso enseñanza aprendizaje.
    - DOCENTE ORIENTADOR: Responsable de definir planes o proyectos pedagógicos tendientes a contribuir a la resolución de conflictos, garantizar el respeto de los derechos humanos y brindar apoyo.
    - ESTUDIANTES: Son el centro del proceso educativo, deben participar activamente en su propia formación integral.
    - FAMILIAS: Núcleo estructural y célula de la sociedad, de vital importancia en la función de formación integral de los hijos.

    ÓRGANOS Y COMITÉS:
    - CONSEJO DIRECTIVO: Máxima autoridad e instancia directiva de participación de la comunidad educativa y de orientación académica y administrativa del establecimiento.
    - CONSEJO ACADÉMICO: Instancia superior para participar en la orientación pedagógica del establecimiento.
    - CONSEJO ESTUDIANTIL: Máximo órgano colegiado que asegura y garantiza el continuo ejercicio de la participación por parte de los educandos.
    - PERSONERO ESTUDIANTIL: Estudiante elegido del último grado que ofrece la institución, para promover el ejercicio de los derechos y deberes de los estudiantes.
    - CONTRALOR ESTUDIANTIL: Figura encargada de promover y actuar como veedora del buen uso de los recursos y de los bienes públicos de la institución educativa.
    - COMITÉ DE CONVIVENCIA ESCOLAR: Instancia encargada de apoyar la labor de promoción, prevención y seguimiento a la convivencia escolar, a la educación para el ejercicio de los derechos humanos, sexuales y reproductivos.
    - CONSEJO DE PADRES DE FAMILIA: Órgano de participación de los padres de familia destinado a asegurar su continua participación en el proceso educativo.

    CONCEPTOS DE CONVIVENCIA Y PROCESOS:
    - CONFLICTOS: Situaciones que se caracterizan porque hay una incompatibilidad real o percibida entre una o varias personas frente a sus intereses.
    - CONFLICTOS MANEJADOS INADECUADAMENTE: Situaciones donde los conflictos no son resueltos de manera constructiva y afectan la convivencia (sin afectación a la salud).
    - AGRESIÓN ESCOLAR: Toda acción realizada por uno o varios integrantes que busca afectar negativamente a otros (física, verbal, gestual, relacional o electrónica).
    - ACOSO ESCOLAR (BULLYING): Conducta negativa, intencional metódica y sistemática de agresión, intimidación o humillación que se presenta de forma reiterada.
    - CIBERACOSO (CIBERBULLYING): Intimidación con uso deliberado de tecnologías de información para ejercer maltrato psicológico y continuado.
    - DEBIDO PROCESO: Procedimiento legal que garantiza a las personas los derechos y condiciones para asegurar que puedan defenderse cuando sean acusadas por alguna falta.
    - MEDIDAS PEDAGÓGICAS: Acciones educativas que buscan hacer que la persona reflexione. No son sanciones, sino acciones preventivas y orientadoras (Ej. Extrañamiento temporal, Matrícula condicional).
    - CONDUCTO REGULAR: Escala jerárquica para solucionar problemáticas: 1. Docente, 2. Director de Grupo, 3. Docente orientador, 4. Rector.
    - RUTA DE ATENCIÓN INTEGRAL: Herramienta de apoyo dividida en componentes de Promoción, Prevención, Atención y Seguimiento.
    - SIUCE: Sistema de Información Unificado de Convivencia Escolar. Apoya la identificación, consulta, registro y seguimiento de casos de acoso, violencia escolar, consumo de Sustancias Psicoactivas y embarazo.
    - P.Q.R.S.F: Peticiones (solicitudes), Quejas (expresiones de malestar), Reclamos (exige solución por incumplimiento), Sugerencias (propuestas de mejoramiento), Felicitaciones (reconocimiento a la labor).

    === CLASIFICACIÓN DE FALTAS Y PROTOCOLOS (LITERALES) ===
    
    🔴 1. DE LAS PROHIBICIONES DISCIPLINARIAS
    PUNTUALIDAD:
    - Dejar de asistir a las clases, actos comunitarios o eventos programados por la Institución sin presentar excusa válida o sin la debida autorización de los acudientes o de la Institución. 
    - Llegar tarde al salón al inicio y durante la jornada escolar (retardos). 
    - Mentir para justificar su inasistencia a la Institución.
    COMPORTAMIENTO:
    - Permanecer en lugares no permitidos o en el salón en horas de descanso o durante el desarrollo de las clases.
    - Uso inadecuado de los diferentes espacios: templo, restaurante escolar, laboratorios, oficinas, actos culturales y deportivos, aulas, auditorios, baños, canchas, otras dependencias de la Institución Educativa o durante salidas institucionales. 
    - Interrumpir las clases o actividades, por estar manipulando juguetes, aparatos o artefactos que no se pueden utilizar durante la jornada escolar (audífonos, bafles, celulares, diademas sonoras).
    - Salirse de clase sin previa autorización.
    - Presentar un comportamiento indebido durante las salidas pedagógicas deteriorando el buen nombre de la Institución. 
    - Interrumpir el trabajo propio o el de las demás personas con charlas frecuentes, risas, burlas, juegos, gestos, silbidos, remedos. 
    - Se prohíbe el ingreso de mascotas u otros animales a la Institución, a menos de que este sea requerido para una actividad o sea un animal de asistencia.
    - Negarse a contribuir con el aseo y la buena presentación de las aulas y demás dependencias de la institución.
    - Consumir bebidas y alimentos, chicles u otros relacionados, durante las clases, en los espacios pedagógicos o actos comunitarios donde no está permitido. 
    - Rayar o marcar sillas, paredes, pasamanos, pisos, prendas del uniforme.
    - Incumplir con la realización de actividades propuestas durante las clases en actividades deportivas, pedagógicas y culturales.
    - Copiar tareas de otros compañeros.
    - Botar basura en lugares inadecuados dentro y fuera de la institución o incumplir con los turnos de aseo asignados en el aula.
    - El uso no autorizado del teléfono celular, reproductor de música y otros aparatos electrónicos en horas de clase y en actos de comunidad.
    - Entrar sin autorización a Rectoría, sala de docentes, oficina de orientación escolar y demás dependencias administrativas de la institución y salones diferentes al suyo. 
    - Salir al baño, tienda, solicitar fotocopias en horas de clase sin el debido permiso y justificación por parte del maestro.
    - Realizar compras o recibir elementos de cualquier tipo, o atender a personas a través de las ventanas o puertas de acceso sin autorización.
    - Ausentarse del aula de clase sin previa autorización.
    - Ingresar o salir de la institución por lugares diferentes a los autorizados (saltar rejas, muros u otros métodos).
    - Falta de cuidado y limpieza de la institución.
    - Uso inadecuado del tablero y de la infraestructura educativa.
    - Desorden al momento de cambio de clase y/o en el desplazamiento a otras aulas o dependencias de la Institución Educativa.
    - Perder tiempo y hacerlo perder a sus compañeros con risas, charlas, juegos, ruidos, o cambios de puesto, entorpeciendo el normal desarrollo de las clases.
    - Comportamientos inadecuados en el restaurante escolar y otras dependencias de la institución educativa.
    - Emitir gritos, risas, silbidos u otro tipo de ruido que interrumpa el normal desarrollo de las clases u otros eventos que se estén desarrollando en la institución.
    - Faltar con los implementos o materiales para las clases. 
    - Actos que atenten contra las normas de derechos de autor. 
    - Portar llaves de la Institución sin la debida autorización.
    - No informar a los padres o acudientes de las citaciones a la institución educativa.
    - Desacatar las orientaciones y/o acciones pedagógicas recibidas en la institución.
    - Levantar la voz imponiendo ideas a la fuerza.
    - Incumplir con las normas de cultura, civismo y urbanidad.
    - Hacer proselitismo político o religioso dentro de la institución.
    - Incumplimiento con actividades y responsabilidades con las que previamente se comprometió con directivos, docentes y demás compañeros. 
    - Utilizar sin permiso o esconder útiles escolares, prendas de vestir o alimentos de sus compañeros o compañeras.
    - Uso de balones en sitios diferentes a las canchas.
    - Permanencia en establecimientos públicos (cantinas, bares, y similares) cuando se porte el uniforme de la institución.
    - PROTOCOLO: 1. Seguir conducto regular. 2. Aplicar medidas formativas. 3. (Específico para retardos): Si acumula 3 o más llegadas tarde en el período, realizará actividades de limpieza por una hora, finalizada la jornada.

    🔴 2. SITUACIONES TIPO I (Conflictos manejados inadecuadamente sin daños a la salud)
    Serán consideradas situaciones TIPO I las siguientes:
    - Arrojar piedras u otros objetos a las personas, animales y plantas o a las instalaciones de la institución o los sectores aledaños siempre y cuando no les cause daño a otras personas. 
    - Utilizar en forma inadecuada los baños, recursos didácticos, mobiliarios, equipos de cómputo, implementos deportivos, musicales y demás recursos institucionales.
    - Tener llamados de atención constante, por parte del docente en los actos comunitarios, interrupciones indebidas en clase o en los actos generales de la comunidad escolar. 
    - Celebrar inadecuadamente cualquier evento, arrojando huevos, harina o bromas que atenten contra el aseo y seguridad de los compañeros y de la institución.
    - El daño a los bienes e inmuebles de la institución o elementos fijados para la comunicación institucional (avisos, carteles, tableros, entre otros).
    - El daño a los bienes de los compañeros o el uso no autorizado de los elementos o utensilios escolares de los otros compañeros. Todo acto de irrespeto por la propiedad ajena.
    - Actos de cariño como besos, abrazos o sentarse en las piernas de la pareja, dentro del aula de clase. 
    - Recolectar dineros, vender, hacer rifas u otras actividades que impliquen ganancias, sin autorización de padres de familia y de la Institución. 
    - Utilizar vocabulario vulgar e irrespetuoso para los compañeros, docentes y directivos o cualquier miembro de la comunidad, con la intención de humillar o hacer daño. 
    - Presentar situaciones excluyentes o discriminatorias por razones de género u orientación sexual.
    - Estimular o generar comentarios o rumores que tengan la intención de dañar la imagen y el buen nombre del otro. 
    - Hacer sentir mal a los demás por medio de insultos, apodos ofensivos, chanzas, burlas, amenazas de agresión y expresiones morbosas.
    - Los desórdenes de diferente clase (saboteo) que causen perturbación en las actividades curriculares, deportivas y culturales o que cree malestar dentro de la comunidad educativa. 
    - Burlas y/o comentarios por características físicas, mentales, orientación sexual, identidad de género, raza o credo de otras personas que hacen parte de la comunidad educativa.
    - Enfrentamientos agresivos verbales presentados esporádicamente. 
    - Incitación a enfrentamientos verbales y/o físicos dentro o fuera de la institución o a cometer faltas.
    - Manifestación de irrespeto por el otro y por lo otro, que se evidencian arrojando útiles, textos, carteles, mensajes grabados en paredes, puertas, escritorios y demás partes, cuyo contenido atenta contra las más elementales normas de respeto, honestidad, orden y moral, o correspondan a la vida íntima de las personas.
    - Desórdenes en la calle portando el uniforme o que afecte el buen nombre de la Institución (incitando actos violentos, acciones que alteren el orden público disturbios, entre otros).
    - Estigmatización del otro a través de la utilización de sobrenombres en forma de broma o charla de manera esporádica o expresarse de manera obscena e irrespetuosa en contra de la dignidad y respeto que se debe tener por las personas dentro y fuera de la Institución.
    - Participación en actividades como la hechicería, superstición, magia, agorería, quiromancia, actos esotéricos y otras relacionadas, dentro de la Institución Educativa o en otros espacios que involucren a la comunidad educativa y que puedan afectar la sana convivencia. 
    - Generación de falsas alarmas que creen situaciones de pánico individual y colectivo, tales como: estallar fulminantes, provocar quemas de basura dentro o fuera del aula, utilizar polvos o sustancias que ocasionen alteraciones orgánicas, emocionales o comportamentales.
    - Ingreso a cualquier tipo de vivienda o negocio en tiempo escolar y sin la autorización de directivos y/o docentes.
    - Desordenes de cualquier índole que afecten la adecuada prestación del servicio de transporte y restaurante escolar.
    - Relaciones que exceden la confianza entre estudiante y docente (manifestaciones extralimitadas y fuera de lugar que impliquen besos, tocamientos u otros comportamientos inadecuados).
    - PROTOCOLO TIPO I: 1. Reunir inmediatamente a las partes involucradas en el conflicto y mediar de manera pedagógica. 2. Escuchar descargos por escrito. 3. Fijar forma de solución imparcial (reparar daños, restablecer derechos, reconciliación). 4. Dejar constancia por escrito en el observador. 5. Realizar seguimiento del caso.

    🔴 3. SITUACIONES TIPO II (Agresión escolar, bullying, ciberacoso y daños sin incapacidad)
    Serán consideradas situaciones TIPO II las siguientes:
    - Reincidir en cualquier situación tipo I después de haber adquirido un compromiso.
    - Agresión escolar, acoso escolar (bullying) y ciberacoso (ciberbullying) que no revisten las características de la comisión de un delito.
    - Bullying por orientación sexual e identidad de género.
    - Situaciones de violencia basada en el género o cualquier otra característica que limita el desarrollo de la libre personalidad. 
    - Agresiones físicas (que no generan daños al cuerpo) presentados de manera esporádica. 
    - Peleas, violencia física y/o causar lesiones personales, daños al cuerpo o a la salud, sin generar incapacidad alguna para cualquiera de las personas involucradas.
    - Atropellar, empujar o estrujar otros y otras estudiantes intencionalmente.  
    - Los juegos bruscos o violentos que causen lesiones personales.
    - Uso de elementos que puedan ser peligrosos u objetos que puedan convertirse en armas para afectar a los otros. 
    - Realización de tatuajes y/o perforaciones a los demás o así mismos dentro de la Institución.  
    - Participación e incitación en trifulcas (escándalos, bullas y algarabías) dentro o fuera del establecimiento educativo o inducir premeditadamente a miembros de la comunidad a cometer faltas, afectando la imagen de la Institución.
    - Realización de mensajes sexuales ofensivos escritos en espacios públicos como baños, paredes, tablero y pupitres que pueden ser considerados como acoso escolar.
    - Actuación en complicidad con otras personas para ocultar hechos o mentir y evitar la sanción personal o de un tercero.
    - Porte, consumo y/o inducir a otros al consumo de energizantes o medicamentos sin prescripción médica.
    - Salida del establecimiento educativo sin autorización durante la jornada escolar, alternado el orden y el desarrollo de la clase. Comprendiendo que una fuga pone en riesgo su integridad.  
    - Consumo de estupefacientes o sustancias psicoactivas (entendiéndose como diversos compuestos naturales o sintéticos, que actúan sobre el sistema nervioso generando alteraciones en las funciones que regulan pensamientos, emociones y el comportamiento) y de cualquier clase (naturales, sintéticas, semisintéticas, depresoras, estimulantes, mixtas, alucinógenos, opiáceos, psicodepresores, alcohol, cualquier tipo de licor, psicoestimulantes mayores, cannabis y sus derivados, sustancias volátiles, psicoestimulantes menores), al interior de la institución educativa o a sus alrededores. 
    - Presentarse a la Institución o a las actividades extraescolares en estado de embriaguez o bajo el efecto de sustancias psicoactivas.
    - PROTOCOLO TIPO II: 1. Informar inmediatamente a acudientes de los involucrados (constancia escrita). 2. Garantizar atención en salud física/mental si hay daño. 3. Remitir a autoridades administrativas (Comisaría/ICBF) si requiere restablecimiento de derechos. 4. Proteger a los involucrados. 5. Remitir al Comité de Convivencia para acciones restaurativas (Matrícula Condicional o Extrañamiento temporal). 6. Reportar obligatoriamente en SIUCE.

    🔴 4. SITUACIONES TIPO III (Presuntos delitos)
    Serán consideradas situaciones TIPO III las siguientes:
    - Reincidencia en situaciones tipo II.
    - Homicidio.
    - Hurto y/o robo comprobado en cualquiera de las formas, incluyendo el intento de hacerlo.
    - Acoso Sexual.
    - Violación.
    - Extorsión.
    - Relaciones sexo-genitales dentro de la institución. (La Institución reconoce los derechos sexuales y reproductivos de las personas, sin embargo, se prohíbe masturbarse en público, exponer sus genitales o los de sus compañeros dentro de la Institución).
    - Corrupción de menores, incitación al delito e instrumentalización. 
    - Porte y/o utilización de cualquier tipo de explosivo dentro de la Institución.
    - Conformar o pertenecer a organizaciones o grupos delictivos que directamente, o a través de terceros, atenten contra personas dentro o fuera de la institución.
    - Expendio y/o distribución de estupefacientes o sustancias de cualquier clase (naturales, sintéticas, semisintéticas, depresoras, estimulantes, mixtas, alucinógenos, opiáceos, psicodepresores, alcohol, cualquier tipo de licor, psicoestimulantes mayores, cannabis y sus derivados, sustancias volátiles, psicoestimulantes menores), al interior o alrededores de la institución educativa.
    - Porte de diferentes elementos electrónicos o de cualquier otro dispositivo o material para el consumo de sustancias psicoactivas, por ejemplo, vapeadores y sus diversas formas de presentación, candelas, pipas, gotas, parches, tabaco, cigarrillo, entre otros relacionados. 
    - Inducir al consumo o a la venta de sustancias psicoactivas a algún integrante de la Institución, así como al porte de elementos electrónicos o cualquier otro dispositivo o material relacionado para el consumo de dichas sustancias, sobre todo si son menores de 14 años. 
    - Comprar sustancias psicoactivas dentro de la Institución o a sus alrededores. 
    - Amenaza de muerte.
    - Atentado contra el derecho a la vida, a la integridad personal o a la dignidad humana de cualquiera de los miembros de la Institución y la comunidad en general. 
    - Apoyo en terceros o ajenos para la solución de su conflicto, sin tener en cuenta el conducto regular, generando intimidación o amenazas a cualquier miembro de la institución educativa y comunidad en general.
    - Acoso estudiantil que revista las características de un delito. 
    - Complicidad para que una persona toque el cuerpo de otra persona con fines sexuales.
    - Exhibición de su cuerpo y/o su vida sexual a través de diferentes medios. 
    - Comisión de delitos informáticos. 
    - Agresión física afectando considerablemente la salud de otras personas.
    - Porte y utilización de pólvora, detonantes, sustancias químicas y otros elementos que atenten contra la integridad física de las personas, infraestructura o cosas.
    - Secuestro, sicariato y terrorismo.
    - Conformación y/o participación en pandillas o bandas dentro o fuera de la Institución con fines delictivos o para crear un mal ambiente escolar.
    - Maltrato animal.
    - Participación en protestas violentas.  
    - Grabación de integrantes de la comunidad educativa sin fines pedagógicos programados por la Institución y sin previa autorización. 
    - Enlace o participación en actividades dedicadas a la explotación sexual.
    - Utilización de elementos que puedan ser peligrosos u objetos que puedan convertirse en armas para afectar a los otros o para afectarse así mismo. 
    - Utilización de armas de fuego, cortopunzantes, contundentes, cortocontundentes, traumáticas o utilización de los materiales de estudio como un arma. 
    - Utilizar implementos que atenten contra la integridad de algún miembro de la comunidad: navajas, bisturí, armas de fuego y corto punzantes, armas contundentes, de fogueo y traumáticas, tijeras puntiagudas, cuchillas, candelas.
    - Realización de agresiones reiterativas con contenido sexual, como el ciberacoso, la agresión sexual por homofobia, lesbofobia, bifobia, transfobia, inequidad de género o de identidad de género.
    - Comisión de un delito tipificado como violación a la Ley 599 del 2000 (Código Penal), Ley 30 de 1986 Estatuto Nacional de Estupefacientes), Ley 1098 de 2006 (Código de Infancia y Adolescencia), Ley 1801 de 2016 (Código Nacional de Policía y Convivencia) y demás normas, leyes y decretos reglamentarios.
    - Promover actividades dirigidas a la consecución de dinero para eventos que comprometan el buen nombre de la Institución y sin su autorización.
    - Utilizar software ilegal en los computadores del colegio. 
    - Falsificar firmas. 
    - Comisión de fraude académico (copia en exámenes, plagio de trabajos, alteración de notas, etc.) en beneficio propio o de terceros.
    - Adulteración de planillas, informes académicos, libros, actas, etc., o cualquier otra.
    - Intento de soborno a cualquier miembro de la comunidad educativa.
    - Utilización del nombre de la institución para efectos personales, de cualquier índole, sin autorización.
    - Suplantación en cualquiera de sus modalidades (presentación de trabajos, redes sociales, envío de mensajes, entre otras).
    - Incriminación, apabullamiento y/o levantar calumnia hacia otra persona de la comunidad educativa. 
    - Falsificación de la información proveniente de las instituciones y que atente contra el buen nombre de éstas. 
    - Alteración y/o destrucción de los libros de asistencia, informes, certificados de estudio, evaluaciones… (libros reglamentarios).
    - Producción, distribución, posesión de pornografía infantil. 
    - Incitar a terceros menores de edad, al consumo o distribución de material pornográfico (Código Penal Colombiano – Art. 218-219).
    - Exhibición forzada de material pornográfico o difusión sin su consentimiento.
    - Actos de calumnia con el fin de dañar el buen nombre de la Institución o de cualquier miembro de la comunidad educativa.
    - PROTOCOLO TIPO III: 1. Informar inmediatamente a los acudientes (constancia escrita). 2. Garantizar atención en salud si hay daño físico/mental. 3. El presidente del Comité informará INMEDIATAMENTE a la Policía Nacional. 4. Citar al Comité de Convivencia Escolar para iniciar Proceso Reeducativo. 5. Reportar en SIUCE. 6. Sugerir Cambio de Institución por parte del Consejo Directivo (si aplica).
    """

    # ==========================================
    # 8. FORMULARIO
    # ==========================================
    st.markdown("#### 📝 Registro de Incidente o Consulta")
    incidente = st.text_area(
        "",
        height=80,  # 👈 Aquí reducimos la altura. Antes estaba en 120.
        placeholder="Ejemplo 1 (Incidente): Estudiante llegó 20 minutos tarde.\nEjemplo 2 (Pregunta): ¿Qué es el Consejo Directivo?",
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
                        st.success("✅ Análisis completo")
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
        f'<div class="model-badge">Consultas realizadas: {st.session_state.contador_consultas}</div>',
        unsafe_allow_html=True
    )

except Exception as e:
    st.error("⚠️ Error de configuración del sistema.")
    st.caption(f"Detalle: {e}")
