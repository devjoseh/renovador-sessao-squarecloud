# Renovador de Sessão para SquareCloud

Este projeto contém um script simples para renovar automaticamente sua sessão no site da [SquareCloud](https://squarecloud.app/), evitando que o login expire após 24 horas de inatividade. O script faz uma requisição autenticada em segundo plano, sem a necessidade de abrir um navegador.

## Como Funciona

O script Python (`renovador_de_sessao.py`) lê um cookie de autenticação de um arquivo de configuração local (`config.json`) e o utiliza para fazer uma requisição para a página do seu dashboard da SquareCloud. Essa atividade sinaliza para o servidor que sua sessão ainda está ativa, reiniciando o contador de expiração.

Um arquivo de lote (`iniciar_renovador.bat`) garante que o script Python seja executado no diretório correto, e ele pode ser configurado para rodar automaticamente toda vez que o Windows é iniciado.

## Como Usar

Siga os passos abaixo para configurar e automatizar a execução do script.

### 1. Instale as Dependências

Abra o Prompt de Comando (CMD) e execute o seguinte comando para instalar a única biblioteca necessária:

```bash
pip install requests
```

### 2. Obtenha seu Cookie de Autenticação

Você precisa pegar o seu cookie de sessão manualmente do navegador **uma única vez**.

1.  Faça login na sua conta no site da [SquareCloud](https://squarecloud.app/).
2.  Após o login, pressione a tecla **F12** para abrir as Ferramentas de Desenvolvedor.
3.  Vá para a aba **"Application"** (ou "Aplicativo").
4.  No menu à esquerda, expanda a seção **"Cookies"** e clique em `https://squarecloud.app`.
5.  Na tabela da direita, encontre o cookie com o nome **`squarecloud.jwt`**.
6.  Clique duas vezes sobre o valor (o texto longo que começa com `eyJ...`) na coluna **"Value"** e copie-o (Ctrl+C).

### 3. Configure o Script

1.  Abra o arquivo `config.json` com um editor de texto (como o Bloco de Notas).
2.  Substitua o texto `COOKIE_JWT_DA_SQUARE_CLOUD` pelo valor do cookie que você copiou no passo anterior.
3.  Salve e feche o arquivo. O resultado deve ser algo assim:

```json
{
    "cookie_value": "eyJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE...muito...mais...texto...aqui...Kw"
}
```

### 4. Teste o Script

Execute o script manualmente para garantir que tudo está funcionando. Abra o Prompt de Comando, navegue até a pasta do projeto e execute:

```bash
python renovador_de_sessao.py
```

Se tudo estiver correto, você não verá nenhuma mensagem de erro. Você pode abrir o arquivo `renovador.log` para confirmar que a execução foi bem-sucedida. A última linha deve conter algo como `Sessão renovada com sucesso! Status: 200`.

### 5. Automatize na Inicialização do Windows

Para que o script rode toda vez que você ligar o computador, siga estes passos:

1.  Pressione as teclas **`Win + R`** no seu teclado para abrir a caixa de diálogo "Executar".
2.  Digite `shell:startup` e pressione **Enter**. Isso abrirá a pasta de inicialização do Windows.
3.  Nesta pasta, clique com o botão direito em um espaço vazio e vá em **Novo > Atalho**.
4.  Na janela que se abre, no campo "Digite o local do item", clique em **"Procurar..."** e navegue até a pasta deste projeto.
5.  Selecione o arquivo **`iniciar_renovador.bat`** e clique em **OK**.
6.  Clique em **"Avançar"**, dê um nome para o atalho (ex: `Renovador SquareCloud`) e clique em **"Concluir"**.

Pronto! Agora, toda vez que o Windows iniciar, o script será executado silenciosamente em segundo plano, mantendo sua sessão da SquareCloud sempre ativa.

## Solução de Problemas

- **Erro no log `Valor do cookie não encontrado`**: Verifique se você salvou o arquivo `config.json` corretamente com o valor do seu cookie.
- **Erro no log `Falha ao renovar a sessão`**: Seu cookie pode ter expirado. Repita o **Passo 2** para obter um novo cookie e atualize o `config.json`.
