# Jogo da Memória com Kivy & SQLite

Este é um projeto de demonstração de um **Jogo da Memória** moderno, responsivo e interativo, construído com a biblioteca **Kivy** para Python. O jogo possui suporte a dois níveis de dificuldade e salva o placar de líderes (leaderboard) localmente usando o banco de dados embutido **SQLite**.

Toda a lógica e documentação do projeto foram criadas em **Português do Brasil**.

---

## 🛠️ Como Testar e Executar no Windows (Desenvolvimento Local)

Uma das maiores vantagens do Kivy em relação ao React Native é que **você não precisa de um emulador pesado ou de uma ferramenta como o Expo para começar a programar e testar**. O Kivy renderiza a interface diretamente no seu computador usando OpenGL, simulando o comportamento móvel perfeitamente em uma janela desktop.

Siga os passos abaixo para configurar o ambiente de desenvolvimento no seu terminal:

### 1. Criar o Ambiente Virtual (venv)
É altamente recomendável utilizar ambientes virtuais em Python para não misturar as dependências do Kivy com as globais do sistema:
```powershell
# Abra o terminal na pasta c:\Projetos\kivy e execute:
python -m venv venv
```

### 2. Ativar o Ambiente Virtual
- No **PowerShell** (Windows):
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- No **Prompt de Comando (CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```

*Nota: Se o PowerShell bloquear a execução de scripts, você pode rodar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` antes de ativar.*

### 3. Instalar o Kivy e Dependências
Com o ambiente ativado (você verá `(venv)` no início da linha do terminal), instale as dependências a partir do `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Executar o Jogo
Para iniciar o aplicativo no seu computador, basta executar o arquivo principal:
```powershell
python main.py
```
Isso abrirá uma janela contendo a interface em modo escuro (Dark Mode). Você pode redimensionar a janela e o layout se ajustará de forma responsiva!

---

## 🗄️ Banco de Dados Local (SQLite)

O jogo utiliza o banco de dados embutido do Python (`sqlite3`). 
- Logo no primeiro início, o Kivy cria um arquivo chamado `placar.db` na raiz da pasta do projeto.
- Quando você vence uma partida, os dados (Nome, Jogadas, Tempo e Data) são automaticamente persistidos.
- O Placar de Líderes exibe os 10 melhores resultados de cada dificuldade, ordenando primeiro pelo **menor número de jogadas** e, depois, pelo **menor tempo**.

Para visualizar e gerenciar o banco manualmente, você pode usar uma extensão do VSCode como *SQLite Viewer* ou baixar o aplicativo gratuito [DB Browser for SQLite](https://sqlitebrowser.org/).

---

## 📱 Como Testar no Celular (Android) - Kivy vs. React Native

Você mencionou que já trabalhou com **React Native** e conhece o workflow do **Expo** e do emulador. Vamos fazer um paralelo de como isso funciona no ecossistema Python/Kivy:

| Aspecto | React Native / Expo | Python / Kivy |
| :--- | :--- | :--- |
| **Ambiente de Testes Rápido** | Expo Go (App no celular lê o código JS via rede) | Execução nativa direta na tela do computador (`python main.py`). |
| **Hot Reload** | Nativo do Metro Bundler | Pode ser configurado no Kivy com bibliotecas auxiliares (ex: `kivy-reloader`), mas o reinício local do Python é tão rápido que geralmente basta fechar e abrir a janela novamente. |
| **Ferramenta de Compilação** | EAS Build (Nuvem) ou Gradle local | **Buildozer** (ferramenta oficial do Kivy para empacotamento). |

### Como gerar o arquivo `.apk` para instalar no Android:

Para empacotar aplicações Python para Android, o Kivy utiliza uma ferramenta de linha de comando chamada **Buildozer**. O Buildozer compila o Python, o Kivy, a sua lógica de código e todas as bibliotecas necessárias em um pacote `.apk` nativo do Android.

> ⚠️ **Importante:** O Buildozer só roda nativamente em sistemas baseados em Unix (Linux ou macOS). No Windows, o recomendado é usar o **WSL2** (Windows Subsystem for Linux) com uma distribuição Ubuntu instalada.

#### Passo a Passo para criar o APK com WSL2:

1. **Configurar o WSL2 e instalar dependências do Buildozer no Ubuntu:**
   Dentro do seu terminal Ubuntu no WSL2:
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev cmake libffi-dev libgomp1
   pip3 install --user --upgrade buildozer
   ```

2. **Iniciar o arquivo de configuração do Buildozer:**
   Navegue até a pasta do seu projeto dentro do WSL2 (ex: `/mnt/c/Projetos/kivy/`) e execute:
   ```bash
   buildozer init
   ```
   Isso criará o arquivo `buildozer.spec`.

3. **Configurar o `buildozer.spec`:**
   Abra este arquivo no VSCode e edite as opções básicas como:
   - `title` = Jogo da Memória
   - `package.name` = jogodamemoria
   - `source.include_exts` = py,png,jpg,kv,db (certifique-se de incluir `.kv`!)
   - `requirements` = python3,kivy,sqlite3

4. **Compilar e Rodar:**
   Conecte o seu celular Android físico no computador via USB com a **Depuração USB** ativada (ou inicie um emulador no Windows com ADB ativo).
   No terminal do WSL2, execute o comando:
   ```bash
   buildozer -v android debug deploy run
   ```
   O Buildozer irá:
   - Baixar o Android SDK/NDK necessários automaticamente.
   - Compilar seu aplicativo em um arquivo `.apk` (gerado na pasta `bin/`).
   - Instalar (`deploy`) o APK no celular conectado.
   - Iniciar (`run`) o jogo automaticamente na tela do celular.
