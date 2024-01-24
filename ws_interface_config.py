import constantes
import entrada_saida as es
import pyautogui as pg
from pynput import keyboard
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter.ttk import Label, Button, Checkbutton, Combobox, Entry, Style, Frame, Separator



class WS_Config:
    def __init__(self, root):
        self.rootwsconfig = root
        # self.rootwsconfig = ThemedTk(theme='arc', themebg=True)
        self.config()
        # self.frames()
        es.carregar_constantes()
        self.ancoras = [
                {
                    "Nome": "Slot vazio",
                    "Arquivo": "ancora_slot_mkt.png"
                },
                {
                    "Nome": "Menu 'Todos os itens'",
                    "Arquivo": "ancora_todos_itens.png"
                },
                {
                    "Nome": "Cancelar",
                    "Arquivo": "ancora_cancelar.png"
                },
                {
                    "Nome": "Avançar",
                    "Arquivo": "ancora_avancar.png"
                },
                {
                    "Nome": "Fechar",
                    "Arquivo": "ancora_fechar.png"  
                },
                {
                    "Nome": "Ok",
                    "Arquivo": "ancora_ok.png"
                },
                {
                    "Nome": "Vender",
                    "Arquivo": "ancora_vender.png"
                },
                {
                    "Nome": "Correio",
                    "Arquivo": "ancora_ouro_correio.png"
                },
                {
                    "Nome": "Coletar",
                    "Arquivo": "ancora_para_bolsa.png"
                }
            ]
        
        
        self.lbl_ancora_img = Label(self.rootwsconfig)
        self.lbl_ancora_img.grid(row = 1, column = 2, padx = 5, pady=5, rowspan=2, sticky="W")

        self.lbl_area_mercado_const = Label(self.rootwsconfig, text=f"{constantes.AREA_MERCADO}")
        self.lbl_area_mercado_const.grid(row=5, column=0, padx=5, pady=5, columnspan=2, sticky="E")

        self.lbl_pos_barra_grande_lateral_const = Label(self.rootwsconfig, text=f"{constantes.POSICAO_BARRA_GRANDE_LATERAL}")
        self.lbl_pos_barra_grande_lateral_const.grid(row=6, column=0, padx=5, pady=5, columnspan=2, sticky="E")

        self.lbl_area_inventario_const = Label(self.rootwsconfig, text=f"{constantes.AREA_ITENS}")
        self.lbl_area_inventario_const.grid(row=7, column=0, padx=5, pady=5, columnspan=2, sticky="E")

        self.lbl_pos_quantidade_const = Label(self.rootwsconfig, text=f"{constantes.POSICAO_QUANTIDADE}")
        self.lbl_pos_quantidade_const.grid(row=8, column=0, padx=5, pady=5, columnspan=2, sticky="E")

        self.lbl_pos_preco_const = Label(self.rootwsconfig, text=f"{constantes.POSICAO_PRECO}")
        self.lbl_pos_preco_const.grid(row=9, column=0, padx=5, pady=5, columnspan=2, sticky="E")

        self.lbl_pos_licenca_const = Label(self.rootwsconfig, text=f"{constantes.POSICAO_LICENSA_MKT}")
        self.lbl_pos_licenca_const.grid(row=10, column=0, padx=5, pady=5, columnspan=2, sticky="E")


        self.widgets()
        self.rootwsconfig.protocol("WM_DELETE_WINDOW", self.encerrar)
        self.rootwsconfig.mainloop()

    def config(self):
        self.rootwsconfig.title("Warspear AutoMarket")
        self.rootwsconfig.resizable(False, False)
        # self.rootwsconfig.theme(ThemedTk)
        # self.rootwsconfig.configure(theme='arc', themebg=True)
        posicao_salva = es.carregar_posicao_config()

        if posicao_salva:
            self.rootwsconfig.geometry(posicao_salva)
        else:
            self.rootwsconfig.geometry("+200+100")

        try:
            self.rootwsconfig.iconbitmap(f"{constantes.PATH_IMGS_ICON}icon_ws_mkt.ico")
        except (ValueError, Exception):
            pass
        
        
        # themed_root = ThemedTk(theme='arc', themebg=True)
        # self.rootwsconfig.tk_setPalette(**themed_root.tk_setPalette())
        # ThemedTk(theme='arc', themebg=True, master=self.rootwsconfig)
    def frames(self):
        self.frame_ws = Frame(self.rootwsconfig)
        self.frame_ws.place(relwidth=1, relheight=1, relx=0, rely=0)

    def widgets(self):
        self.lbl_config_ancoras = Label(self.rootwsconfig, text="Configuração de Ancoras")
        self.lbl_config_ancoras.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

        ancora_nomes = []
        for ancora in self.ancoras:
            ancora_nomes.append(ancora["Nome"])

        self.cbx_ancoras = Combobox(self.rootwsconfig, values=ancora_nomes, state="readonly")
        self.cbx_ancoras.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="NSEW")
        self.cbx_ancoras.current(0)
        self.atualizar_cbx_ancora(event=None)
        self.cbx_ancoras.bind("<<ComboboxSelected>>", self.atualizar_cbx_ancora)

        self.btn_ancoras_printar = Button(self.rootwsconfig, text="Printar e Salvar", command=self.printar_ancora, width=30)
        self.btn_ancoras_printar.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="NSEW")

        style = Style()
        style.configure("TSeparator", background="#CFD6E6")

        self.spt_coords = Separator(self.rootwsconfig, orient="vertical", style="TSeparator")
        self.spt_coords.grid(row = 3, column = 0, padx = 5, pady=5, columnspan = 3, sticky="NSEW")

        self.lbl_config_coords = Label(self.rootwsconfig, text="Configuração de Coordenadas")
        self.lbl_config_coords.grid(row=4, column=0, padx=5, pady=5, columnspan=3, sticky="")




        self.lbl_area_mercado = Label(self.rootwsconfig, text="Mercado:")
        self.lbl_area_mercado.grid(row=5, column=0, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_area_mercado = Button(self.rootwsconfig, text="Definir Posição", command=lambda: self.setar_area("AREA_MERCADO"))
        self.btn_area_mercado.grid(row=5, column=2, padx=5, pady=5, columnspan=1, sticky="W")




        self.lbl_pos_barra_grande_lateral = Label(self.rootwsconfig, text="Barra de rolagem:")
        self.lbl_pos_barra_grande_lateral.grid(row=6, column=0, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_pos_barra_grande_lateral = Button(self.rootwsconfig, text="Definir Posição", command=lambda: self.setar_pos("POSICAO_BARRA_GRANDE_LATERAL"))
        self.btn_pos_barra_grande_lateral.grid(row=6, column=2, padx=5, pady=5, columnspan=1, sticky="W")


        self.lbl_area_inventario = Label(self.rootwsconfig, text="Inventário:")
        self.lbl_area_inventario.grid(row=7, column=0, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_area_inventario = Button(self.rootwsconfig, text="Definir Posição", command=lambda: self.setar_area("AREA_ITENS"))
        self.btn_area_inventario.grid(row=7, column=2, padx=5, pady=5, columnspan=1, sticky="W")


        self.lbl_pos_quantidade = Label(self.rootwsconfig, text="Quantidade:")
        self.lbl_pos_quantidade.grid(row=8, column=0, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_pos_quantidade = Button(self.rootwsconfig, text="Definir Posição", command=lambda: self.setar_pos("POSICAO_QUANTIDADE"))
        self.btn_pos_quantidade.grid(row=8, column=2, padx=5, pady=5, columnspan=1, sticky="W")

        self.lbl_pos_preco = Label(self.rootwsconfig, text="Preço:")
        self.lbl_pos_preco.grid(row=9, column=0, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_pos_preco = Button(self.rootwsconfig, text="Definir Posição", command=lambda: self.setar_pos("POSICAO_PRECO"))
        self.btn_pos_preco.grid(row=9, column=2, padx=5, pady=5, columnspan=1, sticky="W")

        self.lbl_pos_licenca = Label(self.rootwsconfig, text="Licença de merc:")
        self.lbl_pos_licenca.grid(row=10, column=0, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_pos_licenca = Button(self.rootwsconfig, text="Definir Posição", command=lambda: self.setar_pos("POSICAO_LICENSA_MKT"))
        self.btn_pos_licenca.grid(row=10, column=2, padx=5, pady=5, columnspan=1, sticky="W")

        self.btn_resetar = Button(self.rootwsconfig, text="Resetar", command=self.resetar)
        self.btn_resetar.grid(row=11, column=0, padx=5, pady=5, columnspan=1, sticky="NSEW")    

        self.btn_refazer = Button(self.rootwsconfig, text="Refazer", command=self.refazer)
        self.btn_refazer.grid(row=11, column=1, padx=5, pady=5, columnspan=1, sticky="NSEW")

        self.btn_salvar = Button(self.rootwsconfig, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=11, column=2, padx=5, pady=5, columnspan=1, sticky="NSEW")

    def salvar(self):
        es.salvar_constantes()

    def refazer(self):
        es.carregar_constantes()
        self.atualizar_configs()

    def resetar(self):
        es.gerar_constantes_padroes()
        self.atualizar_configs()

    def fechar_messageBox(self):
        pg.press('enter')

    def abrir_messageBox_pos(self):
        self.rootwsconfig.after(2000, self.fechar_messageBox)
        msg = messagebox.showinfo("Instruções", "Mova o mouse para o local e pressione a tecla 'f' para definir a posição.\n(Fecha automaticamente em 2 segundos)")

    def setar_area(self, const):
        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse = pg.position()

        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse2 = pg.position()

        coords = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)
        
        if const == "AREA_MERCADO":
            constantes.AREA_MERCADO = coords
        else:
            constantes.AREA_ITENS = coords
        self.atualizar_configs()

    def setar_pos(self, const):
        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse = pg.position()

        if const == "POSICAO_BARRA_GRANDE_LATERAL":
            constantes.POSICAO_BARRA_GRANDE_LATERAL = (posicao_mouse.x, posicao_mouse.y)
        elif const == "POSICAO_QUANTIDADE":
            constantes.POSICAO_QUANTIDADE = (posicao_mouse.x, posicao_mouse.y)
        elif const == "POSICAO_PRECO":
            constantes.POSICAO_PRECO = (posicao_mouse.x, posicao_mouse.y)
        elif const == "POSICAO_LICENSA_MKT":
            constantes.POSICAO_LICENSA_MKT = (posicao_mouse.x, posicao_mouse.y)


        self.atualizar_configs()

    def atualizar_configs(self):
        self.lbl_area_mercado_const.config(text=f"{constantes.AREA_MERCADO}")
        self.lbl_pos_barra_grande_lateral_const.config(text=f"{constantes.POSICAO_BARRA_GRANDE_LATERAL}")
        self.lbl_area_inventario_const.config(text=f"{constantes.AREA_ITENS}")
        self.lbl_pos_quantidade_const.config(text=f"{constantes.POSICAO_QUANTIDADE}")
        self.lbl_pos_preco_const.config(text=f"{constantes.POSICAO_PRECO}")
        self.lbl_pos_licenca_const.config(text=f"{constantes.POSICAO_LICENSA_MKT}")

    def printar_ancora(self):
        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse = pg.position()

        self.abrir_messageBox_pos()
        self.keyboard_print()
        posicao_mouse2 = pg.position()
        
        coords = (posicao_mouse.x, posicao_mouse.y, posicao_mouse2.x-posicao_mouse.x, posicao_mouse2.y-posicao_mouse.y)

        
        img = pg.screenshot(region=coords)

        
        nome = self.atualizar_cbx_ancora(None)
        if self.ancoras:
            for dado in self.ancoras:
                if dado["Nome"] == nome:
                    arquivo = dado["Arquivo"]

        if not es.existe_diretorio(constantes.PATH_IMGS_ANCORAS):
            es.criar_diretorio(constantes.PATH_IMGS_ANCORAS)
        img.save(f'{constantes.PATH_IMGS_ANCORAS}{arquivo}')
        self.atualizar_cbx_ancora(None)   


    def on_press_print(self, key):
        if key.char == 'f':
            return False 

    def keyboard_print(self):
        with keyboard.Listener(on_press=self.on_press_print) as listener_print:
            listener_print.join()
        pg.sleep(1)

    def atualizar_cbx_ancora(self, event):
        item_selecionado = self.cbx_ancoras.get()
        self.atualizar_img_ancora()
        self.cbx_ancoras.selection_clear()
        return item_selecionado
    
    def atualizar_img_ancora(self):
        item_selecionado = self.cbx_ancoras.get()
        if self.ancoras:
            for dado in self.ancoras:
                if dado["Nome"] == item_selecionado:
                    img = es.load_image(f'{constantes.PATH_IMGS_ANCORAS}{dado["Arquivo"]}', 100, 50)
                    self.lbl_ancora_img.img = img
                    self.lbl_ancora_img.config(image=img)

    def encerrar(self):
        # self.salvarItens()
        # listener_running.clear()
        # myEvent.set()

        # info.salvar_log()
        es.salvar_posicao(self.rootwsconfig.geometry(), "Posicao_na_tela_config")
        self.rootwsconfig.destroy()

if __name__ == "__main__":
    
    rootws= ThemedTk(theme='arc', themebg=True)
    minha_app = WS_Config(rootws)

