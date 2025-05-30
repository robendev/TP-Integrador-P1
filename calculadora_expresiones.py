import re

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def es_operador(c):
    return str(c) in "+-*/^"

def precedencia(op):
    if op in "+-":
        return 1
    if op in "*/":
        return 2
    if op == "^":
        return 3
    return 0

def infija_a_postfija(expresion):
    salida = []
    pila = []
    tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/^()]', expresion)

    for token in tokens:
        if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
            salida.append(token)
        elif token == '(':
            pila.append(token)
        elif token == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()  # Sacar el '('
        else:
            while pila and es_operador(pila[-1]) and precedencia(token) <= precedencia(pila[-1]):
                salida.append(pila.pop())
            pila.append(token)

    while pila:
        salida.append(pila.pop())

    return salida

def construir_arbol(postfijo):
    pila = []
    for token in postfijo:
        if not es_operador(token):
            nodo = Nodo(float(token))
            pila.append(nodo)
        else:
            nodo = Nodo(token)
            nodo.derecha = pila.pop()
            nodo.izquierda = pila.pop()
            pila.append(nodo)
    return pila[0]

def evaluar_arbol(nodo):
    if not es_operador(nodo.valor):
        return nodo.valor

    izq = evaluar_arbol(nodo.izquierda)
    der = evaluar_arbol(nodo.derecha)

    if nodo.valor == '+':
        return izq + der
    elif nodo.valor == '-':
        return izq - der
    elif nodo.valor == '*':
        return izq * der
    elif nodo.valor == '/':
        return izq / der
    elif nodo.valor == '^':
        return izq ** der

def mostrar_arbol(nodo, nivel=0, prefijo="Raíz: "):
    if nodo is not None:
        print(" " * (nivel * 4) + prefijo + str(nodo.valor))
        if nodo.izquierda or nodo.derecha:
            if nodo.izquierda:
                mostrar_arbol(nodo.izquierda, nivel + 1, "L--- ")
            if nodo.derecha:
                mostrar_arbol(nodo.derecha, nivel + 1, "R--- ")

def main():
    expresion = input("Ingresa una expresión matemática: ")
    postfijo = infija_a_postfija(expresion)
    print("Expresión en notación postfija:", ' '.join(postfijo))

    arbol = construir_arbol(postfijo)
    print("\nÁrbol de expresión:")
    mostrar_arbol(arbol)

    resultado = evaluar_arbol(arbol)
    print("\nResultado:", resultado)

if __name__ == "__main__":
    main()

