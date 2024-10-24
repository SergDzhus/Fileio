from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
import requests
import pyperclip


def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()
                download_link = response.json()['link']
                entry.delete(0, END)
                entry.insert(0, download_link)
                pyperclip.copy(download_link)
                mb.showinfo("Ссылка скопирована!",f"Ссылка {download_link} успешно скопирована в буфер обмена!")
    except Exception as e:
        mb.showerror("Ошибка!",f"Произошла ошибка {e}!")

window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("400x200")

button = ttk.Button(text="Загрузить файл", command=upload)
button.pack()

entry = ttk.Entry()
entry.pack()

window.mainloop()