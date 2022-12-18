from bs4 import BeautifulSoup
import requests 
import mysql.connector
import re
car_make = input('car_brand(e.g chevrolet): ')
rsp = requests.get('https://www.truecar.com/used-cars-for-sale/listings/' '%s' % (car_make))
from bs4 import BeautifulSoup
soup = BeautifulSoup(rsp.text, 'html.parser')
carContents = soup.find_all(class_ = 'card-content vehicle-card-body order-3', limit = 20)
for carContent in carContents :
  carmodel = carContent.find(class_ = 'vehicle-card-header w-100').text
  price = re.findall(r'\$(\d*,{0,1}\d*)',carContent.find(attrs = {'data-test' : 'vehicleCardPricingBlockPrice'}).text)
  price = price[0].translate({ord(',') : ('')})
  price = int(price)
  mileage = re.findall(r'(\d*,{0,1}\d*) miles',carContent.find(attrs = {'data-test' : 'vehicleMileage'}).text)
  mileage = int(mileage[0].translate({ord(',') : None}))
  # print(mileage, price)
  cnx = mysql.connector.connect(user = 'root', password = 'SlTuV5680M',
                                    host = 'localhost', port = '3306', 
                                    database = 'car_db')
  cursor = cnx.cursor()
  cursor.execute('INSERT INTO car_info VALUES (\'%s\', \'%s\')' % (mileage, price))
  cnx.commit()
  cnx.close()