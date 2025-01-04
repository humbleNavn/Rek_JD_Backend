
# Project Title

A brief description of what this project does and who it's for

# Job Description Generator

An AI-powered system that generates comprehensive job descriptions based on user requirements, leveraging RAG (Retrieval-Augmented Generation) and OpenAI's GPT models.

## Features

- Generates structured job descriptions following a predefined schema
- Retrieves relevant context using RAG system
- Produces both frontend-friendly and backend-formatted outputs
- Includes SEO optimization
- Generates additional suggestions for requirements, responsibilities, qualifications, and skills
- Supports multiple languages
- Integrates with Milvus vector database for context retrieval

## Prerequisites

- Python 3.x
- Milvus database server running (default: tcp://localhost:19530)
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:

bash
git clone <repository-url>
cd <repository-name>

2. Install dependencies:

pip install -r requirements.txt

3. Create a `.env` file in the root directory with your API keys:

env
OPENAI_API_KEY="your-openai-api-key"
SERP_API_KEY="your-serp-api-key"
LANGFUSE_SECRET_KEY="your-langfuse-secret-key"
LANGFUSE_PUBLIC_KEY="your-langfuse-public-key"
LANGFUSE_HOST="https://cloud.langfuse.com"


## Usage

1. Ensure your Milvus database is running and accessible.

2. Run the main script:


bash
python main_updated.py


3. The script will:
   - Generate context queries based on user requirements
   - Retrieve relevant context from the Milvus database
   - Generate a comprehensive job description
   - Create both frontend and backend responses
   - Save the results in JSON format

## Project Structure

- `main_updated.py`: Main entry point of the application
- `context.py`: Handles context generation and retrieval
- `jd_generation.py`: Core job description generation logic
- `frontend.py`: Frontend response formatting
- `llm.py`: OpenAI API integration
- `JD_Schema.json`: Defines the structure for job descriptions

## Output

The system generates two JSON files for each job description:
- `Frontend_{timestamp}.json`: Frontend-friendly format
- `Backend_{timestamp}.json`: Detailed backend schema

Files are saved in the `Altogether_V2` directory.

## Configuration

- Job description structure can be modified in `JD_Schema.json`
- OpenAI model settings can be adjusted in `llm.py`
- Database connection settings can be modified in `main_updated.py`

## Error Handling

The system includes:
- JSON repair functionality for malformed responses
- Exception handling for API calls
- Fallback content generation when context is missing

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
