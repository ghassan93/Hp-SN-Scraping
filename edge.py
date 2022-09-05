from concurrent.futures import process
from selenium import webdriver
import csv
import time
import traceback
import datetime
from selenium.webdriver import Edge
from msedge.selenium_tools import EdgeOptions
from selenium.webdriver.edge.options import Options
import json

class WarrantyCheck:
    
    def __init__(self):
        # os.environ['MOZ_HEADLESS'] = '1'
        path="C:/Program Files (x86)/msedgedriver.exe"
        
        self.dr = EdgeOptions()
        self.dr.use_chromium = True
        self.dr.add_argument("start-maximized")
        self.dr.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.dr.add_argument("inprivate") 
        self.dr.add_argument("--disable-gpu") 
        self.dr.add_argument("--headless") 
        x=self.dr

        self.driver = Edge(executable_path = "C:/Program Files (x86)/msedgedriver.exe")
        
                
        
       
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
                
        #print(package)
        return package

    
    
    def over20Submit(self):
        self.submitEntry()
        time.sleep(10)
        self.checkForProductNumber()
        self.submitEntry()
        
        time.sleep(10)
        process=self.driver.find_elements_by_class_name('warrantyResultsPageHeader')
        # if not process :
            
        #     self.startChromeBrowser()
        #     self.addSerialNumberToPage()
            
            
        # else :
        #     print('not found')

        # description =self.driver.find_elements_by_css_selector('#sortedWarrantyResultsPlaceholder > div > div > div > div.warrantyResultsTable.hidden-sm > table:nth-child(1) > tbody > tr > td.col-lg-16')
        # startDate = self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div.warrantyResultsTable.hidden-sm > table:nth-child(2) > tbody > tr > td:nth-child(4) > table > tbody > tr:nth-child(1) > td")/
        # warrantyType =self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div:nth-child(1) > table:nth-child(2) > tbody > tr > td:nth-child(1)")
        # # serviceType=self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div.warrantyResultsTable.hidden-sm > table:nth-child(2) > tbody > tr > td:nth-child(2)")
        # # endDate=self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div.warrantyResultsTable.hidden-sm > table:nth-child(2) > tbody > tr > td:nth-child(4) > table > tbody > tr:nth-child(2) > td")
        # # status=self.driver.find_elements_by_css_selector("#sortedWarrantyResultsPlaceholder > div > div > div > div.warrantyResultsTable.hidden-sm > table:nth-child(2) > tbody > tr > td:nth-child(5)")
        # # hp_result=[description,startDate,warrantyType,serviceType,endDate,status]
        # for i in startDate:
            
                
        #             print(i.text+ '\n')
        
        elem = self.driver.find_elements_by_class_name('warrantyResultsTable')
      
        
        
        dict1 = {}
  
# fields in the sample file 
        fields =['description', 'warrantyType', 'serviceType', 'startDate','endDate', 'status']
        
        
            
    
        
        # count variable for employee id creation
      
        l = 1
        for line in elem:
            line=line.text
            print(line) 
            
            # reading line by line from the text file
            description = list( line.strip().split(None, '\n'))
            
            # for output see below
            print(description) 
            
            # for automatic creation of id for each employee
            sno ='emp'+str(l)
        
            # loop variable
            i = 0
            # intermediate dictionary
            dict2 = {}
            while i<len(fields):
                
                    # creating dictionary for each employee
                    dict2[fields[i]]= description[i]
                    i = i + 1
                            
                    # appending the record of each employee to
                    # the main dictionary
                    dict1[sno]= dict2
                    l = l + 1
            
            
            # creating json file        
            out_file = open("test2.json", "w")
            json.dump(dict1, out_file, indent = 4)
            out_file.close()
            
        
        
        
        
        
        # with open('warranty_info.txt', 'a+') as f:
        #     for i in elem:
        #         title=i.text
        #         f.write(i.text + '\n')
                
        #         data['cards_title'].append(title)
        #         count += 1

        #         with open('data.json', 'w') as outfile:
        #                 json.dump(data, outfile)
        #         #print(i.text)
        # self.driver
        time.sleep(8)
        self.driver.execute_script("window.history.go(-1)")
        #self.driver.refresh()
        
        
        
        # self.driver.add_cookie({"name" : "foo", "value" : "bar"})
        # self.driver.get_cookie("foo")
        # # get all cookies in scope of session
        # #print(self.driver.get_cookies())
        
        # # delete browser cookie
        # self.driver.delete_cookie("foo")
        
        # # clear all cookies in scope of session
        # self.driver.delete_all_cookies()
       
        self.startChromeBrowser()
        
    
    
    def addSerialNumberToPage(self, num=None):
        index = 0
        
        for count, data in self.comp_dict.items():
                
            if index <= 3:
                elem = self.driver.find_element_by_id(f"wFormSerialNumber{index + 1}")
                print(count, data)
                print(data['serialNumber'])
                elem.send_keys(data['serialNumber'])
                index += 1
                
            if index == 3:
                self.over20Submit()
                index = 0
                
        self.over20Submit()
        index=0


# if __name__ == '__main__':
#     W = WarrantyCheck()
#     W.scanCSV()
#     W.startChromeBrowser()
#     W.addSerialNumberToPage()

try:
    W = WarrantyCheck()
    W.scanCSV()
    W.startChromeBrowser()
    W.addSerialNumberToPage()
except:
    with open("exceptions.log", "a") as logfile:
        traceback.print_exc(file=logfile )
    raise
   
    