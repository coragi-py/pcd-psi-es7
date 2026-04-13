# Sistema Seguro de Autenticação e Gestão de Credenciais (PSI)

Este projeto foi desenvolvido como parte do **Projeto Integrador** da disciplina de Políticas de Segurança da Informação no Bacharelado de Engenharia de Software (UMC). O objetivo é implementar um sistema de autenticação robusto, com foco na proteção de dados e conformidade com a **LGPD**.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+ 
* **Framework Web:** Flask
* **Criptografia:** Argon2id (Hashing) e PyOTP (2FA)
* **Base de Dados:** SQLite (Ficheiro local)
* **Gestão de Dependências:** Virtualenv (venv)

## Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/coragi-py/pcd-psi-es7
cd pcd-psi-es7
```

### 2. Configurar o Ambiente Virtual
```powershell
# No Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências
```powershell
pip install -r requirements.txt
```

### 4. Inicializar a Base de Dados
Este comando criará as tabelas necessárias para utilizadores e logs de auditoria:
```powershell
python database/init_db.py
```

### 5. Executar a Aplicação
```powershell
python app.py
```
O servidor estará disponível em `http://127.0.0.1:5000`.

## 🛡️ Funcionalidades e Itens de Segurança Implementados

O sistema foi construído para atender aos requisitos técnicos da disciplina (Checklist):

* **Item 1.1 a 1.4 (Gestão de Credenciais):** Armazenamento de passwords utilizando o algoritmo **Argon2id** com salt único por utilizador.
* **Item 1.5 e 1.6 (2FA):** Autenticação de dois fatores funcional via protocolo TOTP.
* **Item 1.11 (Proteção Brute Force):** Bloqueio automático da conta por 15 minutos após 5 tentativas falhadas de login.
* **Item 1.9 e 1.10 (Gestão de Sessão):** Sessões seguras com tempo de expiração e invalidação total no logout.
* **Item 4.4 (Conformidade LGPD):** Registo explícito de consentimento do titular no momento do registo.
* **Item 5.1 e 5.2 (Auditoria):** Trilha imutável de logs para todos os eventos críticos de segurança.
* **Regra de Senha Forte:** Validador dinâmico que exige mínima entropia (12+ caracteres, símbolos, números e letras).

## Como Testar (Exemplo via API)

### Registo de Utilizador
* **Endpoint:** `POST /registrar`
* **JSON:**
    ```json
    {
      "email": "exemplo@dominio.com",
      "senha": "SenhaForte@2026!",
      "consentimento_lgpd": true
    }
    ```

### Login Multifator
1. Realize o login primário enviando o e-mail e password.
2. Utilize o `2fa_secret` retornado no registo para gerar um código de 6 dígitos (TOTP) num dispositivo móvel (Google Authenticator ou Microsoft Authenticator).
3. Envie o código no campo `token_2fa` para completar o acesso.

## Integrantes do Grupo
* Anny Gabrielly Souza do Nascimento
* Antonio Luiz Lins Neto 
* Fábio Yuuki Saruwataru 

---
