import asyncio
import random
import pandas as pd
from scraper_analyzer import SocialinsiderAnalyzer


async def procesar_excel(ruta_archivo):
    # 1. Leer el Excel
    df = pd.read_excel(ruta_archivo)
    df["actividad"] = df["actividad"].astype("object")
    df["eliminar"] = df["eliminar"].astype("object")
    # Asegurar que las columnas existan
    if "eliminar" not in df.columns:
        df["eliminar"] = ""
    if "actividad" not in df.columns:
        df["actividad"] = ""

    analyzer = SocialinsiderAnalyzer(headless=False)
    
    print(f"🚀 Iniciando procesamiento secuencial de {len(df)} URLs...")

    # 2. Procesar una por una
    for index, row in df.iterrows():
        url = row["url"]
        num_registro = index + 1
        print(f"\n🔎 [{num_registro}/{len(df)}] Analizando: {url}")

        try:
            resultado = await analyzer.analyze(url)

            if resultado["status"] == "activa":
                df.at[index, "eliminar"] = "NO"
                df.at[index, "actividad"] = resultado["nivel_actividad"].upper()
                print(f"✅ Activa: {resultado['nivel_actividad']}")
            
            elif resultado["status"] in ["no_existe", "inactiva_30_dias"]:
                df.at[index, "eliminar"] = "SI"
                df.at[index, "actividad"] = "INACTIVA"
                print(f"⚠️ Inactiva o no existe ({resultado['status']})")
            
            elif resultado["status"] == "revisar_manual":
                # No modificamos la columna 'eliminar'
                df.at[index, "actividad"] = "REVISAR"
                print(f"❓ Requiere revisión manual")

        except Exception as e:
            print(f"❌ Error con {url}: {e}")
            df.at[index, "eliminar"] = "SI"
            df.at[index, "actividad"] = "ERROR"

        # 3. Guardado incremental cada 5 registros
        if num_registro % 5 == 0:
            print(f"💾 Guardando progreso incremental ({num_registro} registros)...")
            df.to_excel("resultado_procesado.xlsx", index=False)

        # 4. Delay aleatorio entre 3 y 6 segundos (excepto en la última)
        if index < len(df) - 1:
            delay = random.uniform(3, 6)
            print(f"⏳ Esperando {delay:.2f} segundos...")
            await asyncio.sleep(delay)

    # 5. Guardar resultado final
    df.to_excel("resultado_procesado.xlsx", index=False)
    print("\n✅ Proceso completado. Archivo guardado como: resultado_procesado.xlsx")


if __name__ == "__main__":
    archivo_entrada = "datos.xlsx"
    asyncio.run(procesar_excel(archivo_entrada))

