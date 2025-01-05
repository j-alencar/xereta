from lib.scraper import ScraperEnjoei

def main():
    # demo
    enjoei = ScraperEnjoei()
    products = enjoei.get_products("focusrite")
    print(products)

if __name__ == "__main__":
    main()