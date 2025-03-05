# 📊 Python Finance 

Um sistema simples para gerenciar contas bancárias, transferências e movimentações financeiras utilizando **SQLModel** e **Matplotlib**.

## 🚀 Funcionalidades
- Criar e desativar contas bancárias
- Transferências entre contas
- Registro e consulta de movimentações financeiras
- Filtragem de movimentações por período
- Geração de gráficos com Matplotlib

## 📦 Instalação

### **1️⃣ Clonar o Repositório**
```sh
git clone https://github.com/seuusuario/python-finance.git
cd python-finance
```

### **2️⃣ Criar e Ativar o Ambiente Virtual**
```sh
python -m venv venv  # Criar ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### **3️⃣ Instalar Dependências**
```sh
pip install -r requirements.txt
```

### **4️⃣ Criar o Banco de Dados**
```sh
python -c 'from src.models.models import create_db_and_tables; create_db_and_tables()'
```

### **5️⃣ Executar o Programa**
```sh
python interface.py
```

### 📺 Exemplo de Execução:
```
Escolha uma opção:
[1] -> Criar conta
[2] -> Desativar conta
[3] -> Transferir dinheiro
...
```

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **SQLModel** (Gerenciamento do banco de dados SQLite)
- **Matplotlib** (Geração de gráficos)
- **Pytest** (Testes automatizados)

<!--## 🧪 Testes
Para rodar os testes unitários:
```sh
pytest tests/
```-->

## 🤝 Contribuição
Sinta-se à vontade para contribuir! Abra uma _issue_ ou envie um _pull request_. 
