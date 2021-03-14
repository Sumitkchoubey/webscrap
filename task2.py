import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException,InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub
from fake_useragent import UserAgent

ua = UserAgent()
a = ua.random
user_agent = ua.random
options = Options()
options.add_argument("window-size=1400,600")
options.add_argument(f'user-agent={user_agent}')



class RecapchaFill:
    def __init__(self,selenium_driver,url,send_data):
        self.driver=selenium_driver
        self.url=url
        self.send_data=send_data

    def start(self):
        try:
            #create chrome driver
            driver = webdriver.Chrome(executable_path=self.driver,chrome_options=options) 
            time.sleep(10)
            #go to website
            driver.get(self.url)
        except InvalidArgumentException:
            print("please provide valid url and chromedriver path")
        url_box = driver.find_element_by_name("url")
        url_box.send_keys(self.send_data)
        time.sleep(10)
        #switch to recaptcha frame
        frames=driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frames[0])
        time.sleep(3)

        #click on checkbox to activate recaptcha
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()

        #switch to recaptcha audio control frame
        driver.switch_to.default_content()
        frames=driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frames[0])
        time.sleep(5)

        #click on audio challenge
        driver.find_element_by_id("recaptcha-audio-button").click()

        #switch to recaptcha audio challenge frame
        driver.switch_to.default_content()
        frames= driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frames[-1])
        time.sleep(6)

        driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
        #get the mp3 audio file
        src = driver.find_element_by_id("audio-source").get_attribute("src")
        #download the mp3 audio file from the source
        urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
        sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
        sound.export(os.getcwd()+"\\sample.wav", format="wav")
        sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
        r= sr.Recognizer()

        with sample_audio as source:
            audio = r.record(source)

        #translate audio to text with google voice recognition
        key=r.recognize_google(audio)

        #key in results and submit
        driver.find_element_by_id("audio-response").send_keys(key.lower())
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        driver.switch_to.default_content()
        time.sleep(8)
        driver.find_element_by_class_name("submit").click()


if __name__ == "__main__":
 
    recaptcha=RecapchaFill('/home/sumitkrchoubey/Desktop/test_r/chromedriver','https://safebrowsing.google.com/safebrowsing/report_phish/','test.com')
    recaptcha.start()




