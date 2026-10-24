# DermaAI

AI-assisted skin lesion analysis application with a React/Vite frontend and
FastAPI backend.

## Deployment

### Backend on Render

Create a Render Web Service from this repository. The included
[`render.yaml`](./render.yaml) uses the repository root, installs
`backend/requirements.txt`, and starts FastAPI with Uvicorn.

Set these environment variables in Render:

- `MONGODB_URI`: MongoDB Atlas connection string. Add the Render outbound
  network access to the Atlas IP access list as required by your Atlas setup.
- `JWT_SECRET_KEY`: a long random secret. Render generates this when using the
  Blueprint configuration.
- `CORS_ORIGINS`: the deployed Vercel URL, for example
  `https://your-app.vercel.app` (comma-separated if more origins are needed).

### Frontend on Vercel

Import the repository into Vercel and set the project root directory to
`frontend`. Vercel will use the Vite build defaults. Set:

- `VITE_API_BASE_URL`: the deployed Render URL, for example
  `https://dermaai-api.onrender.com`

The included [`frontend/vercel.json`](./frontend/vercel.json) keeps client-side
routes working on refresh.

## Local development

Run the backend from the repository root:

```powershell
pip install -r backend/requirements.txt
uvicorn --app-dir backend app.main:app --reload
```

Run the frontend:

```powershell
cd frontend
npm install
npm run dev
```

For local frontend development, `VITE_API_BASE_URL` defaults to
`http://127.0.0.1:8000`.

## Large model files

The trained `.pth` files are tracked with Git LFS through
[`.gitattributes`](./.gitattributes). Install and initialize Git LFS before
the first push.