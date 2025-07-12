#!/bin/bash

export HOME=/tmp
export OLLAMA_MODELS=/tmp/.ollama

ollama serve &
sleep 5
ollama pull tinyllama


# Run the app from src/

streamlit run app.py --server.port=7860 --server.address=0.0.0.0


