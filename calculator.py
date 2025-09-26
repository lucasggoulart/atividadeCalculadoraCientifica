import tkinter as tk
import math
import re
import random
from tkinter import *
from fractions import Fraction
from math import cos, radians, factorial, log

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
operation = [0, "#", 0]  # [numero1, operador, numero2]
values = ["#"]
aIndex = 0
Number1 = "0"
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

# ============================ FUNÇÕES DO LEANDRO ============================

# Memória slots
memory_slots = {chr(i): "0" for i in range(65, 91)}  # A-Z

def vld_slots():
    """Return list of valid slot keys."""
    return list(memory_slots.keys())

def is_valid_slot(slot: str) -> bool:
    if not slot or not isinstance(slot, str):
        return False
    return slot.strip().upper() in memory_slots

def set_memory(slot: str, value: str) -> bool:
    if not isinstance(slot, str):
        return False
    s = slot.strip().upper()
    if s in memory_slots:
        memory_slots[s] = value
        return True
    return False

def get_memory(slot: str):
    if not isinstance(slot, str):
        return None
    return memory_slots.get(slot.strip().upper(), None)

# Funções de graus
degreeSign = "°"
minuteSign = "'"
secondSign = '"'

def convertDecimal(value):
    if isinstance(value, str):
        vnorm = value.strip().replace(",", ".")
    else:
        vnorm = str(value)

    try:
        num = float(vnorm)
    except Exception:
        raise ValueError(f"Valor inválido para conversão: {value!r}")

    sign = "-" if num < 0 else ""
    a = abs(num)
    degrees = int(a)
    rem_minutes = (a - degrees) * 60.0
    minutes = int(rem_minutes)
    seconds = (rem_minutes - minutes) * 60.0
    precision_seconds = 2
    seconds = round(seconds, precision_seconds)

    if seconds >= 60.0:
        seconds -= 60.0
        minutes += 1
    if minutes >= 60:
        minutes -= 60
        degrees += 1

    if float(seconds).is_integer():
        sec_str = str(int(round(seconds)))
    else:
        raw = f"{seconds:.{precision_seconds}f}"
        raw = raw.rstrip("0").rstrip(".")
        sec_str = raw

    formatted = f"{sign}{degrees}{degreeSign}{minutes}{minuteSign}{sec_str}{secondSign}"
    return formatted

# Funções de memória STO/RCL
def _ask_slot(parent, title):
    from tkinter import simpledialog, messagebox
    prompt = "Escolha um slot de memória (ex: A, B, C, ...):"
    slot = simpledialog.askstring(title, prompt, parent=parent)
    if not slot:
        return None
    slot = slot.strip().upper()
    if not is_valid_slot(slot):
        messagebox.showerror("Slot inválido", f"Slot '{slot}' inválido.\nUse: {', '.join(vld_slots())}", parent=parent)
        return None
    return slot

def func_sto():
    global numero1, numero2, operacao
    slot = _ask_slot(root, "STO (armazenar)")
    if not slot:
        return
    
    if operacao == "":
        val = numero1
    else:
        val = numero2
        
    if set_memory(slot, val):
        tk.messagebox.showinfo("STO", f"Valor armazenado em {slot}", parent=root)
    else:
        tk.messagebox.showerror("STO", f"Não foi possível armazenar em {slot}", parent=root)

def func_rcl():
    global numero1, numero2, operacao
    slot = _ask_slot(root, "RCL (recuperar)")
    if not slot:
        return
        
    val = get_memory(slot)
    if val is None:
        tk.messagebox.showerror("Erro", f"Nenhum valor em {slot}", parent=root)
        return
        
    if operacao == "":
        numero1 = val
        painel.config(text=formatar_numero(numero1))
    else:
        numero2 = val
        painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))

# Formatação de graus
def format_result(value, mode="norm", digits=2):
    try:
        if mode == "fix":
            out = f"{value:.{digits}f}"
        elif mode == "sci":
            sig = max(1, int(digits))
            out = f"{value:.{sig}e}"
        else:
            out = f"{value:.12g}"
        return out
    except Exception:
        return "Erro"

def formatDegree(expression):
    token_pattern = re.compile(r"([-+]?\d+(?:\.\d+)?)(°?)")
    tokens = list(token_pattern.finditer(expression))

    if tokens:
        all_have_deg = all(m.group(2) == "°" for m in tokens)

        def _strip_deg(match):
            return match.group(1)
        
        expr = token_pattern.sub(_strip_deg, expression)
        expr = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", expr)
        resultado = eval(expr)

        if all_have_deg:
            try:
                dms_str = convertDecimal(str(resultado))
                return dms_str
            except Exception:
                return format_result(resultado)
        else:
            return format_result(resultado)
    else:
        resultado = eval(expression)
        return format_result(resultado)

# Função de troca de sinal
def swapSignals():
    global numero1, numero2, operacao
    
    try:
        if operacao == "":
            expr = numero1
        else:
            expr = numero2
            
        m1 = re.search(r"([+-]?)(\d*+(?:[.,]\d+)?)$", expr)

        if m1:
            op = m1.group(1)
            num = m1.group(2)
            num_norm = num.replace(",", ".")

            try:
                if float(num_norm) == 0:
                    return
            except Exception:
                return
            
            num_sem_sinal = num.lstrip("+-")
            novo_op = "-" if op != "-" else "+"
            nova_expr = novo_op + num_sem_sinal
            
            if operacao == "":
                numero1 = nova_expr
                painel.config(text=formatar_numero(numero1))
            else:
                numero2 = nova_expr
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
            return

        m2 = re.search(r"([+-]?\d*+([.,]\d+)?)$", expr)

        if m2:
            num = m2.group(1)
            num_norm = num.replace(",", ".")
            
            try:
                f = float(num_norm)
            except Exception:
                return

            if f == 0:
                return

            if num.startswith("-"):
                novo_num = num[1:]
            else:
                novo_num = "-" + num

            if operacao == "":
                numero1 = novo_num
                painel.config(text=formatar_numero(numero1))
            else:
                numero2 = novo_num
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
            return

    except Exception as e:
        print(f"Erro ao trocar sinal: {e}")
        return

# ============================ FIM FUNÇÕES DO LEANDRO ============================

def formatar_numero(valor):
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

    # Remove símbolo de grau temporariamente para inserção
    has_degree = "°" in n
    n_clean = n.replace("°", "")
    
    # Se for 0, substitui totalmente (exceto se for ponto decimal)
    if n_clean == "0" and digito != ".":
        n_clean = digito
        pos = 1
    else:
        if posicao_cursor >= len(n_clean):
            # Acrescenta ao final
            n_clean = n_clean + digito
        else:
            # Insere na posição do cursor
            n_clean = n_clean[:posicao_cursor] + digito + n_clean[posicao_cursor:]
        pos = posicao_cursor + 1
    
    # Restaura símbolo de grau se existia
    if has_degree:
        n_clean += "°"

    # Atualiza variáveis
    if operacao == "":
        numero1 = n_clean
    else:
        numero2 = n_clean
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

# Novas funções científicas
def Abc(x: float) -> str:
    """
    Converte número em fração.
      Ab/c normal -> fração imprópria
      SHIFT + Ab/c -> número misto
    """
    try:
        frac = Fraction(x).limit_denominator()
        return f"{frac.numerator}/{frac.denominator}"
    except:
        return "Erro!"

def Dc(x: float) -> str:
    """
    Converte número em número misto (SHIFT + Ab/c)
    """
    try:
        frac = Fraction(x).limit_denominator()
        
        inteiro, resto = divmod(frac.numerator, frac.denominator)
        if inteiro == 0:
            return f"{resto}/{frac.denominator}"
        elif resto == 0:
            return str(inteiro)
        else:
            return f"{inteiro} {resto}/{frac.denominator}"
    except:
        return "Erro!"

def func_abc():
    """
    Função para o botão Ab/c - converte para fração
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            if shift:
                resultado_str = Dc(current_value)
            else:
                resultado_str = Abc(current_value)
            numero1 = resultado_str
            painel.config(text=resultado_str)
        else:
            current_value = float(numero2.replace(",", "."))
            if shift:
                resultado_str = Dc(current_value)
            else:
                resultado_str = Abc(current_value)
            numero2 = resultado_str
            painel.config(text=formatar_numero(numero1) + operacao + resultado_str)
    except:
        painel.config(text="Erro!")

def ENG(x: float) -> str:
    """
    Converte número para notação de engenharia.
    SHIFT + ENG -> volta para decimal.
    """
    try:
        if x == 0:
            return "0"
        exp = int((math.log10(abs(x)) / 3) * 3)
        mantissa = x / (10 ** exp)
        return f"{mantissa}×10^{exp}"
    except:
        return "Erro!"

def func_eng():
    """
    Função para o botão ENG - notação de engenharia
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            if shift:
                # Volta para decimal
                resultado_str = formatar_numero(current_value)
            else:
                resultado_str = ENG(current_value)
            numero1 = resultado_str
            painel.config(text=resultado_str)
        else:
            current_value = float(numero2.replace(",", "."))
            if shift:
                resultado_str = formatar_numero(current_value)
            else:
                resultado_str = ENG(current_value)
            numero2 = resultado_str
            painel.config(text=formatar_numero(numero1) + operacao + resultado_str)
    except:
        painel.config(text="Erro!")

def fnLn(s: str) -> float:
    """ln(x). SHIFT -> e^x. ALPHA -> constante e."""
    try:
        formula = s
        if "ln" in formula:
            formula = formula.strip()
            value = float(formula.removeprefix("ln"))
        else:
            raise ValueError("log não está definido")
        if value <= 0:
            raise ValueError("ln indefinido para x <= 0")
        return math.log(value)
    except:
        return float('nan')

def func_ln():
    """
    Função para o botão ln
    """
    global numero1, numero2, operacao, resultado, shift, alpha
    
    try:
        if alpha:
            # Constante e
            resultado = math.e
            painel.config(text=formatar_numero(resultado))
            return
            
        if shift:
            # e^x
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                resultado = math.exp(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                resultado = math.exp(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
        else:
            # ln(x)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                if current_value <= 0:
                    painel.config(text="Erro!")
                    return
                resultado = math.log(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                if current_value <= 0:
                    painel.config(text="Erro!")
                    return
                resultado = math.log(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def Pol(s) -> float:
    """
    Converte coordenadas retangulares para polares
    """
    try:
        s = s.replace("Pol(", "")
        if ")" in s: 
            s = s.replace(")", "")
        if "," not in s:
            raise ValueError("Faltando argumento em Pol(x, y)")
        n, k = s.split(",")
        if not n or not k:
            raise ValueError("Argumentos inválidos em Pol(x, y)")
        return ((float(n) ** 2 + float(k) ** 2) ** (1/2))
    except:
        return float('nan')

def twoPoints():
    """
    Função para gerar sequências usando notação de dois pontos
    Exemplo: 1:5 gera [1, 2, 3, 4, 5]
    """
    try:
        current_text = painel['text']
        
        # Verifica se há dois pontos na expressão
        if ":" in current_text:
            parts = current_text.split(":")
            
            if len(parts) == 2:
                start = eval(parts[0].strip())
                end = eval(parts[1].strip())
                
                # Gera a sequência
                if start <= end:
                    sequence = list(range(int(start), int(end) + 1))
                else:
                    sequence = list(range(int(start), int(end) - 1, -1))
                
                # Mostra o último valor da sequência no painel
                painel.config(text=str(sequence[-1]))
                return sequence
            else:
                painel.config(text="Invalid format")
                return None
        else:
            # Se não há dois pontos, insere dois pontos no painel
            painel.config(text=current_text + ":")
            return None
            
    except Exception as e:
        painel.config(text="Error")
        print(f"Erro em twoPoints: {e}")
        return None

def func_pol():
    """
    Função para o botão Pol(
    """
    global numero1, numero2, operacao, resultado, shift, alpha
    
    try:
        if alpha:
            # twoPoints function
            if operacao == "":
                current_value = numero1
                resultado = twoPoints(f"Ans:{current_value}")
                if isinstance(resultado, list):
                    resultado = resultado[-1] if resultado else 0
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                painel.config(text="Use apenas com um número")
        elif shift:
            # func_rec - Rec function
            if operacao == "":
                r = float(numero1.replace(",", "."))
                theta = 0  # Valor padrão
                resultado = Rec(f"{r},{theta}")
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                painel.config(text="Use apenas com um número")
        else:
            # Pol function original
            if operacao == "":
                x = float(numero1.replace(",", "."))
                y = 0  # Valor padrão
                resultado = Pol(f"{x},{y}")
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                painel.config(text="Use apenas com um número")
    except:
        painel.config(text="Erro!")

def Rec(s):    
    """
    Converte coordenadas polares para retangulares
    """
    try:
        s = s.replace("Rec(", "")
        s = s.replace(")", "")
        n, k = s.split(",")
        return (float(n) * math.cos(math.radians(float(k))))
    except:
        return float('nan')

def nCr(s):
    """
    Combinação: nCr
    """
    try:
        if "C" in s:
            n,k = s.split("C")
            return math.factorial(int(n)) // (math.factorial(int(k)) * math.factorial(int(n) - int(k)))
    except:
        return float('nan')

def nPr(s):
    """
    Permutação: nPr
    """
    try:
        if "P" in s:
            n,k = s.split("P")
            return math.factorial(int(n)) // math.factorial(int(n) - int(k))
    except:
        return float('nan')

def func_ncr():
    """
    Função para o botão nCr
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if shift:
            # nPr function
            if operacao == "":
                n = int(float(numero1.replace(",", ".")))
                k = 2  # Valor padrão
                resultado = nPr(f"{n}P{k}")
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                painel.config(text="Use apenas com um número")
        else:
            # nCr function original
            if operacao == "":
                n = int(float(numero1.replace(",", ".")))
                k = 2  # Valor padrão
                resultado = nCr(f"{n}C{k}")
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                painel.config(text="Use apenas com um número")
    except:
        painel.config(text="Erro!")

def func_log():
    """
    Função para o botão log
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if shift:
            # 10^x
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                resultado = 10 ** current_value
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                resultado = 10 ** current_value
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
        else:
            # log(x)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                if current_value <= 0:
                    painel.config(text="Erro!")
                    return
                resultado = math.log10(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                if current_value <= 0:
                    painel.config(text="Erro!")
                    return
                resultado = math.log10(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_sin():
    """
    Função para o botão sin
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if shift:
            # sin^-1 (arcsin)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                if current_value < -1 or current_value > 1:
                    painel.config(text="Erro!")
                    return
                resultado = math.asin(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                if current_value < -1 or current_value > 1:
                    painel.config(text="Erro!")
                    return
                resultado = math.asin(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
        else:
            # sin(x)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                resultado = math.sin(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                resultado = math.sin(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_cos():
    """
    Função para o botão cos
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if shift:
            # cos^-1 (arccos)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                if current_value < -1 or current_value > 1:
                    painel.config(text="Erro!")
                    return
                resultado = math.acos(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                if current_value < -1 or current_value > 1:
                    painel.config(text="Erro!")
                    return
                resultado = math.acos(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
        else:
            # cos(x)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                resultado = math.cos(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                resultado = math.cos(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_tan():
    """
    Função para o botão tan
    """
    global numero1, numero2, operacao, resultado, shift
    
    try:
        if shift:
            # tan^-1 (arctan)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                resultado = math.atan(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                resultado = math.atan(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
        else:
            # tan(x)
            if operacao == "":
                current_value = float(numero1.replace(",", "."))
                resultado = math.tan(current_value)
                numero1 = str(resultado)
                painel.config(text=formatar_numero(resultado))
            else:
                current_value = float(numero2.replace(",", "."))
                resultado = math.tan(current_value)
                numero2 = str(resultado)
                painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_fact():
    """
    Função para o botão x!
    """
    global numero1, numero2, operacao, resultado
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            if current_value < 0 or current_value != int(current_value):
                painel.config(text="Erro!")
                return
            resultado = math.factorial(int(current_value))
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            if current_value < 0 or current_value != int(current_value):
                painel.config(text="Erro!")
                return
            resultado = math.factorial(int(current_value))
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_power():
    """
    Função para o botão x^
    """
    global numero1, numero2, operacao, resultado
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            resultado = current_value ** 2  # x^2 por padrão
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            resultado = current_value ** 2
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_power3():
    """
    Função para o botão x^3
    """
    global numero1, numero2, operacao, resultado
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            resultado = current_value ** 3
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            resultado = current_value ** 3
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def func_sqrt3():
    """
    Função para o botão 3√
    """
    global numero1, numero2, operacao, resultado
    
    try:
        if operacao == "":
            current_value = float(numero1.replace(",", "."))
            if current_value < 0:
                resultado = -((-current_value) ** (1/3))
            else:
                resultado = current_value ** (1/3)
            numero1 = str(resultado)
            painel.config(text=formatar_numero(resultado))
        else:
            current_value = float(numero2.replace(",", "."))
            if current_value < 0:
                resultado = -((-current_value) ** (1/3))
            else:
                resultado = current_value ** (1/3)
            numero2 = str(resultado)
            painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2))
    except:
        painel.config(text="Erro!")

def processar_operador_basico(operador):
    global operation, numero1, operacao, numero2
    
    operador_simples = operador.strip().replace("X", "*").replace("÷", "/")
    
    if operation[1] == "#":  
        operation[0] = float(numero1.replace(",", "."))
        operation[1] = operador_simples
        numero1 = "0"
        painel.config(text=numero1)
    else:  
        operation[2] = float(numero1.replace(",", "."))
        resultado = res()
        operation[0] = resultado
        operation[1] = operador_simples
        operation[2] = 0
        numero1 = str(resultado)
        painel.config(text=numero1)

def res():
    try:
        a = operation[0]
        b = operation[2]
        op = operation[1]

        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return "Erro" if b == 0 else a / b
        else:
            return b
    except:
        return "Erro"

def reset_values(result):
    global values, operation, aIndex, numero1
    values = ["#"]
    operation = [result, "#", 0]
    aIndex = 0
    numero1 = str(result)
    painel.config(text=numero1)

def calc_raiz():
    global numero1
    try:
        n = float(numero1.replace(",", "."))
        res = math.sqrt(n)
        reset_values(res)
    except:
        painel.config(text="Erro")

def calc_raiz_cubica():
    global numero1
    try:
        n = float(numero1.replace(",", "."))
        res = n ** (1/3)
        reset_values(res)
    except:
        painel.config(text="Erro")

def calc_radiciacao():
    global values, operation, aIndex, numero1
    try:
        if operation[1] == "rad":
            radicando = float(numero1.replace(",", "."))
            indice = operation[0]
            if indice == 0:
                painel.config(text="Erro")
            else:
                res = radicando ** (1/indice)
                reset_values(res)
        else:
            indice = float(numero1.replace(",", "."))
            operation[0] = indice
            operation[1] = "rad"
            values = ["#"]
            numero1 = str(indice) + "√"
            painel.config(text=numero1)
    except:
        painel.config(text="Erro")
        
def calc_inverso():
    global numero1, shift
    
    if shift:
        calc_fatorial()
        shift = False  
        return
    try:
        n = float(numero1.replace(",", "."))
        if n == 0:
            painel.config(text="Erro")
        else:
            res = 1 / n
            reset_values(res)
    except:
        painel.config(text="Erro")

def calc_fatorial():
    global numero1
    try:
        n = int(float(numero1.replace(",", ".")))
        if n < 0:
            painel.config(text="Erro")
        else:
            res = math.factorial(n)
            reset_values(res)
    except:
        painel.config(text="Erro")

def calc_quadrado():
    global numero1
    try:
        n = float(numero1.replace(",", "."))
        res = n**2
        reset_values(res)
    except:
        painel.config(text="Erro")

def calc_cubo():
    global numero1, shift
    if shift:
        calc_raiz_cubica()
        shift = not shift
    else:
        try:
            n = float(numero1.replace(",", "."))
            res = n**3
            reset_values(res)
        except:
            painel.config(text="Erro")

def calc_exponenciacao():
    global values, operation, aIndex, numero1, shift
    
    if shift:
        calc_raiz_cubica()
        shift = False 
        return
    
    try:
        if operation[1] == "^":
            expoente = float(numero1.replace(",", "."))
            base = operation[0]
            res = base ** expoente
            reset_values(res)
        else:
            base = float(numero1.replace(",", "."))
            operation[0] = base
            operation[1] = "^"
            values = ["#"]
            numero1 = str(base) + "^"
            painel.config(text=numero1)
    except:
        painel.config(text="Erro")

# Formatação de graus
def format_result(value, mode="norm", digits=2):
    try:
        if mode == "fix":
            out = f"{value:.{digits}f}"
        elif mode == "sci":
            sig = max(1, int(digits))
            out = f"{value:.{sig}e}"
        else:
            out = f"{value:.12g}"
        return out
    except Exception:
        return "Erro"

def formatDegree(expression):
    # Remove espaços e substitui vírgulas por pontos
    expr = expression.replace(" ", "").replace(",", ".")
    
    # Verifica se há símbolos de grau na expressão
    if "°" in expr:
        # Substitui ° por *1 e adiciona conversão para radianos para funções trigonométricas
        expr = expr.replace("°", "*math.pi/180")
    
    # Substitui porcentagem
    expr = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expr)
    
    try:
        resultado = eval(expr)
        return format_result(resultado)
    except Exception as e:
        return f"Erro: {str(e)}"

def func_degree():
    """Insere símbolo de grau no número atual"""
    global numero1, numero2, operacao
    if operacao == "":
        numero1 += "°"
        painel.config(text=formatar_numero(numero1.replace("°", "")) + "°")
    else:
        numero2 += "°"
        painel.config(text=formatar_numero(numero1) + operacao + formatar_numero(numero2.replace("°", "")) + "°")

# Painel
painel = Label(root, text=str(numero1), anchor='e', bg="white", relief="sunken", font=("Arial", 24), height=1)
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
btn_inverse = tk.Button(root, text='1/x', width=10, height=3, command=calc_inverso)
btn_inverse.grid(row=2, column=0, padx=PADDING_X, pady=PADDING_Y)

btn_square = tk.Button(root, text='x²', width=10, height=3, command=calc_quadrado)
btn_square.grid(row=2, column=1, padx=PADDING_X, pady=PADDING_Y)
 
btn_sqrt = tk.Button(root, text='²√x', width=10, height=3, command=calc_raiz)
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

    # Colocar o frame inteiro no grid principal
    frame_replay.grid(row=11, column=2, columnspan=2, rowspan=2, padx=PADDING_X, pady=PADDING_Y)

    btn_replay1 = tk.Button(root, text='RCL', width=5, height=2, command=func_rcl)
    btn_replay1.grid(row=15, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay12 = tk.Button(root, text='ENG', width=5, height=2, command=func_eng)
    btn_replay12.grid(row=15, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay13 = tk.Button(root, text='(', width=5, height=2, command=lambda: inserir_numero("("))
    btn_replay13.grid(row=15, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_replay14 = tk.Button(root, text=')', width=5, height=2, command=lambda: inserir_numero(")"))
    btn_replay14.grid(row=15, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_replay15 = tk.Button(root, text=',', width=5, height=2, command=func_equals)
    btn_replay15.grid(row=15, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_mplus = tk.Button(root, text='M+', width=5, height=2, command=func_m_plus)
    btn_mplus.grid(row=15, column=5, padx=PADDING_X, pady=PADDING_Y)

    btn_replay2 = tk.Button(root, text='(-)', width=5, height=2, command=swapSignals)
    btn_replay2.grid(row=14, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay22 = tk.Button(root, text='°,,,', width=5, height=2, command=func_degree)
    btn_replay22.grid(row=14, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay23 = tk.Button(root, text='hyp', width=5, height=2, command=func_equals)
    btn_replay23.grid(row=14, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_replay24 = tk.Button(root, text='sin', width=5, height=2, command=func_sin)
    btn_replay24.grid(row=14, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_replay25 = tk.Button(root, text='cos', width=5, height=2, command=func_cos)
    btn_replay25.grid(row=14, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay26 = tk.Button(root, text='tan', width=5, height=2, command=func_tan)
    btn_replay26.grid(row=14, column=5, padx=PADDING_X, pady=PADDING_Y)

    btn_replay3 = tk.Button(root, text='Ab/c', width=5, height=2, command=func_abc)
    btn_replay3.grid(row=13, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay32 = tk.Button(root, text='√', width=5, height=2, command=calc_raiz)
    btn_replay32.grid(row=13, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay33 = tk.Button(root, text='X²', width=5, height=2, command=calc_quadrado)
    btn_replay33.grid(row=13, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_replay34 = tk.Button(root, text='^', width=5, height=2, command=calc_exponenciacao)
    btn_replay34.grid(row=13, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_replay35 = tk.Button(root, text='log', width=5, height=2, command=func_log)
    btn_replay35.grid(row=13, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay36 = tk.Button(root, text='ln', width=5, height=2, command=func_ln)
    btn_replay36.grid(row=13, column=5, padx=PADDING_X, pady=PADDING_Y)
    
    btn_replay43 = tk.Button(root, text='x-¹', width=5, height=2, command=calc_inverso)
    btn_replay43.grid(row=12, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_replay44 = tk.Button(root, text='nCr', width=5, height=2, command=func_ncr)
    btn_replay44.grid(row=12, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_replay45 = tk.Button(root, text='Pol(', width=5, height=2, command=func_pol)
    btn_replay45.grid(row=12, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay46 = tk.Button(root, text='x³', width=5, height=2, command=calc_cubo)
    btn_replay46.grid(row=12, column=5, padx=PADDING_X, pady=PADDING_Y)

    btn_shift = tk.Button(root, text='shift', width=5, height=2, command=toggle_shift, relief="raised")
    btn_shift.grid(row=11, column=0, padx=PADDING_X, pady=PADDING_Y)
    btn_alpha = tk.Button(root, text='alpha', width=5, height=2, command=toggle_alpha, relief="raised")
    btn_alpha.grid(row=11, column=1, padx=PADDING_X, pady=PADDING_Y)
    btn_mode = tk.Button(root, text='mode', width=5, height=2, command=toggle_mode)
    btn_mode.grid(row=11, column=4, padx=PADDING_X, pady=PADDING_Y)
    btn_replay56 = tk.Button(root, text='on', width=5, height=2, command=func_c)
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

    btn_exp = tk.Button(root, text='EXP', width=10, height=3, command=lambda: inserir_numero("E"))
    btn_exp.grid(row=20, column=2, padx=PADDING_X, pady=PADDING_Y)
    btn_ans = tk.Button(root, text='Ans', width=10, height=3, command=lambda: inserir_numero("Ans"))
    btn_ans.grid(row=20, column=3, padx=PADDING_X, pady=PADDING_Y)
    btn_equals.grid(row=20, column=4,columnspan=5, padx=PADDING_X, pady=PADDING_Y)
    btn_equals.config(width=10)

else:
    modo = False    
 
root.mainloop()
