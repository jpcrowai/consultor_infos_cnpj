
import requests
import smtplib
from email.message import EmailMessage
import ssl
import os

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


    def enviar_email_outlook(destinatario, assunto, corpo, nome_arquivo, arquivo_buffer=None):
        remetente = "seu_email@outlook.com"
        senha = "sua_senha_ou_senha_de_aplicativo"

        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = remetente
        msg["To"] = destinatario
        msg.set_content(corpo)


        if arquivo_buffer:
            arquivo_buffer.seek(0)
            conteudo = arquivo_buffer.read()
            if isinstance(conteudo, str):
                conteudo = conteudo.encode("utf-8")

            msg.add_attachment(conteudo, maintype="text", subtype="csv", filename=nome_arquivo)

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.office365.com", 587) as smtp:
                smtp.starttls(context=context)
                smtp.login(remetente, senha)
                smtp.send_message(msg)
            print("E-mail enviado com sucesso.")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")



