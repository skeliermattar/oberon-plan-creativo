# ÓBERON PLAN CREATIVO

Aplicación académica en Python de Skarlet Mattar.
Calcula el esfuerzo de producción de una campaña y compara las horas requeridas con la capacidad del equipo.

## Abrir en tu Mac con Visual Studio Code

1. Descomprime el ZIP.
2. En VS Code selecciona Archivo > Abrir carpeta y elige Oberon_Plan_Creativo.
3. Abre Terminal > Nueva terminal.
4. Comprueba Python:

    python3 --version

La dependencia fijada requiere Python 3.9 o posterior (excepto 3.9.7). Si la instalación informa una incompatibilidad, conserva el mensaje completo para revisar la versión antes de cambiar nada.

5. Crea un entorno aislado (solo la primera vez):

    python3 -m venv .venv

6. Actívalo:

    source .venv/bin/activate

7. Instala las dependencias (solo la primera vez):

    python3 -m pip install -r requirements.txt

8. Ejecuta la aplicación:

    python3 -m streamlit run app.py

Se abrirá el navegador. Si no se abre, utiliza la dirección Local URL que muestra la terminal.
Normalmente será http://localhost:8501. Esta dirección solo sirve en tu equipo; NO es el enlace para el profesor.

Para cerrar: pulsa Control + C en la terminal.
Para abrir de nuevo: activa el entorno y ejecuta el comando del paso 8.

## Primer recorrido

1. Pulsa "Cargar ejemplo de campaña".
2. Comprueba: 8 piezas estáticas a 1 h, 3 carruseles a 2 h, 2 videos a 4 h.
3. Revisiones 20 %, 1 persona, 4 horas diarias, plazo 5 días.
4. Pulsa "Calcular planificación".
5. Debes ver 26,40 h requeridas; 20 h disponibles; déficit 6,40 h; ocupación 132 %; 7 días.
6. Cambia Personas a 2. El resultado se oculta y se solicita recalcular.
7. Recalcula: 40 h disponibles; saldo 13,60 h; ocupación 66 %; 4 días.
8. Descarga el resumen CSV y ábrelo en Excel o Numbers.

Los tiempos de ejemplo NO son mediciones oficiales de Óberon TSI.
La estimación no asigna tareas individuales ni garantiza una fecha de entrega.

## Archivos

- app.py: interfaz, controles, navegación, resultados y descarga.
- calculos.py: validaciones, fórmulas y exportación.
- test_calculos.py: pruebas automatizadas del cálculo.
- requirements.txt: versión de Streamlit.
- assets/: estilo visual, Montserrat y licencia OFL.
- .streamlit/config.toml: colores y configuración.
- PROYECTO.md: definición, reglas, evidencia pendiente y criterios de aceptación.

## Publicación para el profesor (pendiente)

La app aún no tiene URL pública. Se propone Streamlit Community Cloud:
https://docs.streamlit.io/deploy/streamlit-community-cloud

1. Crear o utilizar una cuenta de GitHub y subir los archivos del proyecto a un repositorio.
   No subir .venv, __pycache__ ni archivos personales.
2. Conectar esa cuenta a Streamlit Community Cloud.
3. Elegir repositorio, rama y archivo principal app.py.
4. Elegir Python 3.11 para el servidor y desplegar.
5. Configurar el acceso público y abrir el enlace en una ventana privada para verificar que el profesor pueda usarlo.
6. Guardar la URL real para el informe; probar cálculo y descarga desde esa URL.

El nombre y la disponibilidad de la URL dependen del despliegue. No se incluye un enlace ficticio.

## Evidencias para el informe final

- Código completo: app.py y calculos.py, con capturas consecutivas legibles.
- App con el ejemplo y su resultado de capacidad insuficiente.
- App con 2 personas y capacidad suficiente.
- Aviso al intentar calcular sin nombre de campaña.
- Aviso de datos modificados antes de recalcular.
- App publicada: dirección visible, entrada y resultado.
- Reflexión personal escrita tras las pruebas: máximo 200 palabras.

El PDF final se elaborará después de comprobar la URL pública y reunir las evidencias de ejecución.
