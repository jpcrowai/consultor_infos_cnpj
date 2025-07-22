
import csv
import json
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


class BrasilIO:
    base_url = "https://brasil.io/api/v1/"

    def __init__(self, auth_token):
        self.__auth_token = auth_token

    @property
    def headers(self):
        return {
            "User-Agent": "python-urllib/brasilio-client-0.1.0",
        }
    @property
    def api_headers(self):
        data = self.headers
        data.update({"Authorization": f"Token {self.__auth_token}"})
        return data

    def api_request(self, path, query_string=None):
        url = urljoin(self.base_url, path)
        if query_string:
            url += "?" + urlencode(query_string)
        request = Request(url, headers=self.api_headers)
        response = urlopen(request)
        return json.load(response)

    def get_empresas(self, search, uf):
        path = "dataset/socios-brasil/empresas/data/"
        resultados = []
        pagina = 1
        while True:
            print(f"Coletando página {pagina}...")
            query = {"search": search, "uf": uf, "page": pagina}
            response = self.api_request(path, query)

            resultados += response.get("results", [])
            if not response.get("next"):
                break
            pagina += 1
        return resultados
def salvar_em_csv(dados, nome_arquivo="empresas.csv"):
    if not dados:
        print("Nenhum dado retornado.")
        return

    campos = list(dados[0].keys())
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

    print(f"Arquivo salvo com sucesso: {nome_arquivo}")



