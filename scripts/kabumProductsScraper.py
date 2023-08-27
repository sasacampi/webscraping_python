import requests
from requests import Response
from bs4 import BeautifulSoup

from scripts.getProductsData import GetProductsData


class KabumProductsScraper:
    def __init__(
            self, 
            products_list: list[str], 
            output_excel_file: str) -> None:
        self.products_list = products_list
        self.output_excel_file = output_excel_file
        
        self.base_url = "https://www.kabum.com.br"

        self.__get_products_data()
    
    def __get_products_data(self) -> None:
        for product in self.products_list:
            product_urls = self.__get_product_pages_url(product)
            if product_urls:
                
                GetProductsData(self.base_url, [product_urls[0]]).main()
                # print(product_data)

    def __searched_product_page_response(self, product: str) -> Response:
        formated_product_name: str = product.replace(" ", "-")
        response = requests.get(url=f"{self.base_url}/busca/{formated_product_name}")
        if response.status_code != 200:
            print(f"Oh no! Falha ao obter lista de produtos da pesquisa: '{product}'")
        return response
    
    def __get_product_pages_url(self, product: str) -> list[str]:
        print(f"\nBuscando produto '{product}' no site: '{self.base_url}'")
        response = self.__searched_product_page_response(product)

        parsed_content = BeautifulSoup(
            response.content, "html.parser")

        total_pages_number = self.__get_total_pages_number(parsed_content)
        print(f"Total de páginas: {total_pages_number}.")

        return self.__make_pages_urls(
            current_url=response.url, 
            total_pages_number=total_pages_number+1)
    
    def __make_pages_urls(
            self, 
            current_url: str, 
            total_pages_number: int) -> list[str]:
        print("Criando lista de urls...")
        return [
            str(f"{current_url}&page_number={str(page_number)}")
            for page_number in range(1, total_pages_number)]

    def __get_total_pages_number(self, parsed_content: BeautifulSoup) -> int:
        elements = parsed_content.find(
            "div", { "id": "listingPagination" }
            ).find("ul").find_all("a")
    
        return int(max(
            [
                value.text for value in elements 
                if str(value.text).isalnum()
            ]
        ))


