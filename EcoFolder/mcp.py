# Se implementa el MCP para análisis financiero y simulación de escenarios

import pandas as pd

def analizar_finanzas(df: pd.DataFrame) -> dict:
    ingresos = df.loc[df["tipo"] == "ingreso", "monto"].sum()
    gastos = df.loc[df["tipo"] == "gasto", "monto"].sum()
    flujo = ingresos - gastos
    ahorro = (flujo / ingresos) if ingresos > 0 else 0
    return {"ingresos": ingresos, "gastos": gastos, "flujo": flujo, "ahorro": ahorro}

def simular_escenario(df: pd.DataFrame, var_ing: float, var_gas: float) -> dict:
    df_sim = df.copy()
    df_sim.loc[df_sim["tipo"] == "ingreso", "monto"] *= (1 + var_ing)
    df_sim.loc[df_sim["tipo"] == "gasto", "monto"] *= (1 + var_gas)
    return analizar_finanzas(df_sim)
