import tkinter as tk
import subprocess

class LauncherApp:
    def __init__(self, master):
        self.master = master
        master.title("Launcher")

        self.label = tk.Label(master, text="Selecciona un archivo para ejecutar:")
        self.label.pack()

        self.file_buttons = []
        self.files = ["gausian/final/gausian_final.py", "gausian/semis/gausian_semi.py", "montecarlo/final/montecarlo_final.py", "montecarlo/semis/montecarlo_semis.py", "random_forest/final/randomforest_final.py", "random_forest/semis/randomforest_semis.py", "xgboost/final/xgboost_final.py", "xgboost/semis/xboost_semis.py"]  # Lista de archivos a ejecutar

        for file in self.files:
            button = tk.Button(master, text=file, command=lambda f=file: self.execute_file(f))
            button.pack()
            self.file_buttons.append(button)

        self.output_label = tk.Label(master, text="")
        self.output_label.pack()

    def execute_file(self, file):
        output = subprocess.check_output(["python", file], universal_newlines=True)
        self.output_label.config(text=output)

root = tk.Tk()
app = LauncherApp(root)
root.mainloop()
