import pyautogui as pg
import random
import constantes
import info
import os

pg.useImageNotFoundException(False)
pg.FAILSAFE = False


def capturar_e_salvar_area(x_inicial, y_inicial, largura, altura, caminho_arquivo):
    # Capturar a área especificada
    screenshot = pg.screenshot(region=(x_inicial, y_inicial, largura, altura))
    
    # Salvar a imagem
    screenshot.save(caminho_arquivo)
    print(f"Screenshot salva em: {caminho_arquivo}")

def capturar_print():
    screenshot = pg.screenshot()
    return screenshot

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

def encontrar_alvo(path, semelhanca=0.8, regiao= None, center: bool = True, necessario: bool = True):
    if os.path.exists(path):
        try:
            slot = pg.locateOnScreen(path, confidence=semelhanca, region=regiao)
        except Exception as e:
            info.printinfo(f'Except no PyAutoGui ao tentar localizar {path} na tela: {e}', True, True)
            pg.sleep(3)
            return None
        if(slot != None):
            if(center == True):
                slot = pg.center(slot)
            return slot
        else:
            if necessario is True:
                info.printinfo(f'Alvo não encontrado: {path}')
            return None
    else:
        info.printinfo(f'Arquivo não encontrado: {path}')
        return None

def encontrar_alvos(path, semelhanca=0.8, regiao = None, center: bool = True, necessario: bool = True):
    if os.path.exists(path):
        try:
            slot = pg.locateAllOnScreen(path, confidence=semelhanca, region=regiao)
        except Exception as e:
            info.printinfo(f'Except no PyAutoGui ao tentar localizar {path} na tela: {e}', True, True)
            pg.sleep(3)
            return None
        if(slot != None):
            # if(center == True):
            #     slot = pg.center(slot)
            return slot
        else:
            if necessario is True:
                info.printinfo(f'Alvo não encontrado: {path}')
            return None
    else:
        info.printinfo(f'Arquivo não encontrado: {path}')
        return None

def ajustar_tela_market(myEvent):
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_fechar.png', necessario=False))
    if verif is not None:
        clicar(1)
    if myEvent.is_set():
        return
    verif = encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_cancelar.png', necessario=False)
    if verif is not None:
        mover_para(verif)
        clicar(1)
        verif = encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_cancelar.png', necessario=False)
        if verif is not None:
            mover_para(verif)
            clicar(1)
        return None

def ajustar_Barra_Lateral(myEvent):
    pg.sleep(0.2)
    ## tratar erro aqui também
    try:
        while pg.pixelMatchesColor(*constantes.POSICAO_BARRA_GRANDE_LATERAL, (57, 57, 49), tolerance=10):
            #print(f"{myEvent}  interface AJUSTARBARRA actions")
            if myEvent.is_set():
                return
            mover_para(constantes.POSICAO_BARRA_GRANDE_LATERAL)
            clicar(1)
    except Exception as e:
        info.printinfo(f'Except no PyAutoGui ao tentar ler a cor do pixel na barra lateral: {e}', True)
        mover_para(constantes.POSICAO_BARRA_GRANDE_LATERAL)
        clicar(1)
        return None
        

def encontrar_slot_vazio(myEvent):
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_slot_mkt.png', regiao=constantes.AREA_MERCADO)) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    verif = encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_todos_itens.png', necessario=False)
    if verif is not None:
        return True
    else:
        if myEvent.is_set():
            return
        clicar(1)
        return True
 
def encontrar_item(myEvent, item):
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ITENS}{item}', semelhanca=0.98, regiao=constantes.AREA_ITENS))
    pg.sleep(0.35)
    if verif is None:
        if myEvent.is_set():
            return
        pg.press('down', 12, 0.12)
        pg.sleep(0.35)
        verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ITENS}{item}', semelhanca=0.98, regiao=constantes.AREA_ITENS))
        if verif is None:
            if myEvent.is_set():
                return
            pg.press('down', 12, 0.12)
            verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ITENS}{item}', semelhanca=0.98, regiao=constantes.AREA_ITENS))
            pg.sleep(0.35)
            if verif is None:
                verif = encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_cancelar.png')
                if verif is not None:
                    mover_para(verif)
                    clicar(1)
                    verif = encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_cancelar.png')
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
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_avancar.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)

def inserir_quantidade(myEvent, qnt):
    
    if myEvent.is_set():
        return
    if qnt != '1':
        verif = mover_para(constantes.POSICAO_QUANTIDADE)
        if verif is None:
            return None
        clicar(1)
        pg.press('backspace')
        pg.write(qnt, 0.07 + random.uniform(-0.03, 0.04))

def ok(myEvent):
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_ok.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    return True

def inserir_preco(myEvent, preco):
    verif = mover_para(constantes.POSICAO_PRECO) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    pg.press('backspace', 9, 0.09 + random.uniform(-0.01, 0.02))
    pg.write(preco, 0.07 + random.uniform(-0.03, 0.04))

def verificar_licensa(myEvent, licensa_mkt):
    if licensa_mkt is True:
        mover_para(constantes.POSICAO_LICENSA_MKT)
        if myEvent.is_set():
            return
        clicar(1)

def vender(myEvent):
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_vender.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)
    

def pegar_ouro_correio(myEvent):
    pg.sleep(0.7 + random.uniform(-0.05, 0.05))
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_ouro_correio.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(2)
    verif = mover_para(encontrar_alvo(f'{constantes.PATH_IMGS_ANCORAS}ancora_para_bolsa.png')) 
    if verif is None:
        return None
    if myEvent.is_set():
        return
    clicar(1)


def vender_itens(myEvent, item, qnt, preco, licensa_mkt, preco_medio):
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

    vendeu = ok(myEvent)
    
    if myEvent.is_set():
        return

    if(preco_medio is False):
        inserir_preco(myEvent, preco)
    else:
        pg.sleep(2)
    
    if myEvent.is_set():
        return

    verificar_licensa(myEvent, licensa_mkt)
    
    if myEvent.is_set():
        return

    vender(myEvent)
    pg.sleep(0.5 + random.uniform(-0.05, 0.05))
    if vendeu is True:
        if preco_medio is False:
            info.printinfo(f'Item colocado no market: {item} x{qnt} por {preco}', enviar_msg=True)
        else:
            info.printinfo(f'Item colocado no market: {item} x{qnt} pelo preço médio', enviar_msg=True)
    return True

def contar_itens(myEvent, item):
    posicao = item.find(".png")
    item = item[:posicao] + "_mkt" + item[posicao:]
    itens = encontrar_alvos(f'{constantes.PATH_IMGS_ITENS}{item}', semelhanca=0.98)
    try:
        itens = list(itens)
    except (ValueError, Exception, AttributeError):
        info.printinfo("Item_mkt.png não foi encontrado")
    info.printinfo(f'{item,' -> ',len(itens)}')
    # for it in itens:
    #     print(it)
    return len(itens)