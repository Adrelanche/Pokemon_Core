# 📚 Team Rocket API
## Visão Geral 📜

Este é um projeto backend desenvolvido com Django e Django REST Framework, utilizando PostgreSQL como banco de dados e JWT para autenticação. O projeto está containerizado com Docker para facilitar a implantação e execução. 🎯🔧📦
## Tecnologias Utilizadas ⚙️

- Python  
- Django  
- PostgreSQL  
- Docker  

## Configuração do Ambiente 🏗️📝
1. Clonar o Repositório 🔄📂💾
Em seu terminal rode o seguinte código:

````sh
mkdir Pokemon_Core
cd Pokemon_Core
git clone https://github.com/Adrelanche/Pokemon_Core.git
````
## 2. Criar e Configurar o Arquivo .env 🔑📄⚙️

Crie um arquivo .env na raiz do projeto e adicione as variáveis de ambiente necessárias:
````sh
SECRET_KEY=
DB_NAME=
DB_USER= 
DB_PASSWORD=
DB_HOST= 
DB_PORT=5432
````
## 3. Construir e Subir os Containers 🏗️🐳

Certifique-se de ter o Docker instalado. Para iniciar os containers, execute:
````sh
docker-compose up --build  
````
Isso iniciará o banco de dados PostgreSQL e o servidor Django na porta 8000. 📡🔄🔗
## 4. Aplicar Migrações 🔄📜⚙️

Dentro do container do backend, execute:
````sh
docker-compose exec web python manage.py migrate  
````
## Endpoints Principais 📡🔐

O backend expõe uma API RESTful protegida por JWT. Alguns dos principais endpoints incluem:
````sh
    POST /api/register/ - Registrar novo usuário

    POST /api/login/ - Logar com um usuário já registrado

    PATCH /api/favorite/ - Atualiza o Pokémon para favorito (requer autenticação)

    GET /api/favorite/ - Listar Pokémons favoritados (requer autenticação)

    PATCH /api/favorite-order/ - Ordena a posição dos Pokémons favoritos (requer autenticação)
````
## Configuração CORS 🔄🌍🛡️

A aplicação permite requisições do frontend localizado em http://localhost:5173. Para modificar essa configuração, edite o arquivo settings.py:
````sh
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
````
## Parando os Containers 🛑🐳📉

Para parar os containers, utilize:
````sh
docker-compose down  
````
## Contribuição 🤝

Contribuições são bem-vindas! Para contribuir, faça um fork do repositório, crie uma branch com sua feature e envie um pull request. 🚀💡

### Desenvolvido por Adrelanche 💻
