import requests
import logging

# --- Configuração ---
LOG_FILE = "logs.log"
URL_DASHBOARD = "https://squarecloud.app/pt-br/dashboard"
COOKIE_DOMAIN = ".squarecloud.app"

# --- Configuração do Logging ---
# Para registrar o que o script está fazendo e depurar se algo der errado.
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_log(mensagem, nivel=logging.INFO):
    # Registra uma mensagem no log e também a imprime na tela.
    print(mensagem)
    if nivel == logging.INFO:
        logging.info(mensagem)
    elif nivel == logging.ERROR:
        logging.error(mensagem)
    elif nivel == logging.WARNING:
        logging.warning(mensagem)

import json

def carregar_config():
    # Carrega o valor do cookie do arquivo config.json.
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
            return config.get("cookie_value")
    except FileNotFoundError:
        registrar_log("Erro: Arquivo 'config.json' não encontrado.", nivel=logging.ERROR)
        return None
    except json.JSONDecodeError:
        registrar_log("Erro: O arquivo 'config.json' está mal formatado.", nivel=logging.ERROR)
        return None

def renovar_sessao():
    # Lê o cookie de sessão do config.json e faz uma requisição para a URL do dashboard para manter a sessão ativa.
    try:
        registrar_log("Iniciando o processo de renovação de sessão (método manual)...")

        # Carrega o valor do cookie do arquivo de configuração
        cookie_value = carregar_config()
        if not cookie_value or cookie_value == "COLE_O_VALOR_DO_SEU_COOKIE_AQUI":
            registrar_log(
                "Valor do cookie não encontrado ou não configurado no 'config.json'.",
                nivel=logging.ERROR
            )
            return

        # Monta o cookie no formato que a biblioteca requests espera
        cookies = {
            'squarecloud.jwt': cookie_value
        }
        registrar_log("Cookie carregado do arquivo de configuração.")

        # Define um User-Agent para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Faz a requisição para a página do dashboard
        registrar_log(f"Fazendo requisição para: {URL_DASHBOARD}")
        response = requests.get(URL_DASHBOARD, cookies=cookies, headers=headers, timeout=30)

        # Verifica a resposta
        if response.status_code == 200:
            if "login" in response.url.lower() or "auth" in response.url.lower():
                 registrar_log(
                    "A requisição foi redirecionada para uma página de login. "
                    "O cookie pode ter expirado ou ser inválido.",
                    nivel=logging.WARNING
                )
            else:
                registrar_log(
                    f"Sessão renovada com sucesso! Status: {response.status_code}",
                    nivel=logging.INFO
                )
        else:
            registrar_log(
                f"Falha ao renovar a sessão. Status: {response.status_code}",
                nivel=logging.ERROR
            )
            registrar_log(f"URL final: {response.url}", nivel=logging.ERROR)


    except Exception as e:
        registrar_log(f"Ocorreu um erro inesperado: {e}", nivel=logging.ERROR)

if __name__ == "__main__":
    renovar_sessao()

