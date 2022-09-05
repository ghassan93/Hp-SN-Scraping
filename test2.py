from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.chrome.options import Options
import csv
import time
import json
import random
from msedge.selenium_tools import EdgeOptions
from selenium.webdriver import Edge
from json.decoder import JSONDecodeError


USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/104.0.1293.70",
'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15',
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
]

class WarrantyCheck:
    
    def __init__(self):
        # os.environ['MOZ_HEADLESS'] = '1'
        # path="C:/Program Files (x86)/chromedriver.exe"

        self.driver = EdgeOptions()
        self.driver.use_chromium = True
        self.driver.add_argument("start-maximized")
        self.driver.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver.add_argument("inprivate") 
        self.driver.add_argument("--disable-gpu") 
        self.driver.add_argument("--headless") 
        self.comp_dict = {}
        self.entries_count = 0
        self.last_SN = ''
        self.driver =Edge(executable_path = "C:/Program Files (x86)/msedgedriver.exe")


    def scanCSV(self):
     
        with open('serialNumber.csv', 'r+') as f:
            csv_reader = csv.reader(f)
            
            _serialNumber = 0
            
            for count, i in enumerate(csv_reader):
                self.comp_dict[count] = {
                      
                        'serialNumber': i[_serialNumber],
                    }
            return self.comp_dict
               

    def re_init(self):
        random_user_agent = random.choice(USER_AGENTS)
        opts=Options()
        opts.add_argument(f"user-agent={random_user_agent}")

        self.driver =Edge(executable_path = "C:/Program Files (x86)/msedgedriver.exe")


    def resume_scraping(self, sn_dict):
        ## find the latest entry in warranty.txt
        new_sn_dict = sn_dict
        if self.comp_dict[self.entries_count]['serialNumber'] == self.last_SN:
            new_sn_dict = dict(sn_dict.items()[:self.entries_count])

        return new_sn_dict
                

    def startChromeBrowser(self):
        self.driver.get("https://support.hp.com/us-en/checkwarranty/multipleproducts")


    def closeChromeBrowser(self):
        self.driver.close()


    def submitEntry(self):
        elem = self.driver.find_element_by_id('btnWFormSubmit')
        self.driver.execute_script("arguments[0].click();", elem)
    
    def checkForProductNumber(self):
        package = []
        for i in range(18):
            try:
                elem = self.driver.find_element_by_id(f"wFormProductNum{i}")
                elem.send_keys(self.comp_dict[i]['productNumber'])
            except:
                pass
                
        print(package)
        return package

    
    
    def over20Submit(self):
        self.submitEntry()
        time.sleep(10)
        self.checkForProductNumber()
        self.submitEntry()
        time.sleep(10)
        elem = self.driver.find_elements_by_class_name('warrantyResultsTable')
        description = self.driver.find_elements_by_css_selector('#sortedWarrantyResultsPlaceholder > div > div > div > div.warrantyResultsTable.hidden-sm > table:nth-child(1) > tbody > tr > td.col-lg-16')
        warrantyType = self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(1)")
        serviceTypeOne = self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td")
        startDateServiceOne = self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td")
        endServiceOne= self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(5) > table > tbody > tr:nth-child(1) > td")
        statusOne= self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(5) > table > tbody > tr:nth-child(1) > td")
        serviceTypeTwo= self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(3) > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td")
        startDateServiceTwo = self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(2) > td")
        endServiceTwo= self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(4) > table > tbody > tr:nth-child(2) > td")
        statusTwo= self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(5) > table:nth-child(2) > tbody > tr > td:nth-child(5) > table > tbody > tr:nth-child(2) > td")
                
        with open('warranty_results.json', 'r+') as f:
            products = []
            try:
                products = json.load(f)
            except JSONDecodeError:
                pass
            product = {}
            for entry in range(0, len(description) - 1):
                product["description"] = description[entry].text
                # product["warranty type"] = warrantyType[entry].text
                # product["service Type One"] = serviceTypeOne[entry].text
                
                # product["start Date Service One"] = startDateServiceOne[entry].text
                # product["end Date Service One"] = endServiceOne[entry].text
                # product["status One"] = statusOne[entry].text
                
                # product["service Type Two"] = serviceTypeTwo[entry].text
                # product["start Date Service Two"] = startDateServiceTwo[entry].text
                # product["end Date ServiceT wo"] = endServiceTwo[entry].text
                # product["status Two"] = statusTwo[entry].text
                print(product)
            products.append(product)
            json.dump(products, f)
         
        
        self.entries_count += 1
        self.driver
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(5)
        self.startChromeBrowser()
    
    
    
    def addSerialNumberToPage(self, sn_dict, num=None):
        index = 0
        for count, data in sn_dict.items():
            if index <= 3:
                try:
                    elem = self.driver.find_element_by_id(f"wFormSerialNumber{index + 1}")
                    elem.send_keys(data['serialNumber'])
                except UnexpectedAlertPresentException:
                    self.closeChromeBrowser()
                    self.re_init()
                    new_dict = self.resume_scraping(sn_dict)
                    self.addSerialNumberToPage(new_dict)

                index += 1
                
            if index == 3:
                try:
                    self.over20Submit()
                except(UnexpectedAlertPresentException, TimeoutException):
                    self.closeChromeBrowser()
                    self.re_init()
                    new_dict = self.resume_scraping(sn_dict)
                    self.addSerialNumberToPage(new_dict)
                index = 0
                
        self.over20Submit()
        index=0




if __name__ == '__main__':
    W = WarrantyCheck()
    sn_dict = W.scanCSV()
    W.startChromeBrowser()
    W.addSerialNumberToPage(sn_dict)