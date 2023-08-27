import aiohttp
import asyncio
from asyncio import gather

import pandas as pd

from bs4 import BeautifulSoup

class GetProductsData:
    def __init__(self, base_url: str, product_urls: list[str]) -> None:
        self.base_url = base_url
        self.product_urls = product_urls

        self.range_urls_maximum_number: int = 5

    def main(self) -> pd.DataFrame:
        
        for url_product_range in self.__create_urls_range():
            asyncio.run(
                self.__get_range_pages_data(
                    url_product_range
                )
            )
    
    async def __get_range_pages_data(self, url_product_range: list[str]) -> list:
        coroutines: list = []

        for url in url_product_range:
            coroutines.append(self.__get_url_product_data(url))

        await gather(*coroutines)
    
    async def __get_url_product_data(self, url: str) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            response_text = await response.read()
                            products_data = self.__get_products_data(response_text)

                            print(products_data)
                except aiohttp.ContentTypeError as error:
                    print(f"Erro ao obter dados da url: '{url}'", error)
        except aiohttp.ContentTypeError as error:
            print(f"Erro ao obter dados da url: '{url}'", error)

    def __get_products_data(self, response_text: str) -> dict[list]:
        parsed_content = BeautifulSoup(response_text, 'html.parser')

        products_elements = parsed_content.findAll(
            "a", { "class": "productLink" }
            )
        
        return [
            {
                "product_url": "".join((self.base_url, str(product.get("href")))),
                "product_title": str(product.find("img").get("title")),
                "product_price": str(product.find('span', {'class' : 'priceCard'}).text).replace('Â', '').replace('\xa0', ' '),
                "freeshipping": True if product.find('div', {'class' : 'freeShippingTagCard'}) is not None else False
            }
            for product in products_elements
        ]

    def __create_urls_range(self) -> list[list]:
        result: list[list] = []
        
        num_lists = len(self.product_urls) // self.range_urls_maximum_number

        for i in range(num_lists):
            current_range = self.product_urls[
                i*self.range_urls_maximum_number:(i+1)*self.range_urls_maximum_number]
            result.append(current_range)

        remaining_values = len(self.product_urls) % self.range_urls_maximum_number
        
        if remaining_values > 0:
            last_range = self.product_urls[-remaining_values:]
            result.append(last_range)

        return result
