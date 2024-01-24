import inspect
import os.path
import entrada_saida as es

log = ''

def printinfo(texto):
    global log
    pilha_de_chamadas = inspect.stack()
    linha_atual = pilha_de_chamadas[1].frame.f_lineno
    nome_arquivo = os.path.relpath(pilha_de_chamadas[1].filename)
    nome_contexto = pilha_de_chamadas[1].function
    nome_classe = pilha_de_chamadas[1].frame.f_locals.get('__qualname__', None)
    if nome_classe is None:
        try:
            nome_classe = pilha_de_chamadas[1].frame.f_locals['self'].__class__.__name__
        except KeyError:
            pass
    msg = f"Arquivo:<'{nome_arquivo}'> Classe:<'{nome_classe}'> Função/Método:<'{nome_contexto}'> Linha:<'{linha_atual}'>\nMensagem:<'{texto}'>"
    log = f'{log}\n{msg}'
    print(msg)

def salvar_log():
    es.salvar_log(log)




