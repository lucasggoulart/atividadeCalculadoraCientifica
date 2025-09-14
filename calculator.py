import tkinter as tk
import math
from tkinter import *
 
root = tk.Tk()
root.title("Calculadora")
root.resizable(0,0)
 
shift = False
alpha = False

# Números e sinais
numero1 = "0"
numero2 = "0"
operacao = ""
resultado = 0
 
 # Para o cursor de edição
posicao_cursor = 0  
modo_cursor = False  

# Expansão
modo = True
 
# Variáveis de padding
PADDING_X = 2
PADDING_Y = 4
 
 # Histórico para replay
historico = []  # cada item será (numero1, numero2, operacao, resultado)
indice_historico = -1  # começa no último item do histórico

def formatar_numero(valor):
    #if isinstance(valor, float):
        #temp_formatado = f"{valor:,.2f}"
        #temp_formatado = temp_formatado.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
        #return temp_formatado
    #try:
     #   float_valor = float(valor)
      #  if float_valor.is_integer():
       #     return f"{int(float_valor):,}".replace(",", ".")
        #else:
         #   temp_formatado = f"{float_valor:,.2f}"
          #  temp_formatado = temp_formatado.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
           # return temp_formatado
   # except ValueError:
    #    return f"{int(valor):,}".replace(",", ".")
    try:
        float_valor = float(valor)
        if float_valor.is_integer():
            return f"{int(float_valor):,}".replace(",", ".")
        else:
            return str(float_valor).replace(".", ",")
    except ValueError:
        return str(valor).replace(".", ",")

def func_percent():
    global numero1, numero2, operacao, resultado

    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            resultado = current_value / 100
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value_num2 = float(numero2.replace(",", "."))
            current_value_num1 = float(numero1.replace(",", "."))
            if(operacao == "+" or operacao == "-"):
                resultado = current_value_num1*(current_value_num2 / 100)
            else:
                resultado = current_value_num2/100
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1)+operacao+formatar_numero(numero2))
    except ValueError:
        painel.config(text="Erro!")
    except ZeroDivisionError:
        painel.config(text="Erro! Divisão por 0")

def func_ce():
    global numero2, numero1, operacao
    
    if(numero2 == "0" and operacao == ""):
        numero1 = "0"
        painel.config(text=numero1)
    elif operacao != "" and numero2 != "0":
        numero2 = "0"
        painel.config(text=numero1 + operacao + numero2)
    else:
        numero1 = "0"
        numero2 = "0"
        operacao = ""
        painel.config(text=numero1)

 
def func_c():
    global numero1, numero2, operacao, resultado

    numero1 = "0"
    numero2 = "0"
    operacao = ""
    resultado = 0

    painel.config(text=numero1)

def func_backspace():
    global numero1, numero2, operacao

    if operacao == "":
        if(len(numero1) > 1):
            numero1 = numero1[:-1]
            if(numero1.endswith(",")):
                numero1 = numero1[:-1]
            painel.config(text=formatar_numero(numero1))
        else:
            numero1 = "0"
            painel.config(text=numero1)
    else:
        if(len(numero2) > 1):
            numero2 = numero2[:-1]
            if numero2.endswith(","):
                numero2 = numero2[:-1]
            painel.config(text=formatar_numero(numero1)+operacao+formatar_numero(numero2))
        else:
            numero2 = "0"
            painel.config(text=formatar_numero(numero1)+operacao+numero2)
 
def func_inverse():
    global numero1, numero2, operacao, resultado, historico
    historico.append((numero1, numero2, operacao, resultado))
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            if current_value == 0:
                return
            resultado = 1 / current_value
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            if current_value == 0:
                return
            resultado = 1 / current_value
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1)+operacao+formatar_numero(numero2))
    except ValueError:
        painel.config(text="Erro!")

def func_square():
    global numero1, numero2, operacao, resultado, historico
    historico.append((numero1, numero2, operacao, resultado))
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            resultado = current_value ** 2
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            resultado = current_value ** 2
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1)+operacao+formatar_numero(numero2))
    except ValueError:
        painel.config(text="Erro!")

def func_sqrt():
    global numero1, numero2, operacao, resultado, historico
    historico.append((numero1, numero2, operacao, resultado))
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            if current_value < 0:
                painel.config(text="Erro!")
                return
            resultado = math.sqrt(current_value)
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            if current_value < 0:
                painel.config(text="Erro!")
                return
            resultado = math.sqrt(current_value)
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1)+operacao+formatar_numero(numero2))
    except ValueError:
        painel.config(text="Erro!")


def inserir_numero(digito):
    global numero1, numero2, operacao, posicao_cursor, modo_cursor

    if operacao == "":
        n = numero1
    else:
        n = numero2

    # Se for 0, substitui totalmente
    if n == "0":
        n = digito
        pos = 1
    else:
        if posicao_cursor >= len(n):
            # Acrescenta ao final
            n = n + digito
        else:
            # Substitui o caractere selecionado
            n = n[:posicao_cursor] + digito + n[posicao_cursor+1:]
        pos = posicao_cursor + 1

    # Atualiza variáveis
    if operacao == "":
        numero1 = n
    else:
        numero2 = n
    posicao_cursor = pos
    modo_cursor = True

    # Atualiza painel
    atualizar_painel_cursor()


def func_0(): inserir_numero("0")
def func_1(): inserir_numero("1")
def func_2(): inserir_numero("2")
def func_3(): inserir_numero("3")
def func_4(): inserir_numero("4")
def func_5(): inserir_numero("5")
def func_6(): inserir_numero("6")
def func_7(): inserir_numero("7")
def func_8(): inserir_numero("8")
def func_9(): inserir_numero("9")
def func_dot(): inserir_numero(".")


def func_divide():
    global operacao, numero1, numero2, resultado, antes, historico, indice_historico

    antes = painel.cget('text')

    if numero1 != "0" and numero2 != "0":
        if operacao == "+":
            resultado = float(numero1)+float(numero2)
        elif operacao == "-":
            resultado = float(numero1)-float(numero2)
        elif operacao == "x":
            resultado = float(numero1)*float(numero2)
        elif operacao == "÷":
            if numero2 == "0":
                painel.config(text="Erro! Divisão por 0")
                return
            resultado = float(numero1)/float(numero2)

        if resultado.is_integer():
            resultado = int(resultado)

        numero1 = str(resultado)
        numero2 = "0"
        painel.config(text=str(formatar_numero(resultado))+"÷")

    operacao = "÷"

    if antes != painel.cget('text'):
        historico.append((numero1, numero2, operacao, resultado))
        indice_historico = len(historico) - 1


def func_multiply():
    global operacao, numero1, numero2, resultado, antes, historico, indice_historico

    antes = painel.cget('text')

    if numero1 != "0" and numero2 != "0":
        if operacao == "+":
            resultado = float(numero1)+float(numero2)
        elif operacao == "-":
            resultado = float(numero1)-float(numero2)
        elif operacao == "x":
            resultado = float(numero1)*float(numero2)
        elif operacao == "÷":
            if numero2 == "0":
                painel.config(text="Erro! Divisão por 0")
                return
            resultado = float(numero1)/float(numero2)

        if resultado.is_integer():
            resultado = int(resultado)

        numero1 = str(resultado)
        numero2 = "0"
        painel.config(text=str(formatar_numero(resultado))+"x")

    operacao = "x"

    if antes != painel.cget('text'):
        historico.append((numero1, numero2, operacao, resultado))
        indice_historico = len(historico) - 1

def func_subtract():
    global operacao, numero1, numero2, resultado, antes, historico, indice_historico

    antes = painel.cget('text')

    if numero1 != "0" and numero2 != "0":
        if operacao == "+":
            resultado = float(numero1)+float(numero2)
        elif operacao == "-":
            resultado = float(numero1)-float(numero2)
        elif operacao == "x":
            resultado = float(numero1)*float(numero2)
        elif operacao == "÷":
            if numero2 == "0":
                painel.config(text="Erro! Divisão por 0")
                return
            resultado = float(numero1)/float(numero2)

        if resultado.is_integer():
            resultado = int(resultado)

        numero1 = str(resultado)
        numero2 = "0"
        painel.config(text=str(formatar_numero(resultado))+"-")

    operacao = "-"

    if antes != painel.cget('text'):
        historico.append((numero1, numero2, operacao, resultado))
        indice_historico = len(historico) - 1

def func_add():
    global operacao, numero1, numero2, resultado, antes, historico, indice_historico

    antes = painel.cget('text')

    if numero1 != "0" and numero2 != "0":
        if operacao == "+":
            resultado = float(numero1)+float(numero2)
        elif operacao == "-":
            resultado = float(numero1)-float(numero2)
        elif operacao == "x":
            resultado = float(numero1)*float(numero2)
        elif operacao == "÷":
            if numero2 == "0":
                painel.config(text="Erro! Divisão por 0")
                return
            resultado = float(numero1)/float(numero2)

        if resultado.is_integer():
            resultado = int(resultado)

        numero1 = str(resultado)
        numero2 = "0"
        painel.config(text=str(formatar_numero(resultado))+"+")

    operacao = "+"

    if antes != painel.cget('text'):
        historico.append((numero1, numero2, operacao, resultado))
        indice_historico = len(historico) - 1
     
def func_equals():
    global resultado, numero1, numero2, operacao, historico, indice_historico

    if operacao == "+":
        resultado = float(numero1)+float(numero2)
    elif operacao == "-":
        resultado = float(numero1)-float(numero2)
    elif operacao == "x":
        resultado = float(numero1)*float(numero2)
    elif operacao == "÷":
        if numero2 == "0":
            painel.config(text="Erro! Divisão por 0")
            return
        resultado = float(numero1)/float(numero2)

    if resultado.is_integer():
        resultado = int(resultado)

    painel.config(text=str(formatar_numero(resultado)))

    numero1 = str(resultado)
    numero2 = "0"
    operacao = ""

    # Histórico apenas com o resultado final
    historico.append((str(resultado), "0", "", resultado))
    indice_historico = len(historico) - 1
       
 
indice_historico = -1  # inicial, fora do histórico

def replay_cima():
    global indice_historico, historico
    if historico:
        if indice_historico == -1:
            indice_historico = len(historico) - 1
        elif indice_historico > 0:
            indice_historico -= 1
        resultado = historico[indice_historico][3]
        painel.config(text=formatar_numero(resultado))

def replay_baixo():
    global indice_historico, historico
    if historico:
        if indice_historico == -1:
            indice_historico = len(historico) - 1
        elif indice_historico < len(historico) - 1:
            indice_historico += 1
        resultado = historico[indice_historico][3]
        painel.config(text=formatar_numero(resultado))

def atualizar_painel_cursor():
    global numero1, numero2, operacao, posicao_cursor
    texto = ""
    if operacao == "":
        n = numero1
    else:
        n = numero2

    # Inserindo o cursor
    if posicao_cursor > len(n):
        posicao = len(n)
    else:
        posicao = posicao_cursor
    texto_cursor = n[:posicao] + "|" + n[posicao:]

    if operacao == "":
        painel.config(text=texto_cursor)
    else:
        painel.config(text=formatar_numero(numero1) + operacao + texto_cursor)

def replay_esquerda():  # ←
    global posicao_cursor, modo_cursor
    modo_cursor = True
    if operacao == "":
        if posicao_cursor > 0:
            posicao_cursor -= 1
    else:
        if posicao_cursor > 0:
            posicao_cursor -= 1
    atualizar_painel_cursor()

def replay_direita():  # →
    global posicao_cursor, modo_cursor
    modo_cursor = True
    if operacao == "":
        if posicao_cursor < len(numero1):
            posicao_cursor += 1
    else:
        if posicao_cursor < len(numero2):
            posicao_cursor += 1
    atualizar_painel_cursor()

def toggle_shift():
    global shift
    shift = not shift

def toggle_alpha():
    global alpha
    alpha = not alpha

memoria = 0

def func_m_plus():
    global memoria, numero1, numero2, operacao, resultado, shift, alpha

    try:
        if alpha:
            # Recupera o valor da memória
            painel.config(text=f"Memória: {formatar_numero(memoria)} (MR)")
            return

        if operacao == "":
            valor = float(numero1.replace(",", "."))
        else:
            valor = float(numero2.replace(",", "."))

        if shift:
            memoria -= valor
            painel.config(text=f"Memória: {formatar_numero(memoria)} (M-)")
        else:
            memoria += valor
            painel.config(text=f"Memória: {formatar_numero(memoria)} (M+)")
    except ValueError:
        painel.config(text="Erro!")

current_mode = "COMP"  # padrão inicial = cálculo normal

def toggle_mode():
    global current_mode

    # Criar janela popup
    mode_window = tk.Toplevel(root)
    mode_window.title("Selecionar Modo")
    mode_window.geometry("250x200")
    mode_window.resizable(False, False)

    # Label de instrução
    tk.Label(mode_window, text="Selecione o modo:", font=("Arial", 12)).pack(pady=10)

    # Função para definir o modo
    def set_mode(mode):
        global current_mode
        current_mode = mode
        painel.config(text=f"Modo atual: {current_mode}")
        mode_window.destroy()

    tk.Button(mode_window, text="1. COMP (Normal)", width=20, command=lambda: set_mode("COMP")).pack(pady=5)
    tk.Button(mode_window, text="2. STAT (Estatística)", width=20, command=lambda: set_mode("STAT")).pack(pady=5)
    tk.Button(mode_window, text="3. TABLE (Tabela)", width=20, command=lambda: set_mode("TABLE")).pack(pady=5)

# Painel
painel = Label(root, text=str(numero1), anchor='e', bg="white", relief="sunken", font=("Arial", 24), height=1) # expansão: alterar height pra 2 para aumentar
painel.grid(row=0, column=0, columnspan=4, padx=PADDING_X, pady=PADDING_Y, sticky="we")
 
# Primeira linha
btn_percent = tk.Button(root, text='%', width=10, height=3, command=func_percent)
btn_percent.grid(row=1, column=0, padx=PADDING_X, pady=PADDING_Y)
 
btn_ce = tk.Button(root, text='AC', width=10, height=3, command=func_ce)
btn_ce.grid(row=1, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_c = tk.Button(root, text='C', width=10, height=3, command=func_c)
btn_c.grid(row=1, column=2, padx=PADDING_X, pady=PADDING_Y)
 
btn_backspace = tk.Button(root, text='⌫', width=10, height=3, command=func_backspace)
btn_backspace.grid(row=1, column=3, padx=PADDING_X, pady=PADDING_Y)
 
# Segunda linha
btn_inverse = tk.Button(root, text='1/x', width=10, height=3, command=func_inverse)
btn_inverse.grid(row=2, column=0, padx=PADDING_X, pady=PADDING_Y)

btn_square = tk.Button(root, text='x²', width=10, height=3, command=func_square)
btn_square.grid(row=2, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_sqrt = tk.Button(root, text='²√x', width=10, height=3, command=func_sqrt)
btn_sqrt.grid(row=2, column=2, padx=PADDING_X, pady=PADDING_Y)
 
btn_divide = tk.Button(root, text='÷', width=10, height=3, command=func_divide)
btn_divide.grid(row=2, column=3, padx=PADDING_X, pady=PADDING_Y)
 
# Terceira linha
btn_7 = tk.Button(root, text='7', width=10, height=3, command=func_7)
btn_7.grid(row=3, column=0, padx=PADDING_X, pady=PADDING_Y)
 
btn_8 = tk.Button(root, text='8', width=10, height=3, command=func_8)
btn_8.grid(row=3, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_9 = tk.Button(root, text='9', width=10, height=3, command=func_9)
btn_9.grid(row=3, column=2, padx=PADDING_X, pady=PADDING_Y)
 
btn_multiply = tk.Button(root, text='×', width=10, height=3, command=func_multiply)
btn_multiply.grid(row=3, column=3, padx=PADDING_X, pady=PADDING_Y)
 
# Quarta linha
btn_4 = tk.Button(root, text='4', width=10, height=3, command=func_4)
btn_4.grid(row=4, column=0, padx=PADDING_X, pady=PADDING_Y)
 
btn_5 = tk.Button(root, text='5', width=10, height=3, command=func_5)
btn_5.grid(row=4, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_6 = tk.Button(root, text='6', width=10, height=3, command=func_6)
btn_6.grid(row=4, column=2, padx=PADDING_X, pady=PADDING_Y)
 
btn_subtract = tk.Button(root, text='−', width=10, height=3, command=func_subtract)
btn_subtract.grid(row=4, column=3, padx=PADDING_X, pady=PADDING_Y)
 
# Quinta linha
btn_1 = tk.Button(root, text='1', width=10, height=3, command=func_1)
btn_1.grid(row=5, column=0, padx=PADDING_X, pady=PADDING_Y)
 
btn_2 = tk.Button(root, text='2', width=10, height=3, command=func_2)
btn_2.grid(row=5, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_3 = tk.Button(root, text='3', width=10, height=3, command=func_3)
btn_3.grid(row=5, column=2, padx=PADDING_X, pady=PADDING_Y)
 
btn_add = tk.Button(root, text='+', width=10, height=3, command=func_add)
btn_add.grid(row=5, column=3, padx=PADDING_X, pady=PADDING_Y)
 
 
 
# Sexta linha
btn_0 = tk.Button(root, text='0', width=10, height=3, command=func_0)
btn_0.grid(row=6, column=0, padx=PADDING_X, pady=PADDING_Y)
 
btn_dot = tk.Button(root, text=',', width=10, height=3, command=func_dot)
btn_dot.grid(row=6, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_equals = tk.Button(root, text='=', width=22, height=3, command=func_equals)
btn_equals.grid(row=6, column=2, columnspan=2, padx=PADDING_X, pady=PADDING_Y)

# Cientifica
if(modo):
    btn_percent.place(x=99999)
    btn_c.place(x=99999)
    btn_inverse.place(x=99999)
    btn_square.place(x=99999)
    btn_sqrt.place(x=99999)

    # Criar o frame para o botão replay
    frame_replay = tk.Frame(root)

    # Quatro botõezinhos dentro do frame de replay
    btn_replay_up = tk.Button(frame_replay, text='↑', width=3, height=1, command=replay_cima)
    btn_replay_up.grid(row=0, column=1)

    btn_replay_left = tk.Button(frame_replay, text='←', width=3, height=1, command=replay_esquerda)
    btn_replay_left.grid(row=1, column=0)

    btn_replay_right = tk.Button(frame_replay, text='→', width=3, height=1, command=replay_direita)
    btn_replay_right.grid(row=1, column=2)

    btn_replay_down = tk.Button(frame_replay, text='↓', width=3, height=1, command=replay_baixo)
    btn_replay_down.grid(row=2, column=1)


    # Colocar o frame inteiro no grid principal (ajuste posição onde quiser)
    frame_replay.grid(row=11, column=2, columnspan=2, rowspan=2, padx=PADDING_X, pady=PADDING_Y)

    btn_replay1 = tk.Button(root, text='RCL', width=5, height=2, command=func_equals)
    btn_replay1.grid(row=15, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay12 = tk.Button(root, text='ENG', width=5, height=2, command=func_equals)
    btn_replay12.grid(row=15, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay13 = tk.Button(root, text='(', width=5, height=2, command=func_equals)
    btn_replay13.grid(row=15, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_replay14 = tk.Button(root, text=')', width=5, height=2, command=func_equals)
    btn_replay14.grid(row=15, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_replay15 = tk.Button(root, text=',', width=5, height=2, command=func_equals)
    btn_replay15.grid(row=15, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_mplus = tk.Button(root, text='M+', width=5, height=2, command=func_m_plus)
    btn_mplus.grid(row=15, column=5, padx=PADDING_X, pady=PADDING_Y)

    btn_replay2 = tk.Button(root, text='(-)', width=5, height=2, command=func_equals)
    btn_replay2.grid(row=14, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay22 = tk.Button(root, text='°,,,', width=5, height=2, command=func_equals)
    btn_replay22.grid(row=14, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay23 = tk.Button(root, text='hyp', width=5, height=2, command=func_equals)
    btn_replay23.grid(row=14, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_replay24 = tk.Button(root, text='sin', width=5, height=2, command=func_equals)
    btn_replay24.grid(row=14, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_replay25 = tk.Button(root, text='cos', width=5, height=2, command=func_equals)
    btn_replay25.grid(row=14, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay26 = tk.Button(root, text='tan', width=5, height=2, command=func_equals)
    btn_replay26.grid(row=14, column=5, padx=PADDING_X, pady=PADDING_Y)

    btn_replay3 = tk.Button(root, text='Ab/c', width=5, height=2, command=func_equals)
    btn_replay3.grid(row=13, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay32 = tk.Button(root, text='√', width=5, height=2, command=func_equals)
    btn_replay32.grid(row=13, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay33 = tk.Button(root, text='X²', width=5, height=2, command=func_equals)
    btn_replay33.grid(row=13, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_replay34 = tk.Button(root, text='^', width=5, height=2, command=func_equals)
    btn_replay34.grid(row=13, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_replay35 = tk.Button(root, text='log', width=5, height=2, command=func_equals)
    btn_replay35.grid(row=13, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay36 = tk.Button(root, text='ln', width=5, height=2, command=func_equals)
    btn_replay36.grid(row=13, column=5, padx=PADDING_X, pady=PADDING_Y)
    
    btn_replay43 = tk.Button(root, text='x-¹', width=5, height=2, command=func_equals)
    btn_replay43.grid(row=12, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay44 = tk.Button(root, text='nCr', width=5, height=2, command=func_equals)
    btn_replay44.grid(row=12, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay45 = tk.Button(root, text='Pol(', width=5, height=2, command=func_equals)
    btn_replay45.grid(row=12, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay46 = tk.Button(root, text='x³', width=5, height=2, command=func_equals)
    btn_replay46.grid(row=12, column=5, padx=PADDING_X, pady=PADDING_Y)

    btn_shift = tk.Button(root, text='shift', width=5, height=2, command=toggle_shift)
    btn_shift.grid(row=11, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_alpha = tk.Button(root, text='alpha', width=5, height=2, command=toggle_alpha)
    btn_alpha.grid(row=11, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_mode = tk.Button(root, text='mode', width=5, height=2, command=toggle_mode)
    btn_mode.grid(row=11, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay56 = tk.Button(root, text='on', width=5, height=2, command=func_equals)
    btn_replay56.grid(row=11, column=5, padx=PADDING_X, pady=PADDING_Y)

    painel.grid(row=0, column=0, columnspan=6, padx=PADDING_X, pady=PADDING_Y, sticky="we")
    btn_0.grid(row=20, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_dot.grid(row=20, column=1, padx=PADDING_X, pady=PADDING_Y)

    btn_7.grid(row=17, column=0, padx=PADDING_X, pady=PADDING_Y)
    
    btn_8.grid(row=17, column=1, padx=PADDING_X, pady=PADDING_Y)
    
    btn_9.grid(row=17, column=2, padx=PADDING_X, pady=PADDING_Y)

    btn_4.grid(row=18, column=0, padx=PADDING_X, pady=PADDING_Y)
    
    btn_5.grid(row=18, column=1, padx=PADDING_X, pady=PADDING_Y)
    
    btn_6.grid(row=18, column=2, padx=PADDING_X, pady=PADDING_Y)

    btn_1.grid(row=19, column=0, padx=PADDING_X, pady=PADDING_Y)
    
    btn_2.grid(row=19, column=1, padx=PADDING_X, pady=PADDING_Y)
    
    btn_3.grid(row=19, column=2, padx=PADDING_X, pady=PADDING_Y)

    btn_backspace.grid(row=17, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_ce.grid(row=17, column=4,columnspan=6, padx=PADDING_X, pady=PADDING_Y)

    btn_multiply.grid(row=18, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_divide.grid(row=18, column=4,columnspan=6, padx=PADDING_X, pady=PADDING_Y)

    btn_add.grid(row=19, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_subtract.grid(row=19, column=4,columnspan=6, padx=PADDING_X, pady=PADDING_Y)

    btn_exp = tk.Button(root, text='EXP', width=10, height=3, command=func_0)
    btn_exp.grid(row=20, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_ans = tk.Button(root, text='Ans', width=10, height=3, command=func_0)
    btn_ans.grid(row=20, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_equals.grid(row=20, column=4,columnspan=5, padx=PADDING_X, pady=PADDING_Y)
    btn_equals.config(width=10)

    
else:
    modo = False    
 
root.mainloop()

