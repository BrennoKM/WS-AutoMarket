import json
import os

global AREA_ITENS, AREA_MERCADO, POSICAO_LICENSA_MKT, POSICAO_BARRA_GRANDE_LATERAL, POSICAO_QUANTIDADE, POSICAO_PRECO


AREA_ITENS = (743, 214, 429, 615)
AREA_MERCADO = (745, 881, 395, 103)

POSICAO_LICENSA_MKT = (759, 639)
POSICAO_BARRA_GRANDE_LATERAL = (1160, 963)
POSICAO_QUANTIDADE = (1034, 571)
POSICAO_PRECO = (1151, 442)

PATH_IMGS = 'imgs/'
PATH_ITENS = 'itens/'
PATH_CONSTS = 'consts/'
ITENS = []

class ControlConfig:
    def __init__(self):
        self.itensDic = []

        itens = self.lerItens()
        consts = self.lerConstantes()
        
        if itens:
            self.carregarItens()
        else:
            self.gerarItensPadroes()
            self.salvarItens()
            self.carregarItens()
        
        if consts:
            self.carregarConstantes()
        else:
            self.salvarConstantes()
            self.carregarConstantes()
        
    def adicionarItem(self, nome, arqNome, qnt=None, preco=None, licenca=False):
        verif = False
        for item in self.itensDic:
            if item["Nome"] == nome:
                self.alterarItem(nome, nome, qnt, preco, arqNome, licenca)
                verif = True
        if verif == False:
            item = {
                "Nome": nome,
                "Quantidade": qnt,
                "Preco": preco,
                "Arquivo": arqNome,
                "Licenca": licenca
            }
            self.itensDic.append(item)
            return item

    def deletarItem(self, nome):
        for item in self.itensDic:
            if item["Nome"] == nome:
                self.itensDic.remove(item)
                return True
        return False

    def alterarItem(self, nome, novo_nome=None, nova_quantidade=None, novo_preco=None, novo_arqNome=None, nova_licenca=None):
        for item in self.itensDic:
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
                return True
        return False
    
    def obterNomesArquivos(self):
        return [item["Nome Arquivo"] for item in self.itensDic if "Nome Arquivo" in item]
    
    def salvarItens(self):
        with open(f'{PATH_ITENS}itens.json', "w") as file:
            file.write(json.dumps(self.itensDic))

    def salvarItensNovaOrdem(self, NovaOrdem):
        with open(f'{PATH_ITENS}itens.json', "w") as file:
            file.write(json.dumps(NovaOrdem))

    def lerItens(self):
        if not os.path.exists(PATH_ITENS):
            os.makedirs(PATH_ITENS)
        if os.path.exists(f'{PATH_ITENS}itens.json'):
            with open(f'{PATH_ITENS}itens.json', "r") as file:
                return json.loads(file.read())
        else:
            return None

    def carregarItens(self):
        for item in self.lerItens():
                self.itensDic.append(item)
                ITENS.append(item["Nome"])

    def gerarItensPadroes(self):
        self.adicionarItem("Sign", "sign.png", 10, 26000)
        self.adicionarItem("Dmg III",  "dmg3.png", 10, 9999)
        self.adicionarItem("Reparo",  "reparo.png", 10, 9999)
        self.adicionarItem("Teleporte",  "tp.png", 10, 8200)
        self.adicionarItem("Teleporte (100un)",  "tp.png", 100, 69200, True)
        self.adicionarItem("Bau Natal", "bau_natal.png", 10, 51000)
    
    def gerarConstantes(self):
        constantes = {
            'AREA_ITENS': AREA_ITENS,
            'AREA_MERCADO': AREA_MERCADO,
            'POSICAO_BARRA_GRANDE_LATERAL': POSICAO_BARRA_GRANDE_LATERAL,
            'POSICAO_QUANTIDADE': POSICAO_QUANTIDADE,
            'POSICAO_PRECO': POSICAO_PRECO,
            'POSICAO_LICENSA_MKT': POSICAO_LICENSA_MKT
        }
        return constantes

    def gerarConstantesPadroes(self):
        global AREA_ITENS, AREA_MERCADO, POSICAO_LICENSA_MKT, POSICAO_BARRA_GRANDE_LATERAL, POSICAO_QUANTIDADE, POSICAO_PRECO
        AREA_ITENS = (743, 214, 429, 615)
        AREA_MERCADO = (745, 881, 395, 103)
        POSICAO_LICENSA_MKT = (759, 639)
        POSICAO_BARRA_GRANDE_LATERAL = (1157, 955)
        POSICAO_QUANTIDADE = (1034, 571)
        POSICAO_PRECO = (1151, 442)

    def salvarConstantes(self):
        constantes = self.gerarConstantes()
        with open(f'{PATH_CONSTS}consts.json', "w") as file:
            file.write(json.dumps(constantes))

    def lerConstantes(self):
        if not os.path.exists(PATH_CONSTS):
            os.makedirs(PATH_CONSTS)
        if os.path.exists(f'{PATH_CONSTS}consts.json'):
            with open(f'{PATH_CONSTS}consts.json', "r") as file:
                return json.loads(file.read())
        else:
            return None

    def carregarConstantes(self):
        const = self.lerConstantes()
        global AREA_ITENS, AREA_MERCADO, POSICAO_LICENSA_MKT, POSICAO_BARRA_GRANDE_LATERAL, POSICAO_QUANTIDADE, POSICAO_PRECO

        AREA_ITENS = const['AREA_ITENS']
        AREA_MERCADO = const['AREA_MERCADO']

        POSICAO_LICENSA_MKT = const['POSICAO_LICENSA_MKT']
        POSICAO_BARRA_GRANDE_LATERAL = const['POSICAO_BARRA_GRANDE_LATERAL']
        POSICAO_QUANTIDADE = const['POSICAO_QUANTIDADE']
        POSICAO_PRECO = const['POSICAO_PRECO']

    def salvar_posicao(self, geometry):
        posicao = geometry
        
        partes = posicao.split("+")[1:]
        posicao_final = "+" + "+".join(partes)

        with open(f"{PATH_CONSTS}config.json", "w") as file:
            json.dump({"Posicao_na_tela": posicao_final}, file)

    def carregar_posicao(self):
        try:
            with open(f"{PATH_CONSTS}config.json", "r") as file:
                data = json.load(file)
                return data.get("Posicao_na_tela")
        except FileNotFoundError:
            return None