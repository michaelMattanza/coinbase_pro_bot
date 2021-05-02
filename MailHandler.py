import smtplib
import json

class MailHandler:
    def __init__(self):
        self.config = self.loadConfig()
        self.mail = self.config["MAIL"]
        self.password = self.config["PASSWORD"]
        self.mailText = ""
        self.counter = 0

    def sendMail(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.mail, self.password)
            server.sendmail(self.mail, self.mail, self.mailText)
            server.close()
        except:
            print("Sending went wrong")
    
    def addCounter(self):
        self.counter += 1
        if self.counter == 10:
            self.sendMail()
            self.counter = 0
            self.mailText = ""
    
    def addText(self, value):
        self.mailText += value + "\n"
        self.addCounter( ) 

    
    def loadConfig(self):
        with open('config.json') as configFile:
            return json.load(configFile)
