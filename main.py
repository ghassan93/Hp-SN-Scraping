from selenium import webdriver
import csv
import time

class WarrantyCheck:
    
    def __init__(self):
        # os.environ['MOZ_HEADLESS'] = '1'
        path="C:/Program Files (x86)/chromedriver.exe"

        self.driver = webdriver.Chrome(path)
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
        time.sleep(10)
        elem = self.driver.find_elements_by_class_name('warrantyResultsTable')
        with open('warranty_info.txt', 'a+') as f:
            for i in elem:
                f.write(i.text + '\n')
        self.driver
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(5)
        self.startChromeBrowser()
    
    
    def addSerialNumberToPage(self, num=None):
        index = 0
        
        for count, data in self.comp_dict.items():
                
            if index <= 18:
                elem = self.driver.find_element_by_id(f"wFormSerialNumber{index + 1}")
                print(count, data)
                print(data['serialNumber'])
                elem.send_keys(data['serialNumber'])
                index += 1
                
            if index == 18:
                self.over20Submit()
                index = 0
                
        self.over20Submit()
        index=0


if __name__ == '__main__':
    W = WarrantyCheck()
    W.scanCSV()
    W.startChromeBrowser()
    W.addSerialNumberToPage()