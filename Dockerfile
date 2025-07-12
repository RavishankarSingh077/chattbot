FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# ✅ Set safe working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make sure start.sh is executable
RUN chmod +x start.sh

# Expose Hugging Face default port
EXPOSE 7860

# Start everything (Ollama + Streamlit)
CMD ["./start.sh"]

