import asyncio
from playwright.async_api import async_playwright
import time
import pandas as pd


async def main():
    url = 'https://webscraper.io/test-sites/e-commerce/allinone'
    async with async_playwright() as p:
        firefox = p.firefox
        browser = await firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
        descriptions = await page.eval_on_selector_all('.caption > .description', 'elements => elements.map(el => el.textContent) ')
        names = await page.eval_on_selector_all('.caption > h4 > .title', 'elements => elements.map(el => el.title) ')
        urls = await page.eval_on_selector_all('.caption > h4 > .title', 'elements => elements.map(el => el.href) ')
        prices = await page.eval_on_selector_all('.caption > .price', 'elements => elements.map(el => el.textContent) ') 
        df = pd.DataFrame({
            'name': names,
            'description': descriptions,
            'price': prices,
            'url': urls
        })
        # remove duplicate name of the item from description
        df['description'] = df.apply(lambda x: x['description'].replace(x['name'],''), axis=1)
        df.to_csv("../result.csv")
        print("done")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
