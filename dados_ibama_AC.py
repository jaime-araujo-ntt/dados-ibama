import requests
import json
import pandas as pd

def main():
    tipos_infracao()

def tipos_infracao(url = "http://dadosabertos.ibama.gov.br/dados/SICAFI/AC/Quantidade/multasDistribuidasBensTutelados.json"):
    print("Estabelecendo conexão...")
    response = requests.get(url)
    if response.status_code == 200:
        list_of_processes = response.json() # pega o json completo (neste ja esta em formato de lista).
        amount = len(list_of_processes['data']) # quantidade total de objetos da lista, dentro do "data".
        print("foram encontrados %d processos..." % amount)
        list_municipio = []
        list_nomeRazaoSocial = []
        list_valorAuto = []
        list_dataAuto = []
        list_situcaoDebito = []
        categories = ["Fauna", "Flora", "Pesca", "Outras"]
        for category in categories:
            print("Acessando multas sobre %s ..." % category)
            for process in list_of_processes['data']:
                if process["tipoInfracao"] == category:
                    list_municipio.append(process["municipio"])
                    list_nomeRazaoSocial.append(process["nomeRazaoSocial"])
                    list_valorAuto.append(process["valorAuto"])
                    list_dataAuto.append(process["dataAuto"])
                    list_situcaoDebito.append(process["situcaoDebito"])
            row = {'municipio': list_municipio, 'nomeRazaoSocial': list_nomeRazaoSocial, 'valorAuto': list_valorAuto, 'dataAuto': list_dataAuto, 'situcaoDebito': list_situcaoDebito}
            df = pd.DataFrame(row, columns=['municipio', 'nomeRazaoSocial', 'valorAuto', 'dataAuto', 'situcaoDebito'])
            df.to_csv('%s.csv' % category)
            print("Multas relacionadas e %s foram salvas na tabela!" % category)
            list_municipio.clear()
            list_nomeRazaoSocial.clear()
            list_valorAuto.clear()
            list_dataAuto.clear()
            list_situcaoDebito.clear()
    else:
        print("Sem conexão com o Site!")

if __name__ == '__main__':
    main()

