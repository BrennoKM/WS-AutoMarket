import requests
import threading
from dotenv import load_dotenv
import os
import time
import info
import entrada_saida as es
import constantes as const
import acoes
import threading
import tempfile
from datetime import datetime


TOKEN = ''
CHAT_IDS = ''
AUTHORIZED_CHAT_IDS = ''

bot_start_time = 0

def verificar_variaveis_ambiente(printinfo_callback=print):
    global TOKEN, CHAT_IDS, AUTHORIZED_CHAT_IDS
    try:
        load_dotenv(dotenv_path=const.PATH_ENV)

        TOKEN = os.getenv("TELEGRAM_TOKEN")
        CHAT_IDS = os.getenv("CHAT_IDS")
        AUTHORIZED_CHAT_IDS = os.getenv("AUTHORIZED_CHAT_IDS").split(",")
        if not TOKEN:
            if printinfo_callback:
                printinfo_callback("Aviso: TELEGRAM_TOKEN não está definido no arquivo .env", erro=True)

        if CHAT_IDS:
            CHAT_IDS = CHAT_IDS.split(",")
        else:
            if printinfo_callback:
                printinfo_callback("Aviso: CHAT_IDS não está definido no arquivo .env", erro=True)

        if not AUTHORIZED_CHAT_IDS:
            printinfo_callback("Aviso: AUTHORIZED_CHAT_IDS não está definido no arquivo .env", erro=True)
    except Exception as e:
        if printinfo_callback:
            printinfo_callback(f"Erro ao verificar variáveis de ambiente no arquivo 'telegram.env'.", erro=True)


session = requests.Session()

def send_telegram_message(message, printinfo_callback=print, parse_mode=None):
    global TOKEN, CHAT_IDS
    if not TOKEN or not CHAT_IDS:
        # if printinfo_callback:
        #     printinfo_callback("Aviso: Não é possível enviar mensagem, TOKEN ou CHAT_IDS não definidos.", erro=True)
        return
    # Inicia uma thread para cada chat_id
    for chat_id in CHAT_IDS:
        thread = threading.Thread(target=send_message, args=(chat_id, message, printinfo_callback, parse_mode))
        thread.start()

def send_message(chat_id, message, printinfo_callback=print, parse_mode=None):
    urlmsg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    if (parse_mode is not None):
        data["parse_mode"] = parse_mode
        
    
    try:
        response = requests.post(urlmsg, headers=headers, json=data, timeout=60)  # Adiciona timeout de 60 segundos
        response.raise_for_status()  # Levanta exceção para códigos de status HTTP de erro
    except requests.exceptions.ConnectionError:
        if printinfo_callback:
            printinfo_callback(f"Erro de conexão ao enviar mensagem para chat_id {chat_id}.", True)
        return None  # Retorna None sem tentar novamente
    except requests.exceptions.RequestException as e:
        if printinfo_callback:
            printinfo_callback(f"Erro na request para chat_id {chat_id}", True, True)
            # printinfo_callback(f"Erro na request para chat_id {chat_id}: {e}", True, True)
        return None  # Retorna None para outros erros
    return response.json()

def send_image(chat_id, image_path, printinfo_callback):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    legenda_hora_atual = datetime.now().strftime("%H:%M:%S")
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {'photo': image_file}
            data = {'chat_id': chat_id, 'caption': f"Printscreen tirada às {legenda_hora_atual}"}
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()  # Levanta exceção para códigos de status HTTP de erro
            
            printinfo_callback("Printscreen enviada com sucesso.")
            return response.json()  # Retorna a resposta se a requisição for bem-sucedida

    except requests.exceptions.ConnectionError:
        printinfo_callback(f"Erro de conexão ao enviar a imagem para chat_id {chat_id}.", True)
        return None  # Retorna None sem tentar novamente
    except requests.exceptions.RequestException as e:
        printinfo_callback(f"Falha ao enviar printscreen para chat_id {chat_id}", True, True)
        return None  # Retorna None para outros erros
    except FileNotFoundError:
        printinfo_callback(f"Arquivo não encontrado: {image_path}", True, True)
        return None  # Retorna None se o arquivo não for encontrado


            
# verificar_variaveis_ambiente()

# URL TO GET CHAT_ID:
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# # ULR TO ACTUALLY SEND TELEGRAM MESSAGE:
# message = "Hello, World!"
# urlmsg = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_IDS[0]}&text={message}"

# print(requests.get(url).json())

# r = requests.get(urlmsg)
# print(r.json())

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        response = session.get(url, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # info.printinfo(f"Erro ao obter atualizações.")
        return None

def process_updates(updates, myEvent):
    global bot_start_time
    for update in updates["result"]:
        message = update.get("message")
        if message:
            update_time = update["message"]["date"]
            if update_time < bot_start_time:
                info.printinfo(f"Ignorando comando que foi submetido antes do bot iniciar.", True)
                continue
            text = message.get("text")
            chat_id = message["chat"]["id"]
            if str(chat_id) in AUTHORIZED_CHAT_IDS:  # Verificar se o chat_id está autorizado
                process_command(text, chat_id, myEvent)

            else:
                if text == "/start":
                    send_message(chat_id, "Bem vindo ao WS-AutoCraft, verifique o menu para enviar comandos.", info.printinfo)
                    info.printinfo(f"Novo /start no bot com chat_id: {chat_id}", False, True)
                else:
                    send_message(chat_id, "Você não está autorizado a usar este comando.")

def listen_for_commands(myEvent):
    global bot_start_time
    offset = None
    if not TOKEN or not CHAT_IDS:
        info.printinfo("Aviso: Não foi possível iniciar o bot do telegram, TOKEN ou CHAT_IDS não definidos.", erro=True)
        return
    info.printinfo("Bot telegram iniciado.", False, True)
    bot_start_time = int(time.time())
    # info.printinfo(f"Bot iniciado em: {bot_start_time}")
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            process_updates(updates, myEvent)
            if updates["result"]:
                offset = updates["result"][-1]["update_id"] + 1
        time.sleep(1)

def process_command(text, chat_id, myEvent):
    ## nesse ponto já se pressupoe que o chat_id é autorizado
    if text == "/start":
        send_message(chat_id, "Bem vindo ao WS-AutoMarket, verifique o menu para enviar comandos.", info.printinfo)
        info.printinfo(f"Novo /start no bot com chat_id: {chat_id}", False, True)
    elif text == "/starttask":
        send_telegram_message("Task de market iniciada.", info.printinfo)
        info.printinfo("Bot de craft foi iniciado remotamente.", False, True)
        if not myEvent.is_set():
            myEvent.set()
        
    elif text == "/stoptask":
        send_telegram_message("Task de market encerrada.", info.printinfo)
        info.printinfo("Bot de market foi encerrado remotamente.", False, True)
        myEvent.clear()
        # myEventPausa.clear()
        time.sleep(2)
        info.salvar_log(resetar=False)

    elif text == "/pause":
        send_telegram_message("Task pausada.", info.printinfo)
        info.printinfo("Bot foi pausado remotamente.", False, True)
        myEvent.set()
    elif text == "/resume":
        send_telegram_message("Task despausada.", info.printinfo)
        info.printinfo("Bot foi despausado remotamente.", False, True)
        myEvent.clear()

    elif text == "/printscreen":
        info.printinfo("Comando de printscreen foi acionado remotamente.")
        screenshot = acoes.capturar_print()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            screenshot_path = tmp_file.name
            screenshot.save(screenshot_path)
        send_image(chat_id, screenshot_path, info.printinfo)
        os.remove(screenshot_path)

def iniciar_bot(myEvent):
    verificar_variaveis_ambiente(info.printinfo)
    threading.Thread(target=listen_for_commands, args=(myEvent,)).start()

# Exemplo de uso
if __name__ == "__main__":
    from threading import Event
    myEvent = Event()
    myEventPausa = Event()
    iniciar_bot(myEvent, myEventPausa)