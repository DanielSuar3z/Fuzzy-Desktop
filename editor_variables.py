import tkinter as tk
from tkinter import ttk
from Postura_Corporal_Funcional import sistema

class EditorVariables(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Editor de Variables")
        self.geometry("400x300")
        self.configure(bg="white")

        self.nombre_var = tk.StringVar()
        self.tipo_var = tk.StringVar(value="input")
        self.rango_min = tk.DoubleVar(value=0)
        self.rango_max = tk.DoubleVar(value=100)

        self.crear_widgets()
        self.refrescar_lista()

    def crear_widgets(self):
        tk.Label(self, text="Nombre de Variable:").pack(pady=5)
        tk.Entry(self, textvariable=self.nombre_var).pack(pady=2)

        frame_tipo = tk.Frame(self)
        frame_tipo.pack(pady=5)
        tk.Label(frame_tipo, text="Tipo:").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_tipo, text="Entrada", variable=self.tipo_var, value="input").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_tipo, text="Salida", variable=self.tipo_var, value="output").pack(side=tk.LEFT)

        frame_rango = tk.Frame(self)
        frame_rango.pack(pady=5)
        tk.Label(frame_rango, text="Rango: ").pack(side=tk.LEFT)
        tk.Entry(frame_rango, textvariable=self.rango_min, width=5).pack(side=tk.LEFT)
        tk.Label(frame_rango, text="a").pack(side=tk.LEFT)
        tk.Entry(frame_rango, textvariable=self.rango_max, width=5).pack(side=tk.LEFT)

        tk.Button(self, text="Agregar Variable", command=self.agregar_variable).pack(pady=10)

        self.lista_vars = tk.Frame(self)
        self.lista_vars.pack(pady=10, fill="both", expand=True)

    def agregar_variable(self):
        nombre = self.nombre_var.get().strip()
        tipo = self.tipo_var.get()
        r_min = self.rango_min.get()
        r_max = self.rango_max.get()

        if not nombre:
            return

        sistema.agregar_variable(nombre, tipo, (r_min, r_max))
        self.refrescar_lista()
        self.nombre_var.set("")
        self.tipo_var.set("input")

    def refrescar_lista(self):
        for widget in self.lista_vars.winfo_children():
            widget.destroy()

        for var in sistema.variables:
            color = "yellow" if var.tipo == "input" else "lightblue"
            etiqueta = tk.Label(self.lista_vars, text=f"{var.nombre} ({var.tipo}) [{var.rango[0]} - {var.rango[1]}]",
                                bg=color, fg="black", padx=5, pady=2)
            etiqueta.pack(pady=2, fill="x", padx=10)

