# 📌 AidBridge - Earthquake Aid Evaluation and Disaster Management System

## 📖 Project Description

**The Earthquake Aid Evaluation and Disaster Management System** is an AI-powered platform that integrates post-disaster need assessment, aid distribution, feedback collection, real-time earthquake tracking, and donation management. Users can request aid, provide feedback, donate, and get directions to the nearest assembly area in case of emergencies.

## 🎯 Objectives

- 🎯 Make disaster aid processes **transparent, fast, and efficient**  
- 🧭 Provide **decision support systems** powered by real-time data  
- 🙌 Systematically evaluate aid recipients' needs and experiences  
- 🧠 Ensure **prioritization and resource optimization** using AI  
- 💬 Unite citizens, donors, and authorities on a single platform  

## 🛠️ Features

- ✅ Aid request form (personal, location, needs, and health information)  
- ✅ Aid feedback / complaint / suggestion submission  
- ✅ Real-time **earthquake tracking and map integration** (via AFAD / Kandilli APIs)  
- ✅ Displays the **nearest emergency assembly area** based on user location  
- ✅ **Navigation support** via map (Google Maps API integration)  
- ✅ Ability to donate directly through the system  
- ✅ AI-powered **automatic prioritization and classification**  
  - (e.g., families with children, individuals with medical conditions, etc.)  

## 🧠 AI Integration

- 🤖 **Prioritization Engine**: Ranks aid requests based on variables like age, number of people, health status, and shelter needs  
- 🗺️ **Critical Zone Detection**: Highlights regions with dense aid requests  
- 🧭 **Assembly Point Prediction**: Recommends alternative gathering points if one is overcrowded  
- 💡 **AI Decision Assistant**: Suggests optimal intervention sequences to authorities  

## 🖥️ Technologies Used

| Layer              | Technology                                  |
|--------------------|---------------------------------------------|
| Backend            | Python (FastAPI)                            |
| Frontend           | Bootstrap                                   |
| Database           | SQL                                         |
| Map & Navigation   | Leaflet.js, Google Maps API, OpenStreetMap  |
| Earthquake APIs    | AFAD, Kandilli Observatory                  |
| Artificial Intelligence | Gemini API and Langchain Integration     |

## 🚀 Setup

```bash
git clone https://github.com/Melihemin/AidBridge/
cd AidBridge
pip install -r requirements.txt
python main.py  # or use the following for live development
uvicorn main:app --reload
