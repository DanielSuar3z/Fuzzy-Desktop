import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Postura_Corporal_Funcional import sistema, ConjuntoDifuso


class EditorMembresias(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Editor de Funciones de Membresía")
        self.geometry("800x600")

        self.var_actual = tk.StringVar()
        self.nombre_conjunto = tk.StringVar()
        self.media = tk.DoubleVar(value=0)
        self.sigma = tk.DoubleVar(value=10)
        self.a = tk.DoubleVar(value=0)
        self.b = tk.DoubleVar(value=0)
        self.c = tk.DoubleVar(value=0)
        self.d = tk.DoubleVar(value=0)
        self.tipo_funcion = tk.StringVar(value="gaussiana")
        self.conjunto_seleccionado = None

        self._crear_widgets()
        self._actualizar_variables()

    #def _actualizar_variables(self):
     #   nombres = [v.nombre for v in SistemaDifuso.variables]
      #  self.combo_var['values'] = nombres


    def _crear_widgets(self):
        frame_top = tk.Frame(self)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Variable:").grid(row=0, column=0)
        self.combo_var = ttk.Combobox(frame_top, textvariable=self.var_actual, state="readonly")
        self.combo_var.grid(row=0, column=1)
        self.combo_var.bind("<<ComboboxSelected>>", lambda e: self._actualizar_lista_conjuntos())

        tk.Label(frame_top, text="Conjunto:").grid(row=1, column=0)
        tk.Entry(frame_top, textvariable=self.nombre_conjunto).grid(row=1, column=1)

        # Variables para a, b, c, d, media, sigma
        self.label_a = tk.Label(frame_top, text="a:")
        self.entry_a = tk.Entry(frame_top, textvariable=self.a)
        self.label_b = tk.Label(frame_top, text="b:")
        self.entry_b = tk.Entry(frame_top, textvariable=self.b)
        self.label_c = tk.Label(frame_top, text="c:")
        self.entry_c = tk.Entry(frame_top, textvariable=self.c)
        self.label_d = tk.Label(frame_top, text="d:")
        self.entry_d = tk.Entry(frame_top, textvariable=self.d)
        self.label_media = tk.Label(frame_top, text="Media:")
        self.entry_media = tk.Entry(frame_top, textvariable=self.media)
        self.label_sigma = tk.Label(frame_top, text="Sigma:")
        self.entry_sigma = tk.Entry(frame_top, textvariable=self.sigma)

        tk.Label(frame_top, text="Tipo de función:").grid(row=6, column=0)
        ttk.Combobox(frame_top, textvariable=self.tipo_funcion, state="readonly",
                    values=["gaussiana", "triangular", "trapezoidal"]).grid(row=6, column=1)

        # Un solo botón para agregar/actualizar conjunto
        tk.Button(frame_top, text="Agregar / Actualizar Conjunto", command=self._agregar_o_actualizar_conjunto).grid(row=7, columnspan=2, pady=5)

        # --- mostrar dinámicamente los campos necesarios ---
        self.tipo_funcion.trace_add("write", lambda *_: self._actualizar_campos_visibles())
        self._actualizar_campos_visibles()
        # Lista de conjuntos
        frame_list = tk.Frame(self)
        frame_list.pack()
        self.lista_conjuntos = tk.Listbox(frame_list, height=5, width=50)
        self.lista_conjuntos.pack(side=tk.LEFT, padx=10)
        self.lista_conjuntos.bind("<<ListboxSelect>>", self._seleccionar_conjunto)

        # Área de gráfica
        fig = Figure(figsize=(7, 3), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



    def _actualizar_variables(self):
        nombres = [v.nombre for v in sistema.variables]
        self.combo_var['values'] = nombres
        if nombres:
            self.var_actual.set(nombres[0])
            self._actualizar_lista_conjuntos()

    def _actualizar_lista_conjuntos(self):
        self.lista_conjuntos.delete(0, tk.END)
        var = sistema.obtener_variable(self.var_actual.get())
        if var:
            for i, c in enumerate(var.conjuntos):
                self.lista_conjuntos.insert(i, f"{c.nombre} ({c.tipo})")
        self._graficar()

    #def _seleccionar_conjunto(self, event):
        #selection = self.lista_conjuntos.curselection()
       # if selection:
           # index = selection[0]
           # var = sistema.obtener_variable(self.var_actual.get())
           # if var:
             #   c = var.conjuntos[index]
             #   self.nombre_conjunto.set(c.nombre)
              #  self.media.set(c.media)
               # self.sigma.set(c.sigma)
               # self.tipo_funcion.set(c.tipo)
               # self.conjunto_seleccionado = index

    def _seleccionar_conjunto(self, event):
        selection = self.lista_conjuntos.curselection()
        if selection:
            index = selection[0]
            var = sistema.obtener_variable(self.var_actual.get())
            if var:
                c = var.conjuntos[index]
                self.nombre_conjunto.set(c.nombre)
                self.tipo_funcion.set(c.tipo)
                self.conjunto_seleccionado = index

            # Mostrar media y sigma estimados a partir de los parámetros
                if c.tipo == "gaussiana":
                    media, sigma = c.parametros
                elif c.tipo == "triangular":
                    a, b, c_ = c.parametros
                    media = b
                    sigma = (c_ - a) / 2
                elif c.tipo == "trapezoidal":
                    a, b, c_, d = c.parametros
                    media = (b + c_) / 2
                    sigma = (d - a) / 4
                else:
                    media = 0
                    sigma = 10

                self.media.set(media)
                self.sigma.set(sigma)

    def _seleccionar_conjunto(self, event):
        selection = self.lista_conjuntos.curselection()
        if selection:
            index = selection[0]
            var = sistema.obtener_variable(self.var_actual.get())
            if var:
                c = var.conjuntos[index]
                self.nombre_conjunto.set(c.nombre)
                self.tipo_funcion.set(c.tipo)
                self.conjunto_seleccionado = index

            # Recuperar media y sigma aproximados para mostrar en la interfaz
                if c.tipo == "gaussiana":
                    media, sigma = c.parametros
                elif c.tipo == "triangular":
                    a, b, c_ = c.parametros
                    media = b
                    sigma = (c_ - a) / 2
                elif c.tipo == "trapezoidal":
                    a, b, c_, d = c.parametros
                    media = (b + c_) / 2
                    sigma = (d - a) / 4
                else:
                    media, sigma = 0, 10  # Por defecto

                self.media.set(media)
                self.sigma.set(sigma)



    def _agregar_o_actualizar_conjunto(self):
        nombre_var = self.var_actual.get()
        var = sistema.obtener_variable(nombre_var)
        if not var:
            return

        nuevo_nombre = self.nombre_conjunto.get()
        tipo = self.tipo_funcion.get()

        if tipo == "gaussiana":
            parametros = (self.media.get(), self.sigma.get())
        elif tipo == "triangular":
            parametros = (self.a.get(), self.b.get(), self.c.get())
        elif tipo == "trapezoidal":
            parametros = (self.a.get(), self.b.get(), self.c.get(), self.d.get())
        else:
            return

        conjunto = ConjuntoDifuso(nuevo_nombre, tipo, parametros)

        if self.conjunto_seleccionado is not None:
            var.conjuntos[self.conjunto_seleccionado] = conjunto
        else:
            var.conjuntos.append(conjunto)

        self._actualizar_lista_conjuntos()
        self._resetear_campos()


    def _resetear_campos(self):
        self.nombre_conjunto.set("")
        self.media.set(0)
        self.sigma.set(10)
        self.tipo_funcion.set("gaussiana")
        self.conjunto_seleccionado = None
        self.lista_conjuntos.selection_clear(0, tk.END)

    def _graficar(self):
        self.ax.clear()
        nombre_var = self.var_actual.get()
        var = sistema.obtener_variable(nombre_var)
        if not var:
            return

        x = np.linspace(var.rango[0], var.rango[1], 200)
        for c in var.conjuntos:
            if c.tipo == "gaussiana":
                y = np.exp(-((x - c.media) ** 2) / (2 * c.sigma ** 2))
                y[0], y[-1] = 1, 1

            elif c.tipo == "triangular":
                a, b, c_ = c.media - c.sigma, c.media, c.media + c.sigma
                y = np.maximum(np.minimum((x - a) / (b - a), (c_ - x) / (c_ - b)), 0)

            elif c.tipo == "trapezoidal":
                a, b = c.media - c.sigma * 2, c.media - c.sigma
                c_, d = c.media + c.sigma, c.media + c.sigma * 2
                y = np.maximum(np.minimum(np.minimum((x - a) / (b - a), 1), (d - x) / (d - c_)), 0)

            else:
                continue

            self.ax.plot(x, y, label=f"{c.nombre} ({c.tipo})")

        self.ax.set_title(f"Funciones de Membresía - {nombre_var}")
        self.ax.set_ylim(0, 1.1)
        self.ax.legend()
        self.canvas.draw()

    def _graficar(self):
        self.ax.clear()
        nombre_var = self.var_actual.get()
        var = sistema.obtener_variable(nombre_var)
        if not var:
            return

        x = np.linspace(var.rango[0], var.rango[1], 200)
        for c in var.conjuntos:
            if c.tipo == "gaussiana":
                media, sigma = c.parametros
                y = np.exp(-((x - media) ** 2) / (2 * sigma ** 2))
                y[0], y[-1] = 1, 1

            elif c.tipo == "triangular":
                a, b, c_ = c.parametros
                y = np.maximum(np.minimum((x - a) / (b - a), (c_ - x) / (c_ - b)), 0)

            elif c.tipo == "trapezoidal":
                a, b, c_, d = c.parametros
                y = np.maximum(np.minimum(np.minimum((x - a) / (b - a), 1), (d - x) / (d - c_)), 0)

            else:
                continue

            self.ax.plot(x, y, label=f"{c.nombre} ({c.tipo})")

        self.ax.set_title(f"Funciones de Membresía - {nombre_var}")
        self.ax.set_ylim(0, 1.1)        
        if self.ax.get_lines():
            self.ax.legend()
        self.canvas.draw()

    



    def _actualizar_campos_visibles(self):
        # Oculta todos los campos primero
        for widget in [self.label_a, self.entry_a, self.label_b, self.entry_b,
                    self.label_c, self.entry_c, self.label_d, self.entry_d,
                    self.label_media, self.entry_media, self.label_sigma, self.entry_sigma]:
            widget.grid_forget()

        tipo = self.tipo_funcion.get()

        if tipo == "gaussiana":
            self.label_media.grid(row=2, column=0)
            self.entry_media.grid(row=2, column=1)
            self.label_sigma.grid(row=3, column=0)
            self.entry_sigma.grid(row=3, column=1)
        elif tipo == "triangular":
            self.label_a.grid(row=2, column=0)
            self.entry_a.grid(row=2, column=1)
            self.label_b.grid(row=3, column=0)
            self.entry_b.grid(row=3, column=1)
            self.label_c.grid(row=4, column=0)
            self.entry_c.grid(row=4, column=1)
        elif tipo == "trapezoidal":
            self.label_a.grid(row=2, column=0)
            self.entry_a.grid(row=2, column=1)
            self.label_b.grid(row=3, column=0)
            self.entry_b.grid(row=3, column=1)
            self.label_c.grid(row=4, column=0)
            self.entry_c.grid(row=4, column=1)
            self.label_d.grid(row=5, column=0)
            self.entry_d.grid(row=5, column=1)

