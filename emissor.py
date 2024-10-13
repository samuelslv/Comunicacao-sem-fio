import tkinter as tk
from tkinter import simpledialog

class BlinkingWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Texto para Binário Piscando")
        self.blinking = False  # Para controlar o estado do piscar
        self.binary_string = ""  # Inicializa a string binária
        self.blink_index = -1  # Índice inicial para controle dos piscas (começa em -1 para incluir o primeiro vermelho)

        # Botão para iniciar a conversão e o piscar
        self.button = tk.Button(self.root, text="Inserir Texto", command=self.on_submit)
        self.button.pack()

    def text_to_binary(self, text):
        """Converte o texto para uma representação binária."""
        return ''.join(format(ord(char), '08b') for char in text)

    def on_submit(self):
        """Função chamada quando o botão é pressionado para iniciar o piscar."""
        user_input = simpledialog.askstring("Input", "Digite um texto:")
        if user_input:
            self.binary_string = self.text_to_binary(user_input)
            self.blinking = True
            self.blink_index = -1  # Redefine o índice para incluir o primeiro piscar vermelho
            self.blink()  # Inicia o piscar

    def blink(self):
        """Controla o piscar da janela com base na string binária."""
        if not self.blinking:
            return  # Para o piscar se o processo não estiver ativo

        if self.blink_index == -1:
            # Primeiro piscar vermelho para indicar o início
            self.root.configure(bg="green")
            self.blink_index += 1
            self.root.after(4000, self.blink)
        elif self.blink_index < len(self.binary_string):
            # Piscar baseado nos bits binários
            bit = self.binary_string[self.blink_index]
            color = "black" if bit == '1' else "white"
            self.root.configure(bg=color)
            self.blink_index += 1
            self.root.after(1000, self.blink)
        elif self.blink_index == len(self.binary_string):
            # Último piscar vermelho para indicar o fim
            self.root.configure(bg="purple")
            self.blink_index += 1
            self.root.after(4000, self.stop_blink)

    def stop_blink(self):
        """Finaliza o processo de piscar."""
        self.blinking = False
        self.root.configure(bg="purple")  # Retorna a janela para cor branca ao final

# Cria a janela principal
root = tk.Tk()
app = BlinkingWindow(root)

# Inicia a aplicação
root.mainloop()
