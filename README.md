# Document Summarizer

A full-stack web application that automatically generates summaries from PDF documents using AI-powered natural language processing. The application also supports question-answering functionality based on the uploaded documents.

## 🚀 Features

- **PDF Upload**: Upload PDF documents for processing
- **AI-Powered Summarization**: Generate intelligent summaries using Hugging Face models
- **Question & Answer**: Ask questions about uploaded documents and get AI-generated answers
- **Vector Search**: Uses Pinecone vector database for efficient document retrieval
- **Modern UI**: Clean and responsive React frontend with Tailwind CSS
- **RESTful API**: Django REST Framework backend with robust error handling

## 🛠️ Technology Stack

### Backend
- **Django 3.2+** - Web framework
- **Django REST Framework** - API development
- **LangChain** - AI/ML pipeline management
- **Pinecone** - Vector database for document embeddings
- **Hugging Face** - Pre-trained language models
- **PyPDF** - PDF processing
- **SQLite** - Database (development)

### Frontend
- **React 19** - UI library
- **Vite** - Build tool and development server
- **Tailwind CSS** - Styling framework
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## ⚙️ Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here

# Hugging Face Configuration
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# Django Configuration
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

### Getting API Keys

1. **Pinecone API Key**:
   - Sign up at [Pinecone.io](https://www.pinecone.io/)
   - Create a new project
   - Copy your API key from the dashboard

2. **Hugging Face Token**:
   - Sign up at [Hugging Face](https://huggingface.co/)
   - Go to Settings → Access Tokens
   - Create a new token with read permissions

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Raj280502/Document_Summarizer.git
cd Document_Summarizer
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install django djangorestframework django-cors-headers python-dotenv
pip install langchain langchain-community langchain-huggingface langchain-pinecone
pip install pinecone-client pypdf tqdm requests

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📖 API Documentation

### Upload and Summarize Document

**Endpoint**: `POST /api/summarize/`

**Request**: Multipart form data with PDF file

**Response**:
```json
{
  "id": 1,
  "file": "/media/documents/document.pdf",
  "summary": "AI-generated summary of the document...",
  "uploaded_at": "2025-10-05T10:00:00Z"
}
```

### Ask Question About Document

**Endpoint**: `POST /api/ask_question/`

**Request**:
```json
{
  "document_id": 1,
  "question": "What is the main topic of this document?"
}
```

**Response**:
```json
{
  "answer": "The main topic is...",
  "question": "What is the main topic of this document?"
}
```

## 🏗️ Project Structure

```
Document_Summarizer/
├── backend/                 # Django configuration
│   ├── settings.py         # Main settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── summarizer/             # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── service.py         # AI/ML processing logic
│   └── urls.py            # App URLs
├── frontend/               # React application
│   ├── src/
│   │   ├── App.jsx        # Main component
│   │   ├── main.jsx       # Entry point
│   │   └── assets/        # Static assets
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
├── media/                  # Uploaded files (not in git)
├── manage.py              # Django management
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Development

### Running Tests

```bash
# Backend tests
python manage.py test

# Frontend tests
cd frontend
npm run test
```

### Building for Production

```bash
# Build frontend
cd frontend
npm run build

# Collect static files (Django)
python manage.py collectstatic
```

## 🚨 Troubleshooting

### Common Issues

1. **"PINECONE_API_KEY not found"**
   - Ensure your `.env` file is in the root directory
   - Check that your Pinecone API key is correct

2. **"Module not found" errors**
   - Make sure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **CORS errors**
   - Verify `django-cors-headers` is installed and configured
   - Check `CORS_ALLOWED_ORIGINS` in settings.py

4. **PDF processing fails**
   - Ensure the PDF is not password-protected
   - Check file size limits in Django settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the AI framework
- [Pinecone](https://www.pinecone.io/) for vector database
- [Hugging Face](https://huggingface.co/) for pre-trained models
- [Django](https://www.djangoproject.com/) and [React](https://reactjs.org/) communities

## 📞 Contact

**Raj Patel** - [@Raj280502](https://github.com/Raj280502)

Project Link: [https://github.com/Raj280502/Document_Summarizer](https://github.com/Raj280502/Document_Summarizer)

---

⭐ Star this repository if you found it helpful!
