# Backend run guide

## Correct way to start the API

From the `backend` folder:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

From the project root:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Common error

If you are already inside `backend`, do **not** add `--app-dir backend`.
That can cause:

`ModuleNotFoundError: No module named 'app'`

because the import path becomes incorrect for `app.main:app`.
