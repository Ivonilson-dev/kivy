import sqlite3
from datetime import datetime

# Nome do arquivo de banco de dados
NOME_BANCO = 'placar.db'

def obter_conexao():
    """Retorna uma conexão ativa com o banco de dados SQLite."""
    return sqlite3.connect(NOME_BANCO)

def inicializar_banco():
    """Cria a tabela de pontuações caso ela não exista no banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontuacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador TEXT NOT NULL,
            dificuldade TEXT NOT NULL,
            jogadas INTEGER NOT NULL,
            tempo_segundos INTEGER NOT NULL,
            data_registro TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def adicionar_pontuacao(jogador, dificuldade, jogadas, tempo_segundos):
    """
    Insere uma nova pontuação no banco de dados.
    A data de registro é gravada no formato padrão ISO.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO pontuacoes (jogador, dificuldade, jogadas, tempo_segundos, data_registro)
        VALUES (?, ?, ?, ?, ?)
    ''', (jogador, dificuldade, jogadas, tempo_segundos, data_atual))
    conexao.commit()
    conexao.close()

def obter_melhores_pontuacoes(dificuldade, limite=10):
    """
    Retorna as melhores pontuações filtradas por dificuldade.
    A ordenação prioriza o menor número de jogadas e, em caso de empate,
    o menor tempo em segundos.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT jogador, jogadas, tempo_segundos, data_registro
        FROM pontuacoes
        WHERE dificuldade = ?
        ORDER BY jogadas ASC, tempo_segundos ASC
        LIMIT ?
    ''', (dificuldade, limite))
    resultados = cursor.fetchall()
    conexao.close()
    return resultados
