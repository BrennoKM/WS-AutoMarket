import pyautogui as pg
import random
import constants
import os

pg.useImageNotFoundException(False)

def mover_para(alvo=None, var_x=0, var_y=0):
    if(alvo is not None):
        x, y = alvo
        x = x + var_x + random.uniform(-5, 5)
        y = y + var_y + random.uniform(-5, 5)
        d = 0.3
        d = 0.3 + random.uniform(-0.2, 0.2)
        t=pg.easeOutQuad
        pg.moveTo(x, y, d, t)
        return True
    else:
        return None

def clicar(qnt):
    pg.sleep(0.1)
    pg.click(clicks=qnt, interval=0.12 + random.uniform(-0.01, 0.02))

def encontrar_alvo(path, semelhanca=0.8, regiao= None, center: bool = True):
    if os.path.exists(path):
        slot = pg.locateOnScreen(path, confidence=semelhanca, region=regiao)
        if(slot != None):
            if(center == True):
                slot = pg.center(slot)
            return slot
        else:
            print(f'Alvo não encontrado: {path}')
            return None
    else:
        print(f'Arquivo não encontrado: {path}')
        return None
    
def ajustar_tela_market(myEvent):
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_fechar.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    verif = encontrar_alvo(f'{constants.PATH_IMGS}_ancora_cancelar.png')
    if verif is not None:
        mover_para(verif)
        clicar(1)
        verif = encontrar_alvo(f'{constants.PATH_IMGS}_ancora_cancelar.png')
        if verif is not None:
            mover_para(verif)
            clicar(1)
        return None

def ajustar_Barra_Lateral(myEvent):
    pg.sleep(0.2)
    while pg.pixelMatchesColor(*constants.POSICAO_BARRA_GRANDE_LATERAL, (57, 57, 49), tolerance=10):
        #print(f"{myEvent}  interface AJUSTARBARRA actions")
        if myEvent.is_set():
            return
        mover_para(constants.POSICAO_BARRA_GRANDE_LATERAL)
        clicar(1)
    

def encontrar_slot_vazio(myEvent):
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_slot_mkt.png', regiao=constants.AREA_MERCADO)) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    verif = encontrar_alvo(f'{constants.PATH_IMGS}_ancora_todos_itens.png')
    if verif is not None:
        return True
    else:
        if myEvent.is_set():
            return
        clicar(1)
        return True
 
def encontrar_item(myEvent, item):
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}{item}', semelhanca=0.98, regiao=constants.AREA_ITENS))
    pg.sleep(0.35)
    if verif is None:
        if myEvent.is_set():
            return
        pg.press('down', 12, 0.12)
        pg.sleep(0.35)
        verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}{item}', semelhanca=0.98, regiao=constants.AREA_ITENS))
        if verif is None:
            if myEvent.is_set():
                return
            pg.press('down', 12, 0.12)
            verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}{item}', semelhanca=0.98, regiao=constants.AREA_ITENS))
            pg.sleep(0.35)
            if verif is None:
                verif = encontrar_alvo(f'{constants.PATH_IMGS}_ancora_cancelar.png')
                if verif is not None:
                    mover_para(verif)
                    clicar(1)
                    verif = encontrar_alvo(f'{constants.PATH_IMGS}_ancora_cancelar.png')
                    if verif is not None:
                        mover_para(verif)
                        clicar(1)
                    return None
                pass
    if myEvent.is_set():
        return
    clicar(1)
    return True

def avancar(myEvent):
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_avancar.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)

def inserir_quantidade(myEvent, qnt):
    verif = mover_para(constants.POSICAO_QUANTIDADE) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    pg.press('backspace')
    pg.write(qnt, 0.07 + random.uniform(-0.03, 0.04))

def ok(myEvent):
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_ok.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)

def inserir_preco(myEvent, preco):
    verif = mover_para(constants.POSICAO_PRECO) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    pg.press('backspace', 9, 0.09 + random.uniform(-0.01, 0.02))
    pg.write(preco, 0.07 + random.uniform(-0.03, 0.04))

def verificar_licensa(myEvent, licensa_mkt):
    if licensa_mkt is True:
        mover_para(constants.POSICAO_LICENSA_MKT)
        if myEvent.is_set():
            return
        clicar(1)

def vender(myEvent):
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_vender.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)

def pegar_ouro_correio(myEvent):
    pg.sleep(0.7 + random.uniform(-0.05, 0.05))
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_ouro_correio.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(2)
    verif = mover_para(encontrar_alvo(f'{constants.PATH_IMGS}_ancora_para_bolsa.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)


def venderItens(myEvent, item, qnt, preco, licensa_mkt):
    verif = True
    #print(f"{myEvent}  interface VENDERITENS actions")
    if myEvent.is_set():
        return

    ajustar_tela_market(myEvent)

    ajustar_Barra_Lateral(myEvent)
    
    if myEvent.is_set():
        return

    verif = encontrar_slot_vazio(myEvent)
    if verif is None:
        return None
    
    if myEvent.is_set():
        return

    verif = True
    verif = encontrar_item(myEvent, item)
    if verif is None:
        return None
    
    if myEvent.is_set():
        return

    avancar(myEvent)
    
    if myEvent.is_set():
        return

    inserir_quantidade(myEvent, qnt)
    
    if myEvent.is_set():
        return

    ok(myEvent)
    
    if myEvent.is_set():
        return

    inserir_preco(myEvent, preco)
    
    if myEvent.is_set():
        return

    verificar_licensa(myEvent, licensa_mkt)
    
    if myEvent.is_set():
        return

    vender(myEvent)
    pg.sleep(0.5 + random.uniform(-0.05, 0.05))
    return True