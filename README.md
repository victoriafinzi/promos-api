# Projeto de Extensão UNOPAR: Inovação Tecnológica para Negócios Locais

Olá! 🐱
Este repositório foi criado para guardar o código realizado para a materia de atividade extensionista da faculdade Unopar. 

# Sobre o Projeto:
Neste projeto, exploramos maneiras criativas de utilizar a tecnologia para fortalecer pequenos negócios locais. A "Casa de Carne Medalha Milagrosa" foi o nosso cenário de estudo, onde desenvolvemos uma aplicação web para notificar os clientes sobre promoções em tempo real. Utilizamos linguagens de programação como Python e frameworks como Flask, além de tecnologias como QR codes e notificações via celular para criar uma solução intuitiva e eficaz.

# Objetivo:
Nosso principal objetivo foi não apenas aprimorar minhas habilidades técnicas, mas também contribuir de maneira tangível para a comunidade local. Ao facilitar a comunicação entre a loja e seus clientes, buscamos aumentar o alcance das promoções e, consequentemente, impulsionar o negócio local.

# promos-api
Python API 

# Run the app in Docker
`docker build -t promos-api .`

`docker run --network host -p 5000:5000 -v $(pwd):/app -e FLASK_APP=main.py promos-api`

## Creating the .env file:
```
DB_USERNAME=""
DB_PASSWORD=""
DB_HOST=""
DB_NAME=""
JWT_SECRET_KEY=""
```

## Running the venv:
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## Running the migrations:
`alembic upgrade head`

## If you need to create a migration:
`alembic revision --autogenerate -m "Migration name"`

## If you need to revert a migration:
`alembic downgrade base`
