# Intelligent-Enterprise-Assistant

# Problem Statement

Develop an intelligent chatbot using deep learning and NLP to respond to employee queries in a large public sector organization. The chatbot should handle HR, IT, and organizational topics, process documents, summarize content, support 2FA (email-based), and maintain response times under 5 seconds.

# Overview / Architecture

# Components:

Backend API — FastAPI (async) serving chat, doc-upload, summarization, 2FA, and admin endpoints.

NLP core — combination of a small transformer-based retrieval-augmented approach for fast, accurate answers: (a) semantic search over FAQ/Policy docs using SentenceTransformers + FAISS, (b) fallback to a lightweight seq2seq summarizer/generator for free-form queries using facebook/bart-large-cnn or t5-small for demo.

Document processing — PDF / DOCX text extraction using PyMuPDF (fitz) and python-docx. Extracted text is chunked & embedded into the FAISS index.

Profanity filter — dictionary-based (configurable wordlist) filtering and masking.

2FA via email — generate short OTP, send via SMTP (or transactional email provider), verify.

Frontend — simple React app to demo chat, upload documents, and 2FA flow.

Caching & Concurrency — Redis for OTP expiry and session caching; run backend with Uvicorn + multiple workers. Use async endpoints so 5 concurrent users easily handled.

# Non-functional goals achieved in demo:

Response time: optimize using local embedding DB (FAISS) and small models to keep <5s for typical queries.

Scalability: docker-compose with Redis and Uvicorn; horizontally scale worker count.

# Performance Goals

Response Time: ≤ 5 seconds for common queries.

Parallel Users: 5+ concurrent users (async FastAPI + multiple workers).

Extensibility: Modular design to plug in LLM or enterprise APIs.

# Future Enhancements

Integrate LLM API (OpenAI / Llama 2) for natural responses.

Add voice interface using SpeechRecognition and TTS.

Store embeddings in persistent vector DB (Weaviate / Milvus).

Add admin panel for HR/IT policy uploads and monitoring.

Deploy on cloud (AWS/GCP/Azure) with HTTPS and autoscaling.
