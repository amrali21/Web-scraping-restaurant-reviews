import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from decouple import config

# default path to file to store data
path_to_file = "ratings.csv"

# default number of scraped pages
num_page = 5



# default tripadvisor website of restaurant
url = config('RESTAURANT_URL')

# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# Import the webdriver
driver = webdriver.Chrome(config('WEBDRIVER_LOC'))
driver.get(url)

# Open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

# change the value inside the range to save more or less reviews
for i in range(0, num_page):
    
    # expand the review 
    time.sleep(2)
    driver.find_element(By.XPATH,"//span[@class='taLnk ulBlueLinks']").click()

    container = driver.find_elements(By.XPATH,".//div[@class='review-container']")
    for j in range(len(container)):
        
        title = container[j].find_element(By.XPATH,".//span[@class='noQuotes']").text
        date = container[j].find_element(By.XPATH,".//span[contains(@class, 'ratingDate')]").get_attribute("title")
        rating = container[j].find_element(By.XPATH,".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
        review = container[j].find_element(By.XPATH,".//p[@class='partial_entry']").text.replace("\n", " ")
        
        csvWriter.writerow([date, rating, title, review]) 
        
    # change the page
    driver.find_element(By.XPATH,'.//a[@class="nav next ui_button primary"]').click()

driver.close()
print("done")