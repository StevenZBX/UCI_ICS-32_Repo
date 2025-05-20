"""
The main module of the Direct Messenger
"""

# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

from ds_messenger import DirectMessenger, DirectMessage


class LoginWindow(tk.Tk):
    def __init__(self) -> None:
        """Initialize the login window."""
        super().__init__()
        self.title("Direct Messenger")
        self.geometry("300x250")
        self.resizable(False, False)
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        title_label = ttk.Label(main_frame, text="Direct Messenger",
                               font=("Helvetica", 14))
        title_label.pack(pady=(0, 20))
        username_frame = ttk.Frame(main_frame)
        username_frame.pack(fill=tk.X, pady=(0, 10))
        # User input username
        ttk.Label(username_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(username_frame, width=30)
        self.username_entry.pack(side=tk.LEFT, padx=(10, 0))
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        # User input password
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(password_frame, show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, padx=(10, 0))
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        login_button = ttk.Button(button_frame, text="Login",
                                 command=self.login, width=20)
        login_button.pack(pady=10)
        self.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
        self.update_idletasks()
        # Find the center of screen and display on there
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def login(self) -> None:
        """Handle login button click and authenticate user."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            try:
                messenger = DirectMessenger(dsuserver='127.0.0.1',
                                          username=username, password=password)
                self.withdraw()  # Hide login window
                ChatWindow(self, messenger)
            except Exception as e:
                # If server is not running, create a messenger without server connection
                messenger = DirectMessenger(username=username, password=password)
                messenger.token = None  # Indicate offline mode
                self.withdraw()
                ChatWindow(self, messenger)
                messagebox.showwarning("Offline Mode", 
                                     "Server is not available. Running in offline mode.\nYou can view history messages but cannot send new messages.")


class ChatWindow(tk.Toplevel):
    def __init__(self, master, messenger: DirectMessenger) -> None:
        """Initialize the chat window UI."""
        super().__init__(master)
        self.path = "./store"
        self.file = "user.json"
        self.messenger = messenger
        self.username = messenger.username
        self.is_online = messenger.token is not None
        self.title(f"Chat - {messenger.username} {'(Offline)' if not self.is_online else ''}")
        self.geometry("900x600")
        self.contacts = set()
        self.messages = {}
        self.main_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        self.contacts_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.contacts_frame, weight=1)
        self.messages_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.messages_frame, weight=3)
        # load the interface with contacts, message area, message input area, sended message area
        self.contacts_area()
        self.message_area()
        self.setup_menu()
        self.load_data()
        if self.is_online:
            self.check_new_messages()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        """
        Close the interface
        """
        self.destroy()
        self.master.destroy()

    def contacts_area(self) -> None:
        """Setup the contacts list widget."""
        ttk.Label(self.contacts_frame, text="Contacts").pack(pady=5)
        self.contacts_tree = ttk.Treeview(self.contacts_frame, selectmode='browse')
        self.contacts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.contacts_tree.bind('<<TreeviewSelect>>', self.contact_select)
        ttk.Button(self.contacts_frame, text="Add Contact",
                   command=self.add_contact).pack(pady=5)

    def message_area(self) -> None:
        """Setup the message display and input area."""
        self.message_display = tk.Text(self.messages_frame, wrap=tk.WORD,
                                       state=tk.DISABLED)
        self.message_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        input_frame = ttk.Frame(self.messages_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.message_input = tk.Text(input_frame, height=3, wrap=tk.WORD)
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=5)
        if not self.is_online:
            send_button.state(['disabled'])
            self.message_input.config(state=tk.DISABLED)
        self.message_input.bind('<Control-Return>', lambda e: self.send_message())

    def setup_menu(self) -> None:
        """Setup the menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

    def add_contact(self) -> None:
        """Add a new contact to the contacts list."""
        if not self.is_online:
            messagebox.showwarning("Offline Mode", 
                                 "Cannot add contacts while offline.")
            return
        contact = simpledialog.askstring("Add Contact", "Enter username:")
        if contact:
            self.contacts.add(contact)
            self.contacts_tree.insert('', 'end', text=contact)
            if contact not in self.messages:
                self.messages[contact] = []

    def contact_select(self, event) -> None:
        """Handle contact selection event."""
        selection = self.contacts_tree.selection()
        if selection:
            contact = self.contacts_tree.item(selection[0])['text']
            self.display_messages(contact)

    def display_messages(self, contact: str) -> None:
        """Display messages for the selected contact."""
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        if contact in self.messages:
            for msg in self.messages[contact]:
                if msg.sender == self.messenger.username:
                    self.message_display.insert(
                        tk.END, f"You: {msg.message}\n", "outgoing")
                else:
                    self.message_display.insert(
                        tk.END, f"{msg.sender}: {msg.message}\n", "incoming")
        self.message_display.config(state=tk.DISABLED)
        self.message_display.tag_configure("outgoing", justify=tk.RIGHT,
                                           foreground="blue")
        self.message_display.tag_configure("incoming", justify=tk.LEFT,
                                           foreground="green")

    def send_message(self) -> None:
        """Send a message to the selected contact."""
        if not self.is_online:
            messagebox.showwarning("Offline Mode", 
                                 "Cannot send messages while offline.")
            return
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a contact!")
            return
        contact = self.contacts_tree.item(selection[0])['text']
        message = self.message_input.get(1.0, tk.END).strip()
        if message:
            if self.messenger.send(message, contact):
                dm = DirectMessage(message=message, recipient=contact,
                                   sender=self.messenger.username)
                if contact not in self.messages:
                    self.messages[contact] = []
                self.messages[contact].append(dm)
                self.message_input.delete(1.0, tk.END)
                self.display_messages(contact)
            else:
                messagebox.showerror("Error", "Failed to send message!")

    def check_new_messages(self) -> None:
        """Periodically check for new messages from the server and update the UI."""
        if self.is_online and self.messenger and self.messenger.token:
            try:
                new_messages = self.messenger.retrieve_new()
                for msg in new_messages:
                    sender = msg.sender
                    if sender not in self.contacts:
                        self.contacts.add(sender)
                        self.contacts_tree.insert('', 'end', text=sender)
                    if sender not in self.messages:
                        self.messages[sender] = []
                    if not any(m.timestamp == msg.timestamp and
                               m.message == msg.message and
                               m.sender == msg.sender for m in self.messages[sender]):
                        self.messages[sender].append(msg)
                    selection = self.contacts_tree.selection()
                    if selection and self.contacts_tree.item(selection[0])['text'] == sender:
                        self.display_messages(sender)
            except Exception:
                self.is_online = False
                self.title(f"Chat - {self.messenger.username} (Offline)")
                messagebox.showwarning("Connection Lost", 
                                     "Lost connection to server. Running in offline mode.")
                return
        if self.is_online:
            self.after(5000, self.check_new_messages)

    def load_data(self) -> None:
        """Load only read history messages from user.json file."""
        try:
            with open('./store/users.json', 'r') as f:
                data = json.load(f)
            user_data = data.get(self.username)
            if user_data and 'messages' in user_data:
                for msg in user_data['messages']:
                    if not msg.get('read', True):
                        continue
                    dm = DirectMessage(
                        message=msg.get('message'),
                        sender=msg.get('from', self.username),
                        recipient=msg.get('recipient', ''),
                        timestamp=msg.get('timestamp')
                    )
                    contact = dm.sender if dm.sender != self.username else dm.recipient
                    if not contact:
                        contact = "history"
                    if contact not in self.contacts:
                        self.contacts.add(contact)
                        self.contacts_tree.insert('', 'end', text=contact)
                    if contact not in self.messages:
                        self.messages[contact] = []
                    self.messages[contact].append(dm)
        except Exception as e:
            print(f"Error loading history: {e}")


def main() -> None:
    """Main entry point for the application."""
    login = LoginWindow()
    login.mainloop()


if __name__ == "__main__":
    main()
