\# Inventory Management API



A \*\*pure backend REST API\*\* built using \*\*FastAPI\*\*, \*\*MySQL\*\*, and \*\*Docker\*\*.  

This project demonstrates real-world backend development including \*\*CRUD operations\*\*, \*\*JWT authentication\*\*, and \*\*containerized deployment\*\*.



---



\## Tech Stack



\- FastAPI

\- MySQL 8

\- SQLAlchemy ORM

\- JWT Authentication

\- Docker \& Docker Compose

\- Python 3.11



---



\## Features



\- User registration \& login

\- JWT-based authentication

\- Product management (CRUD)

\- Order creation with stock handling

\- Relational database design

\- Environment-based configuration

\- Dockerized backend



---



\## Project Structure

Inventory-API/

├── Dockerfile

├── docker-compose.yml

├── .env

├── requirements.txt

└── app/

├── main.py

├── database.py

├── models.py

├── schemas.py

├── auth.py

├── dependencies.py

└── routers/

├── users.py

├── products.py

└── orders.py



---



\## Environment Variables



Create a `.env` file in the project root:



```env

DATABASE\_URL=mysql+pymysql://root:root@mysql:3306/inventory\_db

SECRET\_KEY=supersecretkey

ALGORITHM=HS256

ACCESS\_TOKEN\_EXPIRE\_MINUTES=60





