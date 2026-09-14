"""Generador del dataset del CRM simulado.

Produce los archivos data/*.json con el formato EXTERNO propio de este CRM
simulado, deliberadamente distinto del contrato interno (src/contracts/),
para demostrar el trabajo del SimulatedCRMAdapter.

Caracteristicas:
- Semilla fija (SEED) y fecha de corte fija (ANCHOR): dataset reproducible.
- 6 perfiles de comportamiento con distribuciones distintas de frecuencia,
  gasto, recencia, engagement web y respuesta a campanas, para que el
  clustering tenga grupos descubribles.
- La asignacion de perfil real por cliente se guarda SOLO en data/meta.json
  (ground truth para validar el clustering); nunca se sirve por la API.
- Incluye categorias externas fuera del canon (BOOKS, GARDEN_TOOLS) y unos
  pocos registros corruptos, para probar las reglas de mapeo y de reporte de
  invalides del adaptador.

Uso (desde la raiz del proyecto):
    .venv/Scripts/python.exe -m crm_simulator.generate_data
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

SEED = 42
TOTAL_CUSTOMERS = 500
ANCHOR = datetime(2026, 9, 10, 12, 0, 0, tzinfo=timezone.utc)
HISTORY_DAYS = 550
CAMPAIGN_MONTHS = 8

CITIES = [
    "Monterrey", "CDMX", "Guadalajara", "Puebla", "Tijuana", "Queretaro",
    "Merida", "Leon", "Cancun", "Aguascalientes", "Saltillo", "Chihuahua",
]
CITY_WEIGHTS = [0.20, 0.22, 0.13, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.04, 0.01, 0.01]

PRODUCTS: dict[str, list[str]] = {
    "ELECTRONICS": ["Laptop X14", "Smart TV 55", "Audifonos BT Pro", "Tablet 10", "Smartwatch S3"],
    "HOME_APPLIANCES": ["Cafetera Deluxe", "Aspiradora Turbo", "Microondas 25L", "Licuadora 1200W", "Purificador de aire"],
    "FASHION": ["Chamarra Urban", "Tenis Runner Air", "Camisa Slim", "Bolso Elegance", "Jeans Classic"],
    "SPORTS": ["Mancuernas 10kg", "Bicicleta MTB 26", "Tapete yoga pro", "Mochila trail 30L", "Balon pro 7"],
    "BEAUTY": ["Serum facial N1", "Perfume Azure", "Kit skincare diario", "Secadora ionica", "Mascara volume"],
    "GROCERIES": ["Cafe de origen 1kg", "Aceite de oliva 750ml", "Kit despensa premium", "Te matcha organico", "Miel pura 500g"],
    "TOYS": ["Bloques creativos 500pz", "Dron mini camara", "Peluche gigante", "Juego de mesa estrategia", "Patin delux"],
    "BOOKS": ["Novela bestseller", "Guia de inversion", "Libro de cocina gourmet", "Comic edicion especial", "Manual de fotografia"],
    "GARDEN_TOOLS": ["Kit jardineria pro", "Podadora 18V", "Riego automatico", "Macetero vertical", "Invernadero mini"],
}

PROFILES: dict[str, dict] = {
    "vip": dict(
        share=0.10, reg_days=(400, 1100), freq_per_year=(26, 40), last_days=(0, 12), ticket=(1500, 4800),
        cats={"ELECTRONICS": 0.45, "HOME_APPLIANCES": 0.20, "SPORTS": 0.20, "FASHION": 0.10, "BEAUTY": 0.05},
        web_90d=(40, 80), open_rate=0.88, click_rate=0.60, cart_share=0.04,
    ),
    "frecuente": dict(
        share=0.20, reg_days=(400, 1100), freq_per_year=(12, 22), last_days=(5, 35), ticket=(600, 1800),
        cats={"GROCERIES": 0.30, "FASHION": 0.25, "HOME_APPLIANCES": 0.20, "SPORTS": 0.15, "TOYS": 0.10},
        web_90d=(18, 45), open_rate=0.62, click_rate=0.30, cart_share=0.08,
    ),
    "ocasional": dict(
        share=0.25, reg_days=(300, 1100), freq_per_year=(3, 7), last_days=(15, 160), ticket=(250, 900),
        cats={"GROCERIES": 0.35, "FASHION": 0.30, "TOYS": 0.20, "BOOKS": 0.15},
        web_90d=(3, 15), open_rate=0.35, click_rate=0.10, cart_share=0.10,
    ),
    "riesgo": dict(
        share=0.15, reg_days=(500, 1200), freq_per_year=(9, 16), last_days=(150, 320), ticket=(400, 1500),
        cats={"HOME_APPLIANCES": 0.30, "FASHION": 0.25, "GROCERIES": 0.25, "ELECTRONICS": 0.20},
        web_90d=(0, 4), open_rate=0.12, click_rate=0.03, cart_share=0.05,
    ),
    "nuevo": dict(
        share=0.15, reg_days=(10, 60), freq_total=(1, 3), last_days=(0, 20), ticket=(300, 1600),
        cats={"ELECTRONICS": 0.30, "FASHION": 0.30, "SPORTS": 0.20, "GROCERIES": 0.20},
        web_90d=(15, 40), open_rate=0.55, click_rate=0.25, cart_share=0.12,
    ),
    "navegador": dict(
        share=0.15, reg_days=(180, 600), freq_total=(0, 2), last_days=(30, 240), ticket=(150, 700),
        cats={"ELECTRONICS": 0.35, "SPORTS": 0.25, "TOYS": 0.20, "GARDEN_TOOLS": 0.10, "BOOKS": 0.10},
        web_90d=(70, 160), open_rate=0.70, click_rate=0.45, cart_share=0.38,
    ),
}


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _weighted(rng: random.Random, options: dict[str, float]) -> str:
    r = rng.random()
    acc = 0.0
    for key, weight in options.items():
        acc += weight
        if r <= acc:
            return key
    return next(iter(options))


def _random_dt_between(rng: random.Random, start: datetime, end: datetime) -> datetime:
    span = (end - start).total_seconds()
    return start + timedelta(seconds=rng.random() * span)


def main() -> None:
    rng = random.Random(SEED)

    customers: list[dict] = []
    transactions: list[dict] = []
    interactions: list[dict] = []
    campaign_events: list[dict] = []
    ground_truth: dict[str, str] = {}
    profile_counts: dict[str, int] = {}

    cseq = 0
    cust_profile: dict[str, tuple[str, datetime]] = {}
    for name, p in PROFILES.items():
        n_clients = max(1, round(TOTAL_CUSTOMERS * p["share"]))
        profile_counts[name] = n_clients
        for _ in range(n_clients):
            cseq += 1
            cid = f"CLI-{cseq:04d}"
            reg_dt = ANCHOR - timedelta(days=rng.randint(*p["reg_days"]), seconds=rng.randint(0, 86400))
            customers.append({
                "clientId": cid,
                "demographics": {"age": rng.randint(18, 74), "city": rng.choices(CITIES, weights=CITY_WEIGHTS, k=1)[0]},
                "memberSince": reg_dt.date().isoformat(),
            })
            cust_profile[cid] = (name, reg_dt)
            ground_truth[cid] = name

    tseq = 0
    for cid, (pname, reg_dt) in cust_profile.items():
        p = PROFILES[pname]
        last_dt = ANCHOR - timedelta(days=rng.randint(*p["last_days"]), seconds=rng.randint(0, 86400))
        start = max(reg_dt, ANCHOR - timedelta(days=HISTORY_DAYS))
        if last_dt <= start:
            last_dt = start + timedelta(days=rng.randint(1, 5), seconds=rng.randint(0, 43200))
        if "freq_total" in p:
            n = rng.randint(*p["freq_total"])
        else:
            freq = rng.uniform(*p["freq_per_year"])
            n = max(1, round(freq * (last_dt - start).days / 365.0))
        if n == 0:
            continue
        fracs = sorted(rng.random() for _ in range(n))
        fracs[-1] = 1.0
        span = (last_dt - start).total_seconds()
        for f in fracs:
            t = start + timedelta(seconds=f * span)
            tseq += 1
            cat = _weighted(rng, p["cats"])
            transactions.append({
                "opId": f"TRX-{tseq:05d}",
                "clientId": cid,
                "ts": _iso(t),
                "totalAmount": f"{rng.uniform(*p['ticket']):.2f}",
                "productLine": cat,
                "itemName": rng.choice(PRODUCTS[cat]),
            })

    iseq = 0
    web_start = ANCHOR - timedelta(days=90)
    for cid, (pname, _) in cust_profile.items():
        p = PROFILES[pname]
        for _ in range(rng.randint(*p["web_90d"])):
            iseq += 1
            r = rng.random()
            if r < 0.70 - p["cart_share"] / 2:
                kind, item = "WEB_SESSION", None
            elif r < 1.0 - p["cart_share"]:
                kind, item = "PRODUCT_CONSULT", rng.choice(PRODUCTS[_weighted(rng, p["cats"])])
            else:
                kind, item = "CART_LEFT", rng.choice(PRODUCTS[_weighted(rng, p["cats"])])
            event = {
                "eventId": f"EVT-{iseq:06d}",
                "clientId": cid,
                "kind": kind,
                "eventTs": _iso(_random_dt_between(rng, web_start, ANCHOR)),
            }
            if item is not None:
                event["item"] = item
            interactions.append(event)

    campaigns: list[tuple[str, datetime]] = []
    for m in range(CAMPAIGN_MONTHS):
        dt = ANCHOR - timedelta(days=30 * m + 5)
        campaigns.append((f"CAMP-{dt.year}-{dt.month:02d}", dt))
    for cid, (pname, reg_dt) in cust_profile.items():
        p = PROFILES[pname]
        for camp_id, camp_dt in campaigns:
            if camp_dt < reg_dt:
                continue
            sent = camp_dt.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(minutes=rng.randint(0, 120))
            campaign_events.append({"campId": camp_id, "clientId": cid, "action": "SEND", "actionTs": _iso(sent)})
            if rng.random() >= 0.96:
                continue
            delivered = sent + timedelta(minutes=rng.randint(2, 180))
            campaign_events.append({"campId": camp_id, "clientId": cid, "action": "DELIVER", "actionTs": _iso(delivered)})
            if rng.random() >= p["open_rate"]:
                continue
            opened = delivered + timedelta(minutes=rng.randint(10, 2880))
            campaign_events.append({"campId": camp_id, "clientId": cid, "action": "OPEN", "actionTs": _iso(opened)})
            if rng.random() >= p["click_rate"]:
                continue
            clicked = opened + timedelta(minutes=rng.randint(5, 1440))
            campaign_events.append({"campId": camp_id, "clientId": cid, "action": "CLICK", "actionTs": _iso(clicked)})

    corrupt_tx = [
        {"opId": f"TRX-{tseq + 1:05d}", "clientId": "CLI-0001", "ts": _iso(ANCHOR - timedelta(days=3)), "totalAmount": "-50.00", "productLine": "FASHION", "itemName": "Monto negativo"},
        {"opId": f"TRX-{tseq + 2:05d}", "clientId": "CLI-0002", "ts": _iso(ANCHOR - timedelta(days=4)), "totalAmount": "120.00", "productLine": "BOOKS", "itemName": "Sin clientId"},
        {"opId": f"TRX-{tseq + 3:05d}", "clientId": "CLI-0003", "ts": "fecha-invalida", "totalAmount": "999.90", "productLine": "TOYS", "itemName": "Fecha invalida"},
    ]
    corrupt_tx[1].pop("clientId")
    transactions.extend(corrupt_tx)

    customers[-1]["demographics"]["age"] = 999
    customers[-2]["memberSince"] = "2025-02-31"

    DATA_DIR.mkdir(exist_ok=True)
    meta = {
        "anchor": _iso(ANCHOR),
        "seed": SEED,
        "total_customers": len(customers),
        "profile_distribution": profile_counts,
        "totals": {
            "customers": len(customers),
            "transactions": len(transactions),
            "interactions": len(interactions),
            "campaign_events": len(campaign_events),
        },
        "invalid_records_injected": {
            "transactions": ["monto negativo", "clientId ausente", "fecha invalida"],
            "customers": ["edad fuera de rango", "memberSince invalido"],
        },
        "ground_truth": ground_truth,
    }
    for name, payload in [
        ("customers.json", customers),
        ("transactions.json", transactions),
        ("interactions.json", interactions),
        ("campaign_events.json", campaign_events),
        ("meta.json", meta),
    ]:
        (DATA_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    tx_dates = sorted(t["ts"] for t in transactions if t["ts"].endswith("Z"))
    print("Dataset del CRM simulado generado en", DATA_DIR)
    print("Clientes por perfil:", profile_counts)
    print("Totales:", meta["totals"])
    print("Rango transacciones:", tx_dates[0], "->", tx_dates[-1])
    print("Registros corruptos inyectados: 3 transacciones + 2 clientes")
    print("Ground truth (perfil real por cliente) guardado en meta.json")


if __name__ == "__main__":
    main()
