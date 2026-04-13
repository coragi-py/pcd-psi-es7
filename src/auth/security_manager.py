import re
from argon2 import PasswordHasher
import pyotp

# Item 1.2: Parâmetros de custo do hash configurados e justificados
ph = PasswordHasher(memory_cost=65536, time_cost=3, parallelism=4)

def validar_complexidade_senha(senha):
    """
    Regra de Senha Forte:
    - Mínimo 12 caracteres
    - Letras maiúsculas e minúsculas
    - Números
    - Caracteres especiais
    """
    if len(senha) < 12:
        return False, "A senha deve ter pelo menos 12 caracteres."
    if not re.search(r"[a-z]", senha):
        return False, "A senha deve conter letras minúsculas."
    if not re.search(r"[A-Z]", senha):
        return False, "A senha deve conter letras maiúsculas."
    if not re.search(r"[0-9]", senha):
        return False, "A senha deve conter números."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False, "A senha deve conter caracteres especiais."
    return True, ""

def hash_senha(senha):
    # Item 1.1 e 1.3: Hash seguro com salt único
    return ph.hash(senha)

def verificar_senha(hash_armazenado, senha_digitada):
    try:
        return ph.verify(hash_armazenado, senha_digitada)
    except Exception:
        return False

def gerar_segredo_2fa():
    # Item 1.5: Geração de segredo para 2FA
    return pyotp.random_base32()