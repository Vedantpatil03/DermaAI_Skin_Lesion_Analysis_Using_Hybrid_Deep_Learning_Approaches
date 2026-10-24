# DermaAI

AI-assisted skin lesion analysis application with a React/Vite frontend and
FastAPI backend.

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version required by your dependencies
- Node.js and npm
- MongoDB Atlas account or another configured MongoDB instance
- Git and Git LFS

### 1. Clone the Repository

```bash
git clone https://github.com/Vedantpatil03/DermaAI_Skin_Lesion_Analysis_Using_Hybrid_Deep_Learning_Approaches.git
```

Navigate into the project directory:

```bash
cd DermaAI_Skin_Lesion_Analysis_Using_Hybrid_Deep_Learning_Approaches
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a local `.env` file inside the `backend` directory and add the
environment variables required by the application.

Example:

```env
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET_KEY=your_secret_key
```

Use the exact variable names expected by the backend. For deployment, set
these values in the hosting provider's environment variable settings.

**Important:** Never upload real database credentials, JWT secrets, API keys,
or other sensitive information to GitHub.

### 4. Start the Backend Server

From the repository root, run:

```bash
uvicorn --app-dir backend app.main:app --reload
```

The backend should start at:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

To explore the API documentation, open:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 5. Set Up the Frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL displayed in the terminal, commonly:

[http://localhost:5173](http://localhost:5173)

For local development, the frontend defaults to
`http://127.0.0.1:8000`. To use another backend URL, create
`frontend/.env.local` with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## 🚀 Deployment

### Backend on Render

The repository includes [`render.yaml`](./render.yaml) for deploying the
FastAPI backend. Configure these Render environment variables:

- `MONGODB_URI`: MongoDB Atlas connection string
- `JWT_SECRET_KEY`: a long random secret
- `CORS_ORIGINS`: the deployed Vercel URL, such as
  `https://your-app.vercel.app`

### Frontend on Vercel

Import the repository into Vercel and set the project root directory to
`frontend`. Configure:

- `VITE_API_BASE_URL`: the deployed Render backend URL, such as
  `https://your-api.onrender.com`

The included [`frontend/vercel.json`](./frontend/vercel.json) supports
client-side route refreshes.

The trained model files use Git LFS. Install Git LFS before cloning or pulling
the repository so the model files are downloaded correctly.

---

## 🔐 Security

- Keep `.env` files out of version control.
- Never publish database credentials or authentication secrets.
- Use environment variables for sensitive configuration.
- Validate uploaded files before processing.
- Restrict access to user-specific data.
- Use HTTPS when deploying the application.

---

## 🎯 Project Objectives

- Develop a web-based image analysis application using deep learning.
- Apply image segmentation to identify relevant regions in skin lesion images.
- Integrate a hybrid deep learning classification pipeline.
- Build a user-friendly interface for uploading images and viewing results.
- Provide authentication and backend API functionality.
- Explore the integration of AI-based image analysis into a web application.

---

## 🔮 Future Scope

- Improve model performance using additional validated datasets.
- Evaluate classification performance using appropriate metrics.
- Enhance the visualization of segmentation results.
- Improve application performance and model inference speed.
- Deploy the application using suitable cloud infrastructure.
- Expand testing and usability evaluation.

---

## ⚠️ Medical Disclaimer

DermaAI is an academic and research project intended for educational and
experimental purposes only. It is not a substitute for professional medical
advice, diagnosis, or treatment.
