from importlib import reload
from tkinter import *
from main import *


class UI:
    # Interface
    @staticmethod
    def interface():

        listboxOV = []
        maxChar = 0

        root = Tk()
        root.geometry("600x400")
        frame = Frame(root)
        frame.grid()

        # open plugin file
        with open('LastSavedPluginVersions.txt', "r") as read_obj:
            listboxOV = loadtxt('LastSavedPluginVersions.txt', dtype='str', unpack=True, delimiter='/n')
            # Determine length of lists
            listboxOV = listboxOV.tolist()
            URLCount = len(listboxOV)
            singleUrl = ""
            # Determine Max Width of Items in the list
            for url in listboxOV:
                if len(url) != 1:
                    currentChar = len(url)
                    if currentChar > maxChar:
                        maxChar = currentChar
                else:
                    # Count the number of char in the single string
                    singleUrl += url
                    maxChar = len(singleUrl)

        # open url file
        open('URLList.txt', 'r')

        def refresh(self):
            self.destroy()
            self.__init__()

        # load urls from text file into ui current version list
        def load_URLS():
            urlItem = ""
            for item in listboxOV:
                if len(item) != 1:
                    listBStoredVersion.insert(END, item)
                else:
                    if item != "":
                        urlItem += item
            listBStoredVersion.insert(END, urlItem)

        def add_URL():
            pluginURL = versionEntry.get()
            if pluginURL == "":
                Message(master=None, title='Ok')
            else:
                listBStoredVersion.insert(END, pluginURL)
                urlList.append(pluginURL)
                np.savetxt('URLList.txt', np.array(urlList), fmt="%s")
                versionEntry.delete(0, 'end')
                refresh(self=frame)

        def remove_URL():
            listBStoredVersion.delete(ACTIVE)

        def run():
            print('Running...into a wall')
            Data.version_scraper()
            listBNewVersion.delete(END)
            # Insert new plugin updates into ListBox here
            root.after(1000, UI)

        name = StringVar()

        # UI Elements
        lblPlugin = Label(root, text='Plugin Changelog URL: ')

        versionEntry = Entry(root)
        btnEnter = Button(root, text='Add', command=add_URL)

        lblStoredVersion = Label(root, text="Old Version: ")
        if maxChar != 0:
            listBStoredVersion = Listbox(root, height=URLCount, width=maxChar)
        else:
            listBStoredVersion = Listbox(root, height=15, width=30)

        lblNewVersion = Label(root, text="New Version Available: ")
        if maxChar != 0:
            listBNewVersion = Listbox(root, height=URLCount, width=maxChar)
        else:
            listBNewVersion = Listbox(root, height=15, width=30)

        btnRemove = Button(root, text='Remove', command=remove_URL)
        btnRun = Button(root, text='Run', command=run)

        lblSendto = Label(root, text='Sending to:')
        lblName = Label(root, textvariable=name)

        name.set(email)

        lblPlugin.grid(row=0, column=2)
        versionEntry.grid(row=0, column=3)
        btnEnter.grid(row=0, column=5)
        lblStoredVersion.grid(row=2, column=2)
        listBStoredVersion.grid(row=3, column=2)
        lblNewVersion.grid(row=2, column=5)
        listBNewVersion.grid(row=3, column=5)
        btnRemove.grid(row=4, column=3)
        lblSendto.grid(row=5, column=1)
        lblName.grid(row=5, column=2)
        btnRun.grid(row=4, column=8)
        root.title("Plugin Version Tracker")
        load_URLS()
        root.mainloop()


def every_twenty_four_hours():
    Display = UI()
    Display.interface()


every_twenty_four_hours()
