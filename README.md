# SecureDoc AI: RAG Chatbot with RBAC

A Retrieval-Augmented Generation (RAG) chatbot. This application allows users to query company documents with responses generated based on their specific access roles (Admin, User, Public).

## 🚀 Features

- **Role-Based Access Control (RBAC)**: Smart retrieval system that only searches for documents the logged-in user is authorized to see.
- **RAG Pipeline**: Built with **FastAPI**, **Qdrant** (Vector DB), and **Groq** (Llama-3.1-8b-instant LLM).
- **Persistent Chat History**: Maintains conversation context within a session using `sessionStorage`.
- **High Performance**: Uses `sentence-transformers/all-MiniLM-L6-v2` for efficient embeddings and Groq Cloud for ultra-fast LLM inference.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Vector Database**: Qdrant Cloud, Langchain
- **LLM**: Llama-3.1-8b-instant (via Groq Cloud)
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Authentication**: JWT (JSON Web Tokens) with Argon2 password hashing
- **Database**: PostgreSQL (via SQLAlchemy)

## 📁 Project Structure

```text
My_RAG_Project/
├── main.py              # FastAPI Application entry point
├── rag.py               # RAG logic (Search & LLM interaction)
├── auth.py              # Authentication and JWT logic
├── database.py          # SQLAlchemy Models & DB Connection
├── vector.py            # Qdrant Vector DB wrapper
├── chunk.py             # Text chunking logic
├── data_loader.py       # Document loading (PDF, DOCX, TXT, etc.)
├── create_vector_db.py  # Script to ingest data into Qdrant
├── create_user.py       # Helper for user management
├── templates/           # Frontend assets (HTML, CSS, JS)
├── data/                # Folder for source documents
└── requirements.txt     # Python dependencies
```

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd My_RAG_Project
```

### 2. Set Up Virtual Environment
```bash
python -m venv myenv
myenv\Scripts\activate  # On Windows
# source myenv/bin/activate # On Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```env
QDRANT_URL=your_qdrant_url
QDRANT_API=your_qdrant_api_key

DATABASE_URL=postgresql://user:password@localhost:5432/ragdb
SECRET_KEY=your_jwt_secret_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Initialize Database & Data
**Ingest Documents into Qdrant:**
Place your documents in the `data/` folder and run:
```bash
python create_vector_db.py
```

**Initialize PostgreSQL & Create a User:**
You can use a script or the Python REPL:
```python
from database import init_db
from create_user import create_user

init_db()
create_user("admin", "admin123", "admin")
```

### 6. Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Open your browser and navigate to `http://127.0.0.1:8000`.

## 📖 Usage

1. **Login**: Access the login page and enter your credentials. User roles (Admin/User) determine which documents the RAG system can retrieve.
2. **Chat**: Type your questions in the input field. The bot will search for relevant context and answer based *only* on the provided documents.
3. **History**: Your chat history is persisted per session. You can clear it anytime using the "Clear Chat" button.

## 🔒 Security
- Passwords are encrypted using the **Argon2** hashing algorithm.
- Access tokens (JWT) expire according to the `ACCESS_TOKEN_EXPIRE_MINUTES` setting.
- Document retrieval is strictly filtered by user roles at the vector database level.

---
*Developed for efficient and secure company knowledge management.*
