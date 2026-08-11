import argparse, asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright


async def main(config_path: Path):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    out = Path("assets/landing")
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport=config.get("viewport", {"width": 1280, "height": 720}))
        page = await context.new_page()
        for item in config["pages"]:
            await page.goto(item["url"], wait_until="networkidle")
            await page.screenshot(path=out / f"{item['name']}.png", full_page=item.get("full_page", True))
            print(item["name"], page.url)
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    asyncio.run(main(args.config))

