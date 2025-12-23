# 🛡️ Nexus Enterprise Data Assistant

Chatbot analisis data berbasis AI yang dirancang dengan arsitektur **Secure & Modular**. Menggunakan model **LLaMA 3.1 (Local)** untuk privasi data total.

## 🚀 Fitur Unggulan (Technical Highlights)

1.  **Modular Architecture:** Kode dipisah berdasarkan tanggung jawab (Database, LLM Logic, Config, UI). Mudah di-scale.
2.  **Security Sanitization Layer:** Mencegah *SQL Injection* atau perintah berbahaya (DELETE/DROP) dengan filter logic sebelum eksekusi database.
3.  **Local LLM Inference:** Menggunakan Ollama (LLaMA 3.1) yang berjalan offline. Tidak ada data perusahaan yang dikirim ke cloud/API publik.
4.  **Robust Error Handling:** Sistem tetap stabil meskipun AI memberikan output yang tidak valid.

## 📂 Struktur Proyek
- `modules/database.py`: Menangani koneksi SQL & Security Check.
- `modules/llm.py`: Interface ke Ollama.
- `main.py`: Orchestrator aplikasi (Streamlit).

## 📸 Screenshots
[Tempel Screenshot kamu disini]