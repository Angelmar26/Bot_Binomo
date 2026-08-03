import pandas as pd
import numpy as np

def analizar_mercado(df):
    """
    df: DataFrame con las últimas velas (Open, High, Low, Close, Volume)
    Retorna: 'CALL', 'PUT' o None, junto con la temporalidad sugerida (1-5 min)
    """
    close = df['close']
    
    # 1. Calcular Indicadores
    # EMAs
    ema_20 = close.ewm(span=20, adjust=False).mean()
    ema_50 = close.ewm(span=50, adjust=False).mean()
    ema_200 = close.ewm(span=200, adjust=False).mean()
    
    # RSI (Periodo 14)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Bandas de Bollinger (Periodo 20, Desviación 2)
    sma_20 = close.rolling(window=20).mean()
    std_20 = close.rolling(window=20).std()
    upper_band = sma_20 + (std_20 * 2)
    lower_band = sma_20 - (std_20 * 2)
    
    # Variables de la última vela cerrada
    precio_actual = close.iloc[-1]
    e20 = ema_20.iloc[-1]
    e50 = ema_50.iloc[-1]
    e200 = ema_200.iloc[-1]
    r_actual = rsi.iloc[-1]
    r_anterior = rsi.iloc[-2]
    up_b = upper_band.iloc[-1]
    low_b = lower_band.iloc[-1]
    
    # 2. Análisis de Volatilidad para Temporalidad Dinámica (1 a 5 min)
    # Si las bandas están muy separadas (alta volatilidad), sugerimos 3 o 5 min. 
    # Si están estrechas, 1 o 2 min.
    ancho_bandas = up_b - low_b
    promedio_ancho = (upper_band - lower_band).rolling(window=50).mean().iloc[-1]
    
    if ancho_bandas > (promedio_ancho * 1.2):
        temporalidad = "5 Minutos ⏱️ (Alta volatilidad, darle respiro al precio)"
    elif ancho_bandas < (promedio_ancho * 0.8):
        temporalidad = "1 a 2 Minutos ⚡ (Movimiento rápido en rango estrecho)"
    else:
        temporalidad = "3 Minutos ⏱️ (Temporalidad estándar óptima)"

    # 3. Filtros de Alta Precisión (Cero Ruido)
    senal = None
    
    # Condición de COMPRA (CALL)
    # - Precio cerca o tocando la Banda Inferior
    # - RSI cruzando hacia arriba desde el nivel de sobreventa (<= 30)
    # - Tendencia alcista o soporte en EMA 50 / 200
    if (precio_actual <= low_b * 1.002) and (r_anterior <= 30 and r_actual > 30) and (e20 > e50):
        senal = "CALL 🟢 (Compra)"
        
    # Condición de VENTA (PUT)
    # - Precio cerca o tocando la Banda Superior
    # - RSI cruzando hacia abajo desde el nivel de sobrecompra (>= 70)
    # - Tendencia bajista por debajo de las EMAs
    elif (precio_actual >= up_b * 0.998) and (r_anterior >= 70 and r_actual < 70) and (e20 < e50):
        senal = "PUT 🔴 (Venta)"
        
    return senal, temporalidad
