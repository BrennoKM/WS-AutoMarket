import os
import constantes
import json
import info
from datetime import datetime
from PIL import Image, ImageTk


# global itens_dic
# itens_dic = []

def inicio():
        global itens_dic
        # itens_dic = []
        itens_dic = ler_itens()

        # itens = ler_itens()
        consts = ler_constantes()
        
        if itens_dic:
            carregar_itens()
        else:
            gerar_itens_padroes()
            salvar_itens()
            carregar_itens()
        
        if consts:
            carregar_constantes()
        else:
            salvar_constantes()
            carregar_constantes()

def existe_diretorio(diretorio):
    if os.path.exists(diretorio):
        return True
    return False

def criar_diretorio(diretorio):
    os.makedirs(diretorio)


def load_image(arquivo, x, y):
    if os.path.exists(arquivo):
        load_image = Image.open(arquivo)
        resiz = load_image.resize((x, y))
        return ImageTk.PhotoImage(resiz)
    else:
        info.printinfo(f"Arquivo '{arquivo}' não encontrado.")
        return None
    
def ler_itens():
    if not os.path.exists(constantes.PATH_ITENS):
        os.makedirs(constantes.PATH_ITENS)
    if os.path.exists(f'{constantes.PATH_ITENS}itens.json'):
        with open(f'{constantes.PATH_ITENS}itens.json', "r") as file:
            itens_dic = json.loads(file.read())
            return itens_dic
    else:
        return []


def alterarItem(nome, novo_nome=None, nova_quantidade=None, novo_preco=None, novo_arqNome=None, nova_licenca=None, novo_slots=None, novo_precoMedio=None):
    for item in itens_dic:
        if item["Nome"] == nome:
            if novo_nome is not None:
                item["Nome"] = novo_nome
            if nova_quantidade is not None:
                item["Quantidade"] = nova_quantidade
            if novo_preco is not None:
                item["Preco"] = novo_preco
            if novo_arqNome is not None:
                item["Nome Arquivo"] = novo_arqNome
            if nova_licenca is not None:
                item["Licenca"] = nova_licenca
            if novo_slots is not None:
                item["Slots"] = novo_slots
            if novo_precoMedio is not None:
                item["PrecoMedio"] = novo_precoMedio
            # print(item)
            return True
    return False

def adicionarItem(nome, arqNome, qnt=None, preco=None, licenca=False, slots = 15, precoMedio=None):
        verif = False
        if itens_dic:
            for item in itens_dic:
                if item["Nome"] == nome:
                    alterarItem(nome, nome, qnt, preco, arqNome, licenca, slots, precoMedio)
                    verif = True
        if verif == False:
            item = {
                "Nome": nome,
                "Quantidade": qnt,
                "Preco": preco,
                "Arquivo": arqNome,
                "Licenca": licenca,
                "Slots": slots,
                "PrecoMedio": precoMedio
            }
            itens_dic.append(item)
            return item

def gerar_itens_padroes():
        # itens_dic = []
        adicionarItem("Sign", "sign.png", 10, 26000, False, 15)
        adicionarItem("Dmg III",  "dmg3.png", 10, 9999, False, 15)
        adicionarItem("Stam",  "stam.png", 1, 11500, False, 15)
        adicionarItem("Stam (100un)",  "stam.png", 10, 109000, True, 15)
        adicionarItem("Reparo",  "reparo.png", 10, 9999, False, 15)
        adicionarItem("Teleporte",  "tp.png", 10, 8200, False, 15)
        adicionarItem("Teleporte (100un)",  "tp.png", 100, 69200, True, 15)
        adicionarItem("Bau Natal", "bau_natal.png", 10, 51000, False, 15)

def salvar_itens():
    if not os.path.exists(constantes.PATH_ITENS):
        os.makedirs(constantes.PATH_ITENS)
    with open(f'{constantes.PATH_ITENS}itens.json', "w") as file:
        file.write(json.dumps(itens_dic))

def salvar_itens_novos(dados):
    if not os.path.exists(constantes.PATH_ITENS):
        os.makedirs(constantes.PATH_ITENS)
    with open(f'{constantes.PATH_ITENS}itens.json', "w") as file:
        file.write(json.dumps(dados))

def carregar_itens_nomes():
    ITENS = []
    for item in ler_itens():
        # itensDic.append(item)
        ITENS.append(item["Nome"])
    return ITENS

def carregar_itens():
    dados = []
    for item in ler_itens():
        dados.append(item)
    return dados

def deletar_item(item):
    if os.path.exists(item):
        os.remove(item)

def ler_constantes():
    if not os.path.exists(constantes.PATH_CONSTS):
        os.makedirs(constantes.PATH_CONSTS)
    if os.path.exists(f'{constantes.PATH_CONSTS}consts.json'):
        with open(f'{constantes.PATH_CONSTS}consts.json', "r") as file:
            return json.loads(file.read())
    else:
        return None

def carregar_constantes():
    const = ler_constantes()
    constantes.AREA_ITENS = const['AREA_ITENS']
    constantes.AREA_MERCADO = const['AREA_MERCADO']

    constantes.POSICAO_LICENSA_MKT = const['POSICAO_LICENSA_MKT']
    constantes.POSICAO_BARRA_GRANDE_LATERAL = const['POSICAO_BARRA_GRANDE_LATERAL']
    constantes.POSICAO_QUANTIDADE = const['POSICAO_QUANTIDADE']
    constantes.POSICAO_PRECO = const['POSICAO_PRECO']

def salvar_constantes():
    consts = gerar_constantes()
    with open(f'{constantes.PATH_CONSTS}consts.json', "w") as file:
        file.write(json.dumps(consts))

def gerar_constantes():
    consts = {
        'AREA_ITENS': constantes.AREA_ITENS,
        'AREA_MERCADO': constantes.AREA_MERCADO,
        'POSICAO_BARRA_GRANDE_LATERAL': constantes.POSICAO_BARRA_GRANDE_LATERAL,
        'POSICAO_QUANTIDADE': constantes.POSICAO_QUANTIDADE,
        'POSICAO_PRECO': constantes.POSICAO_PRECO,
        'POSICAO_LICENSA_MKT': constantes.POSICAO_LICENSA_MKT
    }
    return consts

def gerar_constantes_padroes():
    constantes.AREA_ITENS = (743, 214, 429, 615)
    constantes.AREA_MERCADO = (745, 881, 395, 103)
    constantes.POSICAO_LICENSA_MKT = (759, 639)
    constantes.POSICAO_BARRA_GRANDE_LATERAL = (1157, 955)
    constantes.POSICAO_QUANTIDADE = (1034, 571)
    constantes.POSICAO_PRECO = (1151, 442)

def salvar_posicao(posicao, chave):
    partes = posicao.split("+")[1:]
    posicao_final = "+" + "+".join(partes)

    try:
        with open(f"{constantes.PATH_CONSTS}config.json", "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        dados = []

    dados_existentes = [d for d in dados if chave in d]
    if dados_existentes:
        dados_existentes[0][chave] = posicao_final
    else:
        novo_dado = {chave: posicao_final}
        dados.append(novo_dado)

    with open(f"{constantes.PATH_CONSTS}config.json", "w") as file:
        json.dump(dados, file)

# def salvar_posicao(posicao):
#     partes = posicao.split("+")[1:]
#     posicao_final = "+" + "+".join(partes)

#     if not os.path.exists(constantes.PATH_CONSTS):
#         os.makedirs(constantes.PATH_CONSTS)
#     with open(f"{constantes.PATH_CONSTS}config.json", "w") as file:
#         json.dump({"Posicao_na_tela": posicao_final}, file)

def carregar_posicao():
    if not os.path.exists(constantes.PATH_CONSTS):
        os.makedirs(constantes.PATH_CONSTS)
    try:
        with open(f"{constantes.PATH_CONSTS}config.json", "r") as file:
            data = json.load(file)
            for indice in data:
                posicao_tela = indice.get("Posicao_na_tela")
                if posicao_tela is not None:
                    return posicao_tela
    except FileNotFoundError:
        return None
    
# def salvar_posicao_config(posicao):
#     partes = posicao.split("+")[1:]
#     posicao_final = "+" + "+".join(partes)

#     if not os.path.exists(constantes.PATH_CONSTS):
#         os.makedirs(constantes.PATH_CONSTS)
#     with open(f"{constantes.PATH_CONSTS}config.json", "w") as file:
#         json.dump({"Posicao_na_tela_config": posicao_final}, file)

def carregar_posicao_config():
    if not os.path.exists(constantes.PATH_CONSTS):
        os.makedirs(constantes.PATH_CONSTS)
    try:
        with open(f"{constantes.PATH_CONSTS}config.json", "r") as file:
            data = json.load(file)
            for indice in data:
                posicao_tela = indice.get("Posicao_na_tela_config")
                if posicao_tela is not None:
                    return posicao_tela
    except FileNotFoundError:
        return None


def salvar_log(log):
    if not os.path.exists(constantes.PATH_LOGS):
        os.makedirs(constantes.PATH_LOGS)
    data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo_log = os.path.join(constantes.PATH_LOGS, f"log_{data_hora_atual}.txt")
    
    with open(nome_arquivo_log, 'w', encoding='utf-8') as arquivo_log:
        arquivo_log.write(f'{log}\n')
        