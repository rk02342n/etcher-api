# Etcher Backend

A scalable FastAPI backend for caching/indexing Etcher as an API - a decentralized newsletter platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/substack_db
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

4. Virtual Environment (Python)
```
python -m venv .venv
source .venv/bin/activate
```


5. Visit the API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authors
- `POST /api/v1/authors/` - Create author
- `GET /api/v1/authors/` - List authors
- `GET /api/v1/authors/{id}` - Get author by ID
- `GET /api/v1/authors/slug/{slug}` - Get author by slug
- `PATCH /api/v1/authors/{id}` - Update author
- `DELETE /api/v1/authors/{id}` - Delete author

### Publications
- `POST /api/v1/publications/` - Create publication
- `GET /api/v1/publications/` - List publications
- `GET /api/v1/publications/{id}` - Get publication by ID
- `GET /api/v1/publications/slug/{slug}` - Get publication by slug
- `PATCH /api/v1/publications/{id}` - Update publication
- `DELETE /api/v1/publications/{id}` - Delete publication

### Posts
- `POST /api/v1/posts/` - Create post
- `GET /api/v1/posts/` - List posts (with filters)
- `GET /api/v1/posts/{id}` - Get post by ID
- `GET /api/v1/posts/slug/{pub_slug}/{post_slug}` - Get post by slug
- `PATCH /api/v1/posts/{id}` - Update post
- `DELETE /api/v1/posts/{id}` - Delete post

### Subscribers
- `POST /api/v1/subscribers/` - Subscribe to publication
- `GET /api/v1/subscribers/publication/{id}` - List subscribers
- `DELETE /api/v1/subscribers/{id}` - Unsubscribe

## Project Structure

```
etcher-backend/
├── app/
│   ├── core/          # Config and database setup
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   └── api/           # API endpoints
├── .env
└── requirements.txt
```