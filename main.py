import tkinter as tk
from tkinter import scrolledtext
import subprocess

class LauncherApp:
    def __init__(self, master):
        self.master = master
        master.title("Launcher")
        master.geometry("600x400")  # Tamaño de la ventana

        self.label = tk.Label(master, text="Selecciona un archivo para ejecutar:")
        self.label.pack()

        self.file_buttons = []
        self.files = ["gausian/final/gausian_final.py", "gausian/semis/gausian_semi.py", "montecarlo/final/montecarlo_final.py", "montecarlo/semis/montecarlo_semis.py", "random_forest/final/randomforest_final2.py", "random_forest/semis/randomforest_semis.py", "xgboost/final/xgboost_final.py", "xgboost/semis/xboost_semis.py"]  # Lista de archivos a ejecutar

        for file in self.files:
            button = tk.Button(master, text=file, command=lambda f=file: self.execute_file(f))
            button.pack()
            self.file_buttons.append(button)

        self.output_label = tk.Label(master, text="Output:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(master, height=40, width=60)
        self.output_text.pack()

    def execute_file(self, file):
        try:
            output = subprocess.check_output(["python", file], universal_newlines=True, stderr=subprocess.STDOUT)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Error al ejecutar {}: {}".format(file, e.output))

root = tk.Tk()
app = LauncherApp(root)
root.mainloop()
