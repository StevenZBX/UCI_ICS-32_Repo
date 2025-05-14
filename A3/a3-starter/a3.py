# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME: Boxuan Zhang
# EMAIL: boxuanz3@uci.edu
# STUDENT ID: 95535906

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from ds_messenger import DirectMessenger, DirectMessage

class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("300x250")  # Made window slightly taller
        self.window.resizable(False, False)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="ICS 32 Direct Messenger", font=("Helvetica", 14))
        title_label.pack(pady=(0, 20))
        
        # Username frame
        username_frame = ttk.Frame(main_frame)
        username_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(username_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(username_frame, width=30)
        self.username_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Password frame
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(password_frame, show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Login button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Login button with larger size
        login_button = ttk.Button(button_frame, text="Login", command=self.do_login, width=20)
        login_button.pack(pady=10)
        
        # Bind Enter key to login
        self.window.bind('<Return>', lambda e: self.do_login())
        
        # Set focus to username entry
        self.username_entry.focus()
        
        # Center the window on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:
            messenger = DirectMessenger(username=username, password=password)
            if messenger.token:
                self.window.destroy()  # 登录或注册成功
                ChatWindow(messenger)
            else:
                messagebox.showerror("Error", "Login or registration failed!")
    
    def run(self):
        self.window.mainloop()

class ChatWindow:
    def __init__(self, messenger):
        self.messenger = messenger
        self.username = messenger.username
        self.window = tk.Tk()
        self.window.title(f"Chat - {messenger.username}")
        self.window.geometry("800x600")
        
        # Initialize data
        self.contacts = set()
        self.messages = {}
        
        # Create main container
        self.main_container = ttk.PanedWindow(self.window, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for contacts
        self.contacts_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.contacts_frame, weight=1)
        
        # Create right frame for messages
        self.messages_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.messages_frame, weight=3)
        
        # Setup contacts list
        self.setup_contacts_list()
        
        # Setup message display and input
        self.setup_message_area()
        
        # Setup menu
        self.setup_menu()
        
        # Load saved data
        self.load_data()
        
        # Start periodic message check
        self.check_new_messages()
    
    def setup_contacts_list(self):
        """Setup the contacts list widget"""
        # Contacts label
        ttk.Label(self.contacts_frame, text="Contacts").pack(pady=5)
        
        # Contacts treeview
        self.contacts_tree = ttk.Treeview(self.contacts_frame, selectmode='browse')
        self.contacts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.contacts_tree.bind('<<TreeviewSelect>>', self.on_contact_select)
        
        # Add contact button
        ttk.Button(self.contacts_frame, text="Add Contact", command=self.add_contact).pack(pady=5)
    
    def setup_message_area(self):
        """Setup the message display and input area"""
        # Message display
        self.message_display = tk.Text(self.messages_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.message_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message input frame
        input_frame = ttk.Frame(self.messages_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Message input
        self.message_input = tk.Text(input_frame, height=3, wrap=tk.WORD)
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Send button
        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side=tk.RIGHT, padx=5)
        
        # Bind Enter key to send message
        self.message_input.bind('<Control-Return>', lambda e: self.send_message())
    
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)
    
    def add_contact(self):
        """Add a new contact"""
        contact = simpledialog.askstring("Add Contact", "Enter username:")
        if contact:
            self.contacts.add(contact)
            self.contacts_tree.insert('', 'end', text=contact)
            if contact not in self.messages:
                self.messages[contact] = []
    
    def on_contact_select(self, event):
        """Handle contact selection"""
        selection = self.contacts_tree.selection()
        if selection:
            contact = self.contacts_tree.item(selection[0])['text']
            self.display_messages(contact)
    
    def display_messages(self, contact):
        """Display messages for selected contact"""
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        
        if contact in self.messages:
            for msg in self.messages[contact]:
                if msg.sender == self.messenger.username:
                    # Outgoing message
                    self.message_display.insert(tk.END, f"You: {msg.message}\n", "outgoing")
                else:
                    # Incoming message
                    self.message_display.insert(tk.END, f"{msg.sender}: {msg.message}\n", "incoming")
        
        self.message_display.config(state=tk.DISABLED)
        self.message_display.tag_configure("outgoing", justify=tk.RIGHT, foreground="blue")
        self.message_display.tag_configure("incoming", justify=tk.LEFT, foreground="green")
    
    def send_message(self):
        """Send a message to selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a contact!")
            return
        
        contact = self.contacts_tree.item(selection[0])['text']
        message = self.message_input.get(1.0, tk.END).strip()
        
        if message:
            if self.messenger.send(message, contact):
                # Add message to local storage
                dm = DirectMessage(message=message, recipient=contact, sender=self.messenger.username)
                if contact not in self.messages:
                    self.messages[contact] = []
                self.messages[contact].append(dm)
                # Clear input and update display
                self.message_input.delete(1.0, tk.END)
                self.display_messages(contact)
            else:
                messagebox.showerror("Error", "Failed to send message!")
    
    def check_new_messages(self):
        """Periodically check for new messages"""
        if self.messenger and self.messenger.token:
            new_messages = self.messenger.retrieve_new()
            for msg in new_messages:
                sender = msg.sender
                if sender not in self.contacts:
                    self.contacts.add(sender)
                    self.contacts_tree.insert('', 'end', text=sender)
                if sender not in self.messages:
                    self.messages[sender] = []
                self.messages[sender].append(msg)
                # Update display if this contact is selected
                selection = self.contacts_tree.selection()
                if selection and self.contacts_tree.item(selection[0])['text'] == sender:
                    self.display_messages(sender)
        
        # Schedule next check
        self.window.after(5000, self.check_new_messages)
    
    def save_data(self):
        """Save contacts和messages到messenger_data.json"""
        data = {
            'contacts': list(self.contacts),
            'messages': {
                contact: [
                    {
                        'message': msg.message,
                        'sender': msg.sender,
                        'recipient': msg.recipient,
                        'timestamp': msg.timestamp
                    }
                    for msg in messages
                ]
                for contact, messages in self.messages.items()
            }
        }
        
        with open('messenger_data.json', 'w') as f:
            json.dump(data, f)
    
    def load_data(self):
        """Load contacts and messages from file"""
        try:
            with open('messenger_data.json', 'r') as f:
                data = json.load(f)
                
                # Load contacts
                for contact in data['contacts']:
                    self.contacts.add(contact)
                    self.contacts_tree.insert('', 'end', text=contact)
                
                # Load messages
                for contact, messages in data['messages'].items():
                    self.messages[contact] = [
                        DirectMessage(
                            message=msg['message'],
                            sender=msg['sender'],
                            recipient=msg['recipient'],
                            timestamp=msg['timestamp']
                        )
                        for msg in messages
                    ]
        except FileNotFoundError:
            pass
    
    def run(self):
        self.window.mainloop()

def main():
    login = LoginWindow()
    login.run()

if __name__ == "__main__":
    main()
