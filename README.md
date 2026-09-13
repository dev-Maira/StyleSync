# StyleSync - Rule-Based Wardrobe & Outfit Recommendation Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-6BA814?style=for-the-badge&logo=python&logoColor=white)](https://alembic.sqlalchemy.org/)

StyleSync is an asynchronous RESTful API built with Python and FastAPI. It enables users to digitize their physical wardrobe, create custom outfits via Many-to-Many entity relationships, and receive automated outfit recommendations using a deterministic rule-based matching algorithm (Top + Bottom + Shoes).

---

## 📐 Database Entity Relationship Diagram (ERD)

```text
+-------------------+       +-----------------------+       +-------------------+
|       users       |       |     clothingitem      |       |      outfits      |
+-------------------+       +-----------------------+       +-------------------+
| id (PK)           |<----+ | id (PK)               | +---->| id (PK)           |
| email (Unique)    |     | | user_id (FK -> users) | |     | user_id (FK ->u.) |
| hashed_password   |     | | name                  | |     | name (Unique)     |
| created_at        |     | | category (Enum)       | |     | occasion          |
+-------------------+     | | color                 | |     | created_at        |
                          | | season (Enum)         | |     +-------------------+
                          | | brand                 | |               ^
                          | | created_at            | |               |
                          +-----------------------+ |               |
                                      ^             |               |
                                      |             |               |
                          +-------------------+     |               |
                          |   outfit_items    |     |               |
                          +-------------------+     |               |
                          | clothing_item_id  |-----+               |
                          | outfit_id         |---------------------+
                          +-------------------+