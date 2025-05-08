# 🌍 Disaster Aid Request & Prioritization System

A FastAPI-based platform for collecting disaster aid requests, prioritizing them using AI (Google Gemini), and helping authorities respond to critical cases faster and smarter.

[![App Demo]()](https://youtu.be/t63dkufoD70)

## 🚀 Features

### ✅ Aid Request Submission
- Users can submit aid requests by filling out a detailed form.
- Collected fields: `name`, `surname`, `age`, `phone`, `email`, `address`, `patients`, `needs`, `health_status`, `shelter_status`.

### 🧠 AI-Powered Prioritization
- Integrated with **Google Gemini (via LangChain)**.
- AI analyzes submissions and assigns a **priority score between 1 and 100**, along with an explanation.
- Prioritization criteria:
  1. Age (high priority if under 18 or over 65)
  2. Health status (urgent, chronic, or disabled conditions)
  3. Shelter status (unsafe or outdoor living conditions)
  4. Number of dependents (e.g., elderly or children)
  5. Type of needs (water, food, medicine, etc.)
  6. Location-based risk (evaluated via address)

### 📦 CSV Export
- All submissions can be exported as a **UTF-8 BOM compatible CSV** file for Excel use.

### 🔍 Filtering by Priority
- Easily access urgent requests via `/high_priority` (score ≥ 70).

### 🧹 AI Moderation (Planned)
- Optional expansion for spam or misinformation detection via Gemini content analysis.

---

## 🛠️ Installation

### 1. Requirements

```bash
Python 3.9+
FastAPI
SQLAlchemy
Jinja2
Google Generative AI
langchain-google-genai
python-dotenv
beautifulsoup4
markdown
```

### 2. Environment Setup
Create a .env file and add your Google API key:

```env
GENAI_API_KEY=your_google_generative_ai_key
```

3. Run the Project
```bash
uvicorn main:app --reload
```

Then open: http://localhost:8000/

## Project Structure
```bash
📦project_root
 ┣ 📂templates
 ┃ ┣ 📜aid_list.html
 ┃ ┣ 📜new_aid.html
 ┃ ┗ 📜donate.html
 ┣ 📂database
 ┃ ┣ 📜models.py
 ┃ ┗ 📜settings.py
 ┣ 📜main.py
 ┣ 📜router_aid.py
 ┣ 📜.env
 ┗ 📜README.md
```

## API Endpoints

| Method | URL                   | Description               |
| ------ | --------------------- | ------------------------- |
| `GET`  | `/aid/`               | List all aid requests     |
| `GET`  | `/aid/create`         | Display new request form  |
| `POST` | `/aid/create_request` | Submit a new aid request  |
| `GET`  | `/aid/high_priority`  | List high-priority cases  |
| `GET`  | `/aid/donate`         | Static donation info page |
| `GET`  | `/aid/export-csv`     | Download aid data as CSV  |

## Sample AI Evaluation

```json
{
  "name": "Melih Emin",
  "surname": "Kilicoglu",
  "age": 20,
  "phone": "505*****",
  "email": "melihemin10@gmail.com",
  "address": "Gaziantep",
  "patients": 3,
  "needs": "water shoes clothes bread",
  "health_status": "pharyngitis asthma reflux",
  "shelter_status": "our house is solid but I feel scared"
}
```

## AI Output:

```pgsql
85
This individual is young but responsible for 3 people. They report chronic health issues (asthma, reflux) and unsafe feelings at home. Basic needs like food and water are listed. Located near an earthquake zone.
```
## 📬 Suggestions for Improvement
- 📦 Add donation module (inventory, aid matching)
- 📈 Visual dashboards (charts, maps, stats)
- 🔒 Add admin login & auth
-🌐 Support multi-language (EN/TR/AR)

## 🤝 Contribution
Feel free to fork, improve or expand the project. Contributions are welcome!
