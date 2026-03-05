import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
zillow_url = "https://appbrewery.github.io/Zillow-Clone/"
google_form = "YourGoogleForm"


response = requests.get(url=zillow_url, headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
property_listing = soup.select(".StyledPropertyCardDataWrapper a")
property_address = [property.getText().replace(" | ", " ").strip() for property in property_listing]
print(property_address)
property_link = [property["href"] for property in property_listing]
print(property_link)

property_prices = soup.select(".PropertyCardWrapper span")
property_price = [price.getText().replace("/mo", "").split("+")[0] for price in property_prices if "$" in price.text]
print(property_price)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(property_listing)):
    driver.get(google_form)
    question_1 = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    )
    question_1.send_keys(property_address[n])

    question_2 = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    )
    question_2.send_keys(property_price[n])

    question_3 = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    )
    question_3.send_keys(property_link[n])

    submit_button = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span'))
    )
    submit_button.click()
