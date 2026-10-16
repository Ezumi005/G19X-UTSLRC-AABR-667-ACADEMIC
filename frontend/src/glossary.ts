export interface EntradaGlosario {
  titulo: string;
  descripcion: string;
}

export const GLOSARIO: Record<string, EntradaGlosario> = {
  rfm: {
    titulo: "RFM",
    descripcion:
      "Las tres señales básicas de comportamiento de compra: Recencia (hace cuánto compró), Frecuencia (cuántas veces compró) y Monetario (cuánto gastó). Con ellas el modelo agrupa a los clientes.",
  },
  recencia: {
    titulo: "Recencia",
    descripcion:
      "Días transcurridos desde la última compra del cliente. Más días = más tiempo sin actividad.",
  },
  ticket: {
    titulo: "Ticket promedio",
    descripcion:
      "Cuánto gasta el cliente en promedio en cada compra (gasto total ÷ número de compras).",
  },
  carritos: {
    titulo: "Carritos abandonados",
    descripcion:
      "Veces que el cliente puso productos en el carrito y cerró sin comprar. Señal de interés sin conversión.",
  },
  clic: {
    titulo: "Tasa de clic en campañas",
    descripcion:
      "Porcentaje de correos de campaña recibidos en los que el cliente hizo clic. Mide qué tanto engancha el marketing con él.",
  },
  cluster: {
    titulo: "Cluster (grupo)",
    descripcion:
      "Conjunto de clientes con comportamiento parecido, descubierto automáticamente por el modelo. Es lo mismo que un segmento.",
  },
  silhouette: {
    titulo: "Silhouette (calidad del agrupado)",
    descripcion:
      "Métrica de 0 a 1 que indica qué tan bien separados quedaron los grupos: más alto = grupos más nítidos y distintos entre sí.",
  },
  davies: {
    titulo: "Davies-Bouldin (separación)",
    descripcion:
      "Métrica donde MENOR es mejor: mide qué tan distintos son los grupos entre sí (0 = perfectos).",
  },
  k: {
    titulo: "k (número de grupos)",
    descripcion: "Cantidad de grupos en que se dividió a los clientes en esa ejecución.",
  },
  audiencia: {
    titulo: "Audiencia dinámica",
    descripcion:
      "Lista de clientes construida con condiciones (segmento, ciudad, comportamiento…) que se recalcula sola cada vez que la consultas, lista para usarse en campañas.",
  },
  ingesta: {
    titulo: "Ingestión",
    descripcion:
      "Proceso de traer los datos del CRM y guardarlos ya limpios en la base del sistema. Guardados/leídos indica cuántos registros entraron y cuántos se aceptaron.",
  },
  incidencias: {
    titulo: "Incidencias",
    descripcion:
      "Registros con errores (datos inválidos) que el sistema detectó y excluyó sin detener el proceso.",
  },
  inferencia: {
    titulo: "Predicción (inferencia)",
    descripcion:
      "Consulta al modelo servido en la nube de Azure: recibe el perfil del cliente y responde a qué segmento pertenece.",
  },
  contrato: {
    titulo: "Contrato interno",
    descripcion:
      "El formato estándar de datos del sistema (clientes, transacciones, interacciones y campañas). Toda fuente externa se traduce a este formato mediante un adaptador; el motor solo lo conoce a él.",
  },
};
