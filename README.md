# AI Resume Parser (LLM-Powered)

An AI-powered resume parsing system built using Transformer models to extract structured candidate information from PDF resumes. The system uses Named Entity Recognition (NER) and zero-shot classification to semantically identify hard and soft skills without relying on predefined keyword lists, making it ATS-aligned and scalable.

---

## 🚀 Features

- 📄 PDF resume upload
- 🧠 Transformer-based Named Entity Recognition
- 🤖 LLM-style zero-shot skill classification
- 🔍 Extracts:
  - Name
  - Email
  - Phone number
  - Location
  - Experience (company names)
  - Hard skills (technical)
  - Soft skills (behavioral/language)
  - LinkedIn & GitHub links
- 📊 Dynamic table visualization
- 🗑️ Delete resume entries
- ❌ Duplicate detection (email & phone)
- 💾 JSON-based storage (no database)

---

## 🧠 Models Used

| Task | Model |
|----|------|
| Named Entity Recognition | `dslim/bert-base-NER` |
| Skill Classification (Zero-Shot) | `facebook/bart-large-mnli` |

---

## 🏗️ Tech Stack

### Backend
- Python
- Flask
- Hugging Face Transformers
- PyPDF2

### Frontend
- HTML
- CSS
- Vanilla JavaScript

---

## 📁 Project Structure

