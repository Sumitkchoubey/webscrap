from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.chrome.options import Options


class RotatingProxyList:
    def __init__(self,proxy_url,driver):
        self.proxy_url=proxy_url
        self.driver=driver
    def extract_proxy(self):
        browser = webdriver.Chrome(executable_path=self.driver)
        browser.get(self.proxy_url)
        sleep(10)
        select = Select(browser.find_element_by_name('c'))
        select.select_by_visible_text('United States')
        browser.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[3]/td/input').click()
        sleep(20)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr[1]/td[1]/a').text
        row=2
        error=1
        proxy_l=[]
        while True:
            try:
                len_row=len(row)
                if len_row >30:
                    break
                else:
                    k=browser.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr["+str(row)+"]/td[1]/a")
                    port=browser.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr["+str(row)+"]/td[2]")
                    proxy_l.append(k.text+":"+port.text)
                    
                row+=1
            except:
                k=browser.find_element_by_class_name("adsbygoogle")
                row+=1
                error+=1
                
            sleep(3)
        return proxy_l

class DataExtract:
    def __init__(self,proxy_list,driver):
        self.proxy_list=proxy_list
        self.driver=driver
        
    def extract_data(self,option_v,row):
        data_rt=[]
        
        browser = webdriver.Chrome(executable_path=self.driver,chrome_options=option_v)
        data_p=True

        while True:
            try:
                browser.get('https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage='+str(row))
                containers = browser.find_elements_by_xpath('//div[@class="product"]')
                sleep(10)
                i=[]
               
                for i in containers:
                        data_r={}
                        title = i.find_element_by_xpath('.//a[@class="catalog-item-name"]')
                        data_r['title']=title.text
                        price=i.find_element_by_xpath('.//span[@class="price"]')
                        data_r['price']=price.text
                        stock=i.find_element_by_xpath('.//span[@class="status"]')
                        if stock.text=="Out of Stock":
                            data_r['Stock']=False
                        else:
                            data_r['Stock']=True
                        manu=i.find_element_by_xpath('.//a[@class="catalog-item-brand"]')
                        data_r['maftr']=manu.text
                        data_rt.append(data_r)
                        
                sleep(3)
                    #print(data_r)
                popup_err=browser.find_elements_by_xpath('//*[@id="close-button"]')
                if len(popup_err)==0:
                    pass
                else:
                    for k in  popup_err:
                        k.click()
                sleep(10)
                click_b2=browser.find_element_by_link_text("Next")
                if click_b2.is_enabled:
                    row+=1
                    sleep(10)
                else:
                    data_p=False
                    break
            except:
                        pass
        sleep(10)
        browser.quit()
        return row,data_rt,data_p


    def worker(self):
        for k in self.proxy_list:
            options = Options()
            options.add_argument('--proxy-server={}'.format(self.proxy_list[k]))
            row_v=1
            row,data_rt,data_p=self.extract_data(options,row_v)
            if data_p==True:
                print(data_rt)
            else:
                row_v=row


if __name__ == "__main__":
    rotate_p=RotatingProxyList("http://www.freeproxylists.net/",'/home/sumitkrchoubey/Desktop/test_r/chromedriver')
    data_extract=DataExtract(rotate_p,'/home/sumitkrchoubey/Desktop/test_r/chromedriver')
    data_extract.worker()









    