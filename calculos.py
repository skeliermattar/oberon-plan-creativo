"""Cálculos del plan creativo. No depende de la interfaz.
Proyecto académico de Skarlet Mattar.
"""
import csv
import io
from decimal import Decimal, InvalidOperation, ROUND_CEILING


class DatosInvalidos(ValueError):
    """Una entrada no cumple las reglas de la planificación."""


def numero(valor, nombre, minimo, maximo, entero=False):
    """Convierte y valida números; admite coma decimal y rechaza NaN/infinito."""
    try:
        valor = Decimal(str(valor).strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        raise DatosInvalidos(f"{nombre}: escribe un número válido.") from None
    if not valor.is_finite() or not minimo <= valor <= maximo:
        raise DatosInvalidos(f"{nombre}: usa un valor entre {minimo} y {maximo}.")
    if entero and valor != valor.to_integral_value():
        raise DatosInvalidos(f"{nombre}: usa un número entero.")
    return valor


def calcular_plan(campana, piezas, revisiones, personas, horas_dia, plazo):
    """Entrada: campaña, piezas y capacidad. Salida: resumen verificable."""
    nombre = str(campana or "").strip()
    if not nombre or len(nombre) > 100:
        raise DatosInvalidos("Campaña: escribe un nombre de 1 a 100 caracteres.")
    if not piezas or len(piezas) > 30:
        raise DatosInvalidos("Piezas: agrega entre 1 y 30 filas.")
    margen = numero(revisiones, "Revisiones (%)", 0, 100)
    equipo = numero(personas, "Personas", 1, 100, entero=True)
    horas = numero(horas_dia, "Horas por día", Decimal("0.25"), 12)
    dias = numero(plazo, "Plazo (días)", 1, 365, entero=True)
    detalle = []
    horas_base = Decimal("0")
    cantidad_total = 0
    for indice, pieza in enumerate(piezas, start=1):
        tipo = str(pieza.get("tipo", "") or "").strip()
        if not tipo or len(tipo) > 80:
            raise DatosInvalidos(f"Pieza {indice}: indica un tipo de 1 a 80 caracteres.")
        cantidad = numero(pieza.get("cantidad"), f"Pieza {indice}, cantidad", 1, 1000, True)
        tiempo = numero(pieza.get("horas"), f"Pieza {indice}, horas", Decimal("0.25"), 200)
        subtotal = cantidad * tiempo
        horas_base += subtotal
        cantidad_total += int(cantidad)
        detalle.append({"tipo": tipo, "cantidad": int(cantidad),
                        "horas": tiempo, "subtotal": subtotal})
    # El porcentaje para revisiones se aplica sobre el trabajo base.
    horas_revision = horas_base * margen / 100
    requeridas = horas_base + horas_revision
    capacidad_diaria = equipo * horas
    disponibles = capacidad_diaria * dias
    diferencia = disponibles - requeridas
    dias_necesarios = int((requeridas / capacidad_diaria).to_integral_value(
        rounding=ROUND_CEILING))
    if diferencia > 0:
        estado = "Capacidad suficiente"
    elif diferencia == 0:
        estado = "Capacidad justa"
    else:
        estado = "Requiere ajuste"
    return {
        "campana": nombre, "detalle": detalle, "piezas": cantidad_total,
        "revisiones": margen, "personas": int(equipo), "horas_dia": horas,
        "plazo": int(dias), "base": horas_base, "revision": horas_revision,
        "requeridas": requeridas, "disponibles": disponibles,
        "diferencia": diferencia, "ocupacion": requeridas / disponibles * 100,
        "dias_necesarios": dias_necesarios, "estado": estado,
    }


def formato(valor, decimales=2):
    """Presenta números con coma decimal, sin alterar la precisión del cálculo."""
    return f"{valor:,.{decimales}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def celda_segura(texto):
    """Evita interpretar nombres ingresados por el usuario como fórmulas de Excel."""
    texto = str(texto)
    if texto.lstrip().startswith(("=", "+", "-", "@")) or texto.startswith(("\t", "\r", "\n")):
        return "'" + texto
    return texto


def exportar_csv(plan):
    """Exporta exactamente el último cálculo, con UTF-8 para conservar tildes."""
    salida = io.StringIO(newline="")
    escritor = csv.writer(salida, delimiter=";")
    escritor.writerow(["ÓBERON PLAN CREATIVO", "Estimación"])
    escritor.writerow(["Campaña", celda_segura(plan["campana"])])
    escritor.writerow(["Tipo de pieza", "Cantidad", "Horas por pieza", "Horas base"])
    for pieza in plan["detalle"]:
        escritor.writerow([celda_segura(pieza["tipo"]), pieza["cantidad"],
                           formato(pieza["horas"]), formato(pieza["subtotal"])])
    escritor.writerow([])
    for etiqueta, clave in [
        ("Piezas totales", "piezas"), ("Revisiones (%)", "revisiones"),
        ("Personas", "personas"), ("Horas al día por persona", "horas_dia"),
        ("Plazo en días hábiles", "plazo"), ("Horas base", "base"),
        ("Horas de revisión", "revision"), ("Horas requeridas", "requeridas"),
        ("Horas disponibles", "disponibles"), ("Saldo de horas", "diferencia"),
        ("Ocupación (%)", "ocupacion"), ("Días hábiles necesarios", "dias_necesarios")
    ]:
        escritor.writerow([etiqueta, formato(plan[clave])])
    escritor.writerow(["Resultado", plan["estado"]])
    escritor.writerow(["Supuestos", "Disponibilidad constante; trabajo distribuible entre personas."])
    escritor.writerow(["Alcance", "No incluye festivos, esperas de aprobación ni dependencias entre tareas."])
    return ("\ufeff" + salida.getvalue()).encode("utf-8")
