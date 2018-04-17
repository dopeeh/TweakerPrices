from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

productList = ["not a product i", "blablasd base 700", "be quiet dark base 700", "be quiet pure rock"]
successList = []

def checkCookie():
    try:
        driver.find_element_by_name("decision").is_displayed()
        return True;
    except:
        return False;

for product in productList:
    outputfile = product + ".csv"

    driver = webdriver.Chrome(executable_path="C:\\Users\\melk\\PycharmProjects\\GUI\\drivers\\chromedriver.exe")

    driver.set_page_load_timeout(15)
    driver.get("https://tweakers.nl")

    if checkCookie():
        driver.find_element_by_name("decision").click()

    driver.find_element_by_name("keyword").send_keys(product)
    driver.find_element_by_xpath("//input[@value='Zoeken']").click()
    driver.find_element_by_xpath("//input[@value='Zoeken']").click()
    time.sleep(1)
    try:
        driver.find_element_by_xpath("//div[@id='listingContainer']/div/ul/li/a").click()

        #Check of je al op de prijzenpagina bent
        def checkPage():
            try:
                driver.find_element_by_class_name("shop-name").is_displayed()
                return True;
            except:
                return False;

        #Navigeer naar de prijzenpagina
        if checkPage() == False:
            time.sleep(1)
            driver.find_element_by_xpath(".//tr[@class='largethumb']/td[@class='itemname']/p/a").click()


        winkelLijst = []
        winkelLijstElementen = driver.find_elements_by_xpath("//div[@id='listing']/table/tbody//p[@class='ellipsis']/a")
        for i in winkelLijstElementen:
            winkelLijst.append(i.text)


        prijsLijst = []
        prijsLijstElementen = driver.find_elements_by_xpath("//div[@id='listing']/table/tbody//td[@class='shop-price']/p/a")
        for i in prijsLijstElementen:
            prijsLijst.append(i.text)

        result = dict(zip(winkelLijst, prijsLijst))

        with open(outputfile, 'w') as output:
            writer = csv.writer(output)
            for key, value in result.items():
                writer.writerow([key, value])

        successList.append(product)
    except:
        print("Product '" + product + "' not found.")

    time.sleep(1)
    driver.quit()

print("Successfully scraped {0} products!".format(len(successList)))
