import inspect
import os.path
import entrada_saida as es
import telegram_bot as tb
from datetime import datetime

log = ''


def printinfo(texto, erro=False, enviar_msg=False):
    global log
    pilha_de_chamadas = inspect.stack()
    linha_atual = pilha_de_chamadas[1].frame.f_lineno
    nome_arquivo = os.path.basename(pilha_de_chamadas[1].filename).replace('_', '\\_')
    nome_contexto = pilha_de_chamadas[1].function.replace('_', '\\_')
    nome_classe = pilha_de_chamadas[1].frame.f_locals.get('__qualname__', None)
    if nome_classe is None:
        try:
            nome_classe = pilha_de_chamadas[1].frame.f_locals['self'].__class__.__name__
            nome_classe = nome_classe.replace('_', '\\_')
        except KeyError:
            pass
    data_atual = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M:%S")
    msg = f"Arquivo:<'{nome_arquivo}'> Classe:<'{nome_classe}'> Função/Método:<'{nome_contexto}'> Linha:<'{linha_atual}'>\n Mensagem:        <'{texto}'>\n  Data: {data_atual} Hora: {hora_atual}"
    log = f'{log}\n{msg}'
    if enviar_msg == True:
        texto_escapado = texto.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        msg_tb = msg.replace(f"Mensagem:        <'{texto}'>",f"\nMensagem:        \n\n<'```\n\n{texto_escapado}\n\n```'>\n")
        
        tb.send_telegram_message(msg_tb, printinfo_callback=printinfo, parse_mode="Markdown")
    msg = f"Arquivo:<'{nome_arquivo}'> Classe:<'{nome_classe}'> Função/Método:<'{nome_contexto}'> Linha:<'{linha_atual}'>\n Mensagem:        <'{texto}'>\n  Data: {data_atual} Hora: \033[95m{hora_atual}\033[0m"

    if erro:
        msg = msg.replace(f"Mensagem:        <'{texto}'>", f"\033[91mMensagem:        <'{texto}'>\033[0m")
    else:
        msg = msg.replace(f"Mensagem:        <'{texto}'>", f"\033[92mMensagem:        <'{texto}'>\033[0m")
    print(msg)

def salvar_log():
    global log
    es.salvar_log(log)
    log = ''

##tb.verificar_variaveis_ambiente(printinfo)


