import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pandas_market_calendars import get_calendar
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import logging
import datetime as dt
import zipfile
import pyautogui
import numpy as np
import sys
import glob
import time
import cv2
import xlwings as xw
import re
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the list of stock codes
portuguese_month_names = {
    "1": "janeiro",
    "2": "fevereiro",
    "3": "março",
    "4": "abril",
    "5": "maio",
    "6": "junho",
    "7": "julho",
    "8": "agosto",
    "9": "setembro",
    "10": "outubro",
    "11": "novembro",
    "12": "dezembro"
    }

codRV = [
    'BOVB11',
    'KNIP11',
    'XPLG11',
    'HCTR11',
    'HGRU11',
    'URPR11',
    'MCCI11',
    'MXRF11',
    'BCFF11',
    'BOVA11'
]

def pegaPreco(code, excel_file_path):
    
    app = xw.App(visible=False)
    wb = app.books.open(excel_file_path)
    sheet = wb.sheets[0]
    
    for row in range(2, sheet.range("A1").end('down').row + 1):
        row_code = sheet.range(f"C{row}").value  # Assuming code is in the 3rd column (column C)
        price = sheet.range(f"T{row}").value  # Assuming price is in the 21st column (column U)
        
        if row_code is not None:
            row_code = row_code.strip()  # Remove any leading or trailing whitespace
            
            if row_code == code:
                wb.close()
                app.quit()
                return str(price).replace('.', ',')  # Replace dot with comma
    
    wb.close()
    app.quit()
    return None  # Code not found

def Pega_d2(data_inicio = None):
    soD2=False
    # define a data atual
    data_atual = dt.date.today()

    # define a data de início, há 10 dias minimo
    if not data_inicio:
        data_inicio= data_atual - dt.timedelta(days=10)
        soD2=True

    # define o calendário a ser usado (B3), incluindo feriados
    calendario = get_calendar('BMF').schedule(start_date=data_inicio, end_date=data_atual)

    # calcula a data de 2 dias úteis atrás
    if soD2:
        datas_atras = calendario.iloc[len(calendario)-4:len(calendario)-2,0]
    else:
        datas_atras = calendario.iloc[:len(calendario)-2,0].tolist()
        
    lista_datas =[]

    for dti in datas_atras:
        lista_datas.append(dti.date())
    # imprime a data encontrada

    else:
        return(lista_datas[1:])

# Define your codRV list and other constants here

def start_main_code():
    def processo(processo):
        pss = driver.find_element(By.CSS_SELECTOR,'#txArgBusca')
        pss.send_keys(processo)
        pss.send_keys(Keys.ENTER)

    def credencial(credencial, campo):
        username_field = driver.find_element(By.CSS_SELECTOR, '#'+campo)
        username_field.send_keys(credencial)
    
    download_directory = r"W:\PRESI\GERIS\_RESTRITO\BSHV"
    shutil.rmtree(download_directory, ignore_errors=True)
    os.makedirs(download_directory, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://funprespjud.sinqia.com.br/SinqiaFundosPROD/servlet/SQCTRL")

    credencial('SeuNomeDeUsuário', 'Usr')
    credencial('SuaSenha', 'Pwd')

    submit_button = driver.find_element(By.CSS_SELECTOR, '#btnSubmit')
    submit_button.click()

    time.sleep(5)

    dates = Pega_d2()

    for date in dates:
        year = date.strftime('%Y')
        month = date.strftime('%m').lstrip('0')
        monthP = date.strftime('%m')
        day = date.strftime('%d')

        # Get the month name in Portuguese using your portuguese_month_names dictionary
        month_name = f"{month}- {portuguese_month_names[month]}"

        folder_path = os.path.join(
            r"W:\PRESI\GERIS\_RESTRITO\2. Controle de Investimento\2.4 Controle Diário Investimentos",
            year,
            month_name,
            f"{day}_{month}_{year}"
        )

        csv_file_path = os.path.join(folder_path, f"Extrato_PB_{day}_{monthP}_{year}.csv")
        wb = xw.Book(csv_file_path)
        sheet = wb.sheets[0]
        if os.path.exists(csv_file_path):
            wb = xw.Book(csv_file_path)

            for code in codRV:
                price = pegaPreco(code, csv_file_path)
                processo(106)
                print (price)
                di = driver.find_element(By.CSS_SELECTOR, '#el_txFiltroIndice')
                di.click()
                di.send_keys(code)  # Use the current code from the loop
                di = driver.find_element(By.CSS_SELECTOR, '#cp__rgFiltroTipoSerie_2')
                di.click()
                di = driver.find_element(By.CLASS_NAME, "registryButton")
                di.click()
                sleep(2)
                element = driver.find_element(By.XPATH,'//*[@id="dataTable_Registry"]/tbody/tr[1]')
                actions = ActionChains(driver)
                actions.double_click(element).perform()
                sleep(5)
                di = driver.find_element(By.NAME,"btn_btAtualiza")
                di.click()
                sleep(5)
                element = driver.find_element(By.ID,"dataTable_Registry")
                actions = ActionChains(driver)
                actions.context_click(element).perform()
                di = driver.find_element(By.ID,"gridLv_menu_itemMenu_0")
                sleep(10)
                di.click()
                sleep(15)
                
                print("Procurando Valor")
                
                for _ in range(5):
                    driver.switch_to.active_element.send_keys(Keys.TAB)
                    
                driver.switch_to.active_element.send_keys(Keys.TAB)
                driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
                driver.switch_to.active_element.send_keys(Keys.ARROW_LEFT)
                if price is not None and isinstance(price, str):  # Check if price is not None and is a string

                    for char in price:
                        driver.switch_to.active_element.send_keys(char)
                        sleep(0.1)  # Add a slight delay between characters
                else:
                    print("Invalid price value")
                print("Valor inserido")

                print("Procurando ValorMedio")
                for _ in range(1):
                    driver.switch_to.active_element.send_keys(Keys.TAB)
                    
                driver.switch_to.active_element.send_keys(Keys.TAB)
                driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
                driver.switch_to.active_element.send_keys(Keys.ARROW_LEFT)
                if price is not None and isinstance(price, str):  # Check if price is not None and is a string

                    for char in price:
                        driver.switch_to.active_element.send_keys(char)
                        sleep(0.1)  # Add a slight delay between characters
                else:
                    print("Invalid price value")
                print("Valor inserido")

                print("Procurando ValorFechamento")
                for _ in range(0):
                    driver.switch_to.active_element.send_keys(Keys.TAB)
                    
                driver.switch_to.active_element.send_keys(Keys.TAB)
                driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
                driver.switch_to.active_element.send_keys(Keys.ARROW_LEFT)
                if price is not None and isinstance(price, str):  # Check if price is not None and is a string

                    for char in price:
                        driver.switch_to.active_element.send_keys(char)
                        sleep(0.1)  # Add a slight delay between characters
                else:
                    print("Invalid price value")
                print("Valor inserido")

                print("Clicando no botão OK")
                
                for _ in range(4):
                    driver.switch_to.active_element.send_keys(Keys.TAB)
                    
                driver.switch_to.active_element.send_keys(Keys.ENTER)
                print("Ok!")
                sleep(2)
                image_src = "/SinqiaFundosPROD/Obj/bt_sair.gif"
                image_element = driver.find_element(By.CSS_SELECTOR, f'img[src="{image_src}"]')

                # Click on the image
                image_element.click()
        print(Fore.GREEN + "Código principal iniciado." + Style.RESET_ALL)

def list_codes():
    print(Fore.YELLOW + "Lista de códigos:")
    for idx, code in enumerate(codRV, start=1):
        print(Fore.YELLOW + f"{idx}. {code}")
    print(Fore.YELLOW + "\nRVs a serem importados para o dia:")
    rvs_to_import = Pega_d2()
    for idx, rv in enumerate(rvs_to_import, start=1):
        print(Fore.CYAN + f"{idx}. {rv}")
    print(Style.RESET_ALL)

def main_menu():
    print(Fore.MAGENTA + "Menu do Terminal\n")
    print(Fore.MAGENTA + "1. Iniciar Código Principal")
    print(Fore.MAGENTA + "2. Listar Códigos")
    print(Fore.MAGENTA + "3. Sair")
    print(Style.RESET_ALL)

while True:
    main_menu()
    choice = input(Fore.YELLOW + "\nPor favor, insira a sua escolha: ")

    if choice == '1':
        start_main_code()
    elif choice == '2':
        list_codes()
    elif choice == '3':
        print(Fore.RED + "Encerrando o programa." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Escolha inválida. Por favor, selecione uma opção válida." + Style.RESET_ALL)
