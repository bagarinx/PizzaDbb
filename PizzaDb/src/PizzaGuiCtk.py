import json
import customtkinter
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import messagebox
from PizzaDbSqlite import PizzaDbSqlite
from PIL import Image, ImageTk
import PIL
import os
class PizzaGuiCtk(customtkinter.CTk): 

    def __init__(self, dataBase=PizzaDbSqlite('PizzaDb.db')):
        super().__init__()
        self.db = dataBase

    #Logo of Inventory System
        image_path = "pizza2.png" 

        if os.path.exists(image_path):
            NM = ImageTk.PhotoImage(Image.open(image_path))
        else:
            print(f"Error: File not found at {image_path}")

        global png_image

        target_width = 850
        target_height = 500

        original_img = Image.open(image_path)
        resized_img = original_img.resize((target_width, target_height), PIL.Image.Resampling.LANCZOS)
        png_img = ImageTk.PhotoImage(resized_img)
        
        self.png_image_label = Label(self, image=png_img, bd=0)
        self.png_image_label.photo = png_img
        self.png_image_label.place(x=25, y=-10)


        self.title('La Rosas Pizzeria Inventory System')
        self.geometry('1300x550')
        self.config(bg='#AD2517')
        self.resizable(False, False)

        self.font1 = ('Arial', 16, 'bold')
        self.font2 = ('Arial', 10, 'bold')

        # Data Entry Form
        # 'Item' Label and Entry Widgets
        self.id_label = self.newCtkLabel('Ref#')
        self.id_label.place(x=20, y=190)
        self.id_entry = self.newCtkEntry()
        self.id_entry.place(x=100, y=190)

        # 'Item Name' Label and Entry Widgets
        self.item_label = self.newCtkLabel('Item')
        self.item_label.place(x=20, y=240)
        self.item_entry = self.newCtkEntry()
        self.item_entry.place(x=100, y=240)

        # 'Type' Label and Combo Box Widgets
        self.type_label = self.newCtkLabel('Class')
        self.type_label.place(x=20, y=290)
        self.type_cboxVar = StringVar()
        self.type_cboxOptions = ['Pizza', 'Appetizer', 'Beverage', 'Desserts', 'Salads']
        self.type_cbox = self.newCtkComboBox(options=self.type_cboxOptions, 
                                    entryVariable=self.type_cboxVar)
        self.type_cbox.place(x=100, y=290)

        # 'Price' Label and Combo Box Widgets
        self.price_label = self.newCtkLabel('Price')
        self.price_label.place(x=20, y=340)
        self.price_entry = self.newCtkEntry()
        self.price_entry.place(x=100, y=340)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=390)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['In Stock', 'Running Low', 'Not Available']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=390)

        self.add_button = self.newCtkButton(text='Add Item',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=90,y=450)

        self.new_button = self.newCtkButton(text='New Item',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=610,y=450)

        self.update_button = self.newCtkButton(text='Update Item',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=400,y=450)

        self.delete_button = self.newCtkButton(text='Delete Item',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=90, y=500)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=820,y=450)

        self.export_button = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_to_json)
        self.export_button.place(x=1030,y=450)

        self.import_button = self.newCtkButton(text='Import from CSV',
                                    onClickHandler=self.import_from_csv)
        self.import_button.place(x=1030, y=490)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#997950',
                        background='#F5EDCF',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('id','item', 'type', 'price', 'status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('id', anchor=tk.CENTER, width=10)
        self.tree.column('item', anchor=tk.CENTER, width=90)
        self.tree.column('type', anchor=tk.CENTER, width=90)
        self.tree.column('price', anchor=tk.CENTER, width=10)
        self.tree.column('status', anchor=tk.CENTER, width=0)

        self.tree.heading('id', text='Ref#')
        self.tree.heading('item', text='Item')
        self.tree.heading('type', text='Type')
        self.tree.heading('price', text='Price') 
        self.tree.heading('status', text='Status')

        self.tree.place(x=400, y=50, width=800, height=365)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget #Text Beside Box entries
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#F5EDCF'
        widget_BgColor='#AD2517'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#997950'
        widget_FgColor='#F5EDCF'
        widget_BorderColor='#AD2517'
        widget_BorderWidth=2
        widget_Width=200

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#997950'
        widget_FgColor='#F5EDCF'
        widget_DropdownHoverColor='#FFFDE7'
        widget_ButtonColor='#FFFDE7'
        widget_ButtonHoverColor='#FFFDE7'
        widget_BorderColor='#FFFDE7'
        widget_BorderWidth=2
        widget_Width=200
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#032552', hoverColor='#032552', bgColor='#AD2517', borderColor='#AD2517'):
        widget_Font=self.font1
        widget_TextColor='#F5EDCF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=20
        widget_Width=200
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        pizza = self.db.fetch_item()
        self.tree.delete(*self.tree.get_children())
        for pizza in pizza:
            print(pizza)
            self.tree.insert('', END, values=pizza)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entry.delete(0, END)
        self.item_entry.delete(0, END)
        self.type_cboxVar.set('Select class')
        self.price_entry.delete(0, END)
        self.status_cboxVar.set('Select availability')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.item_entry.insert(0, row[1])
            self.type_cboxVar.set(row[2])
            self.price_entry.insert(0, row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        id=self.id_entry.get()
        item=self.item_entry.get()
        type=self.type_cboxVar.get()
        price=self.price_entry.get()
        status=self.status_cboxVar.get()

        if not (id and item and type and price and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_item(id, item, type, price, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an item to delete')
        else:
            id = self.id_entry.get()
            self.db.delete_item(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Item has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an item to update')
        else:
            id=self.id_entry.get()
            item=self.item_entry.get()
            type=self.type_cboxVar.get()
            price=self.price_entry.get()
            status=self.status_cboxVar.get()
            self.db.update_item(item, type, price, status, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Item has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def export_to_json(self):
        try:
            self.db.export_json()
            messagebox.showinfo('Success', f'Data exported to {self.db.dbName.replace(".db", ".json")}')
        except Exception as e:
            messagebox.showerror('Error', f'Error exporting to JSON: {str(e)}')

    def import_from_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data imported from {self.db.dbName}.csv')
