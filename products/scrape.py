
from bs4 import BeautifulSoup
import requests
from .models import Game

base_urls=[
    'https://www.consolemad.co.uk/product-category/atari/atari-2600-games/',
    'https://www.consolemad.co.uk/product-category/commodore/c64-cartridges/',
    'https://www.consolemad.co.uk/product-category/commodore/cd32-games/',
    'https://www.consolemad.co.uk/product-category/microsoft/xbox/uk-xbox-games/',
    'https://www.consolemad.co.uk/product-category/microsoft/xbox-360/uk-xbox-360-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/game-boy/uk-game-boy-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/game-boy-advance/uk-game-boy-advance-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/game-boy-color/uk-game-boy-color-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/gamecube/uk-gamecube-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/nes/uk-nes-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/nintendo-3ds/uk-3ds-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/nintendo-64/uk-n64-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/nintendo-ds/uk-ds-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/snes/uk-snes-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/wii/uk-wii-games/',
    'https://www.consolemad.co.uk/product-category/nintendo/wii-u/uk-wii-u-games/',
    'https://www.consolemad.co.uk/product-category/sega/dreamcast/uk-dreamcast-games/',
    'https://www.consolemad.co.uk/product-category/sega/game-gear/uk-game-gear-games/',
    'https://www.consolemad.co.uk/product-category/sega/master-system/',
    'https://www.consolemad.co.uk/product-category/sega/mega-cd/uk-mega-cd-games/',
    'https://www.consolemad.co.uk/product-category/sega/mega-drive/uk-mega-drive-games/',
    'https://www.consolemad.co.uk/product-category/sega/saturn/uk-saturn-games/',
    'https://www.consolemad.co.uk/product-category/sony/playstation/uk-playstation-games/',
    'https://www.consolemad.co.uk/product-category/sony/playstation-2/uk-playstation-2-games/',
    'https://www.consolemad.co.uk/product-category/sony/playstation-3/uk-playstation-3-games/',
    'https://www.consolemad.co.uk/product-category/sony/ps-vita/ps-vita-games/',
    'https://www.consolemad.co.uk/product-category/sony/psp/psp-games/',
    'https://www.consolemad.co.uk/product-category/other/zx-spectrum-games/',
    'https://www.consolemad.co.uk/product-category/other/3do/uk-3do-games/'
    ]

def scrape(base_urls):
      
    for base_url in base_urls:
          
        url = base_url
        
        while url:
            url_list = url.split('/')
            if url_list[5]=="zx-spectrum-games":
                brand="Sinclair"
                console="spectrum"
            elif url_list[5]=="3do":
                brand="3do"
                console="3do"
            else:
                brand = url_list[4]
                console = url_list[5]
            if console[-6:]=="-games":
                console = console[:-6]
            
            
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')
            
            pages=[]
            for ul in soup.find_all('ul', {'class': 'page-numbers'}):
                for li in ul.find_all('li'):
                    for page_num in li.contents:
                        if page_num.text == '←' or page_num.text == '→':
                            continue
                        else:
                            pages.append(page_num.text)
            
            if soup.find('span', class_="current"):
                current_page = soup.find('span', class_="current").text
            else:
                current_page = None
            
            
            for product in soup.find_all('div', class_="entry-product"):
                
                picture_link = product.find('div', class_="entry-featured").a.img['src']
                
                
                title = product.find('div', class_="entry-wrap").header.h3.a.text
                
                
                price = product.find('div', class_="entry-wrap").header.span.span.text
                price = float(price[1:])
                
                
                game = Game(title=title, image=picture_link, price=price, brand=brand, console=console)
                game.save()
                print(title + " saved to db")
              
            if current_page and current_page != pages[-1]:
                next_page = int(current_page) + 1
                url = base_url + "page/{}/".format(next_page)
            else:
                url = None

scrape(base_urls)
   