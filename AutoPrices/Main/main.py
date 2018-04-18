from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import re
import os
import datetime
from pkg_resources import resource_dir

successList = []

#Open all csv files in the Input folder
directory_csv = "C:\\Users\\melk\\PycharmProjects\\AutoPrices\\Input\\"
for root,dirs,files in os.walk(directory_csv):
    for file in files:
        if file.endswith(".csv"):
            with open(directory_csv + file, 'r') as f:
                reader = csv.reader(f)
                vendor_list = list(reader)
            vendor_list.pop(0)

print(vendor_list)

def checkCookie():
    try:
        driver.find_element_by_name("decision").is_displayed()
        return True;
    except:
        return False;


for product in vendor_list:
    driver = webdriver.Chrome(executable_path="C:\\Users\\melk\\PycharmProjects\\GUI\\drivers\\chromedriver.exe")

    driver.set_page_load_timeout(10)
    driver.get("https://tweakers.nl")

    if checkCookie():
        driver.find_element_by_name("decision").click()

    driver.find_element_by_name("keyword").send_keys(product)
    for i in range(0, 2):
        driver.find_element_by_xpath("//input[@value='Zoeken']").click()
    #time.sleep(1)

    #Try because by default selenium throws exceptions when it can't find certain elements
    try:
        productNaam = driver.find_element_by_xpath("//div[@id='listingContainer']/div/ul/li/p/a").text
        driver.find_element_by_xpath("//div[@id='listingContainer']/div/ul/li/a").click()

        #Preparing the name data for the CSV file
        filteredVN = str(product)[2:-2]
        filteredPN = re.sub('[*."/;|=,]', '', productNaam)

        #Checking on which page you've landed
        def checkPage():
            try:
                driver.find_element_by_class_name("shop-name").is_displayed()
                return True;
            except:
                return False;

        #Navigating to the right page if you landed on a wrong page
        if checkPage() == False:
            #time.sleep(1)
            driver.find_element_by_xpath(".//tr[@class='largethumb']/td[@class='itemname']/p/a").click()
        else:
            debugvar = "Success"

        print("Success!")

        productLijst = []
        vendorpnLijst = []
        winkelLijst = []
        winkelLijstElementen = driver.find_elements_by_xpath("//div[@id='listing']/table/tbody//p[@class='ellipsis']/a")
        for i in winkelLijstElementen:
            winkelLijst.append(i.text)
            productLijst.append(filteredPN)
            vendorpnLijst.append(filteredVN)


        prijsLijst = []
        prijsLijstElementen = driver.find_elements_by_xpath("//div[@id='listing']/table/tbody//td[@class='shop-price']/p/a")
        for i in prijsLijstElementen:
            prijsLijst.append(i.text)

        result_notzipped = [productLijst,
                  vendorpnLijst,
                  winkelLijst,
                  prijsLijst]
        result = zip(*result_notzipped)

        #Output the zipped results as CSV with 4 rows
        outputfile = "../Output/" + filteredPN + ".csv"

        with open(outputfile, 'w') as output:
            writer = csv.writer(output)
            writer.writerows(result)

        successList.append(product)
    except:
        print("Product '" + str(product) + "' not found.")

    #time.sleep(1)
    driver.quit()

print("Successfully scraped {0} products!".format(len(successList)))