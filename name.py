from customtkinter import *

def say_hello():
    label.configure(text="Привіт, друже! 🦑")

window = CTk()
window.geometry("300x200")
window.title("Моя кнопка")

label = CTkLabel(window, text="Натисни кнопку ↓", font=("Arial", 16))
label.pack(pady=20)

button = CTkButton(window, text="Привіт!", command=say_hello)
button.pack(pady=10)

window.mainloop()