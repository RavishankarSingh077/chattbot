#!/bin/bash

export HOME=/tmp
export OLLAMA_MODELS=/tmp/.ollama

ollama serve &
sleep 10
ollama pull phi




# Run the app from src/

streamlit run app.py --server.port=7860 --server.address=0.0.0.0


