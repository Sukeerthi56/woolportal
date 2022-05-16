from bs4 import BeautifulSoup
import requests
import csv
import sqlite3

# Sql connection ( Database )
sqliteConnection = sqlite3.connect('all-about-wool.db')
cursor = sqliteConnection.cursor()


# For adding more websites , brands and items in future into csv file "woolfile.csv"
def woolnewdata():
    continuethis = 'y'
    wooldata = []
    while continuethis == 'y':
        website = input("Enter the base website link ")
        brand = input("Enter the brand name")
        item = input("Enter the item name")
        wooldata.append([website,brand,item])
        continuethis = input("Do you want to add more y for yes or n for no")
        with open("woolfile.csv",'a') as f:
            for row in wooldata:
                writer_object = csv.writer(f)
                writer_object.writerow(row)


# For extracting data for comparing and saving them in a database database name : all-about-wool.db tablename: wools
def woolextractdata():

# Opening the csv file to read website, brand and item details for extracting data
    with open("woolfile.csv") as data_file:
        data = csv.reader(data_file)

        for row in data:

            if row[0] != "Website":
                # url format of the website
                woolname = row[2].replace(" ", "-")
                textcombine = row[0] + "/" + row[1] + "/" + row[1] + "-" + woolname
                print(textcombine)

                try:
                    # Extracting data from the website
                    response = requests.get(textcombine)
                    web_page = response.text
                    soup = BeautifulSoup(web_page, "html.parser")
                    article_price = soup.find(name="span", class_="product-price-amount")

                    table = soup.find("div", id="pdetailTableSpecs")
                    rows = table.findAll('tr')
                    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
                    a = article_price.getText()

                    # Adding data into the table inside database
                    sqlite_insert_query = """INSERT INTO wools(website,brand,item,composition,price,needlesize) 
                        VALUES(?,?,?,?,?,?)"""
                    record = (row[0], row[1], row[2], a, data[3][1][0], data[4][1][0])

                    count = cursor.execute(sqlite_insert_query, record)
                    sqliteConnection.commit()
                    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)


                except sqlite3.Error as error:
                    print("Failed to insert data into sqlite table", error)

                except : # Incase the product/product page is not available

                    a="Not available"
                    sqlite_insert_query = """INSERT INTO wools(website,brand,item,composition,price,needlesize) 
                                            VALUES(?,?,?,?,?,?)"""
                    record = (row[0], row[1], row[2], a, a, a)

                    count = cursor.execute(sqlite_insert_query, record)
                    sqliteConnection.commit()
                    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)


# Main function starts from

print("Portal for wool-knitting information from different websites.")
choice = int(input("1. Add new website and brand details\n2.Extract and compare data"))

if choice == 1:

    # Function to add new data
    woolnewdata()
elif choice == 2:

    # Function to extract data
    woolextractdata()
else:

    # Incase choice is not 1 or 2
    print("Invalid input , Only 1 and 2 Please")

cursor.close()



