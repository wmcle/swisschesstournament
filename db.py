import sqlite3
import os

DB_PATH = "tournament.db"

def init_db():
    """Inicializa o banco de dados e cria a tabela de jogadores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela de Jogadores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER DEFAULT 1200,
            points REAL DEFAULT 0.0,
            active BOOLEAN DEFAULT 1
        )
    ''')
    # Tabela de Partidas (para evitar jogar duas vezes e registrar pontos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round INTEGER DEFAULT 1,
            p1_id INTEGER,
            p2_id INTEGER,
            result TEXT,
            FOREIGN KEY(p1_id) REFERENCES players(id),
            FOREIGN KEY(p2_id) REFERENCES players(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_player(name: str, rating: int = 1200):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name, rating) VALUES (?, ?)", (name, rating))
    conn.commit()
    conn.close()

def get_all_players():
    """Retorna todos os jogadores ativos ordenados por pontos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, rating, points FROM players WHERE active = 1 ORDER BY points DESC, rating DESC")
    players = cursor.fetchall()
    conn.close()
    return players

def delete_player(player_id: int):
    """Remove um jogador do banco de dados pelo ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()
    conn.close()

def update_player(player_id: int, new_name: str, new_rating: int):
    """Atualiza o nome e rating de um jogador existente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET name = ?, rating = ? WHERE id = ?", (new_name, new_rating, player_id))
    conn.commit()
    conn.close()

def record_match(p1_id: int, p2_id, result: str):
    """Registra uma partida e atualiza a pontuação dos jogadores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO matches (p1_id, p2_id, result) VALUES (?, ?, ?)", (p1_id, p2_id, result))
    
    if result == "bye":
        cursor.execute("UPDATE players SET points = points + 1 WHERE id = ?", (p1_id,))
    elif result == "1-0":
        cursor.execute("UPDATE players SET points = points + 1 WHERE id = ?", (p1_id,))
    elif result == "0-1":
        cursor.execute("UPDATE players SET points = points + 1 WHERE id = ?", (p2_id,))
    elif result == "1/2-1/2":
        cursor.execute("UPDATE players SET points = points + 0.5 WHERE id = ?", (p1_id,))
        cursor.execute("UPDATE players SET points = points + 0.5 WHERE id = ?", (p2_id,))
        
    conn.commit()
    conn.close()
