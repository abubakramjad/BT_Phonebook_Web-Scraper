from bs4 import BeautifulSoup
from csv import DictWriter
import requests

file_name=input("Please enter a file name to create a new csv file or overwrite an existing one to store your scraped data: ")
with open(f'{file_name}.csv','w+',newline="") as f:
    csv_writer=DictWriter(f, fieldnames=['NAME','PHONE','STREET','CITY', 'ZIPCODE'])
    csv_writer.writeheader()
    uk_lnames=list(input("Please enter a name or a series of names separated by comma ',': ").split(","))
    uk_cities=list(input("Please enter the city for which you'd like to search for: ").split(","))
    for uk_city in uk_cities:
      for name in uk_lnames:
        html_text=requests.get(f'https://www.thephonebook.bt.com/Person/PersonSearch/?Surname={name}&Location={uk_city}').text
        soup=BeautifulSoup(html_text,"lxml")
        no_results=soup.find("div",class_="h2 py-5 white text-center")
        no_results2=soup.find("div",class_="d-none d-lg-block") 
        if no_results is None and no_results2 is None:
            i=1
            print(f"\nProcessing results for {name.title()} in {uk_city}")
            while True:
                target_url=requests.get(f'https://www.thephonebook.bt.com/Person/PersonSearch/?Surname={name}&Location={uk_city}&PageNumber={i}').text
                comp_conversion=BeautifulSoup(target_url,"lxml")
                control_switch=comp_conversion.find("div",class_="h2 py-5 white text-center")
                if control_switch!=None:
                    break
                data=comp_conversion.find_all("div",class_="mb-3 border border-dark px-3")
                for d in data:
                    person=d.find('span',class_='black medium').text.strip()
                    phone_num=d.find('div',class_='ml-3 d-inline light-blue my-auto no-wrap')
                    if phone_num==None:
                        continue
                    else:
                        phone=d.find('div',class_='ml-3 d-inline light-blue my-auto no-wrap').text.strip().replace("(","").replace(")","").replace(" ","")
                    address=d.find_all('div',class_='col-12 description truncatePL')
                    street=address[0].text
                    city_zip=address[1].text
                    if len((city_zip).split())>2:
                        z1,z2=city_zip.split()[-2:]
                        zipcode=f"{z1} {z2}"
                        city=" ".join(map(str,city_zip.split()[:-2]))
                    elif len((city_zip).split())==2:
                        z1,z2=city_zip.split()[-2:]
                        zipcode=f"{z1} {z2}"
                        city=uk_city
                    else:
                        city=uk_city
                        zipcode=city_zip
                    csv_writer.writerow({'NAME':person,'PHONE':phone,'STREET':street, 'CITY':city, 'ZIPCODE':zipcode})
                print(f"Name: {name.title()}, Page: {i} is Sucessfully Scraped!")
                i+=1
        else:
            print(f"\nNo result to display for {name.title()}")
    print("\nScraping procedure completed!")
