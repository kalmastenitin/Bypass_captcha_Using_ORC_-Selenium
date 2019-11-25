from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib
import requests
import json
import pytesseract
import re

driver = webdriver.Firefox(executable_path='D:\Scraping\geckodriver.exe') #add location of geckodriver
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #add location of tesseract-OCR
#tesseract-ocr download link: https://sourceforge.net/projects/tesseract-ocr/

def convert_image_to_code(image_name):
    try:
        from PIL import Image
    except ImportError:
        import Image
    image_text = pytesseract.image_to_string(Image.open(image_name))
    return(image_text)

def save_captcha():
    element = driver.find_element_by_id("captcha")
    location = element.location
    size = element.size
    driver.save_screenshot("shot.png")
    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open('shot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('image.png')



if __name__=='__main__':
    cin = input('Please Enter CIN Number: ')
    try:
        re.match('^[A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}$',cin)
    except:
        print('Please enter a valid CIN Number')
        exit()

    url = 'http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do'
    driver.get(url)

    inputElement = driver.find_element_by_id('companyID')
    inputElement.send_keys(cin)

    save_captcha()
    captcha_code = convert_image_to_code('image.png')

    try:
        inputElement = driver.find_element_by_id('userEnteredCaptcha')
        inputElement.send_keys(captcha_code.lower())
        submit_button = driver.find_element_by_id('companyLLPMasterData_0')
        submit_button.click()
    except:
        alert = driver.switch_to.alert
        alert.dismiss()

    data = []
    try:
        soup = BeautifulSoup(driver.page_source,'html5lib')
        table1_data = soup.find('div', {'id':'companyMasterData'})
        rows = table1_data.find_all('tr')
        data1=[]
        for row in rows:
            cols = row.find_all('td')
            key = cols[0].text
            value = cols[1].text
            data1.append({key:value})
        json_data = json.dumps(data1)
        print(json_data)
    except AttributeError:
        print('Try again captcha bypass failed!')
    # data.append(data1)
    #more will be scraped in future
