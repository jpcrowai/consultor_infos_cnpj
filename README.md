# consultor_infos_cnpj

Aplicação web interativa desenvolvida em **Python** com **Streamlit**, que permite a **consulta automatizada de dados cadastrais de empresas brasileiras** a partir do número do CNPJ ou da localização (cidade e UF). Ideal para uso em prospecção, compliance, auditoria e análise de mercado.

---

## 🚀 Funcionalidades

- 📄 **Upload de Excel**: Envie uma planilha `.xlsx` com uma coluna de CNPJs para consulta em massa.
- ✍️ **Entrada manual**: Digite múltiplos CNPJs diretamente na interface, separados por vírgula.
- 🏙️ **Busca por Cidade e UF**: Consulte empresas ativas em uma localidade usando a API do [Brasil.IO](https://brasil.io/), e colete automaticamente seus dados.
- 📋 **Consulta Detalhada**: Para cada CNPJ, são buscadas informações como:
  - Razão Social
  - Situação cadastral
  - Data de abertura
  - E-mail
  - Telefone
  - Atividade econômica principal
- 📤 **Exportação dos Resultados**: Baixe os dados em `.csv` ou envie diretamente por e-mail via Outlook.

---

## 🛠️ Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/) — Interface web interativa
- [Pandas](https://pandas.pydata.org/) — Manipulação de dados
- `smtplib`, `ssl`, `email.message` — Envio de e-mails
- [Brasil.IO API](https://brasil.io/) — Consulta de empresas por cidade e UF
- [ReceitaWS API](https://receitaws.com.br/) (ou similar) — Consulta de CNPJ

---

## 🖥️ Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/consulta_infos_cnpj.git
cd consulta_infos_cnpj 
```

2. Instale as dependências
Use um ambiente virtual e instale as bibliotecas:
```bash
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente (opcional)
Crie um arquivo .env com:

EMAIL_OUTLOOK=seu_email@outlook.com
SENHA_OUTLOOK=sua_senha_ou_senha_de_aplicativo
4. Execute a aplicação
```bash
streamlit run main.py
```