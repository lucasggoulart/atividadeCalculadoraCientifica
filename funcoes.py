# Shift e Alpha
# Deve ter duas variáveis chamadas "shift" e "alpha" iniciada como False:

def toggle_shift(shift):
    shift = not shift

def toggle_alpha(alpha):
    alpha = not alpha

# Replay
# Deve ter algumas variáveis criadas:

# Histórico para replay
historico = []  # cada item será (numero1, numero2, operacao, resultado)
indice_historico = -1  # começa no último item do histórico

# Para o cursor de edição
posicao_cursor = 0  
modo_cursor = False  

# função que fizemos para alterar nosso painel e mudar os números pelas setas
def atualizar_painel_cursor():
    global numero1, numero2, operacao, posicao_cursor # aqui obtemos valores do nosso painel
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

    # configurando nosso painel
    if operacao == "":
        painel.config(text=texto_cursor)
    else:
        painel.config(text=formatar_numero(numero1) + operacao + texto_cursor)

def replay_cima():
    global indice_historico, historico
    if historico:
        if indice_historico == -1:
            indice_historico = len(historico) - 1
        elif indice_historico > 0:
            indice_historico -= 1
        resultado = historico[indice_historico][3]
        painel.config(text=formatar_numero(resultado)) # configurando nosso painel (podem alterar caso precise)

def replay_baixo():
    global indice_historico, historico
    if historico:
        if indice_historico == -1:
            indice_historico = len(historico) - 1
        elif indice_historico < len(historico) - 1:
            indice_historico += 1
        resultado = historico[indice_historico][3]
        painel.config(text=formatar_numero(resultado)) # configurando nosso painel (podem alterar caso precise)

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

# M+, M- e M
# Deve ter algumas variáveis criadas, além do Shift e Alpha, é necessário criar:

# Valor global da memória
memoria = 0

def func_m_plus():
    global memoria, numero1, numero2, operacao, resultado, shift, alpha # aqui obtemos valores do nosso painel

    try:
        if alpha:
            # Recupera o valor da memória
            painel.config(text=f"Memória: {formatar_numero(memoria)} (MR)") # muda nosso painel (altere do seu modo se necessário)
            return

        if operacao == "":
            valor = float(numero1.replace(",", "."))
        else:
            valor = float(numero2.replace(",", "."))

        if shift:
            memoria -= valor
            painel.config(text=f"Memória: {formatar_numero(memoria)} (M-)") # muda nosso painel (altere do seu modo se necessário)
        else:
            memoria += valor
            painel.config(text=f"Memória: {formatar_numero(memoria)} (M+)") # muda nosso painel (altere do seu modo se necessário)
    except ValueError:
        painel.config(text="Erro!") # muda nosso painel (altere do seu modo se necessário)

# Mode
# Deve ser criada uma variável:

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
    # Assim mudamos a variável e o tipo da calculadora

# Mais infos:
# Caso precisem, podemos enviar como está nossa calculadora para ser mais entendível como obtemos números e posições deles em nosso painel.