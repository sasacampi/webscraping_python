import requests
from requests import Response
from bs4 import BeautifulSoup

import pandas as pd

from scripts.getProductsData import GetProductsData


class KabumProductsScraper:
    def __init__(
            self, 
            products_list: list[str], 
            output_excel_file: str) -> None:
        self.products_list = products_list
        self.output_excel_file = output_excel_file
        
        self.base_url = "https://www.kabum.com.br"

        self.result_dataframe = pd.DataFrame()

        self.__get_products_data()
    
    def __get_products_data(self) -> None:
        for product in self.products_list:
            product_urls = self.__get_product_pages_url(product)
            
            if product_urls:
                data = GetProductsData(
                    base_url=self.base_url, 
                    product_name=product,
                    product_urls=product_urls).main()
                
                self.result_dataframe = pd.concat(
                    [self.result_dataframe, data], 
                    ignore_index=True)
            else:
                print(f"Falha ao obter os dados do produto: {product}")

        if not self.result_dataframe.empty:
            print(f"\nObtenção dos dados finalizado, exportando arquivo '{self.output_excel_file}'")

            print(self.result_dataframe)
            self.result_dataframe.to_excel(self.output_excel_file, index=False)
        else:
            print("\nObtenção dos dados não foi bem sucedida!")

    def __searched_product_page_response(self, product: str) -> Response:
        formated_product_name: str = product.replace(" ", "-")
        response = requests.get(url=f"{self.base_url}/busca/{formated_product_name}")
        if response.status_code != 200:
            print(f"Falha ao obter lista de produtos da pesquisa: '{product}'")
        return response
    
    def __get_product_pages_url(self, product: str) -> list[str]:
        print(f"\nBuscando produto '{product}' no site: '{self.base_url}'")
        response = self.__searched_product_page_response(product)

        parsed_content = BeautifulSoup(
            response.content, "html.parser")

        if self.__product_exist(parsed_content):
            total_pages_number = self.__get_total_pages_number(
                parsed_content)
            
            if isinstance(total_pages_number, int):
                print(f"Total de páginas: {total_pages_number}.")

                return self.__make_pages_urls(
                    current_url=response.url, 
                    total_pages_number=total_pages_number+1)
            else:
                print(f"\nFalha ao obter o número total de páginas do produto: '{product}'!\n")
                return []
        else:
            print(f"\nProduto: '{product}' não foi encontrado!\n")
            return []
    
    def __product_exist(self, parsed_content: BeautifulSoup) -> bool:
        try:
            product_not_found_element = parsed_content.find(
                "div", { "id": "listingEmpty" }
                ).find("b").text
            if product_not_found_element:
                return False
            return True
        except:
            return True
        
    def __make_pages_urls(
            self, 
            current_url: str, 
            total_pages_number: int) -> list[str]:
        print("Criando lista de urls...\n")
        
        url_list = [
            str(f"{current_url}&page_number={str(page_number)}")
            for page_number in range(2, total_pages_number)]
        url_list.append(current_url)

        return url_list
    
    def __get_total_pages_number(self, parsed_content: BeautifulSoup) -> int | bool:
        try:
            elements = parsed_content.find(
                "div", { "id": "listingPagination" }
                ).find("ul").find_all("a")
        
            return int(max(
                [
                    value.text for value in elements 
                    if str(value.text).isalnum()
                ]
            ))
        except:
            return False
