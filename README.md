# Facebook Page Analyzer

Este proyecto automatiza el análisis de páginas de Facebook utilizando la herramienta de auditoría de Socialinsider. Procesa una lista de URLs desde un archivo Excel y determina si están activas, su nivel de actividad reciente y genera un reporte consolidado.

## 🚀 Características

- **Procesamiento Secuencial**: Analiza las URLs una por una para mayor estabilidad.
- **Auditoría Automatizada**: Utiliza Playwright para interactuar con la herramienta gratuita de Socialinsider.
- **Guardado Incremental**: Guarda el progreso en el archivo de salida cada 5 registros procesados para evitar pérdida de datos.
- **Delays Inteligentes**: Implementa esperas aleatorias (3-6s) entre peticiones para evitar bloqueos.
- **Manejo de Errores**: Identifica páginas inexistentes, inactivas o con errores de carga.

## 📋 Requisitos

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)
- Pandas y Openpyxl (para manejo de Excel)

## 🛠️ Instalación

1. Clona el repositorio o descarga los archivos.
2. Crea un entorno virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```powershell
   pip install pandas playwright openpyxl
   ```
4. Instala los navegadores necesarios para Playwright:
   ```powershell
   playwright install chromium
   ```

## 📖 Uso

1. Prepara un archivo llamado `datos.xlsx` en la raíz del proyecto. Debe contener una columna llamada `url` con los enlaces de Facebook a analizar.
2. Ejecuta el script principal:
   ```powershell
   python .\main.py
   ```
3. El script abrirá el navegador (modo no-headless) y procesará las URLs secuencialmente.
4. Al finalizar (o cada 5 registros), se generará/actualizará el archivo `resultado_procesado.xlsx` con los resultados.

## ⚙️ Estructura del Proyecto

- `excel_batch_runner.py`: Lógica principal de procesamiento del Excel y control de flujo.
- `scraper_analyzer.py`: Clase `SocialinsiderAnalyzer` que realiza el scraping de la web.
- `main.py`: Punto de entrada del script.
- `.gitignore`: Configurado para ignorar entornos virtuales, caché y archivos de datos personales.

## 📊 Lógica de Clasificación

- **Activa**: Si se detectan publicaciones en los últimos 30 días. Se reporta el nivel de actividad (ALTA, MEDIA, BAJA).
- **Inactiva**: Si no hay posts en los últimos 30 días.
- **No existe**: Si la herramienta de auditoría no encuentra el perfil.
- **Error**: En caso de fallos técnicos durante el análisis de esa URL específica.
