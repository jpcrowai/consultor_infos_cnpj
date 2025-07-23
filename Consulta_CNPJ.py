import requests

class Basic:
    def consultar_cnpj(cnpj):
        cnpj = ''.join(filter(str.isdigit, cnpj))
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"erro": f"Erro {response.status_code}"}
        except Exception as e:
            return {"erro": str(e)}

dados = Basic.consultar_cnpj("16640104000109")
print(dados)