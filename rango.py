import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

class AFD:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8','q9','q10','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20','q21','q22','q23','q24','q25'}
        self.alphabet = {'0', '2','5', '6', '7', '8', '9',
                         'A', 'B', 'C','N','Q','S','U'}
        
        self.transitions = {
             'q0': {'C': 'q1', 'B': 'q2', 'Q': 'q3', 'S': 'q4'},
            'q1': {'U': 'q5'},
            'q5': {'7': 'q11'},
            'q11': {'0': 'q16'},
            'q16': {'0': 'q20'},
            'q20': {'0': 'q23'},
            'q2': {'U': 'q6'},
            'q6': {'8': 'q12'},
            'q12': {'2': 'q16'},
            'q3': {'N': 'q7','8': 'q8','6': 'q9'},
            'q7': {'9': 'q13','8': 'q14'},
            'q13': {'0': 'q17'},
            'q17': {'0': 'q21'},
            'q21': {'C': 'q24'},
            'q14': {'0': 'q18'},
            'q18': {'0': 'q22'},
            'q22': {'C': 'q25','A': 'q25'},
            'q8': {'0': 'q15'},
            'q9': {'5': 'q15'},
            'q15': {'B': 'q19'},
            'q4': {'9': 'q10'},
            'q10': {'5': 'q15', '0':'q21'}
        }
        
        self.start_state = 'q0'
        self.accept_states = {'q23','q24','q25','q19'}
        
    def validar(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False  # Caracter no valido
            if current_state not in self.states:
                return False  # Estado no valido
            current_state = self.transitions[current_state].get(symbol, None)
            if current_state is None:
                return False  # No hay transicion para el símbolo
        return current_state in self.accept_states

def validar_automata(input, states):
    current_state = "q0"

    for char in input:
        try:
            if states[current_state][char]:
                print(current_state)
                current_state = states[current_state][char]
               
        except KeyError:
            print(current_state)
            return {'success': False, 'message': f'Autómata no válido, error en el estado {current_state}'}
    print(current_state)
    
    if len(input) == 7:
        return {'success': False, 'message': f'Autómata no válido, error, tamaño de entrada inválido {current_state}'}

    return {'success': True, 'message': 'Autómata válido'}

class AutomataApp:
    def __init__(self, ventana):
        self.automata = AFD()
        self.ventana = ventana
        self.ventana.title("Automata Rangos")

        # Establece el tamaño de la ventana de Tkinter
        self.ventana.geometry("400x250")  # Ancho x Alto en píxeles

        self.etiqueta = tk.Label(ventana, text="Ingrese una cadena:", font=("Helvetica", 12))
        self.etiqueta.pack(pady=10)

        self.entrada = tk.Entry(ventana, font=("Helvetica", 12))
        self.entrada.pack(pady=10)

        self.boton = tk.Button(ventana, text="Verificar", command=self.verificarCadena, font=("Helvetica", 12))
        self.boton.pack(pady=10)

        self.resultado = tk.Label(ventana, text="", font=("Helvetica", 10, "bold"))
        self.resultado.pack()

        self.G = nx.DiGraph()

    def verificarCadena(self):
        input_string = self.entrada.get()
        resultado = validar_automata(input_string, self.automata.transitions)
        if len(input_string) != 4 and len(input_string) != 6:
            self.resultado.config(text="Longitud inválida, ingrese una cadena de longitud 4 o 6.")
        elif resultado['success']:
            self.resultado.config(text=f"Cadena válida: {input_string}")
            self.actualizarGrafo(input_string)
        else:
            self.resultado.config(text=f"{resultado['message']} para la cadena: {input_string}")

    def actualizarGrafo(self, input_string):
        self.G.clear()
        current_state = self.automata.start_state
        self.G.add_node(current_state)

        for symbol in input_string:
            if symbol not in self.automata.alphabet:
                break  # Caracter no válido, detenemos el proceso
            next_state = self.automata.transitions[current_state].get(symbol, None)
            if next_state is None:
                break  # No hay transición para el símbolo, detenemos el proceso
            self.G.add_node(next_state)
            self.G.add_edge(current_state, next_state, label=symbol)
            current_state = next_state

        # Configura el tamaño de la figura de Matplotlib
        plt.figure(figsize=(8, 6))  # Ancho x Alto en pulgadas

        # Dibuja el grafo
        pos = nx.spring_layout(self.G)
        labels = {edge: self.G.edges[edge]['label'] for edge in self.G.edges}
        nx.draw(self.G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_color='black')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels, font_size=10, font_color='red')
        
        # Muestra la figura
        plt.show()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AutomataApp(ventana)
    ventana.mainloop()
