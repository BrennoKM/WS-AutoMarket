import constants
import actions
import threading
import pyautogui as pg
import os
import time
from PIL import Image, ImageTk
from pynput import keyboard
from tkinter.ttk import Label, Button, Checkbutton, Combobox, Entry, Style
from tkinter import messagebox, Tk, Canvas
from ttkthemes import ThemedTk

control = constants.ControlConfig()
dados = control.lerItens()

# posicao_salva = control.carregar_posicao()

ancoras = [
   {
    "Nome": "Slot vazio",
    "Arquivo": "_ancora_slot_mkt.png"
   },
   {
    "Nome": "Menu 'Todos os itens'",
    "Arquivo": "_ancora_todos_itens.png"
   },
   {
    "Nome": "Cancelar",
    "Arquivo": "_ancora_cancelar.png"
   },
   {
    "Nome": "Avançar",
    "Arquivo": "_ancora_avancar.png"
   },
   {
    "Nome": "Fechar",
    "Arquivo": "_ancora_fechar.png"  
   },
   {
    "Nome": "Ok",
    "Arquivo": "_ancora_ok.png"
   },
   {
    "Nome": "Vender",
    "Arquivo": "_ancora_vender.png"
   },
   {
    "Nome": "Correio",
    "Arquivo": "_ancora_ouro_correio.png"
   },
   {
    "Nome": "Coletar",
    "Arquivo": "_ancora_para_bolsa.png"
   }

]

root = ThemedTk(theme='arc', themebg=True)
root.title("Warspear AutoMarket")
root.resizable(False, False)

# if posicao_salva:
#     root.geometry(posicao_salva)
# else:
root.geometry("+200+100")

try:
    root.iconbitmap(f"{constants.PATH_IMGS}__icon_ws_mkt.ico")
except (ValueError, Exception):
    pass

style = Style()
style.configure('TLabel')

def gerar_widget(widget, row, column, sticky="NSEW", columnspan=None, rowspan=None, **kwargs):
    my_widget = widget(**kwargs)
    my_widget.grid(row=row, column=column, padx = 5, pady =5, sticky=sticky, columnspan=columnspan, rowspan=rowspan)
    return my_widget

lbl_qnt = gerar_widget(Label, 1, 0, "W", text="Quantidade")
etr_qnt = gerar_widget(Entry, 1, 1,)

lbl_preco = gerar_widget(Label, 2, 0, "W", text="Preço")
etr_preco = gerar_widget(Entry, 2, 1)

cbn_licen = gerar_widget(Checkbutton, 3, 0, "W", text="Licença de mercado")

lbl_repeticoes = gerar_widget(Label, 3, 1, "W", text="Repetições")
etr_repeticoes = gerar_widget(Entry, 3, 1, "E", width = 10)
etr_repeticoes.delete(0, "end") 
etr_repeticoes.insert(0 , '15')

def runBot(myEvent, item, qnt, preco, repeticoes, licenca_mkt=False):
    for i in range(repeticoes):
        # print(f"{myEvent}  interface FORRUNBOT")
        if myEvent.is_set():
            # print("testandooooooooooo")
            return
        verif = True
        verif = actions.venderItens(myEvent, item, qnt, preco, licenca_mkt)
        if verif is None:
            return None

def run():
    myEvent.clear()
    preset = carregar()
    # print(f"{myEvent}  interface RUN")
    try:
        qnt = int(preset['qnt'])
    except ValueError:
        abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Quantidade'.", 4000)
        return
    try:
        preco = int(preset['preco'])
    except ValueError:
        abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Preço'.", 4000)
        return
    try:
        repeticoes = int(preset['repeticoes'])
    except ValueError:
        abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Repetições'.", 4000)
        return

    runBot(myEvent, preset['item'], preset['qnt'], preset['preco'], repeticoes, preset['licenca'])


def mantendoExecucao():
    myEvent.clear()
    horas_texto = etr_config_horas.get()
    try:
        horas_float = float(horas_texto)

        pausa = 1*60 ## 5 minutos

        start_time = time.time()
        while time.time() - start_time < horas_float * 3600:  
            if myEvent.is_set():
                return
            run()
            
            pg.sleep(pausa)
            print(f'{myEvent} mantendoExecucao aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    except ValueError:
        abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Horas'.", 4000)
    root.deiconify()

def manterExecucao():
    if not listener_running.is_set():
        listener_running.set()
    root.iconify()
    global executando_th
    executando_th = threading.Thread(target=mantendoExecucao)
    executando_th.start()

def abrir_messageBox(titulo, mensagem, tempo):
    root.after(tempo, fechar_messageBox)
    tempo = f"Fecha automaticamente em {int(tempo/1000)} segundos"
    msg = messagebox.showinfo(titulo,f"{mensagem}\n{tempo}")


def on_press(key):
    # if listener_running.is_set():
    if False: # on_press desativado
        try:
            if key == keyboard.Key.esc:
                root.deiconify()
                myEvent.set()
                listener_running.clear()
            if key.char == 'k':
                start()
            if key.char == 'l':
                myEvent.set()
            if key.char == 'o':
                manterExecucao()
                pass

            if key.char == 'p':
                actions.pegar_ouro_correio(myEvent)
                pass

            if key.char is not None:
                pass
            
        except AttributeError:
            pass
    else:
        pass

def on_release(key):
    # if not listener_running.is_set():
    #     return False  # Encerra o listener
    if listener_running.is_set():
        try:
            if key == keyboard.Key.esc:
                root.deiconify()
                myEvent.set()
                listener_running.clear()
                
                # return False
            if key.char == 'k':
                start()
            if key.char == 'l':
                #print(f"{myEvent}  interface L antes")
                myEvent.set()
                #print(f"{myEvent}  interface L depois")
                #group_thread.stop()
            if key.char == 'o':
                manterExecucao()
                pass

            if key.char == 'p':
                actions.pegar_ouro_correio(myEvent)
                #kb.press('k')
                pass

            if key.char is not None:
                pass
                #print(f'Letter pressed: {key.char}')
            
        except AttributeError:
            pass
            #print(f'Special key {key} pressed.')
    else:
        pass

def keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def start():
    if not listener_running.is_set():
        listener_running.set()
    root.iconify()
    global start_th


    start_th = threading.Thread(target=run)
    start_th.start()


def load_image(arquivo, x, y):
    caminho_completo = f'{constants.PATH_IMGS}{arquivo}'
    if os.path.exists(caminho_completo):
        load_image = Image.open(caminho_completo)
        resiz = load_image.resize((x, y))
        return ImageTk.PhotoImage(resiz)
    else:
        print(f"Arquivo '{caminho_completo}' não encontrado.")
        return None

btn_iniciar = gerar_widget(Button, 4, 0, "E", text="Iniciar",columnspan=2, width = 35, command=start)


def on_pressGambiarra(key):
    if key.char == 'f':
        # print("A tecla 'f' foi pressionada.")
        return False 

def gambiarraKeyboard():
    with keyboard.Listener(on_press=on_pressGambiarra) as listenerGambiarra:
        listenerGambiarra.join()
    time.sleep(1)

def fechar_messageBox():
    pg.press('enter')

def abrir_messageBox_pos():
    root.after(2000, fechar_messageBox)
    msg = messagebox.showinfo("Instruções", "Mova o mouse para o local e pressione a tecla 'f' para definir a posição.\n(Fecha automaticamente em 2 segundos)")

def exibirTutorial():
    pass

def exibirTutorialConst():
    pass

def setar_pos_licenca():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()
    constants.POSICAO_LICENSA_MKT = (posicao_mouse.x, posicao_mouse.y)
    atualizarConfigs()

def setar_pos_barra_grande_lateral():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()
    constants.POSICAO_BARRA_GRANDE_LATERAL = (posicao_mouse.x, posicao_mouse.y)
    atualizarConfigs()

def setar_pos_quantidade():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()
    constants.POSICAO_QUANTIDADE = (posicao_mouse.x, posicao_mouse.y)
    atualizarConfigs()

def setar_pos_preco():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()
    constants.POSICAO_PRECO = (posicao_mouse.x, posicao_mouse.y)
    atualizarConfigs()

def setar_area_itens():

    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()

    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse2 = pg.position()
    constants.AREA_ITENS = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)
    atualizarConfigs()

def setar_area_mercado():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()

    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse2 = pg.position()
    
    constants.AREA_MERCADO = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)
    atualizarConfigs()

def salvarConsts():
    control.salvarConstantes()

def refazerConsts():
    control.carregarConstantes()
    atualizarConfigs()

def resetarConsts():
    control.gerarConstantesPadroes()
    atualizarConfigs()


def on_entry_click_item(event):
    if etr_config_item_nome.get() == 'Nome do item':
        etr_config_item_nome.delete(0, "end")
        etr_config_item_nome.config(foreground='black')

def on_focus_out_item(event):
    if etr_config_item_nome.get() == '':
        etr_config_item_nome.insert(0, 'Nome do item')
        etr_config_item_nome.config(foreground='grey') 

def on_entry_click_arquivo(event):
    if etr_config_item_nome_arquivo.get() == 'Nome_do_arquivo.png':
        etr_config_item_nome_arquivo.delete(0, "end")
        etr_config_item_nome_arquivo.config(foreground='black')

def on_focus_out_arquivo(event):
    if etr_config_item_nome_arquivo.get() == '':
        etr_config_item_nome_arquivo.insert(0, 'Nome_do_arquivo.png')
        etr_config_item_nome_arquivo.config(foreground='grey') 



def excluirItemSelecionado():
    nome = etr_config_item_nome.get()
    for item in dados:
            if item["Nome"] == nome:
                if "Arquivo" in item:
                    nome_arquivo = item["Arquivo"]
                    if os.path.exists(f"{constants.PATH_IMGS}{nome_arquivo}"):
                        os.remove(f"{constants.PATH_IMGS}{nome_arquivo}")
                dados.remove(item)
    atualizarCbxValues()

def salvarItem():
    nome = etr_config_item_nome.get()
    arquivo = etr_config_item_nome_arquivo.get()
    novo_item = {"Nome": nome, "Arquivo": arquivo}

    verif = False
    for item in dados:
        if item["Nome"] == nome:
            item["Arquivo"] = arquivo
            verif = True
    
    if verif == False:
        dados.append(novo_item)

    atualizarCbxValues()



def printarItem():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()

    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse2 = pg.position()
    
    coords = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)

    
    img = pg.screenshot(region=coords)

    arquivo = etr_config_item_nome_arquivo.get()
    img.save(f'{constants.PATH_IMGS}{arquivo}')

    if cbn_config_item_gerar.instate(['!selected']):
        salvarItem()
        atualizarCbx(None)
    atualizarImg()
    

row_config = 6
row_config_itens = 2
row_config_constants = 9

lbl_config_avancadas = gerar_widget(Label, row_config, 0, "W", text="Configurações avançadas", columnspan=2)
# infogrid_lbl_config_avancadas = lbl_config_avancadas.grid_info()
# lbl_config_avancadas.grid_remove()

def desativar_listener():
    if listener_running.is_set():
        listener_running.clear()
        print("Os Atalhos foram desativados")
    else:
        listener_running.set()
        print("Os Atalhos foram ativados")

btn_desativar_listener = gerar_widget(Button, row_config, 1, "NSEW", text="Desativar/ativar atalhos",command=desativar_listener)
# infogrid_btn_desativar_listener = btn_desativar_listener.grid_info()
# btn_desativar_listener.grid_remove()


def on_entry_click_item_horas(event):
    if etr_config_horas.get() == 'Digite o tempo em horas':
        etr_config_horas.delete(0, "end")
        etr_config_horas.config(foreground='black')

def on_focus_out_item_horas(event):
    if etr_config_horas.get() == '':
        etr_config_horas.insert(0, 'Digite o tempo em horas')
        etr_config_horas.config(foreground='grey') 

etr_config_horas = gerar_widget(Entry, row_config+1, 0, "NSEW")
infogrid_etr_config_horas = etr_config_horas.grid_info()
etr_config_horas.grid_remove()
etr_config_horas.bind('<FocusIn>', on_entry_click_item_horas)
etr_config_horas.bind('<FocusOut>', on_focus_out_item_horas)
on_focus_out_item_horas(None)

btn_config_deixar_rodando = gerar_widget(Button, row_config+1, 1, "NSEW", text="Manter rodando", command=manterExecucao)
infogrid_btn_config_deixar_rodando = btn_config_deixar_rodando.grid_info()
btn_config_deixar_rodando.grid_remove()

lbl_config_itens = gerar_widget(Label, row_config+row_config_itens, 0, "", text="Configurar itens", columnspan=2)
infogrid_lbl_config_itens = lbl_config_itens.grid_info()
lbl_config_itens.grid_remove()

etr_config_item_nome = gerar_widget(Entry, row_config+row_config_itens+1, 0, "NSEW")
infogrid_etr_config_item_nome = etr_config_item_nome.grid_info()
etr_config_item_nome.grid_remove()
etr_config_item_nome.bind('<FocusIn>', on_entry_click_item)
etr_config_item_nome.bind('<FocusOut>', on_focus_out_item)
on_focus_out_item(None)


etr_config_item_nome_arquivo = gerar_widget(Entry, row_config+row_config_itens+2, 0, "NSEW")
infogrid_etr_config_item_nome_arquivo = etr_config_item_nome_arquivo.grid_info()
etr_config_item_nome_arquivo.grid_remove()
etr_config_item_nome_arquivo.bind('<FocusIn>', on_entry_click_arquivo)
etr_config_item_nome_arquivo.bind('<FocusOut>', on_focus_out_arquivo)
on_focus_out_arquivo(None)

btn_config_item_excluir = gerar_widget(Button, row_config+row_config_itens+3, 0, "W", text="Excluir", width = 8, command=excluirItemSelecionado)
infogrid_btn_config_item_excluir = btn_config_item_excluir.grid_info()
btn_config_item_excluir.grid_remove()

btn_config_item_salvar = gerar_widget(Button, row_config+row_config_itens+3, 0, "E", text="Adicionar", width = 8, command=salvarItem)
infogrid_btn_config_item_salvar = btn_config_item_salvar.grid_info()
btn_config_item_salvar.grid_remove()

img = load_image(dados[0]["Arquivo"], 50,50)
btn_config_img_item = gerar_widget(Button, row_config+row_config_itens+1, 1, "", rowspan=2, image=img, command=exibirTutorial)
infogrid_btn_config_img_item = btn_config_img_item.grid_info()
btn_config_img_item.grid_remove()

btn_config_item_printar = gerar_widget(Button, row_config+row_config_itens+3, 1, "E", text="Printar", width = 7, command=printarItem)
infogrid_btn_config_item_printar = btn_config_item_printar.grid_info()
btn_config_item_printar.grid_remove()

cbn_config_item_gerar = gerar_widget(Checkbutton, row_config+row_config_itens+3, 1, "W", text="Salvar\napenas\no arquivo")
infogrid_cbn_config_item_gerar = cbn_config_item_gerar.grid_info()
cbn_config_item_gerar.grid_remove()



lbl_config_consts = gerar_widget(Label, row_config+row_config_constants, 0, "", text="Constantes Ancoras e Coordenadas", columnspan=2)
infogrid_lbl_config_consts = lbl_config_consts.grid_info()
lbl_config_consts.grid_remove()


ancora_nomes = []
for ancora in ancoras:
    ancora_nomes.append(ancora["Nome"])

img = load_image("_ancora_slot_mkt.png", 50,50)
btn_config_img_ancora = gerar_widget(Button, row_config+row_config_constants+1, 1, "", rowspan=2, image=img, command=exibirTutorialConst)
infogrid_btn_config_img_ancora = btn_config_img_ancora.grid_info()
btn_config_img_ancora.grid_remove()

def atualizarImgAncora(item_selecionado):
    if ancoras:
        for dado in ancoras:
            if dado["Nome"] == item_selecionado:
                img = load_image(dado["Arquivo"], 100, 50)
                btn_config_img_ancora.config(image=img)
                btn_config_img_ancora.image = img

def atualizarCbxAcnora(event):
    item_selecionado = cbx_ancora.get()
    atualizarImgAncora(item_selecionado)
    cbx_ancora.selection_clear()
    return item_selecionado

cbx_ancora = gerar_widget(Combobox, row_config+row_config_constants+1, 0, "NSEW", values=ancora_nomes, state="readonly")
if constants.ITENS:
    cbx_ancora.current(0)
infogrid_cbx_ancora = cbx_ancora.grid_info()
cbx_ancora.grid_remove()
atualizarCbxAcnora(event=None)
cbx_ancora.bind("<<ComboboxSelected>>", atualizarCbxAcnora)

def printarAncora():
    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse = pg.position()

    abrir_messageBox_pos()
    gambiarraKeyboard()
    posicao_mouse2 = pg.position()

    coords = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)
    img = pg.screenshot(region=coords)

     
    nome = atualizarCbxAcnora(None)
    if ancoras:
        for dado in ancoras:
            if dado["Nome"] == nome:
                arquivo = dado["Arquivo"]
    img.save(f'{constants.PATH_IMGS}{arquivo}')
    atualizarCbxAcnora(None)

btn_ancora_printar = gerar_widget(Button, row_config+row_config_constants+2, 0, "NSEW", text="Printar e Salvar", command=printarAncora)
infogrid_btn_ancora_printar = btn_ancora_printar.grid_info()
btn_ancora_printar.grid_remove()

btn_setar_area_mercado = gerar_widget(Button, row_config+row_config_constants+4, 1, "E", text="Definir Posição", width = 13, command=setar_area_mercado)
infogrid_btn_setar_area_mercado = btn_setar_area_mercado.grid_info()
btn_setar_area_mercado.grid_remove()

lbl_area_mercado = gerar_widget(Label, row_config+row_config_constants+4, 0, "W", text=f"Mercado:       {constants.AREA_MERCADO}", columnspan=2)
infogrid_lbl_area_mercado = lbl_area_mercado.grid_info()
lbl_area_mercado.grid_remove()

btn_setar_pos_barra_grande_lateral = gerar_widget(Button, row_config+row_config_constants+5, 1, "E", text="Definir Posição", width = 13, command=setar_pos_barra_grande_lateral)
infogrid_btn_setar_pos_barra_grande_lateral = btn_setar_pos_barra_grande_lateral.grid_info()
btn_setar_pos_barra_grande_lateral.grid_remove()

lbl_pos_barra_grande_lateral = gerar_widget(Label, row_config+row_config_constants+5, 0, "W", text=f"Barra de rolagem:      {constants.POSICAO_BARRA_GRANDE_LATERAL}", columnspan=2)
infogrid_lbl_barra_grande_lateral = lbl_pos_barra_grande_lateral.grid_info()
lbl_pos_barra_grande_lateral.grid_remove()


btn_setar_area_itens = gerar_widget(Button, row_config+row_config_constants+6, 1, "E", text="Definir Posição", width = 13, command=setar_area_itens)
infogrid_btn_setar_area_itens = btn_setar_area_itens.grid_info()
btn_setar_area_itens.grid_remove()

lbl_area_itens = gerar_widget(Label, row_config+row_config_constants+6, 0, "W", text=f"Inventário:      {constants.AREA_ITENS}", columnspan=2)
infogrid_lbl_area_itens = lbl_area_itens.grid_info()
lbl_area_itens.grid_remove()



btn_setar_pos_quantidade = gerar_widget(Button, row_config+row_config_constants+7, 1, "E", text="Definir Posição", width = 13, command=setar_pos_quantidade)
infogrid_btn_setar_pos_quantidade = btn_setar_pos_quantidade.grid_info()
btn_setar_pos_quantidade.grid_remove()

lbl_pos_quantidade = gerar_widget(Label, row_config+row_config_constants+7, 0, "W", text=f"Quantidade:               {constants.POSICAO_QUANTIDADE}", columnspan=2)
infogrid_lbl_quantidade = lbl_pos_quantidade.grid_info()
lbl_pos_quantidade.grid_remove()

btn_setar_pos_preco = gerar_widget(Button, row_config+row_config_constants+8, 1, "E", text="Definir Posição", width = 13, command=setar_pos_preco)
infogrid_btn_setar_pos_preco = btn_setar_pos_preco.grid_info()
btn_setar_pos_preco.grid_remove()

lbl_pos_preco = gerar_widget(Label, row_config+row_config_constants+8, 0, "W", text=f"Preço:                         {constants.POSICAO_PRECO}", columnspan=2)
infogrid_lbl_preco = lbl_pos_preco.grid_info()
lbl_pos_preco.grid_remove()

btn_setar_pos_licenca = gerar_widget(Button, row_config+row_config_constants+9, 1, "E", text="Definir Posição", width = 13, command=setar_pos_licenca)
infogrid_btn_setar_pos_licenca = btn_setar_pos_licenca.grid_info()
btn_setar_pos_licenca.grid_remove()

lbl_pos_licenca = gerar_widget(Label, row_config+row_config_constants+9, 0, "W", text=f"Licença de merc:        {constants.POSICAO_LICENSA_MKT}", columnspan=2)
infogrid_lbl_pos_licenca = lbl_pos_licenca.grid_info()
lbl_pos_licenca.grid_remove()



btn_salvarConsts = gerar_widget(Button, row_config+row_config_constants+10, 1, "NSEW", text="Salvar Constantes", command=salvarConsts)
infogrid_btn_salvarConsts = btn_salvarConsts.grid_info()
btn_salvarConsts.grid_remove()

btn_refazerConsts = gerar_widget(Button, row_config+row_config_constants+10, 0, "E", text="Refazer", width=8, command=refazerConsts)
infogrid_btn_refazerConsts = btn_refazerConsts.grid_info()
btn_refazerConsts.grid_remove()

btn_resetarConsts = gerar_widget(Button, row_config+row_config_constants+10, 0, "W", text="Resetar", width=8, command=resetarConsts)
infogrid_btn_resetarConsts = btn_resetarConsts.grid_info()
btn_resetarConsts.grid_remove()

config_visible_th = threading.Event()

def atualizarConfigs():
    lbl_pos_barra_grande_lateral.config(text=f"Barra de rolagem:      {constants.POSICAO_BARRA_GRANDE_LATERAL}")
    lbl_pos_quantidade.config(text=f"Quantidade:               {constants.POSICAO_QUANTIDADE}")
    lbl_pos_preco.config(text=f"Preço:                         {constants.POSICAO_PRECO}")
    lbl_pos_licenca.config(text=f"Licença de merc:        {constants.POSICAO_LICENSA_MKT}")
    lbl_area_itens.config(text=f"Inventário:      {constants.AREA_ITENS}")
    lbl_area_mercado.config(text=f"Mercado:       {constants.AREA_MERCADO}")

def atualizarImg():
    item_selecionado = cbx_item.get()
    if dados:
        for dado in dados:
            if dado["Nome"] == item_selecionado:
                img = load_image(dado["Arquivo"], 50, 50)
                btn_config_img_item.config(image=img)
                btn_config_img_item.image = img

def config():
    if not config_visible_th.is_set():
        # lbl_config_avancadas.grid(infogrid_lbl_config_avancadas)
        etr_config_horas.grid(infogrid_etr_config_horas)       
        btn_config_deixar_rodando.grid(infogrid_btn_config_deixar_rodando)


        lbl_config_itens.grid(infogrid_lbl_config_itens)
        etr_config_item_nome.grid(infogrid_etr_config_item_nome)
        etr_config_item_nome_arquivo.grid(infogrid_etr_config_item_nome_arquivo)
        btn_config_item_excluir.grid(infogrid_btn_config_item_excluir)
        btn_config_item_salvar.grid(infogrid_btn_config_item_salvar)
        btn_config_img_item.grid(infogrid_btn_config_img_item)
        btn_config_item_printar.grid(infogrid_btn_config_item_printar)
        cbn_config_item_gerar.grid(infogrid_cbn_config_item_gerar)


        lbl_config_consts.grid(infogrid_lbl_config_consts)
        cbx_ancora.grid(infogrid_cbx_ancora)
        btn_config_img_ancora.grid(infogrid_btn_config_img_ancora)
        btn_ancora_printar.grid(infogrid_btn_ancora_printar)
        

        btn_setar_pos_licenca.grid(infogrid_btn_setar_pos_licenca)
        lbl_pos_licenca.grid(infogrid_lbl_pos_licenca)
        btn_setar_pos_barra_grande_lateral.grid(infogrid_btn_setar_pos_barra_grande_lateral)
        lbl_pos_barra_grande_lateral.grid(infogrid_lbl_barra_grande_lateral)
        btn_setar_pos_quantidade.grid(infogrid_btn_setar_pos_quantidade)
        lbl_pos_quantidade.grid(infogrid_lbl_quantidade)
        btn_setar_pos_preco.grid(infogrid_btn_setar_pos_preco)
        lbl_pos_preco.grid(infogrid_lbl_preco)
        btn_setar_area_itens.grid(infogrid_btn_setar_area_itens)
        lbl_area_itens.grid(infogrid_lbl_area_itens)
        btn_setar_area_mercado.grid(infogrid_btn_setar_area_mercado)
        lbl_area_mercado.grid(infogrid_lbl_area_mercado)

        btn_salvarConsts.grid(infogrid_btn_salvarConsts)
        btn_refazerConsts.grid(infogrid_btn_refazerConsts)
        btn_resetarConsts.grid(infogrid_btn_resetarConsts)
        

        # print(root.geometry())
        # root.geometry("+200+100")
        config_visible_th.set()
    else:
        # lbl_config_avancadas.grid_remove()
        etr_config_horas.grid_remove()
        btn_config_deixar_rodando.grid_remove()

        lbl_config_itens.grid_remove()
        etr_config_item_nome.grid_remove()
        etr_config_item_nome_arquivo.grid_remove()
        btn_config_item_excluir.grid_remove()
        btn_config_item_salvar.grid_remove()
        btn_config_img_item.grid_remove()
        btn_config_item_printar.grid_remove()
        cbn_config_item_gerar.grid_remove()




        lbl_config_consts.grid_remove()
        cbx_ancora.grid_remove()
        btn_config_img_ancora.grid_remove()
        btn_ancora_printar.grid_remove()


        btn_setar_pos_licenca.grid_remove()
        lbl_pos_licenca.grid_remove()
        btn_setar_pos_barra_grande_lateral.grid_remove()
        lbl_pos_barra_grande_lateral.grid_remove()
        btn_setar_pos_quantidade.grid_remove()
        lbl_pos_quantidade.grid_remove()
        btn_setar_pos_preco.grid_remove()
        lbl_pos_preco.grid_remove()
        btn_setar_area_itens.grid_remove()
        lbl_area_itens.grid_remove()
        btn_setar_area_mercado.grid_remove()
        lbl_area_mercado.grid_remove()

        btn_salvarConsts.grid_remove()
        btn_refazerConsts.grid_remove()
        btn_resetarConsts.grid_remove()

        # print(root.geometry())
        # root.geometry("+200+200")
        config_visible_th.clear()
    
icon = load_image('__icon_config.png', 20, 20)
btn_config = gerar_widget(Button, 4, 0, "W", width = 2, columnspan=2, command=config, image=icon)

def salvarDados():
    item_selecionado = cbx_item.get()
    if dados:
        for dado in dados:
            if dado["Nome"] == item_selecionado:
                qnt = etr_qnt.get()
                preco = etr_preco.get()
                licenca = cbn_licen.instate(['selected'])
                #arquivo = etr_config_item_nome_arquivo.get()
                dado["Quantidade"] = qnt
                dado["Preco"] = preco
                dado["Licenca"] = licenca
                #dado["Arquivo"] = arquivo
                control.alterarItem(
                    dado["Nome"],
                    novo_nome=dado["Nome"],
                    nova_quantidade=qnt,
                    novo_preco=preco,
                    #novo_arqNome=arquivo,
                    nova_licenca=licenca
                )

def atualizarCbx(event):
    item_selecionado = cbx_item.get()
    atualizarImg()
    etr_config_item_nome.delete(0, "end")
    etr_config_item_nome.insert(0, item_selecionado)

    if dados:
        for dado in dados:
            if dado["Nome"] == item_selecionado:
                etr_qnt.delete(0, "end")

                if "Quantidade" in dado:
                    valor_quantidade = str(dado["Quantidade"])
                    etr_qnt.insert(0, valor_quantidade)

                etr_preco.delete(0, "end")

                if "Preco" in dado:
                    valor_preco = str(dado["Preco"])
                    etr_preco.insert(0, valor_preco)

                if "Arquivo" in dado:
                    etr_config_item_nome_arquivo.delete(0, "end")
                    etr_config_item_nome_arquivo.insert(0, dado["Arquivo"])

                if "Licenca" in dado:
                    if dado["Licenca"]:
                        if cbn_licen.instate(['!selected']):
                            cbn_licen.invoke()
                    else:
                        if cbn_licen.instate(['selected']):
                            cbn_licen.invoke()
                cbx_item.selection_clear()
    return dados          

def salvarCbx(event):
    salvarDados() 

lbl_item = gerar_widget(Label, 0, 0, "W", text="Item")
cbx_item = gerar_widget(Combobox, 0, 1, "W", values=constants.ITENS, state="readonly")
if constants.ITENS:
    cbx_item.current(0)
atualizarCbx(event=None)
cbx_item.bind("<Button-1>", salvarCbx)
cbx_item.bind("<<ComboboxSelected>>", atualizarCbx)

def carregarDados():
    nomes = []
    for item in dados:
            nomes.append(item["Nome"])
    return nomes

def atualizarCbxValues():
    nomes = carregarDados()
    cbx_item["values"]=nomes

def carregar():
    if dados:
        for dado in dados:
            if dado["Nome"] == cbx_item.get():
                caminho = dado["Arquivo"]
    valores = {
        'item': caminho,
        'qnt': etr_qnt.get(),
        'preco': etr_preco.get(),
        'licenca': cbn_licen.instate(['selected']),
        'repeticoes': etr_repeticoes.get()
    }
    return valores

#btn_listener = gerar_widget(Button, 5, 0, "NSEW", text="Iniciar Listener", width = 20, command=prepararListener)
#btn_Salvar = gerar_widget(Button, 5, 1, "NSEW", text="Salvar", width = 20, command=salvar)

global myEvent
myEvent = threading.Event()
global listener_running
listener_running = threading.Event()
# listener_running.clear()
listener_running.set()
listener_th = threading.Thread(target=keyboard_listener, daemon=True)
listener_th.start()




def salvarItens():
    salvarDados()
    nome_elemento_desejado = cbx_item.get()
    indice_elemento = next((index for (index, d) in enumerate(dados) if d["Nome"] == nome_elemento_desejado), None)
    if indice_elemento is not None:
        elemento_movido = dados.pop(indice_elemento)
        dados.insert(0, elemento_movido)
    control.salvarItensNovaOrdem(dados)

iconSave = load_image('__icon_save.png', 15, 15)
btn_salvar = gerar_widget(Button, 0, 0, "E", width=3, command=salvarItens, image=iconSave)

def encerrar():
    salvarItens()
    listener_running.clear()

    # control.salvar_posicao(root.geometry())
    root.destroy()

root.protocol("WM_DELETE_WINDOW", encerrar)
root.mainloop()

