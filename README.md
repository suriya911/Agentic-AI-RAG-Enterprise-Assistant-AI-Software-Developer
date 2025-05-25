# Agentic AI RAG Enterprise Assistant

A production-grade Enterprise Assistant that uses Retrieval-Augmented Generation (RAG) with GPT-4 to answer enterprise queries and perform autonomous tasks.

## Features

- 🤖 RAG-powered query answering using internal documents
- 📧 Autonomous task execution (emailing, scheduling, ticketing)
- 📊 Comprehensive audit logging and transparency
- 🔒 Secure authentication and authorization
- 🚀 Scalable microservices architecture

## Project Structure

```
agentic-ai-enterprise-assistant/
│
├── frontend/                  # Next.js UI for users, logs, and control
├── backend/                  # FastAPI server + LangChain orchestration
├── workers/                  # Celery workers for async task execution
├── vector_db_connector/      # RAG vector store interface
├── infra/                    # Terraform configs for AWS provisioning
├── scripts/                  # Utility scripts (e.g. document ingestion)
├── docker-compose.yml        # Local dev
├── Dockerfile                # Base Docker config
├── helm-chart/               # Kubernetes deployment config
└── .github/workflows/        # GitHub Actions CI/CD
```

## Technology Stack

- Frontend: Next.js
- Backend: FastAPI + LangChain
- Vector DB: Weaviate/Pinecone
- Database: PostgreSQL
- Async Queue: Celery + Redis
- AI Model: GPT-4 via OpenAI Assistants API
- Cloud: AWS EKS + Lambda + RDS
- Infrastructure: Terraform
- CI/CD: GitHub Actions
- Authentication: OAuth2 + API Tokens

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose
- AWS CLI (for production deployment)
- Terraform (for infrastructure)

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=...
WEAVIATE_API_KEY=...
POSTGRES_URL=...
REDIS_URL=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
JIRA_API_TOKEN=...
SLACK_API_KEY=...
```

### Local Development

1. Clone the repository
2. Set up environment variables
3. Run `docker-compose up` for local development
4. Access the dashboard at `http://localhost:3000`

## Development Status

### Completed
- [ ] Project structure setup
- [ ] Basic documentation

### In Progress
- [ ] Frontend development
- [ ] Backend API setup
- [ ] RAG implementation
- [ ] Authentication system

### Pending
- [ ] Async task execution
- [ ] API integrations
- [ ] Infrastructure setup
- [ ] CI/CD pipeline
- [ ] Production deployment

## Contributing

Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 