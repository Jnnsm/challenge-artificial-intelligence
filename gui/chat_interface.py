import customtkinter as ctk
import threading
from typing import Literal, Optional

from core.chat_controller import ChatController


class ChatInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = ChatController()

        self.title("Chat")
        self.geometry("400x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.chat_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.loading_label: ctk.CTkLabel = ctk.CTkLabel(
            self.chat_frame, text="Carregando base de dados...")
        self.loading_label.grid(row=0, column=0, sticky="nsew")

        self.loading_animation: ctk.CTkProgressBar = ctk.CTkProgressBar(
            self.chat_frame, mode="indeterminate")
        self.loading_animation.grid(
            row=1, column=0, sticky="ew", padx=20, pady=10)
        self.loading_animation.start()

        self.chat_history: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(
            self.chat_frame)
        self.chat_history.grid(row=0, column=0, sticky="nsew")
        self.chat_history.grid_columnconfigure(0, weight=1)
        self.chat_history.grid_rowconfigure(0, weight=1)

        self.input_frame: Optional[ctk.CTkFrame] = None
        self.message_entry: Optional[ctk.CTkEntry] = None
        self.send_button: Optional[ctk.CTkButton] = None
        self.progress_bar: Optional[ctk.CTkProgressBar] = None

        threading.Thread(target=self.load_database).start()

    def load_database(self) -> None:
        self.controller.init_database()
        self.after(0, self.setup_chat_interface)
        self.add_bot_message("Oi, seja bem vindo ao chat com o Edu!")

    def setup_chat_interface(self) -> None:
        # Chat
        self.loading_label.destroy()
        self.loading_animation.destroy()

        # Input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = ctk.CTkEntry(self.input_frame)
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            self.input_frame, text="Enviar", command=self.send_message)
        self.send_button.grid(row=0, column=1)
        self.send_button.configure(state="normal")

    def send_message(self, event=None) -> None:
        if self.send_button._state == ctk.DISABLED:
            return

        message: str = self.message_entry.get()
        if message.strip():
            bubble_width: int = self.chat_history.winfo_width() - 40
            message_frame: ctk.CTkFrame = ctk.CTkFrame(
                self.chat_history, fg_color="blue", corner_radius=10)
            message_frame.grid(row=self.chat_history.grid_size()[
                1], column=0, sticky="e", padx=(0, 10), pady=5)
            message_label: ctk.CTkLabel = ctk.CTkLabel(
                message_frame, text=message, wraplength=bubble_width, justify="left")
            message_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            self.message_entry.delete(0, "end")
            self.chat_history._parent_canvas.update_idletasks()
            self.chat_history._parent_canvas.yview_moveto(1.0)

            self.controller.add_new_message(message)

            threading.Thread(target=self.generate_bot_response).start()

    def generate_bot_response(self):
        self.change_input_state('disable')

        bot_response: str = self.controller.generate_response()
        self.add_bot_message(bot_response)
        self.after(0, lambda: self.change_input_state('enable'))

    def change_input_state(self, state: Literal['enable', 'disable']):
        if state == 'enable':
            self.hide_progress_bar()
            self.send_button._state = ctk.NORMAL
            self.send_button.configure(state="normal")
        elif state == 'disable':
            self.show_progress_bar()
            self.send_button._state = ctk.DISABLED
            self.send_button.configure(state="disabled")

    def show_progress_bar(self):
        self.message_entry.grid_remove()
        self.send_button.grid_remove()

        self.progress_bar = ctk.CTkProgressBar(
            self.input_frame, mode="indeterminate")
        self.progress_bar.grid(row=0, column=0, columnspan=2,
                               sticky="ew", padx=10, pady=10)
        self.progress_bar.start()

    def hide_progress_bar(self):
        self.progress_bar.destroy()
        self.progress_bar = None

        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.send_button.grid(row=0, column=1)

    def add_bot_message(self, message: str) -> None:
        bubble_width: int = self.chat_history.winfo_width() - 40
        response_frame: ctk.CTkFrame = ctk.CTkFrame(
            self.chat_history, fg_color="green", corner_radius=10)
        response_frame.grid(row=self.chat_history.grid_size()[
                            1], column=0, sticky="w", padx=(10, 0), pady=5)
        response_label: ctk.CTkLabel = ctk.CTkLabel(
            response_frame, text=message, wraplength=bubble_width,
            justify="left")
        response_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.chat_history._parent_canvas.update_idletasks()
        self.chat_history._parent_canvas.yview_moveto(1.0)
