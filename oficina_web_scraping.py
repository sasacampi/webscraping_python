import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

fabricantes = ["amd", "nvidia", "intel"]
sessao = requests.session()
anuncios_obtidos = []

def iniciar_scraper():
    procurar()
    if anuncios_obtidos:
        extrair()

def procurar():
    for fabricante in fabricantes:

    numero_pagina_atual = 1
    while True:
        pagina_produtos = obter_paginas_anuncios(fabricantes, numero_pagina_atual)
        anuncios = pagina_produtos["anuncios"]
        ultima_pagina = pagina_produtos["ultima_pagina"]
        
        for anuncio in anuncios:
            url_produtos = anuncio.select("a")[0].attrs["href"]
            anuncios_obtidos.append(f"https://www.kabum.com.br{url_produtos}")
            
        if ultima_pagina == "true":
            break
        
        numero_pagina_atual += 1

def obter_paginas_anuncios(fabricante, numero_pagina_atual):
    url_produtos = f"https://www.kabum.com.br/hardware/placa-de-video-vga/placa-de-video-{fabricante}?page_number={numero_pagina_atual}&page_size=100&facet_filters=eyJwcmljZSI6eyJtaW4iOjEzOSwibWF4Ijo0NDU4My45fX0=&sort=most_searched"
    pagina_produtos = sessao.get(url_produtos)
    pagina_parseada = BeautifulSoup(pagina_produtos.text, "html.parser")
    anuncios = pagina_parseada.select(".productCard")
    ultima_pagina = pagina_parseada.select(".nextLink")[0].attrs["aria-disabled"]
    return {"anuncios": anuncios, "ultima_pagina": ultima_pagina}

def extrair():
    qtd_extraidos = 0

    for url_anuncio in anuncios_obtidos:
        pagina_anuncio = sessao.get(url_anuncio)
        pagina_parseada = BeautifulSoup(pagina_anuncio.text, "html.parser")

        titulo = pagina_parseada.select(".dDYTAu")[0].text
        a_vista = pagina_parseada.select(".finalPrice")[0].text

        try:
            a_prazo = pagina_parseada.select(".regularPrice")[0].text
        except Exception:
            a_prazo = "Consultar valor."
        
        titulo = titulo.strip()
        a_vista = corrigir_valor_monetario(a_vista)
        a_prazo = corrigir_valor_monetario(a_prazo)

        print(f"Produto: {titulo}")
        print(f"Preço à vista: {a_vista}")
        print(f"Preço a prazo: {a_prazo}")
        print("=" * 40)
        
        qtd_extraidos += 1

def corrigir_valor_monetario(valor_original):
    valor_original = valor_original.replace('Â', '').replace('\xa0', ' ')
    valor_corrigido = valor_original.encode('iso-8859-1').decode('utf-8')
    return valor_corrigido.replace("R$ ", "").replace(".", "").replace(",", ".")

iniciar_scraper()
