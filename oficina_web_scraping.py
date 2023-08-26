import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

fabricantes = ["nvidia"]
#fabricantes = ["amd", "intel", "nvidia"]
sessao = requests.session()
anuncios_obtidos = []

def iniciar_scraper():
    procurar()
    if anuncios_obtidos:
        extrair()


def procurar():
    url_produtos = "https://www.kabum.com.br/hardware/placa-de-video-vga/placa-de-video-nvidia?page_number=1&page_size=100&facet_filters=eyJwcmljZSI6eyJtaW4iOjEzOSwibWF4Ijo0NDU4My45fX0=&sort=most_searched"
    pagina_produtos = sessao.get(url_produtos)
    pagina_parseada = BeautifulSoup(pagina_produtos.text, "html.parser")
   pass


def extrair():
    pass
                        
                
def corrigir_valor_monetario(valor_original):
    valor_original = valor_original.replace('Â', '').replace('\xa0', ' ')
    valor_corrigido = valor_original.encode('iso-8859-1').decode('utf-8')
    return valor_corrigido.replace("R$ ", "").replace(".", "").replace(",", ".")


iniciar_scraper()