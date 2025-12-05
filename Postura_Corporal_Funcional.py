import numpy as np

# ---------- Función de pertenencia gaussiana ----------
def gaussiana(x, media, sigma):
    return np.exp(-((x - media) ** 2) / (2 * sigma ** 2))

def triangular(x, a, b, c):
    return np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

def trapezoidal(x, a, b, c, d):
    return np.maximum(0, np.minimum(np.minimum((x - a) / (b - a), 1), (d - x) / (d - c)))

# ---------- Representación del sistema difuso ----------

class ConjuntoDifuso:
    def __init__(self, nombre, tipo, parametros):
        self.nombre = nombre
        self.tipo = tipo # "gaussiana", "triangular", "trapezoidal"
        self.parametros = parametros

    def evaluar(self, x):
        if self.tipo == "gaussiana":
            media, sigma = self.parametros
            return gaussiana(x, media, sigma)
        elif self.tipo == "triangular":
            a, b, c = self.parametros
            return triangular(x, a, b, c)
        elif self.tipo == "trapezoidal":
            a, b, c, d = self.parametros
            return trapezoidal(x, a, b, c, d)
        else:
            raise ValueError(f"Tipo de función desconocida: {self.tipo}")


#class VariableDifusa:
    #def __init__(self, nombre, rango=(0, 100)):
        #self.nombre = nombre
       # self.rango = rango
       # self.conjuntos = []

class VariableDifusa:
    def __init__(self, nombre, tipo='entrada', rango=(0, 100)):
        self.nombre = nombre
        self.tipo = tipo
        self.rango = rango
        self.conjuntos = []

#    def agregar_conjunto(self, nombre, tipo, parametros):
 #       conjunto = ConjuntoDifuso(nombre, tipo, parametros)
  #      self.conjuntos.append(conjunto)
    def agregar_conjunto(self, nombre, media, sigma, tipo="gaussiana"):
        if tipo == "gaussiana":
            parametros = (media, sigma)
        elif tipo == "triangular":
            a = media - sigma
            b = media
            c = media + sigma
            parametros = (a, b, c)
        elif tipo == "trapezoidal":
            a = media - 2 * sigma
            b = media - sigma
            c = media + sigma
            d = media + 2 * sigma
            parametros = (a, b, c, d)
        else:
            raise ValueError("Tipo de función no reconocido.")

        conjunto = ConjuntoDifuso(nombre, tipo, parametros)
        self.conjuntos.append(conjunto)

    def agregar_conjunto_directo(self, nombre, tipo, parametros):
        """
        Agrega un conjunto difuso con parámetros explícitos:
        - Gaussiana: (media, sigma)
        - Triangular: (a, b, c)
        - Trapezoidal: (a, b, c, d)
        """
        conjunto = ConjuntoDifuso(nombre, tipo, parametros)
        self.conjuntos.append(conjunto)


class SistemaDifuso:
    def __init__(self):
        self.variables = []        
        self.reglas = []

    #def agregar_variable(self, nombre, rango=(0, 100)):
        #variable = VariableDifusa(nombre, rango)
        #self.variables.append(variable)
    def agregar_variable(self, nombre, tipo='entrada', rango=(0, 100)):
        variable = VariableDifusa(nombre, tipo, rango)
        self.variables.append(variable)


    def mostrar_configuracion(self):
        for var in self.variables:
            print(f"Variable: {var.nombre} (Rango: {var.rango})")
            for c in var.conjuntos:
                print(f"  - Conjunto: {c.nombre}, media={c.media}, sigma={c.sigma}")


# ---------- Representación de una regla difusa ----------
class ReglaDifusa:
    def __init__(self, condiciones, resultado):
        """
        condiciones: lista de tuplas (nombre_variable, nombre_conjunto)
        resultado: tupla (nombre_variable, nombre_conjunto)
        """
        self.condiciones = condiciones
        self.resultado = resultado

    def __str__(self):
        cond_str = " Y ".join([f"{var} ES {conj}" for var, conj in self.condiciones])
        res_str = f"{self.resultado[0]} ES {self.resultado[1]}"
        return f"SI {cond_str} ENTONCES {res_str}"

# ---------- Extensión del sistema difuso para incluir reglas ----------
class SistemaDifuso:
    def __init__(self):
        self.variables = []
        self.reglas = []  # <-- Lista de reglas

    #def agregar_variable(self, nombre, rango=(0, 100)):
     #   variable = VariableDifusa(nombre, rango)
      #  self.variables.append(variable)

    def agregar_variable(self, nombre, tipo='entrada', rango=(0, 100)):
        variable = VariableDifusa(nombre, tipo, rango)
        self.variables.append(variable)

    def agregar_regla(self, condiciones, resultado):
        regla = ReglaDifusa(condiciones, resultado)
        self.reglas.append(regla)


    def mostrar_configuracion(self):
        for var in self.variables:
            print(f"Variable: {var.nombre} (Rango: {var.rango})")
            for c in var.conjuntos:
                print(f"  - Conjunto: {c.nombre}, tipo={c.tipo}, parámetros={c.parametros}")


    def mostrar_reglas(self):
        print("\nReglas definidas:")
        for i, regla in enumerate(self.reglas, start=1):
            print(f"{i}. {regla}")

    def inferir(self, entradas):
        """
        entradas: dict con nombre de variable -> valor real
        Devuelve: lista de tuplas (salida_variable, conjunto_salida, grado_activación)
        """
        resultados = []

        for regla in self.reglas:
            grados = []

            for nombre_var, nombre_conjunto in regla.condiciones:
                valor = entradas.get(nombre_var)
                variable = next((v for v in self.variables if v.nombre == nombre_var), None)
                conjunto = next((c for c in variable.conjuntos if c.nombre == nombre_conjunto), None)
                
                #grado = gaussiana(valor, conjunto.media, conjunto.sigma)
                grado = conjunto.evaluar(valor)  # Evaluar el conjunto difuso
                grados.append(grado)

            grado_activacion = min(grados)  # Operador AND (mínimo)
            salida_var, salida_conj = regla.resultado
            resultados.append((salida_var, salida_conj, grado_activacion))

        return resultados
    
    def obtener_variable(self, nombre):
        for var in self.variables:
            if var.nombre == nombre:
                return var
        return None

sistema = SistemaDifuso()
