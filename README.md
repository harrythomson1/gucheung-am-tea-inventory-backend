<a id="readme-top"></a>
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img width="320" height="320" alt="logo" src="https://github.com/user-attachments/assets/c59d1d4d-f13b-4a5c-924c-0d4a0f359270" />
  </a>
</div>

# 구층암 재고 관리 / Gucheongam Tea Inventory - Backend

<!-- ABOUT THE PROJECT -->
## About The Project

Whilst I was volunteering in Gucheongam temple in Gurye-gun in South Korea I approached the manager of the temple asking if they has any techology they would like built. She asked if I could build an inventory management for the tea they sell which is what you have here.

Propblems this solves:
* Allows accurate tracking off sales with an append only ledger
* Prevents old stock going unsold as it isn't visible
* Tracks sales by customer
* Easy stock visualisation 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Railway][Railway]][Railway-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python 3.13+
* Docker
* Postgresql

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/harrythomson1/gucheung-am-tea-inventory-backend
   ```
2. Start virual environment
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
3. Start databases
   ```sh
   docker-compose up -d
   ```
4. Copy and fill in env vairables
   ```sh
   cp .env.example .env
   ```
5. Run migrations
   ```sh
   alembic upgrade head
   ```
6. Start the server
   ```
   uvicorn app.main:app --reload
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Environment Variables

```env
DB_USER=postgres
DB_PASSWORD=password
POSTGRES_DB=gucheung_am_inventory
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/gucheung_am_inventory
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/gucheung_am_inventory_test
JWKS_URL=https://your-project.supabase.co/auth/v1/.well-known/jwks.json
PROJECT_URL=https://your-project.supabase.co/auth/v1
AUDIENCE=authenticated
ALGORITHM=ES256
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Barcode/QR scanning for remove stock form
- [ ] Conversion feature to convert silver packages into wing or gift packagers
- [ ] Password reset UI

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Harry Thomson - [LinkedIn](https://www.linkedin.com/in/harry-thomson-536674211/) - haroldt95@hotmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Railway]: https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white
[Railway-url]: https://railway.app/
