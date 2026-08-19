import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN BÁSICA DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Asistente de Convivencia - Mariscal Robledo", 
    page_icon="🏫",
    layout="centered"
)

st.markdown("""
    <style>
    h1, h2, h3, h4 { color: #7B1E38 !important; font-weight: bold; }
    .stButton>button {
        background-color: #7B1E38;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #5A1528;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏫 Sistema Experto de Convivencia</h1>", unsafe_allow_html=True)
st.markdown("### Institución Educativa Mariscal Robledo")
st.markdown("---")
st.info("💡 **Instrucciones:** Describa de forma clara el incidente presenciado. El sistema analizará la base legal del Manual de Convivencia vigente.")

# ==========================================
# 2. CONEXIÓN A GOOGLE GEMINI Y LÓGICA
# ==========================================
try:
    # Captura la llave de la pestaña Secrets de Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    generation_config = {"temperature": 0.1}
    
    # ✅ PRIORIZAR MODELOS RÁPIDOS (flash/pro primero, evitar gemma pesado)
    modelos_preferidos = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest', 
        'models/gemini-1.5-pro',
        'models/gemini-2.0-flash-exp',
        'models/gemini-pro'
    ]
    
    modelo_encontrado = None
    nombre_modelo = None
    
    # Primero intentar con modelos preferidos
    for nombre in modelos_preferidos:
        try:
            modelo_test = genai.GenerativeModel(nombre, generation_config=generation_config)
            test = modelo_test.generate_content("Test")
            if test:
                modelo_encontrado = modelo_test
                nombre_modelo = nombre
                break
        except:
            continue
    
    # Si no funcionó ninguno preferido, buscar cualquiera disponible (excepto gemma)
    if modelo_encontrado is None:
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                # Evitar modelos gemma (son lentos)
                if 'gemma' in model_info.name.lower():
                    continue
                nombre_modelo = model_info.name
                try:
                    modelo_encontrado = genai.GenerativeModel(nombre_modelo, generation_config=generation_config)
                    test = modelo_encontrado.generate_content("Hola")
                    if test:
                        break
                except:
                    continue
    
    if modelo_encontrado is None:
        st.error("❌ No se encontró ningún modelo compatible. Verifica tu API Key de Google Gemini.")
        st.stop()
    
    model = modelo_encontrado
    st.caption(f"🤖 Modelo activo: {nombre_modelo}")

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

    === FORMATO ESTRICTO DE RESPUESTA (NO uses XML, solo texto plano con markdown) ===
    
    CLASIFICACION: [Indica si es Prohibición, Tipo I, Tipo II o Tipo III y copia textualmente el nombre de la falta según el manual]
    
    ACCION INMEDIATA DEL DOCENTE: [Indica qué debe hacer el docente que presencia la falta según el conducto regular descrito arriba]
    
    PROTOCOLO INSTITUCIONAL A SEGUIR: [Enumera los pasos exactos del protocolo correspondiente a la clasificación]
    """

    st.markdown("#### 📝 Registro del Incidente")
    incidente = st.text_area("Describa los hechos ocurridos con el estudiante:", height=100)

    if st.button("🔍 Analizar Protocolo Legal"):
        if incidente.strip():
            with st.spinner("⚖️ Consultando el Manual de Convivencia..."):
                prompt_completo = f"{prompt_sistema}\n\nIncidente reportado por el docente: {incidente}\n\nRespuesta:"
                
                try:
                    respuesta = model.generate_content(prompt_completo)
                    
                    if respuesta and respuesta.text:
                        st.success("✅ Análisis completado con base en la normativa vigente.")
                        
                        # Extraer solo el texto, sin markup XML
                        texto_respuesta = respuesta.text.strip()
                        
                        # Formatear la respuesta con emojis
                        texto_formateado = texto_respuesta.replace("CLASIFICACION:", "🔴 **CLASIFICACIÓN:**")
                        texto_formateado = texto_formateado.replace("ACCION INMEDIATA DEL DOCENTE:", "\n\n👩‍🏫 **ACCIÓN INMEDIATA DEL DOCENTE:**")
                        texto_formateado = texto_formateado.replace("PROTOCOLO INSTITUCIONAL A SEGUIR:", "\n\n📋 **PROTOCOLO INSTITUCIONAL A SEGUIR:**")
                        
                        st.markdown(texto_formateado)
                    else:
                        st.warning("⚠️ No se pudo generar una respuesta. Intente reformular el incidente.")
                        
                except Exception as e:
                    st.error("⚠️ Error al procesar la respuesta. Intente nuevamente.")
                    st.caption(f"Detalle: {str(e)[:200]}")
        else:
            st.warning("⚠️ Por favor, describa el incidente antes de realizar la consulta.")

except Exception as e:
    st.error(f"⚠️ Error de configuración del sistema.")
    st.caption(f"Detalle técnico: {e}")
