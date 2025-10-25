import numpy as np
import pandas as pd
from transformers import pipeline

# -----------------------------------------------------
# IA local: zero-shot (funciona sin conexión ni API Key)
# -----------------------------------------------------
_IA = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# -----------------------------------------------------
# Limpieza y normalización flexible
# -----------------------------------------------------
def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas aunque vengan con acentos o minúsculas."""
    df = df.copy()
    # Limpieza de nombres
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace("ó", "o")
        .str.replace("í", "i")
        .str.replace("é", "e")
        .str.replace("á", "a")
        .str.replace("ú", "u")
        .str.replace(" ", "")
    )

    # Verificar columnas básicas
    if not {"descripcion", "monto", "tipo"}.issubset(df.columns):
        raise ValueError("Tu archivo debe tener columnas: Descripcion, Monto y Tipo (Ingreso/Gasto)")

    # Normalización
    df["Descripcion"] = df["descripcion"].astype(str)
    df["Monto"] = pd.to_numeric(df["monto"], errors="coerce").fillna(0)
    df["Tipo"] = np.where(df["tipo"].str.lower().str.contains("ingre"), "Ingreso", "Gasto")

    # Categorías automáticas o existentes
    if "categoria" in df.columns:
        df["Categoria"] = df["categoria"].fillna("Otros")
    else:
        df["Categoria"] = df["Descripcion"].apply(_clasificar)

    return df

# -----------------------------------------------------
# Clasificación IA local
# -----------------------------------------------------
def _clasificar(texto: str) -> str:
    categorias = [
        "Transporte", "Energía", "Alimentación",
        "Vivienda", "Salud", "Educación", "Ocio", "Otros"
    ]
    try:
        res = _IA(texto, categorias)
        return res["labels"][0]
    except Exception:
        return "Otros"

# -----------------------------------------------------
# Análisis financiero
# -----------------------------------------------------
def analizar_finanzas(df: pd.DataFrame) -> dict:
    ingresos = df.loc[df["Tipo"] == "Ingreso", "Monto"].sum()
    gastos = df.loc[df["Tipo"] == "Gasto", "Monto"].sum()
    flujo = ingresos - gastos
    ratio_ahorro = (flujo / ingresos) if ingresos > 0 else 0
    gastos_por_cat = (
        df[df["Tipo"] == "Gasto"]
        .groupby("Categoria")["Monto"]
        .sum()
        .to_dict()
    )
    return {
        "ingresos": ingresos,
        "gastos": gastos,
        "flujo": flujo,
        "ratio_ahorro": ratio_ahorro,
        "gastos_por_cat": gastos_por_cat,
    }

# -----------------------------------------------------
# Simulador What-If
# -----------------------------------------------------
def simular_escenario(df: pd.DataFrame, ajustes: dict) -> dict:
    df = df.copy()
    if "Ingresos" in ajustes:
        df.loc[df["Tipo"] == "Ingreso", "Monto"] *= (1 + ajustes["Ingresos"])
    for cat, delta in ajustes.items():
        if cat == "Ingresos":
            continue
        mask = (df["Tipo"] == "Gasto") & (df["Categoria"].str.lower() == cat.lower())
        df.loc[mask, "Monto"] *= (1 + delta)
    return analizar_finanzas(df)

# -----------------------------------------------------
# Recomendaciones IA locales
# -----------------------------------------------------
TIPS_FINANCIEROS = [
    "Reduce tus gastos variables antes que los fijos.",
    "Asigna al menos un 10% de tus ingresos al ahorro mensual.",
    "Negocia tarifas o suscripciones anuales para reducir costos.",
    "Evita deudas con alto interés o pagos diferidos.",
    "Establece un presupuesto por categoría de gasto.",
    "Destina parte de tus ingresos a inversión segura o educación financiera."
]

def generar_recomendaciones(df: pd.DataFrame, analitica: dict) -> list[str]:
    perfil = (
        f"Ingresos {analitica['ingresos']:.2f}, "
        f"Gastos {analitica['gastos']:.2f}, "
        f"Flujo {analitica['flujo']:.2f}, "
        f"Ahorro {analitica['ratio_ahorro']*100:.1f}%."
    )
    try:
        res = _IA(perfil, TIPS_FINANCIEROS)
        orden = sorted(zip(res["labels"], res["scores"]), key=lambda x: x[1], reverse=True)
        return [t for t, _ in orden[:3]]
    except Exception:
        return TIPS_FINANCIEROS[:3]
