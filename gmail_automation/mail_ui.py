import PySimpleGUI as sg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib 
import pandas as pd

def send_custom_mail(values):
    print(values)
    gmailaddress = values[0]
    gmailpassword = values[1]
    mailto_list = values[2].split(",")
    mailto_list = list(map(str.strip,mailto_list))
    with open("mailto_list.log","w") as f:
        f.write("\n".join(mailto_list))  # LOGGING FOR MAILS " just testing"
    message = MIMEMultipart("alternative")
    
    # SETTING MESSAGE FORMAT
    message["From"] = values[3]
    message["Subject"] = values[4]
    message["To"] = "YOU"
    template_file = values[5]
    
    # HTML FILE ATTACHMENT
    with open(template_file) as f:
        html = f.read()
    print(html)
    message.attach(MIMEText(html, "html"))
    
    # LOGIN PROCESS
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    print("smtp connected")
    mailServer.starttls()
    mailServer.login(gmailaddress , gmailpassword)
    print("logged in")
    print("starting to send emails")
    
    # SEND MAIL LOOP
    for mail in mailto_list:
        mailServer.sendmail(gmailaddress, mail , message.as_string())
        print(" \n Sent! "+mail)
        
    # FINISH UP
    print("Done...")
    mailServer.quit()



## Function under construction
def fetch_emails():
    csv_file = "data2.csv"
    picked_column = "email"
    mails = pd.read_csv(csv_file)[picked_column].tolist()
    return ",".join(mails)


### LAYOUTS AND VARIABLES

your_details = {
    "gmail_address" : "dummy@gmail.com",
    "gmail_password" : "the password",
}

message_details = {
    "from_name" : "Internity HackCovid-19",
    "msg_subject" : "Test Subject"    
}



layout = [
    [sg.Text("-"*10+'  Sender Details  '+"-"*10, size=(30, 1), font=("Helvetica", 10))],
    [sg.Text('Your Gmail address: ', size=(30, 1), font=("Helvetica", 10)), sg.InputText(your_details["gmail_address"])], #0
    [sg.Text('Your Gmail Password: ', size=(30, 1), font=("Helvetica", 10)), sg.InputText(your_details["gmail_password"])], #1
    
    [sg.Text("-"*10+'  Message Details  '+"-"*10, size=(30, 1), font=("Helvetica", 10))],
    [sg.Text('Mail To List(comma seperated): ', size=(30, 1), font=("Helvetica", 10)), 
     sg.Multiline(default_text= fetch_emails(), size=(35, 3))], #2
    
    [sg.Text('From: ', size=(30, 1), font=("Helvetica", 10)), sg.InputText(message_details["from_name"])], #3
    [sg.Text('Suject: ', size=(30, 1), font=("Helvetica", 10)), sg.InputText(message_details["msg_subject"])], #4

    [sg.Text("-"*10+'  Body Templates  '+"-"*10, size=(30, 1), font=("Helvetica", 10))],
    [sg.Text('Body Template: ', size=(30, 1), font=("Helvetica", 10)), sg.Input(), sg.FileBrowse()], #5 #Browse
    
    [sg.Submit(), sg.Cancel()]
]




# sg.ChangeLookAndFeel('GreenTan')
window = sg.Window('Mail Bomber', default_element_size=(40, 1)).Layout(layout)
button, values = window.Read()
send_custom_mail(values)