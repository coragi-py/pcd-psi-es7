# Sistema Seguro de Autenticação e Gestão de Credenciais (PSI)

Este projeto foi desenvolvido como parte do **Projeto Integrador** da disciplina de Políticas de Segurança da Informação no Bacharelado de Engenharia de Software (UMC). [cite_start]O objetivo é implementar um sistema de autenticação robusto, com foco na proteção de dados e conformidade com a **LGPD**[cite: 1, 2, 6].

## 🛠️ Tecnologias Utilizadas

* [cite_start]**Linguagem:** Python 3.10+ [cite: 132]
* **Framework Web:** Flask
* [cite_start]**Criptografia:** Argon2id (Hashing) e PyOTP (2FA) [cite: 86, 90]
* [cite_start]**Base de Dados:** SQLite (Ficheiro local) [cite: 125]
* **Gestão de Dependências:** Virtualenv (venv)

## 🚀 Como Executar o Projeto

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
[cite_start]Este comando criará as tabelas necessárias para utilizadores e logs de auditoria[cite: 125]:
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

* [cite_start]**Item 1.1 a 1.4 (Gestão de Credenciais):** Armazenamento de passwords utilizando o algoritmo **Argon2id** com salt único por utilizador[cite: 86, 88].
* [cite_start]**Item 1.5 e 1.6 (2FA):** Autenticação de dois fatores funcional via protocolo TOTP[cite: 90].
* [cite_start]**Item 1.11 (Proteção Brute Force):** Bloqueio automático da conta por 15 minutos após 5 tentativas falhadas de login[cite: 23, 92].
* [cite_start]**Item 1.9 e 1.10 (Gestão de Sessão):** Sessões seguras com tempo de expiração e invalidação total no logout[cite: 91, 92].
* [cite_start]**Item 4.4 (Conformidade LGPD):** Registo explícito de consentimento do titular no momento do registo[cite: 31, 124].
* [cite_start]**Item 5.1 e 5.2 (Auditoria):** Trilha imutável de logs para todos os eventos críticos de segurança[cite: 34, 125].
* [cite_start]**Regra de Senha Forte:** Validador dinâmico que exige mínima entropia (12+ caracteres, símbolos, números e letras)[cite: 137].

## 🧪 Como Testar (Exemplo via API)

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
2. Utilize o `2fa_secret` retornado no registo para gerar um código de 6 dígitos (TOTP) num dispositivo móvel.
3. Envie o código no campo `token_2fa` para completar o acesso.

## 👥 Integrantes do Grupo
* [cite_start]Anny Gabrielly Souza do Nascimento [cite: 129]
* [cite_start]Antonio Luiz Lins Neto [cite: 130]
* [cite_start]Fábio Yuuki Saruwataru [cite: 131]

---
