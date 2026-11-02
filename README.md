# 🍔 API Raízes do Nordeste (Projeto Back-End UNINTER 2026)

## 📌 Arquitetura e Tecnologias
- **Python 3.10+** (Compatível com 3.15+)
- **FastAPI** (Assíncrono, Pydantic V2)
- **SQLAlchemy 2.0** + Aiosqlite
- **Autenticação JWT** & Bcrypt (sem dependência do Passlib antigo)

## 🚀 Como Executar Localmente
1. Clone o repositório na sua máquina local.
2. Crie e ative o Ambiente Virtual (venv): 
   `python -m venv .venv`
   `source .venv/bin/activate` (Linux/Mac) ou `.venv\Scripts\activate` (Windows)
3. Instale as dependências de negócio:
   `pip install fastapi uvicorn sqlalchemy aiosqlite pydantic pydantic-settings python-jose[cryptography] bcrypt python-multipart`
4. Opcional: Execute o seed inicial para criar alguns lanches se necessário rodando o script:
   `python popular_banco.py`
5. Inicie a API determinando a porta local 8080:
   `uvicorn main:app --reload --port 8080`
6. Acesse o **Swagger UI Interativo** para testar as requisições gerado automaticamente em:
   👉 http://127.0.0.1:8080/docs