# Manual de Usuario — Motor Inteligente de Segmentación de Clientes

**Versión:** 2.0 · **Fecha:** 16/10/2026 · **Audiencia:** usuario final (analista de marketing / presentación comercial)
**Requiere:** sistema instalado y corriendo (ver `Guia_de_Instalacion.md`). Dirección de la aplicación: **http://localhost:5173** (el backend debe estar encendido: http://127.0.0.1:8000).

---

## 1. Qué puede hacer desde la web

Ver el resumen general de clientes y gastos, explorar clientes y predecir su segmento, consultar los 6 segmentos con su perfil y recomendación de IA, crear audiencias objetivo y exportarlas a CSV, conectar fuentes de datos nuevas (CSV con ayuda de IA) y revisar la calidad de las ejecuciones del sistema.

La barra superior tiene 6 vistas: **Dashboard, Clientes, Segmentos, Audiencias, Fuentes y Ejecuciones**, más el interruptor de tema claro/oscuro y el glosario de conceptos (los iconos **i** explican cada término técnico al pasar el hover).

## 2. Dashboard (resumen general)

KPIs principales: **clientes totales, transacciones, gasto total y ticket promedio**.
Gráficas: distribución de clientes por segmento (clic en una barra para ir al detalle), gasto por segmento, recencia promedio y categorías más compradas.
Uso típico: apertura de presentación — responde "¿cuántos clientes, cuánto gastan y cómo se reparten?".

## 3. Clientes

1. La tabla lista clientes con edad, ciudad, fecha de registro y **segmento actual**.
2. **Buscar** por ID usando el buscador (p. ej. `CLI-01`).
3. **Filtros:** por segmento y por ciudad; la fila se expande mostrando **frecuencia, gasto, última compra y recencia**.
4. **"Predecir segmento (Azure)":** envía las features del cliente a la nube y muestra el segmento predicho. Primer uso del día puede tardar 10–30 s (servicio que despierta); reintentar si la primera consulta es lenta.
5. Clic en el ID → **página del cliente**: modelo RFM completo (gráfica), features y su historial.

> Significado de "Recencia": días desde su última compra. Menor = más reciente/activo.

## 4. Segmentos (el núcleo del producto)

1. La vista muestra los **6 segmentos** con su color, descripción comercial y número de clientes:
   frecuentes de alto valor · navegadores sin compra · compradores ocasionales · clientes nuevos · navegadores con compra esporádica · clientes en riesgo de inactividad.
2. Clic en un segmento → **detalle**: perfil medio del grupo (gasto, frecuencia, navegación, carritos abandonados…) con gráficas.
3. **"Generar/Regenerar recomendación (IA)":** la IA comercial recibe el perfil real del segmento y devuelve estrategia, tácticas y canales sugeridos. Se guarda y puede regenerarse cuando cambien los datos.
4. En la pestaña de segmento también puedes **crear una audiencia a partir de este segmento** y continuar en la sección 5.
5. **"Repasar presentación"** (en la sección de segmentos): checklist preparado para la proyección de la demo.

Si aparece "… de baja actividad": es una **variante válida** de compradores ocasionales que el sistema asigna cuando hay dos grupos parecidos: significa clientes poco activos con historial.

## 5. Audiencias (grupos objetivo para campañas)

1. Cree una nueva audiencia poniendo nombre y condiciones: segmento, ciudad, categoría comprada, frecuencia mínima o **días sin compra** (¡el clásico "en riesgo" + categoría!).
2. La membresía es **dinámica**: si los datos cambian, la audiencia se recalcula sola en cada consulta (nadie queda "congelado").
3. **Exportar CSV** para cargarla en la plataforma de campañas (columnas: ID, edad, ciudad, segmento, frecuencia, última compra).
4. Eliminar la audiencia no borra clientes: solo el "guardado" de la condición.

Los números pueden variar entre consultas: es correcto — la audiencia refleja los datos vigentes.

## 6. Fuentes (conectar datos nuevos SIN programar)

Asistente de 3 pasos; en cada paso tú confirmas (la IA jamás toca la base directamente):

1. **Subir CSV:** elige el archivo. El sistema detecta las columnas y muestra las primeras filas.
2. **Revisar mapeo sugerido:** la IA propone a qué entidad corresponde el archivo (clientes/transacciones/interacciones/eventos) y mapea cada columna al campo correcto aunque esté en español crudo (`poblacion` → ciudad, `anios` → edad…). Verás el **badge "Sugerido por IA"** con su % de confianza. Todo editable: cambia la entidad, reasigna columnas con los desplegables.
3. **Validar:** el sistema hace una prueba en seco: cuántas filas son válidas, cuáles se descartan y por qué (se muestran las primeras incidencias) y una vista previa del resultado ya adaptado.
4. **Guardar** (opción: guardar y sincronizar ya). Tras sincronizar, los datos entran a la base con la misma trazabilidad que cualquier fuente y están disponibles en segmentos/audiencias/dashboard.

Después puedes **sincronizar** de nuevo si el archivo cambia, o **eliminar** la fuente (los datos ya sincronizados se conservan).

> Si la IA no está disponible, el asistente manual funciona igual: elige entidad y mapea cada columna.

## 7. Ejecuciones (confianza y calidad)

Historial de lo que el sistema hizo: runs de **ingestión** (duración, filas leídas/válidas/inválidas) y de **segmentación** (modelo, semilla, métricas). Guía rápida:
- **Silhouette** más alto = grupos mejor separados (aprox. 0.41 con k=6 en la demo).
- **Davies-Bouldin** más bajo = mejor (aprox. 0.86).
- Estado `ok` = ejecución completa; `error` = revise el detalle del run; y no hay nada preocupante si `/health` dice `degradado` (solo faltan credenciales de Azure).

## 8. Mensajes que puedes ver y su significado

| Mensaje | Qué significa | Qué hacer |
|---|---|---|
| "Predecir segmento… (tarda)" | El servicio de Azure está despertando | Esperar 10–30 s y reintentar |
| "Azure no disponible (502)" | servicio de scoring dormido/transitorio | Reintentar tras un minuto |
| "IA no disponible (503)" | Azure OpenAI no configurado | Usar el asistente manual; el motor no se afecta |
| "Nombre duplicado" | Ya existe una audiencia/fuente con ese nombre | Cambiar el nombre |
| "Con incidencias (n)" | Filas del CSV inválidas (se descartan al sync, las demás entran) | Abrir el detalle: se muestran las primeras y el motivo |
| "Algo salió mal" (recuadro rojo) | Error interno no esperado en la web | Copiar el mensaje, clic "Recargar la página" y notificar a soporte técnico |

## 9. Consejos para la demostración

1. Arranca todos los servicios 5 minutos antes (ver Guía de Instalación, sección 8).
2. Guion sugerido (≤10 min): Dashboard → Clientes (1 predict en vivo) → Segmento con recomendación de IA regenerada en caliente → Audiencia con export → **Fuentes con un CSV en español crudo (el momento sorpresa: la IA adivina el mapeo)** → Ejecuciones (confianza con métricas).
3. Tema oscuro para proyectar; tema claro para impresiones.
4. Todo funciona sin internet: solo las 3 cosas de Azure requieren conexión (predict, recomendación, sugerencia de mapeo) — sin internet la app sigue consultable completa.
