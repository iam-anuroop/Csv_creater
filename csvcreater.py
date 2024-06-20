import requests
from bs4 import BeautifulSoup
import csv

url = "https://us.princesspolly.com/collections/shoes"

try:
    response = requests.get(url)
    response.raise_for_status()  
except requests.exceptions.RequestException as e:
    print(f"Url fetching error : {e}")
    exit(1)

try:
    soup = BeautifulSoup(response.content, 'html.parser')
except Exception as e:
    print(f"Html error: {e}")
    exit(1)

shoes = soup.find_all('div', class_='product-tile')

if not shoes:
    print("No shoes available.")
    exit(1)

print(f"Total {len(shoes)} shoes available")

try:
    with open('princesspolly_shoes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image Link', 'Shoe Name', 'Price'])
        
        for shoe in shoes:
            image_tag = shoe.find('img')
            name_tag = shoe.find('a', class_='product-tile__name product-tile__name--full')
            price_tag = shoe.find('span', class_='product-tile__price')

            if not (image_tag and name_tag and price_tag):
                print("Missing data for a shoe item")
                # print(shoe.prettify())
                continue
            
            try:
                image = image_tag.get('src')
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                writer.writerow([image, name, price])
            except Exception as e:
                print(f"Error  writing shoe data : {e}")
except Exception as e:
    print(f"Csv writing error : {e}")
    exit(1)

print("Data fetched and saved successfully...")
