# 🌙 Lunna API

> **Acompanhamento Pré-natal de Excelência para Clínicas Privadas.**

A **Lunna API** é o coração tecnológico de um ecossistema mobile-first projetado para transformar a jornada do pré-natal. Focada em clínicas privadas, a plataforma oferece um acompanhamento clínico detalhado, seguro e humanizado para gestantes, médicos e equipes administrativas.

---

## 🚀 Visão Geral

O projeto foi concebido para ser uma solução **SaaS White-label**, permitindo que clínicas personalizem a experiência de suas pacientes enquanto mantêm um padrão rigoroso de gestão de dados clínicos.

### 👥 Perfis Suportados
- **🤰 Paciente (Gestante):** Monitoramento em tempo real da gravidez, registro de sinais vitais, visualização de exames e chat direto com a clínica.
- **🩺 Médico(a):** Gestão completa do prontuário eletrônico, acompanhamento de curvas de saúde (glicose, pressão) e controle de agenda.
- **📅 Secretaria:** Operação logística, agendamentos, cadastros e comunicação institucional.

---

## 🛠️ Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/) (via SQLAlchemy 2.0 & AsyncPG)
- **Cache & Mensageria:** [Redis](https://redis.io/)
- **Migrações:** [Alembic](https://alembic.sqlalchemy.org/)
- **Containerização:** [Docker](https://www.docker.com/) & Docker Compose
- **Validação de Dados:** [Pydantic v2](https://docs.pydantic.dev/)

---

## 📋 Principais Funcionalidades

### 🩺 Monitoramento Clínico
- **Sinais Vitais:** Registro e análise de Pressão Arterial, Glicemia e Controle de Contrações.
- **Evolução Gestacional:** Acompanhamento de peso, altura uterina e idade gestacional.
- **Exames:** Centralização de Ultrassons (USG), Sorologias e exames laboratoriais.

### 🗓️ Gestão de Atendimento
- **Agendamentos:** Fluxo completo de marcação, confirmação e solicitação de remarcação.
- **Prontuário Digital:** Histórico clínico completo com classificação de risco.

### 💬 Comunicação
- **Chat Integrado:** Canal seguro para dúvidas e orientações entre paciente e equipe médica.
- **Avisos:** Sistema de notificações e informativos da clínica.

---

## ⚙️ Como Executar

### Pré-requisitos
- Docker & Docker Compose

### Instalação e Execução

1. **Clonar o repositório:**
   ```bash
   git clone <repo-url>
   cd lunna-api
   ```

2. **Configurar variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o .env com suas configurações se necessário
   ```

3. **Subir os containers:**
   ```bash
   docker-compose up -d --build
   ```

A API estará disponível em `http://localhost:8000`.  
A documentação interativa (Swagger) pode ser acessada em `http://localhost:8000/docs`.

---

## 📂 Estrutura do Projeto

```text
├── app/
│   ├── api/          # Endpoints e Rotas (v1)
│   ├── core/         # Configurações, Segurança e Database
│   ├── models/       # Modelos SQLAlchemy
│   └── schemas/      # Modelos Pydantic (DTOs)
├── alembic/          # Migrações do Banco de Dados
├── main.py           # Ponto de entrada da aplicação
└── docker-compose.yml # Orquestração de containers
```

