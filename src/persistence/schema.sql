-- Esquema interno del Motor de Segmentacion de Clientes (PostgreSQL).
-- Espeja el Contrato Interno de Datos V1 (docs/contrato_interno_datos_v1.md).
--
-- Notas de diseno:
-- * Sin claves foraneas por ahora: la integridad referencial es
--   responsabilidad de la etapa de procesamiento (contrato, seccion 2).
--   La ingesta no debe romperse por registros huerfanos.
-- * Upserts idempotentes desde el repositorio: re-sincronizar no duplica.
-- * Tablas de segmentacion (segmentation_runs, segments, customer_segments,
--   recommendations) se agregaran en su etapa correspondiente.
-- * Idempotente: CREATE ... IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS customers (
    customer_id   TEXT PRIMARY KEY,
    age           INT CHECK (age IS NULL OR (age >= 0 AND age <= 120)),
    city          TEXT,
    registered_at TIMESTAMPTZ NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id    TEXT NOT NULL,
    purchased_at   TIMESTAMPTZ NOT NULL,
    amount         NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    category       TEXT NOT NULL CHECK (category IN
        ('electronica','hogar','moda','deportes','belleza','alimentos','juguetes','otros')),
    product_name   TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_transactions_customer    ON transactions (customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_purchased_at ON transactions (purchased_at);

CREATE TABLE IF NOT EXISTS interactions (
    interaction_id   TEXT PRIMARY KEY,
    customer_id      TEXT NOT NULL,
    interaction_type TEXT NOT NULL CHECK (interaction_type IN
        ('web_visit','product_view','abandoned_cart')),
    occurred_at      TIMESTAMPTZ NOT NULL,
    product_name     TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_interactions_customer ON interactions (customer_id);
CREATE INDEX IF NOT EXISTS idx_interactions_occurred_at ON interactions (occurred_at);

CREATE TABLE IF NOT EXISTS campaign_events (
    campaign_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    event_type  TEXT NOT NULL CHECK (event_type IN
        ('sent','delivered','opened','clicked')),
    occurred_at TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- CampaignEvent no tiene ID propio: identidad compuesta (contrato, seccion 3.4)
    CONSTRAINT uq_campaign_event_identity UNIQUE (campaign_id, customer_id, event_type, occurred_at)
);
CREATE INDEX IF NOT EXISTS idx_campaign_events_customer   ON campaign_events (customer_id);
CREATE INDEX IF NOT EXISTS idx_campaign_events_occurred_at ON campaign_events (occurred_at);

-- Trazabilidad de ingestiones (RF-25 / RNF-MVP-08)
CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id         BIGSERIAL PRIMARY KEY,
    source         TEXT NOT NULL,
    started_at     TIMESTAMPTZ NOT NULL,
    finished_at    TIMESTAMPTZ,
    status         TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running','ok','error')),
    customers_read         INT NOT NULL DEFAULT 0,
    customers_saved        INT NOT NULL DEFAULT 0,
    transactions_read      INT NOT NULL DEFAULT 0,
    transactions_saved     INT NOT NULL DEFAULT 0,
    interactions_read      INT NOT NULL DEFAULT 0,
    interactions_saved     INT NOT NULL DEFAULT 0,
    campaign_events_read   INT NOT NULL DEFAULT 0,
    campaign_events_saved  INT NOT NULL DEFAULT 0,
    error          TEXT
);

-- Incidencias reportadas por el adaptador (RF-05: registrar sin detener el proceso)
CREATE TABLE IF NOT EXISTS ingestion_incidents (
    incident_id BIGSERIAL PRIMARY KEY,
    run_id      BIGINT NOT NULL REFERENCES ingestion_runs (run_id) ON DELETE CASCADE,
    entity      TEXT NOT NULL,
    external_id TEXT,
    field       TEXT,
    error       TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Segmentacion (etapa 8): cada ejecucion conserva sus segmentos y asignaciones
CREATE TABLE IF NOT EXISTS segmentation_runs (
    run_id      BIGSERIAL PRIMARY KEY,
    model_name  TEXT NOT NULL,
    k           INT NOT NULL,
    seed        INT NOT NULL,
    params      JSONB,
    metrics     JSONB,
    started_at  TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    status      TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running','ok','error')),
    error       TEXT,
    n_customers INT
);

CREATE TABLE IF NOT EXISTS segments (
    segment_id  BIGSERIAL PRIMARY KEY,
    run_id      BIGINT NOT NULL REFERENCES segmentation_runs (run_id) ON DELETE CASCADE,
    cluster_id  INT NOT NULL,
    label       TEXT NOT NULL,
    description TEXT,
    n_customers INT NOT NULL,
    profile     JSONB NOT NULL,
    CONSTRAINT uq_segment_run_cluster UNIQUE (run_id, cluster_id)
);

CREATE TABLE IF NOT EXISTS customer_segments (
    run_id      BIGINT NOT NULL REFERENCES segmentation_runs (run_id) ON DELETE CASCADE,
    customer_id TEXT NOT NULL REFERENCES customers (customer_id) ON DELETE CASCADE,
    cluster_id  INT NOT NULL,
    segment_id  BIGINT NOT NULL REFERENCES segments (segment_id) ON DELETE CASCADE,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, customer_id)
);
CREATE INDEX IF NOT EXISTS idx_customer_segments_customer ON customer_segments (customer_id);

-- Recomendaciones comerciales por segmento (Azure OpenAI; etapa 12)
CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id BIGSERIAL PRIMARY KEY,
    segment_id   BIGINT NOT NULL REFERENCES segments (segment_id) ON DELETE CASCADE,
    model        TEXT NOT NULL,
    descripcion  TEXT,
    recomendaciones JSONB NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_recommendations_segment ON recommendations (segment_id);

-- Audiencias dinamicas (PRD seccion 16 / RF-18, RF-19): condiciones almacenadas,
-- membresia recalculada en cada consulta contra los datos vigentes
CREATE TABLE IF NOT EXISTS audiences (
    audience_id      BIGSERIAL PRIMARY KEY,
    name             TEXT NOT NULL UNIQUE,
    description      TEXT,
    conditions       JSONB NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_calculated_at TIMESTAMPTZ,
    n_customers      INT
);
