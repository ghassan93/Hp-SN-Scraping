from asyncio import sleep
from concurrent.futures import process
from selenium import webdriver
import csv
import time
import traceback
import datetime
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
class WarrantyCheck:
    
    def __init__(self):
        # os.environ['MOZ_HEADLESS'] = '1'
        #path="C:/Program Files (x86)/chromedriver.exe"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        #self.driver.set_window_position(-10000,0)
        
        self.comp_dict = {}


    def scanCSV(self):
     
        with open('serialNumber.csv', 'r+') as f:
            csv_reader = csv.reader(f)
            
            _serialNumber = 0
            
            for count, i in enumerate(csv_reader):
                self.comp_dict[count] = {
                      
                        'serialNumber': i[_serialNumber],
                    }
              
               

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
        
        
        #process=self.driver.find_elements_by_class_name('warrantyResultsPageHeader')
        # if not process :
            
        #     self.driver.refresh()
        #     self.addSerialNumberToPage()
            
            
        # else :
        #     pass
        
        elem = self.driver.find_elements_by_class_name('warrantyResultsTable')
        with open('warranty_info.txt', 'a+') as f:
            for i in elem:
                f.write(i.text + '\n')
        self.driver
        time.sleep(8)
        self.driver.execute_script("window.history.go(-1)")
        self.driver.refresh()
        
        
        
        # self.driver.add_cookie({"name" : "foo", "value" : "bar"})
        # self.driver.get_cookie("foo")
        # # get all cookies in scope of session
        # print(self.driver.get_cookies())
        
        # # delete browser cookie
        # self.driver.delete_cookie("foo")
        
        # # clear all cookies in scope of session
        # self.driver.delete_all_cookies()
       
        # #self.startChromeBrowser()
        
    
    
    def addSerialNumberToPage(self, num=None):
        index = 0
        
        for count, data in self.comp_dict.items():
                
            if index <= 5:
                elem = self.driver.find_element_by_id(f"wFormSerialNumber{index + 1}")
                
                print(count, data)
                print(data['serialNumber'])
                elem.send_keys(data['serialNumber'])
                
                index += 1
                
            if index == 5.:
                self.over20Submit()
                index = 0
                
        self.over20Submit()
        index=0


if __name__ == '__main__':
    W = WarrantyCheck()
    W.scanCSV()
    W.startChromeBrowser()
    W.addSerialNumberToPage()

# try:
#     W = WarrantyCheck()
#     W.scanCSV()
#     W.startChromeBrowser()
#     W.addSerialNumberToPage()
# except:
#     with open("exceptions.log", "a") as logfile:
#         traceback.print_exc(file=logfile )
#     raise
   
    