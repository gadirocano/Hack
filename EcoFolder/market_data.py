# market_data.py
"""
Módulo simple para obtener datos de mercado externos.
Por defecto devuelve datos mock; puedes extenderlo para conectar APIs (AlphaVantage, Yahoo, banco central).
"""

import pandas as pd
from datetime import datetime

def datos_mercado_mock() -> dict:
    """
    Retorna diccionario con tasas e indicadores básicos.
    """
    return {
        "fecha": datetime.utcnow().isoformat(),
        "tasa_interes_referencia_pct": 11.5,  # ejemplo
        "inflacion_anual_pct": 4.2,
        "rendimiento_sector_promedio_pct": 8.0,
        "condiciones_credito": "moderado"
    }

def obtener_datos_mercado(api_key: str = None, fuente: str = "mock") -> dict:
    """
    Si 'fuente' == 'mock' retorna el mock; si quieres, implementa lógica para conectarte a APIs.
    """
    if fuente == "mock":
        return datos_mercado_mock()
    # placeholder para integraciones reales
    raise NotImplementedError("Conectar API real si es necesario.")
