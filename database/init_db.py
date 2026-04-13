import sqlite3

def init_db():
    # Definição do caminho do banco conforme estrutura de pastas do projeto
    conn = sqlite3.connect('database/sistema_seguro.db')
    cursor = conn.cursor()
    
    # Tabela de Usuários: Estruturada para atender requisitos de Segurança e LGPD
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,           -- Item 1.1: Armazenamento de hash seguro (Argon2)
            dois_fatores_secret TEXT,           -- Item 1.5: Segredo para Autenticação de dois fatores (2FA)
            tentativas_falhas INTEGER DEFAULT 0, -- Item 1.11: Contador para proteção contra força bruta
            bloqueado_ate DATETIME,             -- Item 1.11: Controle de bloqueio temporário
            consentimento_lgpd INTEGER,         -- Item 4.4: Registro de consentimento explícito do titular
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Item 5.1 e 5.2: Tabela para Logs de Auditoria e Registro de Falhas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            evento TEXT NOT NULL,               -- Registro de sucessos, falhas e eventos críticos
            ip_origem TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados e tabelas de segurança inicializados com sucesso.")

if __name__ == "__main__":
    init_db()