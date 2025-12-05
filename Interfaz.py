import tkinter as tk
from tkinter import ttk
from editor_variables import EditorVariables
from editor_membresias import EditorMembresias
from editor_reglas import EditorReglas
from sistema_inferencia import InferenciaFrame

class FuzzyLogicDesignerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Diseñador de Lógica Difusa - Postura Corporal")
        self.geometry("600x400")

        titulo = tk.Label(self, text="Diseñador de Lógica Difusa", font=("Arial", 18, "bold"))
        titulo.pack(pady=20)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=30)

        tk.Button(frame_botones, text="Editor de Variables", width=25, command=self.abrir_editor_variables).pack(pady=5)
        tk.Button(frame_botones, text="Editor de Membresías", width=25, command=self.abrir_editor_membresias).pack(pady=5)
        tk.Button(frame_botones, text="Editor de Reglas", width=25, command=self.abrir_editor_reglas).pack(pady=5)
        tk.Button(frame_botones, text="Sistema de Inferencia", width=25, command=self.abrir_inferencia).pack(pady=5)

    def abrir_editor_variables(self):
        EditorVariables(self)

    def abrir_editor_membresias(self):        
        EditorMembresias(self)        
        #EditorMembresias._actualizar_variables(self)        

    def abrir_editor_reglas(self):
        EditorReglas(self)

    def abrir_inferencia(self):
        InferenciaFrame(self)  # o InferenciaVentana si lo renombraste así

if __name__ == "__main__":
    from Postura_Corporal_Funcional import sistema

    # 1. Definir variables
    sistema.agregar_variable("ángulo_cuello", tipo="entrada", rango=(0, 100))
    sistema.agregar_variable("inclinacion_espalda", tipo="entrada", rango=(0, 100))
    sistema.agregar_variable("alineacion_piernas", tipo="entrada", rango=(0, 100))
    sistema.agregar_variable("postura", tipo="salida", rango=(0, 100))

    # 2. Agregar conjuntos a cada variable
    # Ángulo del cuello
    #sistema.obtener_variable("ángulo_cuello").agregar_conjunto("muy_bajo", a=10, b=5, c=10, tipo="triangular")
    #sistema.obtener_variable("ángulo_cuello").agregar_conjunto("bajo", a=30, b=7, c=10, tipo="triangular")
    #sistema.obtener_variable("ángulo_cuello").agregar_conjunto("neutral", a=50, b=7, c=10, tipo="triangular")
    #sistema.obtener_variable("ángulo_cuello").agregar_conjunto("alto", a=70, b=7, c=10, tipo="triangular")
    #sistema.obtener_variable("ángulo_cuello").agregar_conjunto("muy_alto", a=90, b=5, c=10, tipo="triangular")
    sistema.obtener_variable("ángulo_cuello").agregar_conjunto_directo("muy_bajo", tipo="triangular", parametros=(0, 10, 20))
    sistema.obtener_variable("ángulo_cuello").agregar_conjunto_directo("bajo", tipo="triangular", parametros=(15, 30, 45))
    sistema.obtener_variable("ángulo_cuello").agregar_conjunto_directo("neutral", tipo="triangular", parametros=(40, 50, 60))
    sistema.obtener_variable("ángulo_cuello").agregar_conjunto_directo("alto", tipo="triangular", parametros=(55, 70, 85))
    sistema.obtener_variable("ángulo_cuello").agregar_conjunto_directo("muy_alto", tipo="triangular", parametros=(80, 90, 100))
    #sistema.obtener_variable("ángulo_cuello").agregar_conjunto_directo("muy_bajo", tipo="trapezoidal", parametros=(0, 10, 20, 30))


    # Inclinación de espalda (tipo triangular)
    sistema.obtener_variable("inclinacion_espalda").agregar_conjunto_directo("recta", tipo="triangular", parametros=(4, 10, 16))
    sistema.obtener_variable("inclinacion_espalda").agregar_conjunto_directo("ligera", tipo="triangular", parametros=(24, 30, 36))
    sistema.obtener_variable("inclinacion_espalda").agregar_conjunto_directo("moderada", tipo="triangular", parametros=(44, 50, 56))
    sistema.obtener_variable("inclinacion_espalda").agregar_conjunto_directo("inclinada", tipo="triangular", parametros=(64, 70, 76))
    sistema.obtener_variable("inclinacion_espalda").agregar_conjunto_directo("muy_inclinada", tipo="triangular", parametros=(84, 90, 96))

    # Alineación de piernas (tipo triangular)
    sistema.obtener_variable("alineacion_piernas").agregar_conjunto_directo("cerradas", tipo="triangular", parametros=(5, 10, 15))
    sistema.obtener_variable("alineacion_piernas").agregar_conjunto_directo("ligeramente_abiertas", tipo="triangular", parametros=(25, 30, 35))
    sistema.obtener_variable("alineacion_piernas").agregar_conjunto_directo("neutras", tipo="triangular", parametros=(45, 50, 55))
    sistema.obtener_variable("alineacion_piernas").agregar_conjunto_directo("abiertas", tipo="triangular", parametros=(65, 70, 75))
    sistema.obtener_variable("alineacion_piernas").agregar_conjunto_directo("muy_abiertas", tipo="triangular", parametros=(85, 90, 95))

    # Postura (salida) (tipo triangular)
    sistema.obtener_variable("postura").agregar_conjunto_directo("excelente", tipo="triangular", parametros=(5, 10, 15))
    sistema.obtener_variable("postura").agregar_conjunto_directo("buena", tipo="triangular", parametros=(28, 35, 42))
    sistema.obtener_variable("postura").agregar_conjunto_directo("regular", tipo="triangular", parametros=(43, 50, 57))
    sistema.obtener_variable("postura").agregar_conjunto_directo("mala", tipo="triangular", parametros=(63, 70, 77))
    sistema.obtener_variable("postura").agregar_conjunto_directo("crítica", tipo="triangular", parametros=(85, 90, 95))




    # 3. Agregar algunas reglas
    sistema.agregar_regla(
        condiciones=[
            ("ángulo_cuello", "neutral"),
            ("inclinacion_espalda", "recta"),
            ("alineacion_piernas", "neutras")
        ],
        resultado=("postura", "excelente")
    )

    sistema.agregar_regla(
        condiciones=[
            ("ángulo_cuello", "bajo"),
            ("inclinacion_espalda", "ligera"),
            ("alineacion_piernas", "ligeramente_abiertas")
        ],
        resultado=("postura", "buena")
    )

    sistema.agregar_regla(
        condiciones=[
            ("ángulo_cuello", "alto"),
            ("inclinacion_espalda", "moderada"),
            ("alineacion_piernas", "neutras")
        ],
        resultado=("postura", "regular")
    )

    sistema.agregar_regla(
        condiciones=[
            ("ángulo_cuello", "muy_alto"),
            ("inclinacion_espalda", "inclinada"),
            ("alineacion_piernas", "abiertas")
        ],
        resultado=("postura", "mala")
    )

    sistema.agregar_regla(
        condiciones=[
            ("ángulo_cuello", "muy_alto"),
            ("inclinacion_espalda", "muy_inclinada"),
            ("alineacion_piernas", "muy_abiertas")
        ],
        resultado=("postura", "crítica")
    )


    app = FuzzyLogicDesignerApp()
    app.mainloop()



