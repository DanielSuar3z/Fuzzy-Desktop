import tkinter as tk
from tkinter import ttk, messagebox
from Postura_Corporal_Funcional import sistema
import itertools
from tkinter import messagebox


class EditorReglas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Editor de Reglas Difusas")
        self.geometry("700x500")

        self.var_entrada1 = tk.StringVar()
        self.var_entrada2 = tk.StringVar()
        self.var_entrada3 = tk.StringVar()
        self.var_salida = tk.StringVar()

        self.var_conjunto1 = tk.StringVar()
        self.var_conjunto2 = tk.StringVar()
        self.var_conjunto3 = tk.StringVar()
        self.var_conjunto_salida = tk.StringVar()

        self.reglas = []

        self._crear_widgets()
        self._cargar_variables()
        self._cargar_reglas_existentes()

    def _crear_widgets(self):
        frame_vars = tk.LabelFrame(self, text="Variables")
        frame_vars.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_vars, text="Entrada 1:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_entrada1 = ttk.Combobox(frame_vars, textvariable=self.var_entrada1, state="readonly")
        self.combo_entrada1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_vars, text="Entrada 2:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_entrada2 = ttk.Combobox(frame_vars, textvariable=self.var_entrada2, state="readonly")
        self.combo_entrada2.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_vars, text="Entrada 3:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_entrada3 = ttk.Combobox(frame_vars, textvariable=self.var_entrada3, state="readonly")
        self.combo_entrada3.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_vars, text="Salida:").grid(row=3, column=0, padx=5, pady=5)
        self.combo_salida = ttk.Combobox(frame_vars, textvariable=self.var_salida, state="readonly")
        self.combo_salida.grid(row=3, column=1, padx=5, pady=5)

        frame_conjuntos = tk.LabelFrame(self, text="Conjuntos Difusos")
        frame_conjuntos.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_conjuntos, text="Conjunto Entrada 1:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_conjunto1 = ttk.Combobox(frame_conjuntos, textvariable=self.var_conjunto1, state="readonly")
        self.combo_conjunto1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_conjuntos, text="Conjunto Entrada 2:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_conjunto2 = ttk.Combobox(frame_conjuntos, textvariable=self.var_conjunto2, state="readonly")
        self.combo_conjunto2.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_conjuntos, text="Conjunto Entrada 3:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_conjunto3 = ttk.Combobox(frame_conjuntos, textvariable=self.var_conjunto3, state="readonly")
        self.combo_conjunto3.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_conjuntos, text="Conjunto Salida:").grid(row=3, column=0, padx=5, pady=5)
        self.combo_conjunto_salida = ttk.Combobox(frame_conjuntos, textvariable=self.var_conjunto_salida, state="readonly")
        self.combo_conjunto_salida.grid(row=3, column=1, padx=5, pady=5)

        # Eventos
        self.combo_entrada1.bind("<<ComboboxSelected>>", lambda e: self._actualizar_conjuntos(self.combo_entrada1, self.combo_conjunto1))
        self.combo_entrada2.bind("<<ComboboxSelected>>", lambda e: self._actualizar_conjuntos(self.combo_entrada2, self.combo_conjunto2))
        self.combo_salida.bind("<<ComboboxSelected>>", lambda e: self._actualizar_conjuntos(self.combo_salida, self.combo_conjunto_salida))
        self.combo_entrada3.bind("<<ComboboxSelected>>", lambda e: self._actualizar_conjuntos(self.combo_entrada3, self.combo_conjunto3))
        


        # Inicialización
        self._actualizar_conjuntos(self.combo_entrada1, self.combo_conjunto1)
        self._actualizar_conjuntos(self.combo_entrada2, self.combo_conjunto2)
        self._actualizar_conjuntos(self.combo_salida, self.combo_conjunto_salida)
        self._actualizar_conjuntos(self.combo_entrada3, self.combo_conjunto3)

        # Botón para añadir regla
        btn_guardar = tk.Button(self, text="Guardar Regla", command=self._guardar_regla)
        btn_guardar.pack(pady=10)

        # Lista de reglas guardadas
        frame_lista = tk.LabelFrame(self, text="Reglas Definidas")
        frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        self.lista_reglas = tk.Listbox(frame_lista)
        self.lista_reglas.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(self, text="Generar Reglas Automáticas", command=self.generar_reglas_automaticas).pack(pady=5)



    def _cargar_variables(self):
        nombres = [v.nombre for v in sistema.variables]
        self.combo_entrada1['values'] = nombres
        self.combo_entrada2['values'] = nombres
        self.combo_entrada3['values'] = nombres
        self.combo_salida['values'] = nombres

        if nombres:
            self.var_entrada1.set(nombres[0])
            self.var_entrada2.set(nombres[0])
            self.var_entrada3.set(nombres[0])
            self.var_salida.set(nombres[0])

    def _actualizar_conjuntos(self, combo_var, combo_conj):
        nombre_variable = combo_var.get()
        variable = next((v for v in sistema.variables if v.nombre == nombre_variable), None)
        if variable:
            nombres_conjuntos = [c.nombre for c in variable.conjuntos]
            combo_conj['values'] = nombres_conjuntos
            if nombres_conjuntos:
                combo_conj.set(nombres_conjuntos[0])
            else:
                combo_conj.set("")

    def _guardar_regla(self):
        entrada1 = self.var_entrada1.get()
        conjunto1 = self.var_conjunto1.get()

        entrada2 = self.var_entrada2.get()
        conjunto2 = self.var_conjunto2.get()

        entrada3 = self.var_entrada3.get()
        conjunto3 = self.var_conjunto3.get()

        salida = self.var_salida.get()
        conjunto_salida = self.var_conjunto_salida.get()

        if not all([entrada1, conjunto1, entrada2, conjunto2, entrada3, conjunto3, salida, conjunto_salida]):
            messagebox.showwarning("Faltan datos", "Completa todos los campos para guardar la regla.")
            return

        regla = f"SI {entrada1} ES {conjunto1} Y {entrada2} ES {conjunto2} Y {entrada3} ES {conjunto3} ENTONCES {salida} ES {conjunto_salida}"
        self.reglas.append({
            "entrada1": (entrada1, conjunto1),
            "entrada2": (entrada2, conjunto2),
            "entrada3": (entrada3, conjunto3),
            "salida": (salida, conjunto_salida),
            "texto": regla
        })
        self.lista_reglas.insert(tk.END, regla)

        sistema.agregar_regla(
            condiciones=[(entrada1, conjunto1), (entrada2, conjunto2), (entrada3, conjunto3)],
            resultado=(salida, conjunto_salida)
    )
 # Botones de edición y eliminación
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=5)

        btn_editar = tk.Button(frame_botones, text="Editar Regla Seleccionada", command=self._editar_regla)
        btn_editar.grid(row=0, column=0, padx=10)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar Regla Seleccionada", command=self._eliminar_regla)
        btn_eliminar.grid(row=0, column=1, padx=10)

    def _editar_regla(self):
        seleccion = self.lista_reglas.curselection()
        if not seleccion:
            messagebox.showinfo("Selecciona una regla", "Selecciona una regla para editar.")
            return

        index = seleccion[0]
        regla = self.reglas[index]

        # Prellenar campos
        self.var_entrada1.set(regla["entrada1"][0])
        self._actualizar_conjuntos(self.combo_entrada1, self.combo_conjunto1)
        self.var_conjunto1.set(regla["entrada1"][1])

        self.var_entrada2.set(regla["entrada2"][0])
        self._actualizar_conjuntos(self.combo_entrada2, self.combo_conjunto2)
        self.var_conjunto2.set(regla["entrada2"][1])
        
        self.var_entrada3.set(regla["entrada3"][0])
        self._actualizar_conjuntos(self.combo_entrada3, self.combo_conjunto3)
        self.var_conjunto3.set(regla["entrada3"][1])

        self.var_salida.set(regla["salida"][0])
        self._actualizar_conjuntos(self.combo_salida, self.combo_conjunto_salida)
        self.var_conjunto_salida.set(regla["salida"][1])

        # Eliminar la regla actual
        del self.reglas[index]
        self.lista_reglas.delete(index)

    def _eliminar_regla(self):
        seleccion = self.lista_reglas.curselection()
        if not seleccion:
            messagebox.showinfo("Selecciona una regla", "Selecciona una regla para eliminar.")
            return

        index = seleccion[0]
        confirm = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de eliminar esta regla?")
        if confirm:
            del self.reglas[index]
            self.lista_reglas.delete(index) 

    def _cargar_reglas_existentes(self):
        self.lista_reglas.delete(0, tk.END)
        self.reglas.clear()
        for regla in sistema.reglas:
            texto = f"SI " + " Y ".join([f"{v} ES {c}" for v, c in regla.condiciones])
            texto += f" ENTONCES {regla.resultado[0]} ES {regla.resultado[1]}"
            self.reglas.append({
                "entrada1": regla.condiciones[0] if len(regla.condiciones) > 0 else ("", ""),
                "entrada2": regla.condiciones[1] if len(regla.condiciones) > 1 else ("", ""),
                "entrada3": regla.condiciones[2] if len(regla.condiciones) > 2 else ("", ""),
                "salida": regla.resultado,
                "texto": texto
            })
            self.lista_reglas.insert(tk.END, texto)

    

    def generar_reglas_automaticas(self):
        try:
            entradas = [v for v in sistema.variables if v.tipo == "entrada"]
            salida = next((v for v in sistema.variables if v.tipo == "salida"), None)

            if len(entradas) < 3 or salida is None:
                messagebox.showwarning("Error", "Se requieren 3 variables de entrada y 1 de salida para generar reglas automáticamente.")
                return

            sistema.reglas.clear()

            for c1, c2, c3 in itertools.product(
                entradas[0].conjuntos, 
                entradas[1].conjuntos, 
                entradas[2].conjuntos
            ):
                # Lógica de decisión para determinar salida según combinación
                resultado_nombre = self.determinar_saliente(c1.nombre, c2.nombre, c3.nombre)

                sistema.agregar_regla(
                    condiciones=[
                        (entradas[0].nombre, c1.nombre),
                        (entradas[1].nombre, c2.nombre),
                        (entradas[2].nombre, c3.nombre)
                    ],
                    resultado=(salida.nombre, resultado_nombre)
                )

            messagebox.showinfo("Reglas generadas", f"Se generaron automáticamente {len(sistema.reglas)} reglas.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reglas: {str(e)}")

    def determinar_saliente(self, v1, v2, v3):
        # Ponderaciones simples por riesgo
        puntaje = 0

        for v in [v1, v2, v3]:
            if "muy_alto" in v or "muy_inclinada" in v or "muy_abiertas" in v:
                puntaje += 3
            elif "alto" in v or "inclinada" in v or "abiertas" in v:
                puntaje += 2
            elif "neutral" in v or "moderada" in v or "neutras" in v:
                puntaje += 1
            else:
                puntaje += 0

        if puntaje >= 8:
            return "crítica"
        elif puntaje >= 6:
            return "mala"
        elif puntaje >= 4:
            return "regular"
        elif puntaje >= 2:
            return "buena"
        else:
            return "excelente"


