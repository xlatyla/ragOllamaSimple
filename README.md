# 🤖 Chatbot RAG con Ollama y FAISS

*Un chatbot en español con memoria conversacional y recuperación de conocimiento contextual*

## ⚙️ Configuración

### Instalación de Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
```

```bash
pip install -r requirements.txt
```

## 🛠️ Configuration
Edit the contexto variable with your knowledge:
```bash
python
contexto = [
    """
    Add your custom knowledge here.
    Example: "Si preguntan sobre X, responde Y..."
    """
]
Modify RAG_PROMPT_TEMPLATE to adjust bot behavior
```


## 🚀 Usage
Run the chatbot:

```bash
python main.py
Example interaction:
```

Tú: Hola
Bot: ¡Hola! ¿Cómo estás hoy?

Tú: Qué sabes sobre X?
Bot: [Respuesta basada en tu contexto]
Type salir, exit or quit to end the session.

## 🧠 Architecture
Diagram
Code

📂 File Structure
```bash
.
├── main.py          # Main application
├── README.md           # This file
└── requirements.txt    # Dependencies
```

