# Asistente Financiero Inteligente

*Splicación interactiva desarrollada con **Streamlit* que permite analizar, simular y optimizar la salud financiera de una empresa.   
Integra análisis automatizados, visualizaciones dinámicas, simuladores de escenarios y un asistente IA impulsado por *Gemini*.

---

## 🚀 Características principales

- *Dashboard financiero:* Visualización interactiva de ingresos, gastos y flujo de caja.  
- *Simulador What-If:* Prueba escenarios de variaciones en ingresos o gastos y observa el impacto.  
- *Asistente IA (Gemini):* Haz preguntas sobre tus finanzas y recibe análisis con recomendaciones.  
- *Optimizador inteligente:* Prototipo para optimización financiera (requiere optimizer.py).  
- *Salud Financiera 360:* Evalúa la estabilidad, ahorro y diversificación con un puntaje global.  
- *Detector de anomalías:* Identifica comportamientos financieros atípicos mediante IA (Isolation Forest).  

---

## 🏗 Arquitectura general del proyecto


FinMind-MCP/
│
├── app.py                   # Punto de entrada principal de la aplicación Streamlit
├── gemini.py                # Módulo del asistente financiero IA (Gemini API)
├── mcp.py                   # Motor de Cálculo Financiero Principal (MCP)
├── health.py                # Cálculo del índice de salud financiera y detección de anomalías
├── utils.py                 # Utilidades: carga de datos, validación, KPIs y dashboards
├── optimizer.py             # (Opcional) Módulo para optimización inteligente
├── Components         #Carpeta con todos los componentes del front 
└── .env                     # Clave de API de Gemini (no subir al repositorio)


---

## ⚙ Guía básica de ejecución

### 1. *Requisitos previos*

- Python 3.9 o superior  
- Clave de API de *Google Gemini* (modelo gemini-2.5-flash)  
- Librerías necesarias instaladas

### 2. *Instalación*

bash
# Clonar el repositorio
git clone https://github.com/tuusuario/FinMind-MCP.git
cd FinMind-MCP

# Crear entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt


Ejemplo de requirements.txt recomendado:

streamlit
pandas
plotly
numpy
scikit-learn
google-generativeai
python-dotenv
openpyxl


---

### 3. *Configurar la API de Gemini*

Crea un archivo .env en la raíz del proyecto con tu clave de API:

bash
GEMINI_API_KEY=tu_clave_de_api_aquí


---

### 4. *Ejecutar la aplicación*

bash
streamlit run app.py


Abre en tu navegador: [http://localhost:8501](http://localhost:8501)

---

## 🧠 Flujo general de la aplicación

1. *Inicio:* Se muestra una landing page antes de acceder a la app principal.  
2. *Carga de datos:* El usuario sube un Excel o usa datos de ejemplo (utils.py).  
3. *Análisis financiero:* El módulo mcp.py calcula ingresos, gastos, flujo y ahorro.  
4. *Visualización:* utils.py y plotly generan dashboards y KPIs.  
5. *Simulación:* El usuario puede ajustar ingresos/gastos y ver resultados instantáneamente.  
6. *Asistente IA:* gemini.py analiza los datos y responde consultas personalizadas.  
7. *Salud financiera:* health.py evalúa estabilidad y detecta anomalías en el flujo mensual.

---

@Gadiro 
y esto
───────────────────────────────────────────────
💹 FINMIND MCP — MAPA CONCEPTUAL DE ARQUITECTURA
───────────────────────────────────────────────

               👤 USUARIO
                   │
                   ▼
        ┌──────────────────────────┐
        │     FRONTEND (Streamlit) │
        │        ──────────────    │
        │ • app.py                 │
        │ • Interfaz UI            │
        │ • Dashboard              │
        │ • Simulador What-If      │
        │ • Asistente IA           │
        │ • Salud Financiera 360   │
        └──────────┬───────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │  SERVIDOR MCP (Backend)  │
        │       ────────────────   │
        │ • utils.py  → carga y validación de datos
        │ • mcp.py    → análisis financiero base
        │ • health.py → índice de salud y anomalías
        │ • gemini.py → conexión con API Gemini
        │ • optimizer.py → optimizador inteligente
        └──────────┬───────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │     CAPA DE DATOS        │
        │        ──────────        │
        │ • Archivo Excel (.xlsx)  │
        │ • pandas DataFrame       │
        │ • Procesamiento en memoria
        └──────────┬───────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │    SERVICIOS EXTERNOS    │
        │       ──────────────     │
        │ • Google Gemini API      │
        │   ↳ Procesa consultas IA │
        │ • .env                   │
        │   ↳ Clave segura API     │
        └──────────┬───────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │     SALIDA / OUTPUTS     │
        │        ───────────       │
        │ • KPIs y métricas        │
        │ • Dashboards dinámicos   │
        │ • Simulaciones What-If   │
        │ • Reporte de salud 360   │
        │ • Respuestas del Asistente IA
        └──────────────────────────┘

───────────────────────────────────────────────
🔁 FLUJO RESUMIDO
───────────────────────────────────────────────
👤 Usuario 
   ↓
📊 Streamlit (Frontend)
   ↓
⚙ MCP (Procesamiento financiero)
   ↓
🧮 DataFrame (Datos procesados)
   ↓
🤖 Gemini API (Asistente IA)
   ↓
📈 Resultados visuales + Recomendaciones
───────────────────────────────────────────────