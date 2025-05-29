# NAME
# EMAIL
# STUDENT ID

import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog
from bookmarker import Bookmarker


class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._id = 0
        self._draw()
    
    def node_select(self, event):
        index = int(self.url_tree.selection()[0])
        s = self.url_tree.item(index)

        if self._select_callback is not None:
            self._select_callback(s['text'])


    def insert_url(self, url) -> str:
        self._insert_tree(self._id, url)
        self._id+=1
        self.message_editor.delete(1.0, tk.END)
        return url

    def remove_selected_url(self):
        index = int(self.url_tree.selection()[0])
        self.url_tree.delete(index)

    def get_url(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def get_selected_url(self) -> str:
        index = int(self.url_tree.selection()[0])
        item = self.url_tree.item(index)
        return item['text']
    
    def load_urls(self, urls:list):
        for i in range(0, len(urls)):
            url = str(urls[i]).strip()
            self._insert_tree(i, url)
            self._id+=i
    
    def _insert_tree(self, id, url):
        id = self.url_tree.insert('', id, id, text=url)


    def reset_ui(self):
        self.message_editor.delete(1.0, tk.END)
        for item in self.url_tree.get_children():
            self.url_tree.delete(item)

    def _draw(self):
        entry_frame = tk.Frame(master=self)
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame)
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        self.url_tree = ttk.Treeview(editor_frame) 
        self.url_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.url_tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=2, pady=0)
        
        message_frame = tk.Frame(master=self)
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)
        


class Footer(tk.Frame):
    def __init__(self, root, add_callback=None, delete_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._add_callback = add_callback
        self._delete_callback = delete_callback
        self._draw()
    
    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()
    
    def delete_click(self):
        if self._delete_callback is not None:
            self._delete_callback()

    def disable(self):
        self.delete_button["state"] = "disabled"
        self.add_button["state"] = "disabled"

    def enable(self):
        self.delete_button["state"] = "active"
        self.add_button["state"] = "active"
    
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    def _draw(self):
        self.delete_button = tk.Button(master=self, text="Delete", width=20)
        self.delete_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        self.add_button = tk.Button(master=self, text="Add", width=20)
        self.add_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        
        self.footer_label = tk.Label(master=self, text="Open or Create New Bookmark File.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)
        
        self.disable() 
    
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._filename = None
        self._bookmarker = None

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.reset_ui()

    def new_file(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('PyBookmark', '*.pbm')])
        self._filename = filename.name

        # update status bar and enable buttons
        self.footer.set_status(self._filename) 
        self.footer.enable()

        # create bookmarker object
        self._bookmarker = Bookmarker(Path(self._filename))
        # reset
        self.body.reset_ui()
    
    def open_file(self):
        filename = tk.filedialog.askopenfile(filetypes=[('PyBookmark', '*.pbm')])
        self._filename = filename.name
        
        # update status bar and enable buttons
        self.footer.set_status(self._filename) 
        self.footer.enable()
        
        self.body.reset_ui()
        # create bookmarker object
        self._bookmarker = Bookmarker(Path(self._filename))

        # load tree
        self.body.load_urls(self._bookmarker.all_notes)
    
    def close(self):
        self.root.destroy()
    
    def add_clicked(self):
        # get url from text input
        url = self.body.get_url()
        try:
            self._bookmarker.add(url)
        except ValueError as ve:
            self.footer.set_status(ve)
        else:
            self.body.insert_url(url)
            self.footer.set_status(self._filename) 
    
    def delete_clicked(self):
        url = self.body.get_selected_url()
        try:
            self._bookmarker.remove_by_url(url+'\n')
        except ValueError as ve:
            self.footer.set_status(ve)
        else:
            self.body.remove_selected_url()
            self.footer.set_status(self._filename) 
    
    def reset_ui(self):
        pass
    
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        
        menu_file = tk.Menu(menu_bar)
        
        menu_bar.add_cascade(menu=menu_file, label='File')
        #menu_bar.add_cascade(menu=menu_file, label='Edit')
        
        menu_file.add_command(label='New', command=self.new_file)
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close', command=self.close)
        
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":

    main = tk.Tk()

    main.title("PyBookmarker")

    main.geometry("720x480")

    main.option_add('*tearOff', False)

    MainApp(main)
    
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()


