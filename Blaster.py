#Import the goodies 
import smtplib
import getpass
import csv

#open the file 
data = open('Book1.csv', encoding='utf-8')

#csv.reader
csv_data = csv.reader(data)

#reformat it into python list of lists
data_lines = list(csv_data)

#Establish a server connection with smtp to Google
smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
smtp_object.ehlo()
smtp_object.starttls()

#Log into the gmail account with app key
email = getpass.getpass("Email:  ")
password = getpass.getpass("Password: ")
smtp_object.login(email,password)

# Parse for the correct variable assignments

amount = int(input("Emails to send: "))

for item in data_lines[1:amount+1]:
    from_address = email
    to_address = item[3]
    name = item[1]+' '+item[2]
    company = item[4]  
    title = item[-1]
    subject = "Test Message"
    message = "This is the message. Roosevelt Racers needs your help"
    
    # Customize and format the message
    msg = "Subject: "+subject+"\n"+message+" for "+name+" who works at "+company+" as an "+title+" seeking an sponsorship."
    
    # Send the Email
    smtp_object.sendmail(from_address,to_address,msg)
