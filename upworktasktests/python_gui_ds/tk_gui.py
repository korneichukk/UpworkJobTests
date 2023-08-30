import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd


def open_and_plot():
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )

    if file_path:
        data = pd.read_csv(file_path)
        x = data[
            "X"
        ]  # Assuming 'X' is the column name in your CSV file
        y = data[
            "Y"
        ]  # Assuming 'Y' is the column name in your CSV file

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker="o")
        plt.title("CSV Data Plot")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.grid(True)
        plt.show()


root = tk.Tk()
root.title("CSV Data Plotter")
root.geometry("1000x1000")

button = tk.Button(
    root, text="Open CSV File and Plot", command=open_and_plot
)
button.pack(pady=10)

root.mainloop()
