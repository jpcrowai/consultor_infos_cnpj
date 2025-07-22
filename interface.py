import time
from env import token
from busca_city import *
import streamlit as st
from Consulta_CNPJ import Basic
import pandas as pd
import io


def interface():
    st.set_page_config(page_title="Consulta CNPJ", layout="centered")
    st.title("Consulta de CNPJs")
    modo = st.radio("Escolha o modo de busca", (
        "Upload de Excel",
        "Digitar CNPJs",
        "Buscar por Cidade e UF"
    ))
    cnpjs = []
    resultados = []
    buffer = None

    if modo == "Upload de Excel":
        arquivo = st.file_uploader("Envie o arquivo .xlsx com uma coluna de CNPJs", type=["xlsx"])
        if arquivo:
            df = pd.read_excel(arquivo)
            cnpjs = df.iloc[:, 0].astype(str).tolist()

    elif modo == "Digitar CNPJs":
        entrada = st.text_area("Digite os CNPJs separados por vírgula")
        if entrada:
            cnpjs = [x.strip() for x in entrada.split(',')]

    elif modo == "Buscar por Cidade e UF":
        cidade = st.text_input("Cidade").lower()
        uf = st.text_input("UF").upper()
        email_destino = st.text_input("📧 E-mail para envio (opcional)")

        if st.button("🔎 Buscar e Consultar Empresas"):
            if not cidade or not uf:
                st.warning("Preencha cidade e UF corretamente.")
            else:
                with st.spinner("Buscando empresas na cidade..."):
                    api = BrasilIO(token)
                    empresas = api.get_empresas(cidade, uf)

                    if not empresas:
                        st.warning("Nenhum dado encontrado para os filtros fornecidos.")
                        return

                    df_cnpjs = pd.DataFrame(empresas)
                    cnpjs = df_cnpjs.iloc[:, 0].astype(str).tolist()

                    st.info(f"🔍 {len(cnpjs)} CNPJs encontrados. Iniciando consulta detalhada...")
                    with st.spinner("Consultando dados detalhados..."):
                        for cnpj in cnpjs:
                            time.sleep(1)
                            dados = Basic.consultar_cnpj(cnpj)
                            if 'erro' not in dados:
                                resultados.append({
                                    "CNPJ": cnpj,
                                    "Razão Social": dados.get("nome", ""),
                                    "Situação": dados.get("situacao", ""),
                                    "Abertura": dados.get("abertura", ""),
                                    "E-mail": dados.get("email", ""),
                                    "Telefone": dados.get("telefone", ""),
                                    "Atividade Principal": dados.get("atividade_principal", [{}])[0].get("text", "")
                                })
                            else:
                                resultados.append({"CNPJ": cnpj, "Erro": dados['erro']})

                    df_resultado = pd.DataFrame(resultados)
                    st.subheader("📋 Resultado")
                    st.dataframe(df_resultado)

                    buffer = io.StringIO()
                    df_resultado.to_csv(buffer, index=False)
                    buffer.seek(0)

                    if email_destino:
                        try:
                            Basic.enviar_email(email_destino, buffer)
                            st.success(f"Dados enviados para {email_destino} com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao enviar e-mail: {e}")
                    else:
                        st.download_button("Baixar CSV", data=buffer.getvalue(), file_name="consulta_cnpjs.csv", mime="text/csv")

    # Parte comum para Upload ou Digitação manual
    if modo in ["Upload de Excel", "Digitar CNPJs"]:
        email_destino = st.text_input("E-mail para envio (opcional)")

        if st.button("🔍 Consultar CNPJs"):
            if not cnpjs:
                st.warning("Insira ao menos um CNPJ válido.")
                return

            with st.spinner("Consultando..."):
                for cnpj in cnpjs:
                    time.sleep(1)
                    dados = Basic.consultar_cnpj(cnpj)
                    if 'erro' not in dados:
                        resultados.append({
                            "CNPJ": cnpj,
                            "Razão Social": dados.get("nome", ""),
                            "Situação": dados.get("situacao", ""),
                            "Abertura": dados.get("abertura", ""),
                            "E-mail": dados.get("email", ""),
                            "Telefone": dados.get("telefone", ""),
                            "Atividade Principal": dados.get("atividade_principal", [{}])[0].get("text", "")
                        })
                    else:
                        resultados.append({"CNPJ": cnpj, "Erro": dados['erro']})

            df_resultado = pd.DataFrame(resultados)
            st.subheader("📋 Resultado")
            st.dataframe(df_resultado)

            buffer = io.StringIO()
            df_resultado.to_csv(buffer, index=False)
            buffer.seek(0)

            if email_destino:
                try:
                    Basic.enviar_email(email_destino, buffer)
                    st.success(f"Dados enviados para {email_destino} com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao enviar e-mail: {e}")
            else:
                st.download_button("Baixar CSV", data=buffer.getvalue(), file_name="consulta_cnpjs.csv", mime="text/csv")
