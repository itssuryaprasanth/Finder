import tkinter as tk
from tkinter import ttk
import pandas as pd

# Input data
data = [
    {'className': ['truste-button3']}, {}, {'className': ['truste-button2']}, {},
    {'className': ['truste-button1']}, {},
    {'className': ['footer-link', 'oui-p-0', 'oui-h-auto', 'oui-btn', 'oui-btn-link', 'oui-btn-sm', 'oui-disabled']}, {},
    {'className': ['oui-p-0', 'oui-btn', 'oui-btn-link', 'oui-btn-sm']}, {},
    {'className': ['login-button', 'oui-btn', 'oui-btn-primary', 'oui-btn-block', 'oui-disabled', 'oui-mr-0', 'oui-mt-4', 'oui-mb-4']}, {},
    {'className': ['oui-form-control']}, {'Name': 'email'}
]

# Create DataFrame and drop rows with all NaN values
df = pd.DataFrame(data).dropna(how='all')

# Convert list values to strings for all columns
df = df.map(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Data Display")
root.geometry("600x400")

# Create the Treeview widget
tree = ttk.Treeview(root, columns=list(df.columns), show="headings")

# Define the column headings
for column in df.columns:
    tree.heading(column, text=column)
    tree.column(column, width=250)  # Adjust width as needed

# Insert rows into the Treeview
for _, row in df.iterrows():
    tree.insert("", tk.END, values=list(row))

# Pack the Treeview to the Tkinter window
tree.pack(expand=True, fill="both")

# Run the Tkinter event loop
root.mainloop()
