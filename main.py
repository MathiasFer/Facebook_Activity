import asyncio
from scraper_analyzer import SocialinsiderAnalyzer
from excel_batch_runner import procesar_excel


async def main():

    # ----------------------------
    # MODO 1 → TEST INDIVIDUAL
    # ----------------------------
    modo_test = False  # cambia a True si quieres probar un solo link

    if modo_test:
        test_url = "https://www.facebook.com/RCNoticiasQRoo/#"

        analyzer = SocialinsiderAnalyzer(headless=False)
        result = await analyzer.analyze(test_url)

        print("\n========== RESULTADO ==========")
        print(result)

    # ----------------------------
    # MODO 2 → PROCESAR EXCEL
    # ----------------------------
    else:
        ruta_excel = "datos.xlsx"
        await procesar_excel(ruta_excel)


if __name__ == "__main__":
    asyncio.run(main())
