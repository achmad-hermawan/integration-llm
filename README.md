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
<img width="1919" height="976" alt="image" src="https://github.com/user-attachments/assets/2e0a2be3-9426-40c4-bb6e-4749ac0e4e2d" />
