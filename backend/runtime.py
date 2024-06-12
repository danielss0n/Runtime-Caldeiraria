import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from urllib3.exceptions import InsecureRequestWarning
import json
import time
import os
import threading
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


service = webdriver.ChromeService(executable_path="path/to/chromedriver.exe")
options = webdriver.ChromeOptions()
options.set_capability("unhandledPromptBehavior", "ignore")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)


def get_event_type(evento_posto):
    if evento_posto in ["PRODUÇÃO SEM ORDEM", "OPERANDO"]:
        return "Operacional - Automático"
    if evento_posto in ["FALTA DE PROGRAMAÇÃO"]:
        return "FALTA DE PROGRAMAÇÃO"
    if evento_posto in ["REFEIÇÃO", "GINÁSTICA", "MANUTENÇÃO PREVENTIVA", "TROCA DE TURNO / LIMPEZA", "TROCA DE CARRETEIS", "TROCA DE TURNO", "POSTO SEM SFM"]:
        return "Parada Planejada"
    else:
        return "Parada não Planejada"

def get_posto_maquina():
    
    driver.get("url/to/scrapping/site")

    try:
        elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//tr[@ng-class='isAlertByEvents(workstation)']")))
        elements = driver.find_elements(By.XPATH, "//tr[@ng-class='isAlertByEvents(workstation)']")

        for element in elements:
            nome_posto = element.find_element(By.XPATH, ".//td[@ng-hide='columns[1].hidden']")
            nome_posto = nome_posto.get_attribute('innerHTML')

            evento_posto = element.find_element(By.XPATH, ".//td[@ng-hide='columns[3].hidden']//span[@class='ng-binding']")
            evento_posto = evento_posto.get_attribute('innerHTML')

            duracao_evento = element.find_element(By.XPATH, ".//td[@ng-hide='columns[4].hidden']//span[@class='ng-binding']")
            duracao_evento = duracao_evento.get_attribute('innerHTML')
            event_type = get_event_type(evento_posto)

            posto_trabalho = {
                "Workstation":nome_posto, 
                "Event": evento_posto, 
                "Duration": duracao_evento,
                "AreaEventColor": get_event_color(evento_posto),
                "Employee": "MAQ SEM NOME",
                "Area": "null",
                "Workstation": nome_posto,
                "WorkstationShort": nome_posto,
                "WorkstationType": "machine",
                "EventType": event_type,
                "Event": evento_posto,
                "CommonRedEvent": evento_posto,
                "AreaEventColor": get_event_color(event_type),
                "Order": "null",
            }
            runtime_json.append(posto_trabalho)
    except:
        time.sleep(1)


def update_mod():
    dir = os.path.dirname(os.path.abspath(__file__))
    with open("get/auth", "r") as arquivo:
        GCF_AUTH = arquivo.readline()

    headers = {"Cookie" : f'GcfAuth={GCF_AUTH}'}
    url = 'https://url.site/LaborRuntime/Load'

    try:
        response = requests.get(url, verify=False, headers=headers)
        response.raise_for_status()  
  
        if response.text:  
            mod_json = json.loads(response.text)
        else:
            print("A resposta do servidor está vazia.")

        dataRedJoined = joinWorkstate(process_mod_data(mod_json))

        for obj in dataRedJoined:
            runtime_json.append(obj)


    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except json.JSONDecodeError as json_err:
        print(f"Erro de decodificação JSON: {json_err}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def setAllWrokstateCommonEvents(data, redWorkstationName, RedEvent):
    for item in data:
        workstationName = item["Workstation"]

        if workstationName == redWorkstationName:
            item["AreaEventColor"] = 'red'
            item["CommonRedEvent"] = RedEvent

    return data

def setAllWrokstateCommonEventsYellow(data, redWorkstationName, YellowEvent):
    for item in data:
        workstationName = item["Workstation"]

        if workstationName == redWorkstationName:
            item["AreaEventColor"] = 'yellow'
            item["CommonRedEvent"] = YellowEvent

    return data

def joinWorkstate(data):
    newDataRed = []
    for item in data:
        workstationName = item["Workstation"]
        AreaEventColor = item["AreaEventColor"]
        Event = item["Event"]
        EventType = item["EventType"]
        CommonRedEvent = item["CommonRedEvent"]

        if EventType == "Parada Planejada":
            newDataRed = setAllWrokstateCommonEventsYellow(data, workstationName, Event)

        if EventType == "Parada não Planejada":
            newDataRed = setAllWrokstateCommonEvents(data, workstationName, Event)
    return newDataRed


def process_mod_data(mod_json):
    processed_json = [
        {
            "Employee": obj["EmployeeName"],
            "Area": get_secao_by_group(obj["WorkstationGroupDescription"]),
            "Duration": "Null",
            "Workstation": obj["WorkstationDescription"],
            "WorkstationShort": obj["WorkstationReducedDescription"],
            "WorkstationType": "labor",
            "EventType": obj["TypeEventDescription"],
            "Event": obj["EventOperationalDescription"],
            "CommonRedEvent": obj["EventOperationalDescription"],
            "AreaEventColor": get_event_color(obj["TypeEventDescription"]),
            "Order": obj["OrderId"],
        }
        for obj in mod_json
    ]
    return processed_json

def get_event_color(event_type):
    if event_type in ["Operacional - Manual", "Operacional", "Operacional - Automático"]:
        return "green"
    elif event_type == "Parada não Planejada":
        return "red"
    elif event_type == "FALTA DE PROGRAMAÇÃO":
        return "gray"
    else:
        return "yellow"
    
def get_secao_by_group(workstation_group):
    if workstation_group == "MONTAGEM DE PACOTES":
        return "MONTAGEM DE PACOTES"
    elif workstation_group == "CORTE A LASER":
        return "PREPARACAO"
    elif workstation_group == "CALDEIRARIA":
        return "CALDEIRARIA MONTAGEM"
    else:
        return ""


JSON_DIR = "Q://runtime.json"

while True:
    runtime_json = []

    update_mod()
    get_posto_maquina()

    with open(JSON_DIR, "w", encoding="utf-8") as file:
        json.dump(runtime_json, file, ensure_ascii=False, indent=4)

    time.sleep(8)
    print(runtime_json)