# Contrato Interno de Datos — Versión 1

| Atributo | Valor |
|---|---|
| Fecha de definición | 10/09/2026 |
| Estado | Vigente |
| Codificación oficial | `src/contracts/` (Pydantic v2) |
| Prueba automática | `tests/test_contrato.py` |
| Documentos de origen | README.md §4, PRD v1.1 §9, MVP v1.1 §6 |

## 1. Propósito

El contrato interno es la **frontera estable** entre las fuentes externas y el núcleo del sistema.

- Los **adaptadores** traducen cualquier fuente externa a estas entidades.
- El **núcleo** (procesamiento, PostgreSQL, ML, FastAPI) solo conoce estas entidades.
- Ningún formato externo (CRM simulado, HubSpot, CSV, etc.) puede atravesar esta frontera.

## 2. Convenciones globales

- **IDs**: strings no vacíos y opacos. El núcleo no asigna significado al formato interno del ID; eso es asunto de cada adaptador.
- **Fechas y horas**: ISO 8601 (`datetime`). El adaptador convierte a UTC cuando la fuente declara zona horaria; si la fuente no declara zona, se interpreta como UTC (supuesto del MVP).
- **Montos**: `float` ≥ 0. El MVP trabaja en **moneda única** (sin conversión de divisas). No se usa `Decimal` porque el destino es análisis/ML (pandas), no aritmética contable.
- **Campos opcionales**: pueden ser `null`. Los obligatorios están marcados por entidad (§3).
- **Alcance de la validación**: el contrato valida estructura y tipos de cada registro. La integridad cruzada (transacciones cuyo `customer_id` no existe, IDs duplicados) la valida la **etapa de procesamiento**, no el contrato.

## 3. Entidades

### 3.1 Customer

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `customer_id` | `str` | Sí | Identificador único del cliente |
| `age` | `int` (0–120) | No | Edad en años |
| `city` | `str` | No | Ciudad |
| `registered_at` | `datetime` | Sí | Fecha de alta del cliente |

### 3.2 Transaction

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `transaction_id` | `str` | Sí | Identificador único de la compra |
| `customer_id` | `str` | Sí | Referencia lógica a Customer |
| `purchased_at` | `datetime` | Sí | Fecha y hora de la compra |
| `amount` | `float` ≥ 0 | Sí | Monto total de la compra (moneda única) |
| `category` | `ProductCategory` | Sí | Categoría canónica (§4.1) |
| `product_name` | `str` | No | Producto comprado; habilita análisis de preferencias sin ser bloqueante |

### 3.3 Interaction (comportamiento digital fuera de campañas)

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `interaction_id` | `str` | Sí | Identificador único de la interacción |
| `customer_id` | `str` | Sí | Referencia lógica a Customer |
| `interaction_type` | `InteractionType` | Sí | Tipo canónico (§4.2) |
| `occurred_at` | `datetime` | Sí | Fecha y hora |
| `product_name` | `str` | No | Producto en `product_view` / `abandoned_cart` |

### 3.4 CampaignEvent (embudo de campañas de marketing)

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `campaign_id` | `str` | Sí | Identificador de la campaña |
| `customer_id` | `str` | Sí | Referencia lógica a Customer |
| `event_type` | `CampaignEventType` | Sí | Tipo canónico (§4.3) |
| `occurred_at` | `datetime` | Sí | Fecha y hora |

Nota: CampaignEvent **no tiene ID propio**. Su identidad es el conjunto (`campaign_id`, `customer_id`, `event_type`, `occurred_at`). Un mismo cliente puede tener varios eventos del mismo tipo en una campaña en momentos distintos.

### 3.5 NormalizedDataset

Resultado completo que entrega un adaptador tras una sincronización:

| Campo | Tipo |
|---|---|
| `customers` | `list[Customer]` |
| `transactions` | `list[Transaction]` |
| `interactions` | `list[Interaction]` |
| `campaign_events` | `list[CampaignEvent]` |

## 4. Enumeraciones canónicas

### 4.1 ProductCategory

`electronica` · `hogar` · `moda` · `deportes` · `belleza` · `alimentos` · `juguetes` · `otros`

Regla de mapeo del adaptador: toda categoría externa debe traducirse a un valor del canon; si no hay equivalente, se asigna `otros`.

### 4.2 InteractionType

`web_visit` · `product_view` · `abandoned_cart`

### 4.3 CampaignEventType

`sent` · `delivered` · `opened` · `clicked`

### Notas de mapeo

- **Correos abiertos y clics de campañas** pertenecen a `CampaignEvent` (`opened` / `clicked`). Así se derivan las features `emails_opened` y `campaign_click_rate` del MVP §10.
- `Interaction` cubre el comportamiento digital fuera de campañas (visitas, productos consultados, carritos abandonados).
- **Valores desconocidos**: una categoría externa sin equivalente → `otros`. Un tipo de interacción o evento desconocido → el adaptador **descarta el registro y lo reporta** en su log de incidencias (no existe "otros" para eventos porque distorsionaría las features).
- Nuevos tipos de interacción o evento requerirán una **V2** del contrato.

## 5. Responsabilidades

**Un adaptador debe entregar**: tipos convertidos, enums canónicos, campos obligatorios presentes, registros inválidos reportados (nunca en silencio) y sin lógica de negocio ni de ML.

**El procesamiento puede asumir**: registros válidos según schema; y debe encargarse de referencias cruzadas, duplicados, faltantes y transformaciones (PRD §11).

## 6. Versionado

- Cambios **compatibles** (p. ej. nuevo campo opcional) → V1.x: actualizar este documento, el código, las pruebas y registrar entrada en `Bitacora.md`.
- Cambios **rompientes** (quitar campo, cambiar tipo, redefinir enums) → V2: además, actualizar todos los adaptadores y validar el impacto en PostgreSQL y ML antes de aprobar.
