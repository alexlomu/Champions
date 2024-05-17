import tkinter as tk
from tkinter import scrolledtext
import subprocess

class LauncherApp:
    def __init__(self, master):
        self.master = master
        master.title("Launcher")
        master.geometry("1000x700")  # Tamaño de la ventana ajustado para más espacio

        self.label = tk.Label(master, text="Selecciona un archivo para ejecutar:")
        self.label.pack()

        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Añadir texto encima de cada listado de botones
        self.left_label = tk.Label(self.left_frame, text="Archivos que predicen ganador/empate")
        self.left_label.pack()

        self.right_label = tk.Label(self.right_frame, text="Archivos que predicen el marcador")
        self.right_label.pack()

        self.file_buttons_left = []
        self.file_buttons_right = []

        # Lista de archivos a ejecutar
        self.files = [
            "gausian/final/gausian_final_ganador.py", "gausian/semis/gausian_semis_ganador.py", 
            "montecarlo/final/montecarlo_final_ganador.py", "montecarlo/semis/montecarlo_semis_ganador.py",
            "random_forest/final/randomforest_final_ganador.py", "random_forest/semis/randomforest_semis_ganador.py", 
            "xgboost/final/xgboost_final_ganador.py", "xgboost/semis/xboost_semis_ganador.py",
            "gausian/final/gausian_final_marcador.py", "gausian/semis/gausian_semis_marcador.py", 
            "montecarlo/final/montecarlo_final_marcador.py", "montecarlo/semis/montecarlo_semis_marcador.py",
            "random_forest/final/randomforest_final_marcador.py", "random_forest/semis/randomforest_semis_marcador.py", 
            "xgboost/final/xgboost_final_marcador.py", "xgboost/semis/xgboost_semis_marcador.py"
        ]

        # Dividir los archivos en dos listas
        half = len(self.files) // 2
        files_left = self.files[:half]
        files_right = self.files[half:]

        for file in files_left:
            button = tk.Button(self.left_frame, text=file, command=lambda f=file: self.execute_file(f))
            button.pack(pady=5)
            self.file_buttons_left.append(button)

        for file in files_right:
            button = tk.Button(self.right_frame, text=file, command=lambda f=file: self.execute_file(f))
            button.pack(pady=5)
            self.file_buttons_right.append(button)

        self.output_label = tk.Label(master, text="Output:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(master, height=30, width=120) 
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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
