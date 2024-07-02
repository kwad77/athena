# Athena AI Assistant

Athena is a powerful AI assistant application built with PyQt6 and integrated with Ollama for local language model inference. It provides a user-friendly interface for interacting with AI models, managing documents, and conducting AI-assisted conversations.

## Features

- Interactive chat interface with AI models
- Document upload and processing (PDF, DOCX)
- Multiple chat sessions management
- Model selection for different conversations
- Image pasting and display in chat
- Chat export functionality
- Customizable settings

## Prerequisites

- Python 3.7+
- Ollama (for local language model inference)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/athena-ai-assistant.git
   cd athena-ai-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Ollama following the instructions at [Ollama's official website](https://ollama.ai/).

## Configuration

1. Open `athena/config.py` and adjust the settings as needed:
   - `OLLAMA_BASE_URL`: Set this to the URL where your Ollama instance is running
   - `DEFAULT_WORKSPACE`: Set the default workspace directory

## Usage

1. Start the Ollama service on your machine.

2. Run the Athena application:
   ```
   python main.py
   ```

3. Use the interface to:
   - Start new chat sessions
   - Upload and process documents
   - Interact with AI models
   - Export chat histories

## Development

- The main application logic is in `athena/controllers/main_controller.py`
- UI components are in the `athena/views/` directory
- Services for AI and document processing are in `athena/services/`

## Testing

Run the tests using pytest:
```
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]

## Acknowledgements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [Ollama](https://ollama.ai/)
- [PyPDF2](https://pypdf2.readthedocs.io/)
- [python-docx](https://python-docx.readthedocs.io/)
