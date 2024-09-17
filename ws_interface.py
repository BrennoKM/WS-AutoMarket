import constantes
import acoes
import info
import entrada_saida as es
import ws_interface_config as wsc
import time
import tkinter as tk
import threading
import pyautogui as pg
from pynput import keyboard
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter.ttk import Label, Button, Checkbutton, Combobox, Entry, Style, Frame, Separator



class WS:
    def __init__(self):
        global listener_running
        listener_running = threading.Event()
        global myEvent
        myEvent = threading.Event()
        global presets
        presets = None
        es.inicio()

        self.rootws = ThemedTk(theme='arc', themebg=True)
        self.config()
        # self.frames()
        self.etr_quantidade = Entry(self.rootws)
        self.etr_quantidade.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "NSEW")
        self.etr_preco = Entry(self.rootws)
        self.etr_preco.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "NSEW")
        self.cbn_licenca = Checkbutton(self.rootws, text = "Licença")
        self.cbn_licenca.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "NSEW")
        self.cbn_preco_medio = Checkbutton(self.rootws, text = "Preço médio")
        self.cbn_preco_medio.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "NSE")
        
        self.etr_slots = Entry(self.rootws, width = 5)
        self.etr_slots.grid(row = 3, column = 0, padx=5, pady=5, sticky = "E")

        self.etr_horas = Entry(self.rootws, width = 5)
        self.etr_horas.grid(row = 9, column = 0, padx=5, pady=5, sticky = "W")  
        self.etr_minutos = Entry(self.rootws, width = 5)
        self.etr_minutos.grid(row = 10, column = 0, padx=5, pady=5, sticky = "W")
        self.etr_horas.insert(0, 48)
        self.etr_minutos.insert(0, 5)



        
        self.etr_config_item_nome = Entry(self.rootws, width=13)
        self.etr_config_item_nome.grid(row = 13, column = 0, padx = 5, pady=5, columnspan = 2, sticky="W")
        self.etr_config_item_nome.bind('<FocusIn>', self.on_entry_click_item)
        self.etr_config_item_nome.bind('<FocusOut>', self.on_focus_out_item)
        self.on_focus_out_item(None)

        self.etr_config_item_nome_arquivo = Entry(self.rootws, width=13)
        self.etr_config_item_nome_arquivo.grid(row = 14, column = 0, padx = 5, pady=5, columnspan = 2, sticky="W")
        self.etr_config_item_nome_arquivo.bind('<FocusIn>', self.on_entry_click_arquivo)
        self.etr_config_item_nome_arquivo.bind('<FocusOut>', self.on_focus_out_arquivo)
        self.on_focus_out_arquivo(None)

        self.lbl_img = Label(self.rootws, text="", width=8)
        self.lbl_img.grid(row = 13, column = 1, padx = 20, pady=5, rowspan=2, sticky="W")
        

        self.cbn_config_item_excluir = Button(self.rootws, text="Excluir", command=self.excluir_item_selecionado)
        self.cbn_config_item_excluir.grid(row = 15, column = 0, padx = 5, pady=5, sticky="W")
        self.cbn_config_item_salvar = Button(self.rootws, text="Salvar", width=8, command=self.salvar_item)
        self.cbn_config_item_salvar.grid(row = 15, column = 1, padx = 5, pady=5, sticky="W")

        self.cbn_config_item_gerar = Checkbutton(self.rootws, text="Criar item\ncom print")
        self.cbn_config_item_gerar.grid(row = 13, column = 1, padx = 5, pady=5, sticky="E", rowspan=2)
        self.cbn_config_item_gerar.invoke()

        self.cbn_config_item_printar = Button(self.rootws, text="Printar", width=8, command=self.printar_item)
        self.cbn_config_item_printar.grid(row = 15, column = 1, padx = 5, pady=5, sticky="E")

        listener_th = threading.Thread(target=self.listener, daemon=True)
        listener_th.start()
        self.ad_atalhos()
        self.widgets()


        

        self.rootws.protocol("WM_DELETE_WINDOW", self.encerrar)
        self.rootws.mainloop()

    def config(self):
        self.rootws.title("Warspear AutoMarket")
        self.rootws.resizable(False, False)
        posicao_salva = es.carregar_posicao()

        if posicao_salva:
            self.rootws.geometry(posicao_salva)
        else:
            self.rootws.geometry("+200+100")

        try:
            self.rootws.iconbitmap(f"{constantes.PATH_IMGS_ICON}icon_ws_mkt.ico")
        except (ValueError, Exception):
            pass


    def frames(self):
        self.frame_ws = Frame(self.rootws)#, bg = '#ffffff')
        self.frame_ws.place(relwidth = 1, relheight = 1, relx=0, rely=0)
        pass
        
    def widgets(self):
        
        
        self.lbl_item = Label(self.rootws, text = "Item")
        self.lbl_item.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "W")

        itens = es.carregar_itens_nomes()
        self.cbx_itens = Combobox(self.rootws, state="readonly", values = itens)
        self.cbx_itens.grid(row = 0, column = 1, padx = 5, pady = 5)
        if itens:
            self.cbx_itens.current(0)
        self.atualizar_cbx(event=None)
        self.cbx_itens.bind("<Button-1>", self.salvar_cbx)
        self.cbx_itens.bind("<<ComboboxSelected>>", self.atualizar_cbx)

        self.lbl_quantidade = Label(self.rootws, text = "Quantidade")
        self.lbl_quantidade.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "W")

        # self.etr_quantidade = Entry(self.rootws)
        # self.etr_quantidade.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "NSEW")
        
        self.lbl_preco = Label(self.rootws, text = "Preço")
        self.lbl_preco.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "W")

        # self.etr_preco = Entry(self.rootws)
        # self.etr_preco.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "NSEW")

        self.lbl_slots = Label(self.rootws, text = "Slots")
        self.lbl_slots.grid(row = 3, column = 0, padx=5, pady=5, sticky = "W")

        

        # self.cbn_licenca = Checkbutton(self.rootws, text = "Licença de mercado")
        # self.cbn_licenca.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "NSEW")

        self.btn_atalhos = Button(self.rootws, text = "Ativar/Desativar Atalhos", command = self.ad_atalhos)
        self.btn_atalhos.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "NSEW", columnspan = 2)
        
        self.btn_config_img = es.load_image(f'{constantes.PATH_IMGS_ICON}icon_config.png', 20, 20)
        self.btn_config = Button(self.rootws, image=self.btn_config_img, command = self.abrir_configs, width=3)
        self.btn_config.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "NSW")
    
        self.btn_save_img = es.load_image(f'{constantes.PATH_IMGS_ICON}icon_save.png', 25, 20)
        self.btn_save = Button(self.rootws, image=self.btn_save_img, command = self.salvar_estado, width=3)
        self.btn_save.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "NSE")
    
        self.btn_iniciar = Button(self.rootws, command = self.iniciar, text = "Iniciar")
        self.btn_iniciar.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = "NSEW")

        style = Style()
        style.configure("TSeparator", background="#CFD6E6")

        self.spt_modo = Separator(self.rootws, orient="vertical", style="TSeparator")
        self.spt_modo.grid(row = 7, column = 0, padx = 5, pady=5, columnspan = 2, sticky="NSEW")

        self.lbl_modo_continuo = Label(self.rootws, text = "Modo contínuo por")
        self.lbl_modo_continuo.grid(row = 8, column = 0, padx = 5, pady=5, columnspan = 2, sticky="W")

        self.lbl_horas = Label(self.rootws, text = "Tempo em horas")
        self.lbl_horas.grid(row = 9, column = 0, padx=60, pady=5, sticky = "W", columnspan=2)

        self.lbl_minutos = Label(self.rootws, text = "Intervalo em minutos")
        self.lbl_minutos.grid(row = 10, column = 0, padx=60, pady=5, sticky = "W", columnspan = 2)
        

        self.btn_iniciar_continuo = Button(self.rootws, command = self.iniciar_continuo, text = "Iniciar", width = 6)
        self.btn_iniciar_continuo.grid(row = 10, column = 1, padx = 5, pady = 5, sticky = "E")


        self.spt_itens = Separator(self.rootws, orient="vertical", style="TSeparator")
        self.spt_itens.grid(row = 11, column = 0, padx = 5, pady=5, columnspan = 2, sticky="NSEW")


        self.lbl_config_itens = Label(self.rootws, text = "Configurar item")
        self.lbl_config_itens.grid(row = 12, column = 0, padx = 5, pady=5, columnspan = 2, sticky="W")


    def excluir_item_selecionado(self):
        nome = self.etr_config_item_nome.get()
        dados = es.carregar_itens()
        for item in dados:
                if item["Nome"] == nome:
                    if "Arquivo" in item:
                        nome_arquivo = item["Arquivo"]
                        es.deletar_item(f"{constantes.PATH_IMGS_ITENS}{nome_arquivo}")
                    dados.remove(item)
                    es.salvar_itens_novos(dados)
        self.atualizar_cbx_values()
    
    def salvar_item(self):
        nome = self.etr_config_item_nome.get()
        arquivo = self.etr_config_item_nome_arquivo.get()
        novo_item = {"Nome": nome, "Arquivo": arquivo}

        verif = False
        dados = es.carregar_itens()
        for item in dados:
            if item["Nome"] == nome:
                item["Arquivo"] = arquivo
                verif = True
        
        if verif == False:
            dados.append(novo_item)

        es.salvar_itens_novos(dados)
        self.atualizar_cbx_values()
        self.atualizar_cbx(None)
        self.cbx_itens.set(nome)

    def printar_item(self):
        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse = pg.position()

        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse2 = pg.position()
        
        coords = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)

        
        img = pg.screenshot(region=coords)

        arquivo = self.etr_config_item_nome_arquivo.get()

        if not es.existe_diretorio(constantes.PATH_IMGS_ITENS):
            es.criar_diretorio(constantes.PATH_IMGS_ITENS)
        img.save(f'{constantes.PATH_IMGS_ITENS}{arquivo}')

        if self.cbn_config_item_gerar.instate(['selected']):
            self.salvar_item()
            self.atualizar_cbx(None)
        self.atualizar_img()

    def atualizar_img(self):
        item_selecionado = self.cbx_itens.get()
        dados = es.carregar_itens()
        if dados:
            for dado in dados:
                if dado["Nome"] == item_selecionado:
                    img = es.load_image(dado["Arquivo"], 50, 50)
                    # img = es.load_image(f'{constantes.PATH_IMGS_ITENS}{dado["Arquivo"]}', 50, 50)
                    self.lbl_img.config(image=img)

    def on_press_print(self, key):
        if key.char == 'f':
            return False 

    def keyboard_print(self):
        with keyboard.Listener(on_press=self.on_press_print) as listener_print:
            listener_print.join()
        time.sleep(1)



    def on_entry_click_item(self, event):
        if self.etr_config_item_nome.get() == 'Nome do item':
            self.etr_config_item_nome.delete(0, "end")
            self.etr_config_item_nome.config(foreground='black')

    def on_focus_out_item(self, event):
        if self.etr_config_item_nome.get() == '':
            self.etr_config_item_nome.insert(0, 'Nome do item')
            self.etr_config_item_nome.config(foreground='grey') 

    def on_entry_click_arquivo(self, event):
        if self.etr_config_item_nome_arquivo.get() == 'Arquivo.png':
            self.etr_config_item_nome_arquivo.delete(0, "end")
            self.etr_config_item_nome_arquivo.config(foreground='black')

    def on_focus_out_arquivo(self, event):
        if self.etr_config_item_nome_arquivo.get() == '':
            self.etr_config_item_nome_arquivo.insert(0, 'Arquivo.png')
            self.etr_config_item_nome_arquivo.config(foreground='grey') 

    def atualizar_cbx_values(self):
        nomes = es.carregar_itens_nomes()
        self.cbx_itens["values"]=nomes

    def salvar_cbx(self, event):
        item_selecionado = self.cbx_itens.get()
        dados = es.carregar_itens()
        if dados:
            for dado in dados:
                if dado["Nome"] == item_selecionado:
                    qnt = self.etr_quantidade.get()
                    preco = self.etr_preco.get()
                    licenca = self.cbn_licenca.instate(['selected'])
                    slots = self.etr_slots.get()
                    arquivo = self.etr_config_item_nome_arquivo.get()
                    precoMedio = self.cbn_preco_medio.instate(['selected'])
                    dado["Quantidade"] = qnt
                    dado["Preco"] = preco
                    dado["Licenca"] = licenca
                    dado["Slots"] = slots
                    dado["Arquivo"] = arquivo
                    dado["PrecoMedio"] = precoMedio
                    es.alterarItem(
                        dado["Nome"],
                        novo_nome=dado["Nome"],
                        nova_quantidade=qnt,
                        novo_preco=preco,
                        novo_arqNome=arquivo,
                        nova_licenca=licenca,
                        novo_slots = slots,
                        novo_precoMedio = precoMedio
                    )
                    es.salvar_itens_novos(dados)
        
    def atualizar_cbx(self, event):
        item_selecionado = self.cbx_itens.get()
        dados = es.carregar_itens()

        self.etr_config_item_nome.delete(0, "end")
        self.etr_config_item_nome.insert(0, item_selecionado)
        if dados:
            for dado in dados:
                if dado["Nome"] == item_selecionado:
                    self.etr_quantidade.delete(0, "end")

                    if "Quantidade" in dado:
                        valor_quantidade = str(dado["Quantidade"])
                        self.etr_quantidade.insert(0, valor_quantidade)

                    self.etr_preco.delete(0, "end")

                    if "Preco" in dado:
                        valor_preco = str(dado["Preco"])
                        self.etr_preco.insert(0, valor_preco)
                    
                    self.etr_slots.delete(0, "end")

                    if "Slots" in dado:
                        slots = str(dado["Slots"])
                        self.etr_slots.insert(0, slots)

                    if "Arquivo" in dado:
                        self.etr_config_item_nome_arquivo.delete(0, "end")
                        self.etr_config_item_nome_arquivo.insert(0, dado["Arquivo"])

                        # info.printinfo(f'{constantes.PATH_IMGS_ITENS}{dado["Arquivo"]}')
                        self.img = es.load_image(f'{constantes.PATH_IMGS_ITENS}{dado["Arquivo"]}', 60, 60)
                        self.lbl_img.config(image=self.img)

                    if "Licenca" in dado:
                        if dado["Licenca"]:
                            if self.cbn_licenca.instate(['!selected']):
                                self.cbn_licenca.invoke()
                        else:
                            if self.cbn_licenca.instate(['selected']):
                                self.cbn_licenca.invoke()

                    if "PrecoMedio" in dado:
                        if dado["PrecoMedio"]:
                            if self.cbn_preco_medio.instate(['!selected']):
                                self.cbn_preco_medio.invoke()
                        else:
                            if self.cbn_preco_medio.instate(['selected']):
                                self.cbn_preco_medio.invoke()
                    self.cbx_itens.selection_clear()
        return dados   
    def on_release(self, key):
    # if not listener_running.is_set():
    #     return False  # Encerra o listener
        try:
            if key == keyboard.Key.ctrl_r:
                self.ad_atalhos()
                # return False
            
            if listener_running.is_set():
                
                if key == keyboard.Key.esc:
                    info.printinfo("Bot encerrado, mostrando a interface")
                    self.rootws.deiconify()
                    myEvent.set()
                    listener_running.clear()
                    info.printinfo("Os Atalhos foram desativados (Ctrl_r para ativar/deativar)", erro=True)
                if key.char == 'k':
                    info.printinfo("Iniciando o bot")
                    self.iniciar()
                if key.char == 'l':
                    #print(f"{myEvent}  interface L antes")
                    info.printinfo("Pausando o bot")
                    myEvent.set()
                    #print(f"{myEvent}  interface L depois")
                    #group_thread.stop()
                if key.char == 'o':
                    self.iniciar_continuo()
                    pass

                if key.char == 'p':
                    self.coletar_ouro()
                    #kb.press('k')
                    pass
                
                if key.char == 'n':
                    self.adicionar_preset()
                    pass
                if key.char == 'b':
                    self.resetar_preset()
                    pass
                if key.char == 'v':
                    acoes.contar_itens(myEvent, 'bau_prima.png')
                    pass
                if key.char is not None:
                    pass
                    #print(f'Letter pressed: {key.char}')
            
            else:
                pass  
        except AttributeError:
                pass
                #print(f'Special key {key} pressed.')
          
    
    def listener(self):
        with keyboard.Listener(on_release=self.on_release) as listener:
            listener.join()
        
    def ad_atalhos(self):
        if listener_running.is_set():
            listener_running.clear()
            info.printinfo("Os Atalhos foram desativados (Ctrl_r para ativar/deativar)", erro=True)
        else:
            listener_running.set()
            info.printinfo("Os Atalhos foram ativados (Ctrl_r para ativar/deativar)")
        
    def abrir_configs(self):
        config_window = tk.Toplevel(self.rootws)
        config_app = wsc.WS_Config(config_window)
        # config_app.style = Style()
        # config_app.style.theme_use(self.rootws.style.theme_get())

    def salvar_estado(self):
        self.salvar_itens()


    def carregar_preset(self, rep: bool = True):
        preset = self.carregar()
        # print(f"{myEvent}  interface RUN")
        preco_medio = self.cbn_preco_medio.instate(['selected'])
        try:
            qnt = int(preset['qnt'])
        except ValueError:
            self.abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Quantidade'.", 4000)
            return
        try:
            preco = int(preset['preco'])
        except ValueError:
            self.abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Preço'.", 4000)
            return
        try:
            repeticoes = int(preset['slots'])
        except ValueError:
            self.abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Repetições'.", 4000)
            return
        if rep is True:
            return (myEvent, preset['item'], preset['qnt'], preset['preco'], repeticoes, preset['licenca'], preco_medio)
        else:
            return (myEvent, preset['item'], preset['qnt'], preset['preco'], preset['licenca'], preco_medio)
        
    def adicionar_preset(self):
        global presets
        if presets is not None:
            presets = presets + [self.carregar_preset(rep=False)]
            info.printinfo(presets)
        else:
            presets = [self.carregar_preset(rep=False)]
            info.printinfo(presets)

    def resetar_preset(self):
        global presets
        presets = [self.carregar_preset(rep=False)]
        info.printinfo(presets)

    def runBot(self, myEvent, item, qnt, preco, repeticoes, licenca_mkt=False, preco_medio=False):
        global presets
        if presets is not None and len(presets) > 1:
            for i in range(repeticoes):
                item_faltando = None
                menor_qnt = 99
                for p in presets:
                    if myEvent.is_set():
                        return
                    p = list(p)
                    # print(f'{p[1]}')
                    qnt = acoes.contar_itens(myEvent, p[1])
                    # print(qnt)
                    p = tuple(p)
                    
                    if qnt < menor_qnt:
                        menor_qnt = qnt
                        item_faltando = p
                self.rodar(myEvent, 1, item_faltando)
        else:
            preset = (myEvent, item, qnt, preco, licenca_mkt, preco_medio)
            presets = [preset]
            self.rodar(myEvent, repeticoes, presets[0])

    def rodar(self, myEvent, repeticoes, preset):
        for i in range(repeticoes):
            # print(f"{myEvent}  interface FORRUNBOT")
            if myEvent.is_set():
                # print("testandooooooooooo")
                return
            verif = True
            verif = acoes.vender_itens(*preset)
            if verif is None:
                return None

    def run(self):
        myEvent.clear()
        self.runBot(*self.carregar_preset())

    def fechar_messageBox(self):
        pg.press('enter')

    def abrir_messageBox(self, titulo, mensagem, tempo):
        self.rootws.after(tempo, self.fechar_messageBox)
        tempo = f"Fecha automaticamente em {int(tempo/1000)} segundos"
        msg = messagebox.showinfo(titulo,f"{mensagem}\n{tempo}")

    def abrir_messageBox_pos(self):
        self.rootws.after(2000, self.fechar_messageBox)
        msg = messagebox.showinfo("Instruções", "Mova o mouse para o local e pressione a tecla 'f' para definir a posição.\n(Fecha automaticamente em 2 segundos)")


    def carregar(self):
        dados = es.carregar_itens()
        if dados:
            for dado in dados:
                if dado["Nome"] == self.cbx_itens.get():
                    caminho = dado["Arquivo"]
        valores = {
            'item': caminho,
            'qnt': self.etr_quantidade.get(),
            'preco': self.etr_preco.get(),
            'licenca': self.cbn_licenca.instate(['selected']),
            'slots': self.etr_slots.get()
        }
        return valores

    def pegando_ouro(self):
        myEvent.clear()
        while not myEvent.is_set():
            acoes.pegar_ouro_correio(myEvent)

    def coletar_ouro(self):
        ouro_th = threading.Thread(target=self.pegando_ouro)
        ouro_th.start()    

    def iniciar(self):
        if not listener_running.is_set():
            listener_running.set()
        self.rootws.iconify()
        global start_th
        start_th = threading.Thread(target=self.run)
        start_th.start()

    def exec_continua(self):
        myEvent.clear()
        horas_texto = self.etr_horas.get()
        minutos_intervalo = self.etr_minutos.get()
        try:
            horas_float = float(horas_texto)
            minutos_float = float(minutos_intervalo)
            pausa = minutos_float*60  ## minutos

            start_time = time.time()
            while time.time() - start_time < horas_float * 3600:  
                if myEvent.is_set():
                    return
                self.run()
                tempo_decorrido = time.time() - start_time
                tempo_restante = (horas_float * 3600) - tempo_decorrido

                # Convertendo o tempo restante para horas
                horas_restantes = tempo_restante // 3600
                minutos_restantes = (tempo_restante % 3600) // 60
                segundos_restantes = tempo_restante % 60

                info.printinfo(f"Mantendo execução: {int(horas_restantes)}h {int(minutos_restantes)}m {int(segundos_restantes)}s restantes")
                for i in range(int(pausa)//2):
                    if myEvent.is_set():
                        info.printinfo("Cancelando execução")
                        return
                    ##info.printinfo("Sleep")
                    pg.sleep(2)
                    ##pg.sleep(pausa)
                # print(f'{myEvent} mantendoExecucao aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

        except ValueError:
            self.abrir_messageBox("Aviso", "Valor númerico inválido na variável 'Horas' ou 'Intervalo em Minutos'.", 4000)
        self.rootws.deiconify()

    def iniciar_continuo(self):
        if not listener_running.is_set():
            listener_running.set()
        self.rootws.iconify()
        global executando_th
        executando_th = threading.Thread(target=self.exec_continua)
        executando_th.start()

    def salvar_itens(self):
        self.salvar_cbx(None)
        dados = es.carregar_itens()
        nome_elemento_desejado = self.cbx_itens.get()
        indice_elemento = next((index for (index, d) in enumerate(dados) if d["Nome"] == nome_elemento_desejado), None)
        if indice_elemento is not None:
            elemento_movido = dados.pop(indice_elemento)
            dados.insert(0, elemento_movido)
        es.salvar_itens_novos(dados)   
    
    def encerrar(self):
        self.salvar_itens()
        listener_running.clear()
        myEvent.set()

        info.salvar_log()
        es.salvar_posicao(self.rootws.geometry(), "Posicao_na_tela")
        self.rootws.destroy()
    
if __name__ == "__main__":
    
    meu_bot = WS()