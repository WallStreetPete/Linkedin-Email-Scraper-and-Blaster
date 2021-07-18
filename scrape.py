from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import bs4
from bs4 import BeautifulSoup
import string
from string import digits
import csv

email_address = input("Enter Email: ")
email_password = input("Enter Password: ")

base_url = "https://salesql.com/dashboard/contacts?current_tab=257489&page=1&pageSize=10"
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(base_url)

# More Automation
input_email = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div/div[2]/form/div[1]/div/div/input")
input_email.send_keys(email_address)
time.sleep(2)

input_pass = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div/div[2]/form/div[2]/div/div/input")
input_pass.send_keys(email_password)
time.sleep(60)

page_source = driver.page_source
soup = bs4.BeautifulSoup(page_source, 'lxml')

def find_row_info(n):
    row_info = []
    
    #get the ID
    index = n+1
    
    
    #get the name of the person
    name = soup.find_all("div", class_="name-wrapper")
    parsed_firstname = name[2*n].get_text().split(" ")[0]
    parsed_lastname = name[2*n].get_text().split(" ")[1]
    
    
    #get the email address of the person
    email = soup.find_all(class_="contact-info-list cellcolumn-undefined")
    s = email[2*n].get_text()
    for r in (("verified", ""), ("more", ""), ("+", ""), ("warning", ""), (", " ,"")):
        s = s.replace(*r).strip()
    parsed_email = ''.join([i for i in s if not i.isdigit()])
    
    
    #get the company of the person (name index plus one)
    company = soup.find_all(class_="name-wrapper")
    parsed_company = company[2*n+1].get_text().replace(", ", " of ").strip()
    

    #get the job title of the person
    title = soup.find_all("div", class_="primary-job-title")[n]
    parsed_title = title.get_text().replace(", ", " of ")
    
    
    #format it
    row_info.extend([index, parsed_firstname, parsed_lastname, parsed_email, parsed_company, parsed_title])
    
    return row_info
    
    
file_to_output = open('to_save_file.csv','w',newline='')
csv_writer = csv.writer(file_to_output,delimiter=',')
csv_writer.writerow(["ID", "First_name", "Last_name", "Email_Address", "Company", "Title"])

n=0
while n < 5:
    csv_writer.writerow(find_row_info(n))
    n+=1
file_to_output.close()
