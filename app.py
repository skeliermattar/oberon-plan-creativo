"""Interfaz web de ÓBERON PLAN CREATIVO.
Ejecutar desde la carpeta del proyecto: python3 -m streamlit run app.py
"""
import base64
from pathlib import Path

import streamlit as st

from calculos import DatosInvalidos, calcular_plan, exportar_csv, formato

st.set_page_config(page_title="Óberon · Plan Creativo", page_icon="📐", layout="wide")
ROOT = Path(__file__).parent

# Montserrat se distribuye con el proyecto: no depende de Google Fonts.
@st.cache_data
def estilos():
    regular = base64.b64encode((ROOT / "assets/Montserrat-Regular.ttf").read_bytes()).decode()
    bold = base64.b64encode((ROOT / "assets/Montserrat-Bold.ttf").read_bytes()).decode()
    css = (ROOT / "assets/estilos.css").read_text(encoding="utf-8")
    return css.replace("FUENTE_REGULAR", regular).replace("FUENTE_BOLD", bold)

st.markdown("<style>" + estilos() + "</style>", unsafe_allow_html=True)
st.markdown(
    '<div class="brand"><div><b>ÓBERON</b> TSI'
    '<span class="brand-product">PLAN CREATIVO</span></div>'
    '<span class="author">Proyecto de Skarlet Mattar</span></div>',
    unsafe_allow_html=True,
)

TIPOS = ["Pieza estática", "Carrusel", "Video corto", "Presentación",
         "Infografía", "Banner", "Otro"]
TIEMPOS = [1.0, 2.0, 4.0, 3.0, 2.0, 1.0, 1.0]


def cambiar():
    """Oculta resultados anteriores al editar una entrada."""
    st.session_state.modificado = True
    st.session_state.error = None


def agregar():
    identificador = st.session_state.siguiente
    st.session_state.ids.append(identificador)
    st.session_state.siguiente += 1
    cambiar()


def eliminar(identificador):
    st.session_state.ids.remove(identificador)
    for prefijo in ("tipo", "cantidad", "horas", "otro"):
        st.session_state.pop(f"{prefijo}_{identificador}", None)
    cambiar()


def cambiar_tipo(identificador):
    # La referencia cambia con el tipo; siempre puede ajustarse manualmente.
    tipo = st.session_state[f"tipo_{identificador}"]
    st.session_state[f"horas_{identificador}"] = TIEMPOS[TIPOS.index(tipo)]
    cambiar()


def cargar_ejemplo():
    for clave in list(st.session_state):
        if clave.startswith(("tipo_", "cantidad_", "horas_", "otro_")):
            del st.session_state[clave]
    st.session_state.ids = [0, 1, 2]
    st.session_state.siguiente = 3
    st.session_state.campana = "Campaña de servicios · Noviembre"
    st.session_state.revisiones = 20
    st.session_state.personas = 1
    st.session_state.horas_dia = 4.0
    st.session_state.plazo = 5
    for i, (tipo, cantidad, horas) in enumerate([
        ("Pieza estática", 8, 1.0), ("Carrusel", 3, 2.0), ("Video corto", 2, 4.0)
    ]):
        st.session_state[f"tipo_{i}"] = tipo
        st.session_state[f"cantidad_{i}"] = cantidad
        st.session_state[f"horas_{i}"] = horas
    st.session_state.plan = None
    cambiar()


if "ids" not in st.session_state:
    st.session_state.ids = [0]
    st.session_state.siguiente = 1
    st.session_state.plan = None
    st.session_state.modificado = False
    st.session_state.error = None

seccion = st.radio("Navegación", ["Nueva planificación", "Cómo funciona"],
                   horizontal=True, label_visibility="collapsed")

if seccion == "Cómo funciona":
    st.title("De las piezas a un plan viable.")
    st.write("Define lo que vas a producir y comprueba si alcanza el tiempo de tu equipo.")
    for titulo, texto in [
        ("1. Describe la campaña", "Escribe un nombre que permita reconocer el trabajo."),
        ("2. Agrega las piezas", "Indica cantidades y horas por pieza. Los tiempos sugeridos son ejemplos editables, no mediciones oficiales de Óberon TSI."),
        ("3. Reserva tiempo para revisiones", "El porcentaje se aplica a la suma de horas de producción."),
        ("4. Define la capacidad", "Indica personas, horas disponibles por persona al día y plazo en días hábiles."),
        ("5. Calcula y ajusta", "Revisa las horas faltantes o disponibles. Después de editar, pulsa Calcular nuevamente."),
        ("6. Conserva el resumen", "Descarga el CSV con los datos y resultados del cálculo vigente.")
    ]:
        with st.container(border=True):
            st.subheader(titulo)
            st.write(texto)
    with st.expander("Fórmulas y límites del cálculo", expanded=True):
        st.write("**Horas base:** suma de cantidad × horas por pieza.")
        st.write("**Horas requeridas:** horas base × (1 + porcentaje de revisiones / 100).")
        st.write("**Capacidad:** personas × horas al día × plazo.")
        st.write("**Ocupación:** horas requeridas / capacidad × 100.")
        st.write("**Días necesarios:** horas requeridas / capacidad diaria, redondeado hacia arriba.")
        st.info("La estimación supone disponibilidad constante y trabajo distribuible entre personas. "
                "No programa tareas individuales ni considera festivos, esperas o dependencias.")
    st.stop()

with st.container(key="hero"):
    cabecera, ejemplo = st.columns([3, 1], vertical_alignment="center")
    with cabecera:
        st.markdown('<div class="eyebrow">TU ESPACIO DE PLANIFICACIÓN</div>'
                    '<h1>De la idea a un plan viable.</h1>'
                    '<p class="intro">Define las piezas, organiza tu equipo y comprueba si llegas a tiempo.</p>',
                    unsafe_allow_html=True)
    with ejemplo:
        st.button("Cargar ejemplo de campaña", on_click=cargar_ejemplo,
                  use_container_width=True,
                  help="Reemplaza los datos actuales por el ejemplo de 13 piezas.")
    
with st.container(key="layout"):
    izquierda, derecha = st.columns([1.5, 1], gap="medium")

with izquierda:
    st.text_input("Nombre de la campaña", key="campana", max_chars=100,
                  placeholder="Ej.: Lanzamiento de servicios", on_change=cambiar)
    with st.container(border=True, key="produccion"):
        st.subheader("1. ¿Qué necesitas producir?")
        st.caption("Ajusta los tiempos de referencia según tu proceso creativo.")
        piezas = []
        for i in st.session_state.ids:
            with st.container(key=f"pieza_{i}"):
                columnas = st.columns([2.1, 1, 1.35, .75, .45])
                with columnas[0]:
                    tipo = st.selectbox("Tipo de pieza", TIPOS, key=f"tipo_{i}",
                                        on_change=cambiar_tipo, args=(i,))
                with columnas[1]:
                    cantidad = st.number_input("Cantidad", 1, 1000, key=f"cantidad_{i}",
                                               on_change=cambiar)
                with columnas[2]:
                    horas = st.number_input("Horas/pieza", .25, 200.0,
                                            value=TIEMPOS[TIPOS.index(tipo)], step=.25,
                                            key=f"horas_{i}", on_change=cambiar)
                with columnas[3]:
                    st.markdown(f'<div class="table-label">Total</div><div class="row-total">{formato(cantidad * horas)} h</div>', unsafe_allow_html=True)
                with columnas[4]:
                    st.markdown('<div class="table-label">Quitar</div>', unsafe_allow_html=True)
                    st.button("×", key=f"quitar_{i}", help=f"Eliminar pieza {i + 1}",
                              disabled=len(st.session_state.ids) == 1,
                              on_click=eliminar, args=(i,))
            if tipo == "Otro":
                tipo = st.text_input("Nombre del tipo de pieza", key=f"otro_{i}",
                                     max_chars=80, on_change=cambiar)
            piezas.append({"tipo": tipo, "cantidad": cantidad, "horas": horas})
        st.button("＋ Añadir pieza", on_click=agregar, disabled=len(piezas) >= 30)
        revisiones = st.number_input("Tiempo adicional para revisiones (%)", 0, 100,
                                     value=20, key="revisiones", on_change=cambiar,
                                     help="Se aplica sobre las horas base de todas las piezas.")
    with st.container(border=True, key="equipo"):
        st.subheader("2. ¿Con qué capacidad cuentas?")
        a, b, d = st.columns(3)
        with a:
            personas = st.number_input("Personas", 1, 100, key="personas", on_change=cambiar)
        with b:
            horas_dia = st.number_input("Horas al día por persona", .25, 12.0, value=4.0,
                                        step=.25, key="horas_dia", on_change=cambiar)
        with d:
            plazo = st.number_input("Plazo en días hábiles", 1, 365, value=5,
                                    key="plazo", on_change=cambiar)
        st.caption("Cuenta únicamente las horas dedicadas a esta campaña.")
    with st.container(key="accion"):
        if st.button("Calcular planificación", type="primary", use_container_width=True):
            try:
                st.session_state.plan = calcular_plan(
                    st.session_state.campana, piezas, revisiones, personas, horas_dia, plazo)
                st.session_state.modificado = False
                st.session_state.error = None
            except DatosInvalidos as error:
                st.session_state.error = str(error)
                st.session_state.modificado = True
    if st.session_state.error:
        st.error(st.session_state.error)

with derecha:
    with st.container(border=True, key="resultado"):
        st.subheader("Resultado de la planificación")
        plan = st.session_state.plan
        if plan is None:
            st.markdown('<div class="empty"><span>◎</span><h3>¿Tu equipo llega a tiempo?</h3>'
                        '<p>Completa los datos y pulsa <b>Calcular planificación</b>.</p>'
                        '<div class="empty-chips">Horas de trabajo · Capacidad · Plazo</div></div>',
                        unsafe_allow_html=True)
        elif st.session_state.modificado:
            st.warning("Cambiaste los datos. Pulsa Calcular planificación para actualizar el resultado.")
            st.caption("La descarga se habilitará cuando recalcules.")
        else:
            st.caption(plan["campana"])
            if plan["diferencia"] < 0:
                st.warning("⚠ Requiere ajuste")
            elif plan["diferencia"] == 0:
                st.info("Capacidad justa · No queda margen adicional")
            else:
                st.success("✓ Capacidad suficiente")
            a, b = st.columns(2)
            a.metric("Trabajo estimado", f'{formato(plan["requeridas"])} h')
            b.metric("Capacidad disponible", f'{formato(plan["disponibles"])} h')
            # Barras con la misma escala. No se recorta una ocupación superior al 100 %.
            escala = max(plan["requeridas"], plan["disponibles"])
            trabajo = float(plan["requeridas"] / escala * 100)
            capacidad = float(plan["disponibles"] / escala * 100)
            color = "#b66a12" if plan["diferencia"] < 0 else "#037a8b"
            st.markdown(
                f'<div class="bars"><label>Trabajo estimado · {formato(plan["requeridas"])} h</label>'
                f'<div class="track"><div style="width:{trabajo}%;background:{color}"></div></div>'
                f'<label>Capacidad disponible · {formato(plan["disponibles"])} h</label>'
                f'<div class="track"><div style="width:{capacidad}%;background:#12507f"></div></div></div>',
                unsafe_allow_html=True)
            if plan["diferencia"] < 0:
                st.markdown(f'**Faltan {formato(-plan["diferencia"])} horas para cumplir el plazo.**')
            elif plan["diferencia"] > 0:
                st.markdown(f'**Quedan {formato(plan["diferencia"])} horas disponibles dentro del plazo.**')
            else:
                st.markdown("**El trabajo ocupa exactamente la capacidad disponible.**")
            st.markdown(
                f'<div class="recommendation"><b>Necesitas {plan["dias_necesarios"]} días hábiles</b>'
                f'<p>Con {plan["personas"]} persona(s) y {formato(plan["horas_dia"])} horas al día por persona.</p></div>',
                unsafe_allow_html=True)
            if plan["diferencia"] < 0:
                st.caption("Para ajustar el plan, cambia el plazo o la capacidad en el apartado 2 y recalcula.")
            st.metric("Ocupación estimada", f'{formato(plan["ocupacion"], 1)} %')
            with st.expander("Ver desglose de la estimación"):
                st.write(f'Piezas: **{plan["piezas"]}**')
                st.write(f'Producción base: **{formato(plan["base"])} h**')
                st.write(f'Revisiones ({formato(plan["revisiones"], 0)} %): **{formato(plan["revision"])} h**')
                st.table([{"Pieza": fila["tipo"], "Cantidad": fila["cantidad"],
                           "Horas base": formato(fila["subtotal"])} for fila in plan["detalle"]])
            st.download_button("Descargar resumen CSV", data=exportar_csv(plan),
                               file_name="Resumen_Plan_Creativo.csv", mime="text/csv",
                               use_container_width=True)
        with st.expander("¿Qué contempla esta estimación?"):
            st.caption("Supone disponibilidad constante y trabajo distribuible. "
                       "No incluye festivos, esperas de aprobación ni dependencias.")
        st.caption("Los datos duran esta sesión. Descarga el CSV para conservarlos.")
st.caption("ÓBERON PLAN CREATIVO · Proyecto académico · Python")
