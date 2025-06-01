# 🏛️ Heritage Sites Dashboard – YourStory x Snowflake Hero Challenge

A Streamlit-powered interactive dashboard to explore, analyze, and visualize heritage site information in Tamil Nadu using Snowflake as the data backend. This solution bridges cultural insights with modern data infrastructure.

---

## 🚀 Project Objective

To build a lightweight yet powerful tool that makes heritage site information more accessible and meaningful through:
- **Real-time filtering** (state, city, type, use)
- **Map-based visualization** using geolocation data
- **Secure integration with Snowflake** for cloud data warehousing
- A smooth UI built with **Streamlit** for intuitive exploration

---

## 📌 Features

- 🔍 **Dynamic Filters**: Choose your city, type, or use — the map and table update instantly.
- 🗺️ **Interactive Map**: See heritage locations visually with tooltips and zoom.
- 📊 **Data Table View**: Filtered heritage data in a tabular format.
- 📈 **Analytics View**: Visual charts showing city-wise and type-wise heritage distributions.
- ☁️ **Snowflake Integration**: Connects live to a Snowflake database for scalable querying.
- 🔒 **Secrets Protected**: Credentials are stored securely using `.streamlit/secrets.toml`.

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: Snowflake
- **Data Processing**: Pandas
- **Mapping**: Pydeck / Streamlit Map
- **Visualization**: Matplotlib

---

## 📷 Snapshots

![image](https://github.com/user-attachments/assets/782e63df-ea9d-420d-bb60-0c42820b66cd)

*With filters applied:*

![image](https://github.com/user-attachments/assets/4707b7e6-1e34-4d86-9f22-119566f2b56e)

*Some analytics from the data:*

![image](https://github.com/user-attachments/assets/bb99396b-2ef9-40a9-bdd1-7dddcb856331)


---

## 🎥 Demo

[![Watch Demo](https://img.youtube.com/vi/i902YFKiJ4M/0.jpg)](https://youtu.be/i902YFKiJ4M)

> Click the image above or the link below to watch the full demo on YouTube.

🔗 **Demo YouTube Link**: https://youtu.be/i902YFKiJ4M

---

## 🚀 Live App

👉 **Live Streamlit App**: [https://your-story-challenge-8re2xtuchycke5f2dtgzs2.streamlit.app/](https://your-story-challenge-8re2xtuchycke5f2dtgzs2.streamlit.app/)

No installation required — just open the link in your browser!

---

## 🧑‍💻 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/stargalax/Your-story-challenge.git
cd Your-story-challenge
```
### 2. Install Dependencies
``` bash
pip install -r requirements.txt
```
### 3. Add snowflake credentials
*create a file named: .streamlit/secrets.toml*
Then paste your details
- [snowflake]
- user = "your_username"
- password = "your_password"
- account = "your_account"
- warehouse = "your_warehouse"
- database = "your_database"
- schema = "your_schema"
### 4. Run the app
``` bash
streamlit run app.py
```
The app will open in browser at: http://localhost:8501

---


> Due of time constraint I have implemented the project with just data from one state ,  I will implement the project for rest of States and scale it with apis to fetch popularity and foot fall


