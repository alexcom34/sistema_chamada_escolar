import tkinter as tk
from tkinter import messagebox

print("1 - Iniciando Python")

janela = tk.Tk()

print("2 - Tkinter criado")

janela.title("Teste do Sistema")
janela.geometry("500x300")

label = tk.Label(
    janela,
    text="A interface está funcionando!",
    font=("Arial", 20)
)

label.pack(pady=80)

print("3 - Antes do mainloop")

janela.mainloop()

print("4 - Programa encerrado")