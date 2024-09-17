import requests
import threading
from dotenv import load_dotenv
import os


TOKEN = ''
CHAT_IDS = ''

def verificar_variaveis_ambiente(printinfo_callback=None):
    global TOKEN, CHAT_IDS
    load_dotenv(dotenv_path='telegram.env')

    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_IDS = os.getenv("CHAT_IDS")
    if not TOKEN:
        if printinfo_callback:
            printinfo_callback("Aviso: TELEGRAM_TOKEN não está definido no arquivo .env", erro=True)

    if CHAT_IDS:
        CHAT_IDS = CHAT_IDS.split(",")
    else:
        if printinfo_callback:
            printinfo_callback("Aviso: CHAT_IDS não está definido no arquivo .env", erro=True)

session = requests.Session()

def send_telegram_message(message, printinfo_callback=None):
    global TOKEN, CHAT_IDS
    if not TOKEN or not CHAT_IDS:
        if printinfo_callback:
            printinfo_callback("Aviso: Não é possível enviar mensagem, TOKEN ou CHAT_IDS não definidos.", erro=True)
        return

    def send_message(chat_id):
        urlmsg = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        try:
            response = session.get(urlmsg, timeout=60)  # Adiciona timeout de 60 segundos
            response.raise_for_status()  # Levanta exceção para códigos de status HTTP de erro
        except requests.exceptions.RequestException as e:
            if printinfo_callback:
                printinfo_callback(f"Erro na request para chat_id {chat_id}.", True)
            return None
        # if printinfo_callback:
        #     printinfo_callback(f"Mensagem enviada para chat_id {chat_id}.")
        return response.json()

    # Inicia uma thread para cada chat_id
    for chat_id in CHAT_IDS:
        thread = threading.Thread(target=send_message, args=(chat_id,))
        thread.start()


# verificar_variaveis_ambiente()

# URL TO GET CHAT_ID:
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# # ULR TO ACTUALLY SEND TELEGRAM MESSAGE:
# message = "Hello, World!"
# urlmsg = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_IDS[0]}&text={message}"

# print(requests.get(url).json())

# r = requests.get(urlmsg)
# print(r.json())