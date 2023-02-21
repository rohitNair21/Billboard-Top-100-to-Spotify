import customtkinter
import tkinter
import threading
from time import sleep
from billTop100Scrape import scrapeAndMake

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
         
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")

        self.title("Billboard Top 100 to Spotify")
        self.minsize(600, 600)

        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20,padx=60,fill="both",expand=True)

        title = customtkinter.CTkLabel(master=frame, text="Billboard Top 100 to Spotify", font=("Roboto", 30))
        title.pack(pady=15, padx=15)

        fromWeb = customtkinter.CTkButton(master=frame, text="From Web...", command=self.loading)
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
        text = customtkinter.CTkLabel(master=frame, text="Loading.", font=("Roboto", 30))
        text.pack(pady=15,padx=15)
        loadScreen.mainloop()
        thread = threading.Thread(target=self.generatePlaylist)
        thread.daemon = True
        thread.start()
        x = 0
        while thread.is_alive():
            sleep(0.3)
            if x == 0:
                loadScreen.update()
                text.configure(text="Loading.")
                loadScreen.update()
                x += 1
            elif x == 1:
                loadScreen.update()
                text.configure(text="Loading..")
                loadScreen.update()
                x += 1
            elif x == 2:
                loadScreen.update()
                text.configure(text="Loading...")
                loadScreen.update()
                x = 0
        loadScreen.destroy()
        







if __name__ == "__main__":
    app = App()
    app.mainloop()