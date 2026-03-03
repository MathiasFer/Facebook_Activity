import asyncio
import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


class SocialinsiderAnalyzer:

    def __init__(self, headless=False):
        self.headless = headless

    async def analyze(self, facebook_url: str):

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)

            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )

            page = await context.new_page()

            print("🌐 Abriendo Socialinsider...")
            await page.goto(
                "https://www.socialinsider.io/es/herramientas-gratuitas/herramientas-informes-redes-sociales/facebook-audit",
                wait_until="domcontentloaded",
            )

            # ----------------------------
            # 1️⃣ Escribir URL
            # ----------------------------
            input_selector = "input[formcontrolname='profileInput']"
            await page.wait_for_selector(input_selector)

            print("✏ Escribiendo URL...")
            await page.click(input_selector)
            await page.keyboard.type(facebook_url, delay=40)

            # ----------------------------
            # 2️⃣ Esperar botón habilitado
            # ----------------------------
            await page.wait_for_function(
                """
                () => {
                    const btn = document.querySelector("button[type='submit']");
                    return btn && !btn.disabled;
                }
            """
            )

            print("🚀 Click en Check...")
            await page.locator("button[type='submit']").click(force=True)

            # ----------------------------
            # 3️⃣ Detectar resultado
            # ----------------------------

            try:
                # ❌ Caso: No existe
                await page.wait_for_selector("div.border-red-500", timeout=5000)
                print("❌ Página no existe")
                await browser.close()
                return {"status": "no_existe"}

            except PlaywrightTimeout:
                pass

            try:
                # ⚠ Caso: Inactiva últimos 30 días
                await page.wait_for_selector(
                    "text=There are no posts published by this profile in the last 30 days",
                    timeout=5000,
                )
                print("⚠ Página inactiva últimos 30 días")
                await browser.close()
                return {"status": "inactiva_30_dias"}

            except PlaywrightTimeout:
                pass

            # ----------------------------
            # 4️⃣ Si no fue ninguno → Hay análisis
            # ----------------------------

            print("📊 Buscando bloque de análisis...")

            analysis_selector = (
                "div.grid.grid-cols-1.si-tablet-and-mobile\\:grid-cols-12"
            )

            await page.wait_for_selector(analysis_selector, timeout=10000)

            # Scroll para asegurar carga completa
            await page.mouse.wheel(0, 1500)
            await page.wait_for_timeout(2000)

            # Extraer ambos bloques (Contenido + Engagement)
            blocks = page.locator(analysis_selector)
            count = await blocks.count()

            analysis_text_raw = []

            for i in range(count):
                text = await blocks.nth(i).inner_text()
                analysis_text_raw.append(text)

            full_text = "\n".join(analysis_text_raw)

            # -----------------------------
            # Extraer números correctamente
            # -----------------------------

            numbers = re.findall(r"\d+\.?\d*", full_text)

            # Esperado:
            # [131, 4.37, 1729, 13.2]

            if len(numbers) >= 4:
                total_posts = int(float(numbers[0]))
                avg_posts_per_day = float(numbers[1])
                engagement_total = int(float(numbers[2]))
                avg_engagement = float(numbers[3])
            else:
                total_posts = 0
                avg_posts_per_day = 0
                engagement_total = 0
                avg_engagement = 0

            # -----------------------------
            # Clasificación de actividad
            # -----------------------------

            if avg_posts_per_day >= 0.23:
                activity_level = "alta"
            elif 0.10 <= avg_posts_per_day < 0.23:
                activity_level = "media"
            elif 0.03 <= avg_posts_per_day < 0.10:
                activity_level = "baja"
            else:
                activity_level = "inactiva"

            print("✅ Página activa detectada")

            await browser.close()

            return {
                "status": "activa",
                "total_posts_30d": total_posts,
                "avg_posts_per_day": avg_posts_per_day,
                "engagement_total": engagement_total,
                "avg_engagement": avg_engagement,
                "nivel_actividad": activity_level,
            }
