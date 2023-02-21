import customtkinter
import tkinter
import threading
from time import sleep
from billTop100Scrape import scrapeAndMake
from PIL import Image, ImageTk
import os
myPath = os.path.dirname(os.path.realpath(__file__))
imageA = customtkinter.CTkImage(Image.open(myPath +"/logo-internet-clipart-internet-logo-clipground-33.jpeg"), size=(25,25))
imageB = customtkinter.CTkImage(Image.open(myPath +"/file-spotify-logo-png-4.png"), size=(25,25))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
         
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")

        self.title("Billboard Top 100 to Spotify")
        self.minsize(300, 300)

        frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        frame.pack(pady=20,padx=60,fill="both",expand=True)

        title = customtkinter.CTkLabel(master=frame, text="Billboard Top 100 to Spotify", font=("Roboto", 30), image=imageB, compound="left")
        title.pack(pady=15, padx=15)

        fromWeb = customtkinter.CTkButton(master=frame, text="Import From Web...", command=self.loading, width=100, height=50, image=imageA)
        fromWeb.pack(pady=15,padx=15)

    def generatePlaylist(self):
        playlist = scrapeAndMake()
        playlist.addSongs()

    def loading(self):
        loadScreen = customtkinter.CTk()
        loadScreen.geometry("250,250")
        loadScreen.title("")
        frame = customtkinter.CTkFrame(master=loadScreen)
        frame.pack(pady=20,padx=60,fill="both",expand=True)
        text = customtkinter.CTkLabel(master=frame, text="Creating playlist.", font=("Roboto", 30))
        text.pack(pady=15, padx=15)
        thread = threading.Thread(target=self.generatePlaylist)
        thread.daemon = True
        thread.start()
        x = 0
        loadScreen.update_idletasks()
        while thread.is_alive():
            sleep(0.5)
            if x == 0:
                loadScreen.update()
                text.configure(text="Creating playlist.")
                loadScreen.update()
                x += 1
            elif x == 1:
                loadScreen.update()
                text.configure(text="Creating playlist..")
                loadScreen.update()
                x += 1
            elif x == 2:
                loadScreen.update()
                text.configure(text="Creating playlist...")
                loadScreen.update()
                x = 0
        loadScreen.destroy()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()