import smtplib
import ssl
import os
from datetime import datetime
import numpy as np
from numpy import loadtxt
from pynput import keyboard
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
import UI

to = ['robm@oryxsystems.co.za']  # used in display and email

urlList = []

old_versionList = []

update_list = []

email = 'robm@oryxsystems.co.za'


class Data:
    # HTML Webscapper
    @staticmethod
    def version_scraper():
        print('Stage 1 Started')

        # Print the date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        # Make an empty new file if one does not exist
        # file = open('LastSavedPluginVersions.txt', "w+")

        # Load the Old Version Array with Plugins from the Text File
        with open('LastSavedPluginVersions.txt', "r") as read_obj:
            Counter = 0
            one_char = read_obj.read(1)
            if one_char:
                array_data_text_file = loadtxt('LastSavedPluginVersions.txt', dtype='str', unpack=True, delimiter='/n')
                data_text_file = array_data_text_file.tolist()

                for plugin in data_text_file:
                    if len(plugin) != 1:
                        old_versionList.append(plugin)
                    else:
                        while Counter == 0:
                            old_versionList.append(data_text_file)
                            Counter += 1
            else:
                print('Empty File')

        # Load the UrlList Array with Urls from the Text File
        with open('URLList.txt', "r") as read_obj:
            Counter = 0
            one_char = read_obj.read(1)
            if one_char:
                array_data_text_file = loadtxt('URLList.txt', dtype='str', unpack=False, delimiter='/n')
                data_text_file = array_data_text_file.tolist()

                for url in data_text_file:
                    if len(url) != 1:
                        Counter += 1
                        urlList.append(url)
                    else:
                        while Counter == 0:
                            urlList.append(data_text_file)
                            Counter += 1
            else:
                print('Empty File')

        print('Url:', urlList)
        # Scrape the websites changelogs for any new updates
        if Counter == 1:
            singleUrl = ""
            for char in urlList:
                singleUrl += char
            dataRemovedApostrophe = singleUrl.replace("'", "")
            dataRemovedBracket = dataRemovedApostrophe.replace("[", "")
            data = dataRemovedBracket.replace("]", "")
            page = requests.get(data)
            soup = BeautifulSoup(page.content, 'html.parser')
            soup = soup.find('h1', class_='title').contents[0]
            version = soup.strip()
            if version == "":
                print('No plugin version available')
            else:
                # Separates plugin name from the version number
                if any(version.strip() in a for a in old_versionList):
                    split_text = version.split()[0]
                    # Check if plugin name exists
                    if any(split_text in b for b in old_versionList):
                        list_index = [i for i, s in enumerate(old_versionList) if split_text in s]
                        index = list_index[0]
                        old_versionList.pop(index)
                        old_versionList.append(version)
                        update_list.append(version)
                    else:
                        print('Not sure:', version)
                        old_versionList.append(version)
                else:
                    # If new plugin
                    old_versionList.append(version)
        else:
            for url in urlList:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                soup = soup.find('h1', class_='title').contents[0]
                version = soup.strip()
                if version == "":
                    print('No plugin version available')
                else:
                    # Separates plugin name from the version number
                    if any(version.strip() in a for a in old_versionList):
                        split_text = version.split()[0]
                        # Check if plugin name exists
                        if any(split_text in b for b in old_versionList):
                            list_index = [i for i, s in enumerate(old_versionList) if split_text in s]
                            index = list_index[0]
                            old_versionList.pop(index)
                            old_versionList.append(version)
                            update_list.append(version)
                        else:
                            print('Not sure:', version)
                            old_versionList.append(version)
                    else:
                        # If new plugin
                        old_versionList.append(version)

        # Save plugin versions to a text file
        np.savetxt('LastSavedPluginVersions.txt', np.array(old_versionList), fmt="%s")
        print('Stage 1 Complete')


class Communication:
    # Sends email via Gmail SMTP server
    @staticmethod
    def send_email(self):
        print('Stage 2 Start')
        gmail_user = 'pluginupdated@gmail.com'
        gmail_password = 'pluginupdated1!'

        port = 465  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = gmail_user
        password = gmail_password
        message = f"""To:<{email}>\n\r
            Plugin Updated:
            {update_list}
                        """

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            try:
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, to, message)
                print('Stage 2 Complete')
            except:
                if smtplib.SMTPRecipientsRefused:
                    print(smtplib.SMTPRecipientsRefused)
                else:
                    if smtplib.SMTPHeloError:
                        print(smtplib.SMTPHeloError)
                    else:
                        if smtplib.SMTPSenderRefused:
                            print(smtplib.SMTPSenderRefused)
                        else:
                            if smtplib.SMTPDataError:
                                print(smtplib.SMTPDataError)
                            else:
                                if smtplib.SMTPNotSupportedError:
                                    print(smtplib.SMTPNotSupportedError)
            finally:
                print('Failed')

    @staticmethod
    def send_alternate_email(self):
        print('Stage 3 Starting')
        gmail_user = 'pluginupdated@gmail.com'
        gmail_password = 'pluginupdated1!'

        port = 465  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = gmail_user
        password = gmail_password
        message = f"""To:<{email}>\n\r
                Testing: Nothing has been updated today!
                            """

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            try:
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, to, message)
                print('Stage 3 Complete')
            except:
                if smtplib.SMTPRecipientsRefused:
                    print(smtplib.SMTPRecipientsRefused)
                else:
                    if smtplib.SMTPHeloError:
                        print(smtplib.SMTPHeloError)
                    else:
                        if smtplib.SMTPSenderRefused:
                            print(smtplib.SMTPSenderRefused)
                        else:
                            if smtplib.SMTPDataError:
                                print(smtplib.SMTPDataError)
                            else:
                                if smtplib.SMTPNotSupportedError:
                                    print(smtplib.SMTPNotSupportedError)
                print('Failed')


# Instantiate methods


    # Email = Communication()
    # if len(update_list) != 0:
    #     Email.send_email()
    # else:
    #     Email.send_alternate_email()
    # update_list.clear()
    # old_versionList.clear()



# Scheduler runs every 24 hours checking for updates
# scheduler = BlockingScheduler()
# scheduler.add_job(every_twenty_four_hours, 'interval', hours=24, misfire_grace_time=240)
# scheduler.start()
