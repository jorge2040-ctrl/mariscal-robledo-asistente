import streamlit as st
import google.generativeai as genai
import base64
import os

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Asistente de Convivencia - Mariscal Robledo", 
    page_icon="🏫",
    layout="centered"
)

# ==========================================
# 2. FUNCIÓN PARA FONDO INSTITUCIONAL (WATERMARK)
# ==========================================
def set_background(image_file):
    # Verifica si la imagen existe para evitar errores si no se ha subido
    if os.path.exists(image_file):
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        
        # CSS avanzado con efecto Glassmorphism (Cristal)
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }}
        /* Capa semitransparente blanca para asegurar la lectura del texto */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(255, 255, 255, 0.88);
            z-index: -1;
        }}
        
        /* Estilos de las tarjetas (Paneles de cristal) */
        .glass-panel {{
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            margin-bottom: 20px;
        }}
        
        h1, h2, h3, h4 {{
            color: #7B1E38 !important; /* Vinotinto del escudo */
            font-weight: 800;
            text-align: center;
        }}
        
        .stTextArea textarea {{
            border-radius: 10px;
            border: 2px solid #7B1E38;
            background-color: rgba(255, 255, 255, 0.9);
        }}
        
        .stButton>button {{
            background-color: #7B1E38;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            width: 100%;
            padding: 0.7rem;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(123, 30, 56, 0.4);
        }}
        .stButton>button:hover {{
            background-color: #5A1528;
            color: white;
            transform: translateY(-2px);
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Llamamos a la función con el nombre de tu imagen
set_background("escudo.png")

# ==========================================
# 3. INTERFAZ GRÁFICA (UI)
# ==========================================
st.markdown("""
<div class="glass-panel">
    <h1>🏫 Sistema Experto de Convivencia</h1>
    <h4>Institución Educativa Mariscal Robledo</h4>
    <hr style="border-top: 2px solid #7B1E38;">
    <p style="text-align: justify; font-size: 1.1em; color: #333;">
        <strong>💡 Instrucciones:</strong> Describa de forma clara y objetiva el incidente presenciado. El sistema analizará la base legal del Manual de Convivencia vigente y determinará la clasificación, su deber inmediato como docente y el protocolo institucional a seguir.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. LÓGICA DE IA Y BASE DE CONOCIMIENTO ESTRICTA
# ==========================================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Temperatura muy baja (0.1) para que el modelo sea analítico y no invente nada
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

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

    === FORMATO ESTRICTO DE RESPUESTA (Usa Markdown) ===
    **🔴 CLASIFICACIÓN:** [Indica si es Prohibición, Tipo I, Tipo II o Tipo III y copia textualmente el nombre de la falta según el manual].
    
    **👩‍🏫 ACCIÓN INMEDIATA DEL DOCENTE:** [Indica qué debe hacer el docente que presencia la falta según el conducto regular descrito arriba].
    
    **📋 PROTOCOLO INSTITUCIONAL A SEGUIR:** [Enumera los pasos exactos del protocolo correspondiente a la clasificación].
    """

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("#### 📝 Registro del Incidente")
    incidente = st.text_area(
        "", 
        placeholder="Describa los hechos ocurridos con el estudiante (Ej. Fue sorprendido rayando un pupitre o en posesión de un vapeador)...",
        height=120
    )

    if st.button("🔍 Analizar Protocolo Legal"):
        if incidente.strip():
            with st.spinner("⚖️ Consultando el Manual de Convivencia y evaluando el conducto regular..."):
                prompt_completo = f"{prompt_sistema}\n\nIncidente reportado por el docente: {incidente}\n\nRespuesta estructurada:"
                respuesta = model.generate_content(prompt_completo)
                
                st.success("✅ Análisis completado con base en la normativa vigente.")
                st.markdown(respuesta.text)
        else:
            st.warning("⚠️ Por favor, describa el incidente antes de realizar la consulta.")
    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ El error técnico exacto que reporta el sistema es: {e}")
