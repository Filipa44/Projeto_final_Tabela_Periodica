# Importa as bibliotecas necessárias
# Biblioteca tkinter é usada para criar a interface gráfica
# Biblioteca ttk é usada para criar mensagens
# Biblioteca json é usada para manipular arquivos JSON, onde contém os dados dos elementos químicos
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

#  Carrega o arquivo JSON com os dados dos elementos químicos
# O arquivo contém  várias informações sobre os elementos presentes na tabela periódica.
with open("dados_traduzidos_pt-PT_com_variaveis.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

elementos = dados["elementos"]

# Mensagem educativa conforme o estado físico do elemento químico
mensagem_estado = {
    "Gás": " É um gás à temperatura ambiente.Provavelmente não tem forma ou volume definidos!",
    "Sólido": " É sólido à temperatura ambiente.Possui forma e volume definidos.",
    "Líquido": " É líquido à temperatura ambiente.Flui e adapta-se ao formato do recipiente em que está inserido."
}

# Função para pesquisar e exibir o resultado do elemento químico
def pesquisar_elemento():
    termo = entrada.get().strip().lower() # lê a entrada do utilizador, remove espaços extras e converte para minúsculas

    if not termo: # se não se verificar a condição anterior, exibe uma mensagem de aviso
        messagebox.showwarning("Aviso", "Por favor, insira o símbolo ou o nome de um elemento.")
        return

    elemento_encontrado = None # percorre a lista de elementos químicos para encontrar o elemento correspondente ao símbolo ou nome fornecido pelo utilizador
    for e in elementos:
        if e["simbolo"].lower() == termo or e["nome"].lower() == termo:
            elemento_encontrado = e
            break

    if elemento_encontrado: # se o elemento for encontrado, exibe as suas informações consoante os dados da bibilioteca JSON
        e = elemento_encontrado
        info = f"""
 {e['nome']} ({e['simbolo']})
Número Atómico: {e['numeroAtomico']}
Massa Atómica: {e['massaAtomica']}
Grupo: {e['grupo']} Período: {e['periodo']}
Família: {e['familia']}
Camada Eletrónica: {e['camada'].capitalize()}
Estado à temperatura ambiente: {e['estadoPadrao']}
Ano de descoberta: {e['anoDescoberta']}
Ocorrência: {e['ocorrencia']}
Radioativo? {"Sim" if e['radioativo'] else "Não"}
Configuração eletrónica: {e['configuracaoEletronica']}
Estados de oxidação: {e['estadosOxidacao']}
Afinidade eletrónica: {e['afinidadeEletronica']}
Raio atómico: {e['raioAtomico']}
Calor específico: {e['calorEspecifico']}
"""
# Atualiza o texto com as informações do elemento encontrado
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, info)

 # Exibe a mensagem educativa sobre o estado físico do elemento químico
        estado = e["estadoPadrao"]
    
        if estado.lower() in ["gasoso", "gas"]:
            estado = "Gás"
        elif estado.lower() in ["solido", "sólido"]:
            estado = "Sólido"
        elif estado.lower() in ["liquido", "líquido"]:
            estado = "Líquido"

        estado_msg = mensagem_estado.get(estado, "")
        label_mensagem.config(text=estado_msg)
    else: # Se o elemento não for encontrado, limpa o texto do resultado e exibe uma mensagem de erro
        texto_resultado.delete("1.0", tk.END)
        label_mensagem.config(text="")
        messagebox.showerror("Erro", "Elemento não encontrado. Verifica o símbolo ou nome.")

# Organiza a interface gráfica
# Cria a janela principal( com 900 de comprimento e 650 de altura)
janela = tk.Tk()
janela.title("Tabela Periódica")
janela.geometry("900x650")
janela.minsize(900, 650)
# Configura o redimensionamento da janela automático
janela.columnconfigure(0, weight=1) 
janela.rowconfigure(2, weight=1)


# Adiciona imagem da tabela periódica e configura o tamanho
imagem = Image.open("tabela_periodica.png")
imagem_redimensionada = imagem.resize((800, 400), Image.Resampling.LANCZOS)
imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
frame_imagem = tk.Frame(janela)
# Garante que a imagem se expanda corretamente quando a janela é redimensionada
frame_imagem.grid(row=1, column=0, sticky="nsew")
frame_imagem.rowconfigure(0, weight=1)
frame_imagem.columnconfigure(0, weight=1)
# Rótulo para exibir a imagem da tabela periódica
label_imagem = tk.Label(frame_imagem, image=imagem_tk)
label_imagem.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Cria o bloco para a pesquisa de acordo com o símbolo ou nome do elemento
frame_pesquisa = tk.Frame(janela)
frame_pesquisa.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
frame_pesquisa.columnconfigure(1, weight=1)

# configuração do botão de pesquisa
tk.Label(frame_pesquisa, text="Insere o símbolo ou nome do elemento:").grid(row=0, column=0, sticky="w", padx=5)
entrada = tk.Entry(frame_pesquisa, font=("Arial", 12))
entrada.grid(row=0, column=1, sticky="ew", padx=5)
entrada.bind("<Return>", lambda event: pesquisar_elemento())
botao_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_elemento)
botao_pesquisar.grid(row=0, column=2, padx=5)


# Área de resultados(com as informações do elemento químico e a mensagem educativa)
frame_resultado = tk.Frame(janela)
frame_resultado.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
frame_resultado.columnconfigure(0, weight=1)
frame_resultado.rowconfigure(0, weight=1)
# Área de texto para exibir as informações do elemento químico com o tamanho da fonte definido
texto_resultado = tk.Text(frame_resultado, wrap="word", font=("Arial", 10))
texto_resultado.grid(row=0, column=0, sticky="nsew")
# Configura a barra de rolagem para a área de texto
scrollbar = tk.Scrollbar(frame_resultado, command=texto_resultado.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
texto_resultado.config(yscrollcommand=scrollbar.set)

# Rótulo para exibir a mensagem educativa sobre o estado físico do elemento químico
label_mensagem = tk.Label(frame_resultado, text="", font=("Arial", 10, "italic"), fg="blue", anchor="w", justify="left")
label_mensagem.grid(row=1, column=0, sticky="w", pady=(5, 0))


# Inicia a janela principal
janela.mainloop()
