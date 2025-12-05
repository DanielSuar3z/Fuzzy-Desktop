import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from Postura_Corporal_Funcional import sistema

class SistemaInferencia:
    def __init__(self, sistema_difuso):
        self.sistema_difuso = sistema_difuso
        self.control_vars = {}
        self._crear_variables()
        self._crear_reglas()

    def _crear_variables(self):
        # Crear variables de entrada y salida para skfuzzy
        for var in self.sistema_difuso.variables:
            universo = np.arange(var.rango[0], var.rango[1] + 1, 1)
            if var.tipo == 'entrada':
                self.control_vars[var.nombre] = ctrl.Antecedent(universo, var.nombre)
            else:
                self.control_vars[var.nombre] = ctrl.Consequent(universo, var.nombre)

            # Agregar conjuntos difusos
            for conjunto in var.conjuntos:
                if conjunto.tipo == 'gaussiana':
                    #mf = fuzz.gaussmf(universo, conjunto.parametros['media'], conjunto.parametros['desviacion'])
                    media, sigma = conjunto.parametros
                    mf = fuzz.gaussmf(universo, media, sigma)

                elif conjunto.tipo == 'triangular':
                    #mf = fuzz.trimf(universo, [
                      #  conjunto.parametros['a'], 
                     #   conjunto.parametros['b'], 
                      #  conjunto.parametros['c']
                    #])
                    a, b, c = conjunto.parametros
                    mf = fuzz.trimf(universo, [a, b, c])
                elif conjunto.tipo == 'trapezoidal':
                    #mf = fuzz.trapmf(universo, [
                      # conjunto.parametros['a'], 
                      #  conjunto.parametros['b'], 
                      #  conjunto.parametros['c'], 
                      #  conjunto.parametros['d']
                    #])
                    a, b, c_, d = conjunto.parametros
                    mf = fuzz.trapmf(universo, [a, b, c_, d])
                else:
                    continue
                self.control_vars[var.nombre][conjunto.nombre] = mf

    def _crear_reglas(self):
        self.reglas = []
        for regla in self.sistema_difuso.reglas:
            antecedentes = None
            for nombre_var, nombre_conjunto in regla.condiciones:
                actual = self.control_vars[nombre_var][nombre_conjunto]
                if antecedentes is None:
                    antecedentes = actual
                else:
                    antecedentes &= actual

            consecuente_var, consecuente_conjunto = regla.resultado
            consecuente = self.control_vars[consecuente_var][consecuente_conjunto]
            self.reglas.append(ctrl.Rule(antecedentes, consecuente))

        self.sistema_ctrl = ctrl.ControlSystem(self.reglas)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_ctrl)

    def evaluar(self, entradas: dict) -> dict:
        for var, valor in entradas.items():
            self.simulador.input[var] = valor
        self.simulador.compute()

        salidas = {}
        for nombre_var, var in self.control_vars.items():
            if isinstance(var, ctrl.Consequent):
                salidas[nombre_var] = self.simulador.output[nombre_var]
        return salidas


import tkinter as tk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from Postura_Corporal_Funcional import sistema
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class InferenciaFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Sistema de Inferencia Difusa")
        self.geometry("1000x600")

        self.metodo_entrada = tk.StringVar(value="radio")  # Método por defecto
        self.radio_vars = {}
        self.slider_vars = {}

        self._construir_ui()

    def _construir_ui(self):
        tk.Label(self, text="Método de Entrada:", font=("Arial", 12)).pack(pady=5)
        frame_opciones = tk.Frame(self)
        frame_opciones.pack()
        tk.Radiobutton(frame_opciones, text="Botones", variable=self.metodo_entrada, value="radio", command=self._cambiar_metodo_entrada).pack(side="left")
        tk.Radiobutton(frame_opciones, text="Deslizadores", variable=self.metodo_entrada, value="slider", command=self._cambiar_metodo_entrada).pack(side="left")

        self.frame_radio = tk.Frame(self)
        self.frame_slider = tk.Frame(self)

        self.frame_radio.pack(pady=10)
        self.frame_slider.pack_forget()

        self.radio_vars = {}
        self.slider_vars = {}

        self.frame_entradas = tk.Frame(self.frame_radio)
        self.frame_entradas.pack()

        for var in sistema.variables:
            if var.tipo == 'entrada':
                # ---------- RadioButtons ----------
                frame_rb = tk.Frame(self.frame_entradas)
                frame_rb.pack(fill="x", padx=10, pady=5)

                tk.Label(frame_rb, text=var.nombre + ":", font=("Arial", 10)).pack(side="left", padx=5)

                selected = tk.StringVar()
                self.radio_vars[var.nombre] = selected

                frame_botones = tk.Frame(frame_rb)
                frame_botones.pack(side="left")
                for conjunto in var.conjuntos:
                    rb = tk.Radiobutton(frame_botones, text=conjunto.nombre, variable=selected, value=conjunto.nombre)
                    rb.pack(side="left", padx=3)

                # ---------- Sliders ----------
                frame_sl = tk.Frame(self.frame_slider)
                frame_sl.pack(fill="x", padx=10, pady=5)

                frame_sl_inner = tk.Frame(frame_sl)
                frame_sl_inner.pack(fill="x")

                tk.Label(frame_sl_inner, text=var.nombre + ":", font=("Arial", 10), width=18, anchor="e").pack(side="left", padx=5)

                val = tk.DoubleVar(value=(var.rango[0] + var.rango[1]) / 2)
                self.slider_vars[var.nombre] = val

                slider = tk.Scale(frame_sl_inner, from_=var.rango[0], to=var.rango[1],
                                orient="horizontal", variable=val, resolution=1, length=300)
                slider.pack(side="left", padx=5)


        # Frame fijo para el botón y resultado
        self.frame_resultado = tk.Frame(self)
        self.frame_resultado.pack(pady=10)

        tk.Button(self.frame_resultado, text="Evaluar", command=self.evaluar).pack(pady=5)
        self.resultado_texto = tk.Label(self.frame_resultado, text="Resultado:", font=("Arial", 12))
        self.resultado_texto.pack()



    def _cambiar_metodo_entrada(self):
        if self.metodo_entrada.get() == "radio":
            self.frame_slider.pack_forget()
            self.frame_radio.pack(pady=10)
        else:
            self.frame_radio.pack_forget()
            self.frame_slider.pack(pady=10)

    def evaluar(self):
        if self.metodo_entrada.get() == "slider":
            entradas = {nombre: var.get() for nombre, var in self.slider_vars.items()}
        else:
            entradas = {}
            for var in sistema.variables:
                if var.tipo == 'entrada':
                    conjunto_sel = self.radio_vars[var.nombre].get()
                    conjunto = next((c for c in var.conjuntos if c.nombre == conjunto_sel), None)
                    if conjunto:
                        if conjunto.tipo == 'gaussiana':
                            entradas[var.nombre] = conjunto.parametros[0]
                        else:
                            entradas[var.nombre] = sum(conjunto.parametros) / len(conjunto.parametros)

        sistema_inferencia = SistemaInferencia(sistema)
        resultados = sistema_inferencia.evaluar(entradas)
        interpretar_resultado = lambda x: "Leve" if x < 25 else "Moderado" if x < 50 else "Severo" if x < 75 else "Insoportable"
        salida_texto = "\n".join(f"{k}: {interpretar_resultado(v)}" for k, v in resultados.items())
        self.resultado_texto.config(text=f"Resultado:\n{salida_texto}")

        # Mostrar resultado interpretado
        interpretar_resultado = lambda x: "Leve" if x < 25 else "Moderado" if x < 50 else "Severo" if x < 75 else "Insoportable"
        salida_texto = "\n".join(f"{k}: {interpretar_resultado(v)}" for k, v in resultados.items())
        self.resultado_texto.config(text=f"Resultado:\n{salida_texto}")

        # Graficar resultados
        if hasattr(self, 'canvas_frame') and self.canvas_frame.winfo_exists():
            self.canvas_frame.destroy()
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        graficar_resultados(self.canvas_frame, sistema_inferencia, entradas, resultados)


#Graficar resultados
# Función para graficar los resultados en la interfaz de Tkinter
def graficar_resultados(parent, sistema_inferencia, entradas, resultados):
    n = len(entradas) + 1  # una por entrada + una salida
    fig = plt.figure(figsize=(10, 3.8 * n))
    gs = GridSpec(n * 2, 1, figure=fig)  # 2 filas por cada gráfico        


    variables = sistema_inferencia.control_vars

    idx = 0
    for nombre, valor in entradas.items():
        if nombre in variables:
            # Gráfico
            ax_plot = fig.add_subplot(gs[idx * 2, 0])
            variable = variables[nombre]
            for conjunto_nombre, mf in variable.terms.items():
                ax_plot.plot(variable.universe, mf.mf, label=conjunto_nombre)
            ax_plot.axvline(valor, color='red', linestyle='--', label='Valor seleccionado')
            ax_plot.set_title(nombre.replace("_", " ").capitalize())
            ax_plot.set_ylim(0, 1.1)

            # Leyenda debajo
            ax_legend = fig.add_subplot(gs[idx * 2 + 1, 0])
            ax_legend.axis("off")
            handles, labels = ax_plot.get_legend_handles_labels()
            ax_legend.legend(handles, labels, loc='center', ncol=4, fontsize=8, frameon=False)

            idx += 1
    fig.tight_layout(pad=3.5)
    # Salida
    for nombre, valor in resultados.items():
        ax_plot = fig.add_subplot(gs[idx * 2, 0])
        variable = variables[nombre]
        for conjunto_nombre, mf in variable.terms.items():
            ax_plot.plot(variable.universe, mf.mf, label=conjunto_nombre)
        ax_plot.axvline(valor, color='red', linestyle='--', label='Resultado')
        ax_plot.set_title(f"Resultado: {nombre.replace('_', ' ').capitalize()}")
        ax_plot.set_ylim(0, 1.1)
    
        # Leyenda        
        ax_legend = fig.add_subplot(gs[idx * 2 + 1, 0])
        ax_legend.axis("off")
        handles, labels = ax_plot.get_legend_handles_labels()
        ax_legend.legend(handles, labels, loc='center', ncol=4, fontsize=8, frameon=False)

    # Crear canvas y frame con scroll
    scroll_canvas = tk.Canvas(parent)
    scroll_frame = tk.Frame(scroll_canvas)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    # Posicionar
    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Vincular el frame al canvas
    window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Asegurar el ajuste del scroll al contenido
    def on_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scroll_frame.bind("<Configure>", on_configure)

    # Insertar figura en el frame con scroll
    canvas = FigureCanvasTkAgg(fig, master=scroll_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)





    

    