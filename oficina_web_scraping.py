import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

fabricantes = "nvidia"
#fabricantes = ["amd", "intel", "nvidia"]
sessao = requests.session()
anuncios_obtidos = []

def iniciar_scraper():
    procurar()
    if anuncios_obtidos:
        extrair()


def procurar():
    numero_pagina_atual = 1
    pagina_produtos = obter_pagina_anuncios(fabricante, numero_pagina_atual)
    anuncios = pagina_produtos["anuncios"]
    ultima_pagina = pagina_produtos["ultima_pagina"]


while True:
for anuncio in anuncios:
    url_produtos = anuncio.select("a")[0].attrs["href"]
    anuncios_obtidos.append(f"www.kabum.com.br{url_produtos}")
   
    if ultima_pagina == "true" :
    break 

    numero_pagina_atual += 1 
    pagina_parseada = obter_paginas_anuncios(fabricantes, numero_pagina_atual)
    anuncios = proxima_pagina["anuncios"]
    ultima_pagina = proxima_pagina["ultima_pagina"]

def obter_paginas_anuncios(fabricantes, numero_pagina_atual):
    url_produtos = f"https://www.kabum.com.br/hardware/placa-de-video-vga/placa-de-video-{fabricante}?page_number={numero_da_pagina_atual}&page_size=100&facet_filters=eyJwcmljZSI6eyJtaW4iOjEzOSwibWF4Ijo0NDU4My45fX0=&sort=most_searched"
    pagina_produtos = sessao.get(url_produtos)
    pagina_parseada = BeautifulSoup(pagina_produtos.text, "html.parser")
    anuncios = pagina_parseada.select(."productCard")
    ultima_pagina = pagina_parseada.select(".nextLink")[0].attrs["aria.disabled"]
    return ("anuncios": anuncios, "ultima_pagina": ultima_pagina)

def extrair():
    qtd_extraidos = 0

    for url_anuncio in anuncios_obtidos:
        pagina_anuncio = sessao.get(url_anuncio)
        pagina_parseada = BeautifulSoup(pagina_anuncio.text, "html.parser")


    pass
                        
                
def corrigir_valor_monetario(valor_original):
    valor_original = valor_original.replace('Â', '').replace('\xa0', ' ')
    valor_corrigido = valor_original.encode('iso-8859-1').decode('utf-8')
    return valor_corrigido.replace("R$ ", "").replace(".", "").replace(",", ".")


iniciar_scraper()