from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import re
import datetime

with open('../Input/MelvTest.csv', 'r') as f:
  reader = csv.reader(f)
  vendor_list = list(reader)
vendor_list.pop(0)
successList = []


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
    driver.find_element_by_xpath("//input[@value='Zoeken']").click()
    driver.find_element_by_xpath("//input[@value='Zoeken']").click()
    #time.sleep(1)
    try:
        productNaam = driver.find_element_by_xpath("//div[@id='listingContainer']/div/ul/li/p/a").text
        driver.find_element_by_xpath("//div[@id='listingContainer']/div/ul/li/a").click()

        filteredVN = str(product)[2:-2]
        filteredPN = re.sub('[*."/;|=,]', '', productNaam)

        outputfile = "../Output/" + filteredPN + ".csv"

        #Check of je al op de prijzenpagina bent
        def checkPage():
            try:
                driver.find_element_by_class_name("shop-name").is_displayed()
                return True;
            except:
                return False;

        #Navigeer naar de prijzenpagina
        if checkPage() == False:
            #time.sleep(1)
            driver.find_element_by_xpath(".//tr[@class='largethumb']/td[@class='itemname']/p/a").click()
        else:
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

        with open(outputfile, 'w') as output:
            writer = csv.writer(output)
            writer.writerows(result)

        successList.append(product)
    except:
        print("Product '" + str(product) + "' not found.")

    #time.sleep(1)
    driver.quit()

print("Successfully scraped {0} products!".format(len(successList)))