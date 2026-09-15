# CodeShot

CodeShot is a Django learning project for creating syntax-highlighted code
previews and exporting them as PNG or JPEG images.

The project currently demonstrates a multi-service backend with Django,
PostgreSQL, Redis and Celery. Export jobs are created through an HTTP API,
processed in the background and stored with a persistent status.

## Current limitation

The asynchronous export pipeline works, but the current image generator is a
placeholder: it creates a plain white 100x100 image. Rendering the real editor
state with highlighted source code is planned as the next project improvement.

## Architecture

Docker Compose starts four services:

- `web` - Django application and HTTP API;
- `db` - PostgreSQL, the permanent data store;
- `redis` - Celery broker and Django cache;
- `worker` - Celery worker that processes export jobs.

The asynchronous export flow is:

```text
Client sends POST /api/exports/
-> Django validates the request
-> Django creates ExportJob with status pending
-> Django sends job_id to Redis
-> API immediately returns 202 Accepted
-> Celery worker receives job_id
-> Worker generates and saves the image
-> Worker changes the status to completed or failed
-> Client reads the current status through GET /api/exports/<id>/
```

PostgreSQL is the source of truth for users, analytics and export jobs. Redis
contains temporary queue messages and cached analytics results.

## Requirements

- Docker Desktop with Docker Compose;
- Git.

Python does not need to be installed on the host when the project is run fully
through Docker.

## Environment variables

Create a local `.env` file from `.env.example`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Set your own values in `.env`:

```dotenv
SECRET_KEY=replace_with_a_private_secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_USER=codeshot
POSTGRES_PASSWORD=replace_with_a_private_password
POSTGRES_DB=codeshot
DATABASE_URL=postgresql://codeshot:replace_with_a_private_password@db:5432/codeshot
CELERY_BROKER_URL=redis://redis:6379/0
```

Do not commit `.env`. The `.env.example` file contains only safe example values
and documents which variables are required.

`DATABASE_URL` documents the complete connection string. The current Django
settings read the same connection values from the separate `POSTGRES_*`
variables.

## First launch

Validate the Compose configuration:

```powershell
docker compose config -q
```

Build the images and start all services:

```powershell
docker compose up -d --build
```

Apply database migrations:

```powershell
docker compose exec web python manage.py migrate
```

Create the permission groups:

```powershell
docker compose exec web python manage.py setup_groups
```

Open the application:

```text
http://localhost:8000
```

The Django admin is available at:

```text
http://localhost:8000/admin/
```

An administrator can be created with:

```powershell
docker compose exec web python manage.py createsuperuser
```

## Permissions

The `setup_groups` management command creates two groups:

- `Export users` receives `codeshot.export_images` and can create export jobs;
- `Analysts` receives `codeshot.view_product_stats` and can read event summary.

Authentication alone is not enough to create an export. The user must also
have the required permission. A user can read only their own `ExportJob`.
CodeShot returns `403 Forbidden` for another user's job according to the chosen
API contract.

## API

CodeShot uses Django session authentication. A successful login creates a
`sessionid` cookie. Unsafe requests such as `POST` also require a valid CSRF
token when sent from a browser or REST client.

### Authentication

- `POST /api/auth/register/` - create a user and start a session, returns `201`;
- `POST /api/auth/login/` - authenticate and start a session, returns `200`;
- `POST /api/auth/logout/` - end the current session, returns `204`;
- `GET /api/auth/me/` - return the current user, returns `200`.

User responses contain an ID, username, groups and permissions. Passwords and
password hashes are never returned.

### Asynchronous exports

- `POST /api/exports/` - create an export job, requires
  `codeshot.export_images`, returns `202`;
- `GET /api/exports/<id>/` - return the owner's job status, returns `200`.

Accepted form field:

```text
export_format=png
```

Supported values are `png` and `jpg`.

An export status can be:

- `pending` - created but not started;
- `processing` - being processed by the worker;
- `completed` - file generated successfully;
- `failed` - generation failed.

### Synchronous preview and download

- `POST /preview/` - validate and store the editor state in the session;
- `GET /download/png` - return a PNG file immediately;
- `GET /download/jpg` - return a JPEG file immediately.

These endpoints are retained from the earlier synchronous implementation.

### Analytics

- `GET /stats/` - return aggregated product events, requires
  `codeshot.view_product_stats`.

The event summary uses Django cache with Redis. On a cache miss, Django
calculates ORM aggregates and saves the result for 60 seconds. Creating a new
`ProductEvent` invalidates the old cache entry.

Analytics stores only:

- event name;
- language;
- theme;
- export format;
- creation timestamp.

It does not store user source code, generated image bytes or private local
filenames.

## Running tests

The source code is copied into the Docker image. Rebuild `web` after changing
Python files or tests:

```powershell
docker compose up -d --build web
```

Run the complete test suite:

```powershell
docker compose exec web python -m pytest -q
```

Run only export API tests:

```powershell
docker compose exec web python -m pytest codeshot/tests/exports/test_export_api.py -q
```

Celery tasks are executed synchronously in their unit tests, so the tests do
not have to wait for a real background worker.

## Diagnostics

Show service status:

```powershell
docker compose ps
```

Check Django:

```powershell
docker compose logs web --tail 50
```

Check PostgreSQL:

```powershell
docker compose logs db --tail 50
```

Check Redis:

```powershell
docker compose logs redis --tail 50
```

Check Celery:

```powershell
docker compose logs worker --tail 50
```

Check migrations:

```powershell
docker compose exec web python manage.py showmigrations
docker compose exec web python manage.py migrate --check
```

Check that the worker knows the tasks:

```powershell
docker compose exec worker celery -A config inspect registered
```

## Stopping the project

Stop and remove the containers and Compose network:

```powershell
docker compose down
```

PostgreSQL and generated media remain in named volumes. Do not add `-v` unless
you intentionally want to delete those persistent volumes and their data.

## Development note

Because the project directory is not mounted as a bind volume, a running
container does not automatically see source-code changes. Rebuild the affected
service after edits:

```powershell
docker compose up -d --build web worker
```

Rebuilding is required for changes to Django or Celery code. Starting existing
containers without code changes only requires `docker compose up -d`.

## Security notes

- never commit `.env` or real credentials;
- never store user source code in product analytics;
- never return passwords or password hashes from API responses;
- never trust a user-supplied `job_id` without checking ownership;
- do not render untrusted user code with Django's `safe` filter without a
  reviewed escaping strategy and security tests.
