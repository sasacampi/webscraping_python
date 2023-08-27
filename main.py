from scripts.kabumProductsScraper import KabumProductsScraper

if __name__ == "__main__":
    KabumProductsScraper(
        products_list=[
            "computador amd",
            "monitor dell",
            'mouse razer'
        ],
        output_excel_file="kabum_products.xlsx")
