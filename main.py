import threading
from customtkinter import *
from PIL import Image
from socket import *


# ⬅️ ➡️
class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('500x500')
        self.title('LogiTalk')
        self.name = 'maksym'

        # menu Frame
        self.menu_frame = CTkFrame(self, width=0, height=300, fg_color="#3A6EA5")  # темно-синій
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = 5
        self.btn = CTkButton(self, text='меню', width=30, command=self.show_menu, fg_color="#6CA2EB",
                             hover_color="#00388F")
        self.btn.place(x=0, y=0)

        # main
        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.place(x=0, y=0)
        self.message_entry = CTkEntry(self, placeholder_text='Повідомлення:', height=40, fg_color="#A7C7E7",
                                      text_color='white')
        self.message_entry.place(x=0, y=0)
        self.send_button = CTkButton(self, text='>>', width=50, height=40, command=self.send_message,
                                     fg_color="#6CA2EB", hover_color="#00388F")
        self.send_button.place(x=0, y=0)

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 12345))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except:
            pass

        self.adaptive_ui()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message(f"{self.name}: {message}")
            data = f"{self.name} {message}"
            try:
                self.sock.sendall(data.encode())
            except:
                self.add_message('Помилка! Повідомлення не відправилось.')
            self.message_entry.delete(0, END)

    def recv_message(self):
        while True:
            try:
                ms = self.sock.recv(4096).decode().split(' ')
                author = ms[0]
                message = ' '.join(ms[1:])
                self.add_message(f"{author}: {message}")
            except:
                break
        self.sock.close()

    def add_message(self, message):
        message_frame = CTkFrame(
            self.chat_field,
            fg_color='#5B9BD5',  # світло-синій
            corner_radius=25
        )
        message_frame.pack(pady=5, anchor='w')
        message_frame_width = self.winfo_width() - self.menu_frame.winfo_width() - 50
        CTkLabel(
            message_frame,
            text=message,
            wraplength=message_frame_width,
            text_color='white',
            justify='left',
            font=('Robot', 12)
        ).pack(padx=10, pady=10)

    def get_name(self):
        name = self.entry_name.get()
        if name:
            self.name = name
            self.destroy_menu_widgets()
            self.create_menu_widgets()

    def create_menu_widgets(self):
        self.img = CTkImage(light_image=Image.open('Focus_eng_imperial_federation.png'), size=(100, 100))
        self.user_img = CTkLabel(self.menu_frame, text='', image=self.img)
        self.user_img.pack(pady=15)
        self.user_name_label = CTkLabel(self.menu_frame, text=self.name, text_color='white')
        self.user_name_label.pack(pady=10)
        self.entry_name = CTkEntry(self.menu_frame, placeholder_text="Змінити ім'я:", fg_color="#A7C7E7",
                                   text_color='white')
        self.entry_name.pack()
        self.btn_accept = CTkButton(self.menu_frame, text='змінити', width=self.entry_name.winfo_width() / 2,
                                    command=self.get_name, fg_color="#6CA2EB", hover_color="#00388F")
        self.btn_accept.pack(pady=5)

    def destroy_menu_widgets(self):
        self.user_img.destroy()
        self.user_name_label.destroy()
        self.entry_name.destroy()
        self.btn_accept.destroy()

    def show_menu(self):
        if not self.is_show_menu:
            if self.menu_frame.winfo_width() <= 200:
                self.menu_frame.configure(width=200)
                self.is_show_menu = True
                self.create_menu_widgets()
        else:
            self.is_show_menu = False
            if self.menu_frame.winfo_width() > 5:
                self.menu_frame.configure(width=-1)
            self.destroy_menu_widgets()

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.btn.place(x=self.menu_frame.winfo_width())
        self.chat_field.place(x=self.btn.winfo_width() + self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width() - 20,
                                  height=self.winfo_height() - 40)
        self.send_button.place(x=self.winfo_width() - self.send_button.winfo_width(),
                               y=self.winfo_height() - self.send_button.winfo_height())
        self.message_entry.place(x=self.menu_frame.winfo_width(),
                                 y=self.winfo_height() - self.message_entry.winfo_height())
        self.message_entry.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width())
        self.after(30, self.adaptive_ui)


MainWindow().mainloop()