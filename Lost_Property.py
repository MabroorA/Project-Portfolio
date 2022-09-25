from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("Lost Property")
root.geometry("735x500")
root.resizable(0,0)
root["bg"] = "#CBC3E3"

# Database
conn = sqlite3.connect('lost_property.db')
c = conn.cursor()

# Create table item searching table
# c.execute("""CREATE TABLE addresses (
#             ItemName text,
#             Description text,
#             InStock int,
#             DateIn text
#             )""")
#
conn.commit()
conn.close()


# submit button
def submit():
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()

    # Execute into Table
    c.execute("INSERT INTO addresses VALUES(:ItemName ,:Description ,:InStock ,:DateIn ,:Location )",
              {
                  "ItemName": ItemName.get(),
                  "Description": Description.get(),
                  "InStock": InStock.get(),
                  "DateIn": DateIn.get(),
                  "Location": Location.get()
              }

              )
    conn.commit()
    conn.close()





# Delete function

def delete():
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()

    c.execute("DELETE from addresses WHERE oid = " + delete_box.get())

    delete_box.delete(0, END)

    conn.commit()
    conn.close()


# edit button

def edit():
    global editor
    editor = Tk()
    editor.title("Update A Record ")
    editor.geometry("400x600")
    # Edit Query
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall()

    # Create global variables

    global ItemName_editor
    global Description_editor
    global InStock_editor
    global DateIn_editor
    global Location_editor

    # Create Editor Text boxs
    ItemName_editor = Entry(editor, width=30)
    ItemName_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    Description_editor = Entry(editor, width=30)
    Description_editor.grid(row=1, column=1)
    InStock_editor = Entry(editor, width=30)
    InStock_editor.grid(row=2, column=1)
    DateIn_editor = Entry(editor, width=30)
    DateIn_editor.grid(row=3, column=1)
    Location_editor = Entry(editor, width=30)
    Location_editor.grid(row=4, column=1)

    # Create Text box labels
    ItemName_label = Label(editor, text="Item Name")
    ItemName_label.grid(row=0, column=0, pady=(10, 0))
    Description_label = Label(editor, text="Description")
    Description_label.grid(row=1, column=0)
    InStock_label = Label(editor, text="InStock")
    InStock_label.grid(row=2, column=0)
    DateIn_label = Label(editor, text="DateIn")
    DateIn_label.grid(row=3, column=0)
    LocationStored_label = Label(editor, text="Location Stored")
    LocationStored_label.grid(row=4, column=0)

    # Create a Save Button to save edited record
    edit_btn = Button(editor, text="Save Record", bg="#ADD8E6", command=update)
    edit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=144)

    # loop through result
    for record in records:
        ItemName_editor.insert(0, record[0])
        Description_editor.insert(0, record[1])
        InStock_editor.insert(0, record[2])
        DateIn_editor.insert(0, record[3])
        Location_editor.insert(0, record[4])


# Save Record

def update():
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE addresses SET 
        ItemName = :ItemName,
        Description = :Description,
        InStock = :InStock,
        DateIn = :DateIn,
        Location = :Location
        
        WHERE oid = :oid""",
              {
                  'ItemName': ItemName_editor.get(),
                  'Description': Description_editor.get(),
                  'InStock': InStock_editor.get(),
                  'DateIn': DateIn_editor.get(),
                  'Location': Location_editor.get(),
                  'oid': record_id
              })

    conn.commit()
    conn.close()
    # Shut window
    editor.destroy()


#

def add_data_to_table():
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()

    c.execute("SELECT rowid,* FROM addresses ")
    records = c.fetchall()
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=("evenrow",))
        else:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=("oddrow",))
        count += 1

    print(records)

    conn.commit()
    conn.close()


# Select record
def select_record(event):
    # Clear box
    Item_number.delete(0, END)
    ItemName.delete(0, END)
    Description.delete(0, END)
    DateIn.delete(0, END)
    InStock.delete(0, END)
    Location.delete(0, END)

    # Get record number
    selected = my_tree.focus()

    # Grab record values

    values = my_tree.item(selected, "values")
    Item_number.insert(0, values[0])
    ItemName.insert(0, values[1])
    Description.insert(0, values[2])
    InStock.insert(0, values[3])
    DateIn.insert(0, values[4])
    Location.insert(0, values[5])


# Clear Text boxs
def clear_entries():
    # Clear box
    ItemName.delete(0, END)
    Description.delete(0, END)
    InStock.delete(0, END)
    DateIn.delete(0, END)
    Location.delete(0, END)




# Update record

def update_record():
    selected = my_tree.focus()
    # Update record
    my_tree.item(selected, text="", values=(
        Item_number.get(), ItemName.get(), Description.get(), InStock.get(), DateIn.get(), Location.get(),))
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()

    c.execute("""UPDATE addresses SET 
           ItemName = :ItemName,
           Description = :Description,
           InStock = :InStock,
           DateIn = :DateIn,
           Location = :Location

           WHERE oid = :oid""",
              {
                  'oid': Item_number.get(),
                  'ItemName': ItemName.get(),
                  'Description': Description.get(),
                  'InStock': InStock.get(),
                  'DateIn': DateIn.get(),
                  'Location': Location.get()

              })
    conn.commit()
    conn.close()







# ADD RECORD








# ADD RECORD
def Add_record():


    # Update record
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()


    c.execute("INSERT INTO addresses VALUES(:ItemName ,:Description ,:InStock ,:DateIn ,:Location )",
              {
                  "ItemName": ItemName.get(),
                  "Description": Description.get(),
                  "InStock": InStock.get(),
                  "DateIn": DateIn.get(),
                  "Location": Location.get()
              }

              )

    conn.commit()
    conn.close()
    # CLEAR boxs after adding
    ItemName.delete(0, END)
    Description.delete(0, END)
    InStock.delete(0, END)
    DateIn.delete(0, END)
    Location.delete(0, END)
    Item_number.delete(0,END)
    # Clear The Treeview Table
    my_tree.delete(*my_tree.get_children())
    #Run Treeview again
    add_data_to_table()

# Delete Record
def delete_record():
    selected = my_tree.focus()
    # Update record
    my_tree.item(selected, text="", values=(
        Item_number.get(), ItemName.get(), Description.get(), InStock.get(), DateIn.get(), Location.get(),))
    conn = sqlite3.connect('lost_property.db')
    c = conn.cursor()

    c.execute("DELETE FROM addresses WHERE oid="+Item_number.get())
    conn.commit()
    conn.close()

    # CLEAR boxs after adding
    ItemName.delete(0, END)
    Description.delete(0, END)
    InStock.delete(0, END)
    DateIn.delete(0, END)
    Location.delete(0, END)
    # Clear The Treeview Table
    my_tree.delete(*my_tree.get_children())
    # Run Treeview again
    add_data_to_table()

    messagebox.showinfo("Deleted!","Record has been deleted")












# Creating a tree view for CRM



my_tree = ttk.Treeview(root)

style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3"
                )
style.map("Treeview",
          background=[("selected", "#347083")])

# Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)
# scroll bar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
# Create Tree view
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# configure scroll bar
tree_scroll.config(command=my_tree.yview)
# Rows color
my_tree.tag_configure("oddrow", background="white")
my_tree.tag_configure("evenrow", background="lightblue")

my_tree['columns'] = ("Item Number", "Item", "Description", "Date In", "InStock", "Location Stored")

# format our columns
my_tree.column("#0", width=0, stretch=0)
my_tree.column("Item Number", anchor=W, width=90, minwidth=90)
my_tree.column("Item", anchor=W, width=90, minwidth=90)
my_tree.column("Description", anchor=W, width=120, minwidth=120)
my_tree.column("InStock", anchor=CENTER, width=50, minwidth=50)
my_tree.column("Date In", anchor=CENTER, width=50, minwidth=50)
my_tree.column("Location Stored", anchor=CENTER, width=140, minwidth=90)

# Tree view headings
my_tree.heading("#0", text="Label", anchor=W)
my_tree.heading("Item Number", text="Item Number", anchor=W)
my_tree.heading("Item", text="Item", anchor=W)
my_tree.heading("Description", text="Description", anchor=W)
my_tree.heading("InStock", text="Date In", anchor=CENTER)
my_tree.heading("Date In", text="InStock", anchor=CENTER)
my_tree.heading("Location Stored", text="Location Stored", anchor=CENTER)

# binding treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# adding data to tree view at start
add_data_to_table()

# Input Frame
data_frame = LabelFrame(root, text="Record", background="lightgray", relief=SOLID)
data_frame.pack(fill="x", expand="yes", padx=20)

ItemName_label = Label(data_frame, text="Item Name")
ItemName_label.grid(row=0, column=0, padx=10, pady=10)
ItemName = Entry(data_frame)
ItemName.grid(row=0, column=1, padx=10, pady=10)

Description_label = Label(data_frame, text="Description")
Description_label.grid(row=1, column=0, padx=10, pady=10)
Description = Entry(data_frame)
Description.grid(row=1, column=1, padx=10, pady=10)

InStock_label = Label(data_frame, text="InStock")
InStock_label.grid(row=0, column=2, padx=10, pady=10)
InStock = Entry(data_frame)
InStock.grid(row=0, column=3, padx=10, pady=10)

DateIn_label = Label(data_frame, text="Date In")
DateIn_label.grid(row=1, column=2, padx=10, pady=10)
DateIn = Entry(data_frame)
DateIn.grid(row=1, column=3, padx=10, pady=10)

Location_label = Label(data_frame, text="Location Stored")
Location_label.grid(row=0, column=4, padx=10, pady=10)
Location = Entry(data_frame)
Location.grid(row=0, column=5, padx=10, pady=10)

Item_number_label = Label(data_frame, text="Item Number")
Item_number_label.grid(row=1, column=4, padx=10, pady=10)
Item_number = Entry(data_frame)
Item_number.grid(row=1, column=5, padx=10, pady=10)


# Buttons Frame
button_frame = LabelFrame(root, text="Commands", background="lightgray", relief=SOLID)
button_frame.pack(fill="x", expand="yes", padx=20)

# Buttons
# ADD RECORD button
ADD_btn = Button(button_frame, text="Add Record ", bg="#90ee90", command=Add_record)
ADD_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=10, )
# Update RECORD Button
update_btn = Button(button_frame, text="Update Record", bg="#ADD8E6", command=update_record)
update_btn.grid(row=0, column=2, columnspan=1, padx=10, pady=10)
# Delete Record Button
delete_btn = Button(button_frame, text="Delete Record", bg="#FFCCCB", command=delete_record)
delete_btn.grid(row=0, column=4, columnspan=2, pady=10, padx=10, )
# Clear button
Clear_btn = Button(button_frame, text="Clear Entry Boxes", bg="#a9a9a9", command=clear_entries)
Clear_btn.grid(row=0, column=6, columnspan=2, pady=10, padx=10)

root.mainloop()
