import requests
from bs4 import BeautifulSoup
import mysql.connector

# Function to crawl data from Amazon
def crawl_amazon_data():
    url = 'https://www.amazon.com/s?k=laptop'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', {'class': 's-result-item'})

    data = []
    for product in products:
        name = product.find('span', {'class': 'a-size-base-plus'}).text.strip()
        price = product.find('span', {'class': 'a-price-whole'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip()
        data.append((name, price, rating))

    return data

# Function to crawl data from Flipkart
def crawl_flipkart_data():
    url = 'https://www.flipkart.com/search?q=laptop'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', {'class': '_2kHMtA'})

    data = []
    for product in products:
        name = product.find('div', {'class': '_4rR01T'}).text.strip()
        price = product.find('div', {'class': '_30jeq3 _1_WHN1'}).text.strip()
        rating = product.find('div', {'class': '_3LWZlK'}).text.strip()
        data.append((name, price, rating))

    return data

# Connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

# Create a cursor object
cursor = db.cursor()

# Execute SQL queries to create tables
cursor.execute("CREATE TABLE IF NOT EXISTS Amazon (name VARCHAR(255), price VARCHAR(255), rating VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS Flipkart (name VARCHAR(255), price VARCHAR(255), rating VARCHAR(255))")

# Insert data into the Amazon table
amazon_data = crawl_amazon_data()
for item in amazon_data:
    sql = "INSERT INTO Amazon (name, price, rating) VALUES (%s, %s, %s)"
    val = (item[0], item[1], item[2])
    cursor.execute(sql, val)
    db.commit()

# Insert data into the Flipkart table
flipkart_data = crawl_flipkart_data()
for item in flipkart_data:
    sql = "INSERT INTO Flipkart (name, price, rating) VALUES (%s, %s, %s)"
    val = (item[0], item[1], item[2])
    cursor.execute(sql, val)
    db.commit()

# Close the database connection
db.close()
