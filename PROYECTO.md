# Mi primer programa en Python
## ÓBERON PLAN CREATIVO
Autora: Skarlet Mattar

### Problema propuesto
Estimar la producción de una campaña requiere relacionar tipos de piezas, cantidades, tiempo por pieza y capacidad disponible. Calcular estos elementos de forma dispersa dificulta identificar si el plazo solicitado es viable. El proyecto ofrece una estimación uniforme y explicable para apoyar esa decisión.

Este problema es una propuesta contextualizada en marketing de Óberon TSI. Aún debe confirmarse cómo realiza el área sus estimaciones actuales; no se afirma que exista una medición interna ni una mejora porcentual demostrada.

### Pregunta
¿Cómo calcular el esfuerzo de producción de una campaña y compararlo con la capacidad del equipo dentro del plazo solicitado?

### Objetivo general
Desarrollar una aplicación web en Python que estime las horas de producción de piezas de marketing, las compare con la capacidad disponible y presente resultados comprensibles para apoyar la planificación.

### Objetivos específicos
- Validar datos de entrada.
- Calcular esfuerzo base y adicional por revisiones.
- Clasificar la capacidad como suficiente, justa o insuficiente.
- Mostrar ocupación, saldo de horas y días necesarios.
- Exportar un resumen reproducible.
- Probar casos normales, límites y entradas incorrectas.

### Usuarios
Persona que coordina campañas o producción de diseño. Para la evaluación, el profesor puede realizar el mismo recorrido con datos de ejemplo.

### Alcance del MVP
Una campaña por sesión; hasta 30 filas de piezas; valores editables; exportación CSV; guía dentro de la aplicación. Sin cuentas de usuario, base de datos, integración con sistemas corporativos ni generación con IA. El nombre de autora identifica el proyecto, no una sesión autenticada.

### Entradas y límites
- Nombre de campaña: 1–100 caracteres.
- Tipo: selección o nombre personalizado de 1–80 caracteres.
- Cantidad: entero de 1 a 1000 por fila.
- Horas por pieza: 0,25 a 200.
- Revisiones: 0–100 % del esfuerzo base.
- Personas: entero de 1 a 100.
- Disponibilidad diaria individual: 0,25 a 12 horas.
- Plazo: entero de 1 a 365 días hábiles.

Los límites son decisiones de alcance para esta versión académica, no reglas laborales.

### Procesamiento
1. Validar nombre, filas y valores.
2. Multiplicar cantidad por horas para cada fila.
3. Sumar horas base.
4. Calcular horas de revisión: base × porcentaje / 100.
5. Calcular horas requeridas: base + revisión.
6. Calcular capacidad: personas × horas al día × plazo.
7. Restar requeridas a disponibles.
8. Calcular ocupación: requeridas / disponibles × 100.
9. Calcular días: techo(requeridas / (personas × horas al día)).
10. Clasificar estado y presentar resultados.

Se utiliza Decimal para evitar que errores de representación binaria alteren el redondeo hacia arriba de los días. Se mantienen los valores sin redondear para los cálculos; el formato visual usa dos decimales.

### Pseudocódigo
INICIO
  Leer campaña, piezas, revisiones, personas, horas_diarias, plazo
  Si una entrada es inválida: mostrar error y solicitar corrección
  base ← 0
  Para cada pieza:
    base ← base + cantidad × horas_por_pieza
  requeridas ← base × (1 + revisiones / 100)
  disponibles ← personas × horas_diarias × plazo
  saldo ← disponibles - requeridas
  Si saldo < 0: estado ← "Requiere ajuste"
  Sino si saldo = 0: estado ← "Capacidad justa"
  Sino: estado ← "Capacidad suficiente"
  ocupación ← requeridas / disponibles × 100
  días ← redondear_hacia_arriba(requeridas / (personas × horas_diarias))
  Mostrar resultados
  Permitir descargar resumen del cálculo vigente
FIN

### Decisiones UX/UI
- Formulario y resultados en columnas en escritorio.
- Secciones numeradas; campos con etiquetas persistentes.
- Estado inicial con instrucciones; ejemplo opcional.
- Resultados con texto y color, sin depender solo del color.
- Ocultar resultados desactualizados al editar; descarga bloqueada hasta recalcular.
- Límite mínimo de una fila; posibilidad de añadir y eliminar.
- Desglose consultable sin recargar la pantalla principal.
- Navegación “Cómo funciona” con fórmulas y supuestos.
- Montserrat local y paleta azul/verde de referencia.
- Adaptación de columnas según el ancho del navegador.

### Supuestos y límites
La capacidad supone que todas las personas disponen de las horas indicadas y pueden compartir el trabajo. No se modelan diferentes habilidades, tareas secuenciales, festivos, fechas de calendario, esperas de aprobación ni otras campañas simultáneas. El usuario debe introducir capacidad neta disponible. Los datos se conservan solo en la sesión; recargar o cerrar puede reiniciarlos. El CSV conserva el resumen, pero no hay función de importación.

### Pruebas de aceptación
| Caso | Entradas | Resultado esperado |
|---|---|---|
| Capacidad insuficiente | Ejemplo: 22 h base, 20 %, 1 persona, 4 h/día, 5 días | 26,4 h requeridas; 20 disponibles; 7 días |
| Capacidad suficiente | Mismo ejemplo, 2 personas | 40 disponibles; 13,6 h de saldo; 4 días |
| Capacidad exacta | 20 piezas a 1 h, 0 %, 1 persona, 4 h/día, 5 días | Capacidad justa; 5 días |
| Nombre vacío | Sin nombre | Error; no permite exportar cálculo inválido |
| Datos modificados | Editar después de calcular | Solicita recalcular; oculta resumen anterior |
| Personalización | Tipo Otro sin nombre | Error con identificación de la fila |
| Decimal | Horas de 0,3; 3 unidades; 0 %; 0,3 h/día | 3 días, sin error de redondeo |
| Exportación | Descargar ejemplo | CSV coincide con los resultados vigentes |

### Entrega académica pendiente
Documento Skarlet_Mattar_PrimerProgramaPython.pdf con portada, problema, objetivos, alcance, algoritmo, captura del código completo, explicación, capturas de ejecución, URL pública verificada, guía, reflexión personal de hasta 200 palabras y referencias APA.

### Fuentes técnicas
- Python Software Foundation. Documentación de decimal: https://docs.python.org/3/library/decimal.html
- Streamlit. Documentación: https://docs.streamlit.io/
- Streamlit. Publicación: https://docs.streamlit.io/deploy/streamlit-community-cloud
