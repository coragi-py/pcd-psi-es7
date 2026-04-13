import os
import sqlite3
import pyotp
from flask import Flask, request, jsonify, session
from datetime import datetime, timedelta
from src.auth.security_manager import hash_senha, verificar_senha, gerar_segredo_2fa, validar_complexidade_senha

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Item 1.9: Configuração de sessões com tempo de expiração definido
app.permanent_session_lifetime = timedelta(minutes=30)

@app.before_request
def make_session_permanent():
    session.permanent = True
    
def get_db_connection():
    conn = sqlite3.connect('database/sistema_seguro.db')
    conn.row_factory = sqlite3.Row
    return conn

def registrar_log(usuario_id, evento, ip):
    """
    Item 5.1: Logs de autenticação registrados
    Item 5.2: Logs de falhas e 2FA registrados
    """
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO logs_auditoria (usuario_id, evento, ip_origem)
        VALUES (?, ?, ?)
    ''', (usuario_id, evento, ip))
    conn.commit()
    conn.close()

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    consentimento = data.get('consentimento_lgpd')

    if not consentimento:
        return jsonify({"erro": "O consentimento para tratamento de dados é obrigatório conforme a LGPD"}), 400

    # Validação de Senha Forte
    is_valida, mensagem = validar_complexidade_senha(senha)
    if not is_valida:
        return jsonify({"erro": mensagem}), 400

    # Item 1.1 a 1.4: Processamento após validação de complexidade
    senha_protegida = hash_senha(senha)
    segredo_2fa = gerar_segredo_2fa()

    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO usuarios (email, senha_hash, dois_fatores_secret, consentimento_lgpd)
            VALUES (?, ?, ?, ?)
        ''', (email, senha_protegida, segredo_2fa, 1))
        conn.commit()
        conn.close()
        
        return jsonify({
            "mensagem": "Utilizador registado com sucesso!",
            "2fa_secret": segredo_2fa 
        }), 201
    except Exception:
        return jsonify({"erro": "Erro ao processar o registo. O e-mail pode já estar em uso."}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    token_2fa = data.get('token_2fa')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

    if not user:
        return jsonify({"erro": "Credenciais inválidas"}), 401

    # Item 1.11: Proteção contra força bruta - Verificação de bloqueio ativo
    if user['bloqueado_ate'] is not None:
        try:
            bloqueio = datetime.fromisoformat(user['bloqueado_ate'])
            if datetime.now() < bloqueio:
                conn.close() # Importante fechar antes de retornar
                return jsonify({"erro": "Acesso bloqueado temporariamente por excesso de tentativas"}), 403
        except ValueError:
            # Caso a data esteja em formato inválido, ignoramos o bloqueio para não travar o sistema
            pass

    # Validação da autenticação primária (Item 1.1)
    if not verificar_senha(user['senha_hash'], senha):
        novas_tentativas = user['tentativas_falhas'] + 1
        bloqueio_temp = None
        
        # Item 1.11: Bloqueio automático após 5 falhas consecutivas 
        if novas_tentativas >= 5:
            # Definimos o bloqueio para 15 minutos à frente
            bloqueio_temp = (datetime.now() + timedelta(minutes=15)).isoformat()
            # Item 5.2: Registro de falha crítica no log 
            registrar_log(user['id'], "Bloqueio de conta: Força bruta detectada", request.remote_addr)
        else:
            registrar_log(user['id'], "Falha na validação de password", request.remote_addr)
        
        conn.execute('UPDATE usuarios SET tentativas_falhas = ?, bloqueado_ate = ? WHERE id = ?',
                     (novas_tentativas, bloqueio_temp, user['id']))
        conn.commit()
        conn.close()
        
        return jsonify({"erro": "Credenciais inválidas"}), 401

    # Item 1.5 e 1.6: Validação do 2FA após sucesso na autenticação primária
    totp = pyotp.TOTP(user['dois_fatores_secret'])
    if not totp.verify(token_2fa):
        registrar_log(user['id'], "Falha no segundo fator (2FA)", request.remote_addr)
        conn.close()
        return jsonify({"erro": "Código de verificação inválido"}), 401

    # Reset de tentativas após login bem-sucedido (Limpeza de estado de segurança)
    conn.execute('UPDATE usuarios SET tentativas_falhas = 0, bloqueado_ate = NULL WHERE id = ?', (user['id'],))
    conn.commit()
    conn.close()
    
    # Item 1.9: Estabelecimento de sessão segura
    session['user_id'] = user['id']
    
    # Item 5.1: Log de sucesso na autenticação 
    registrar_log(user['id'], "Autenticação completa realizada", request.remote_addr)
    return jsonify({"mensagem": "Login efetuado. Acesso autorizado."}), 200

@app.route('/logout', methods=['POST'])
def logout():
    """Item 1.10: Invalidação de sessão no logout """
    user_id = session.get('user_id')
    if user_id:
        registrar_log(user_id, "Sessão encerrada voluntariamente", request.remote_addr)
    
    session.clear() 
    return jsonify({"mensagem": "Logout realizado com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)