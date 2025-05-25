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
- ☁️ **Snowflake Integration**: Connects live to a Snowflake database for scalable querying.
- 🔒 **Secrets Protected**: Credentials are stored securely using `.streamlit/secrets.toml`.

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: Snowflake
- **Data Processing**: Pandas
- **Mapping**: Pydeck / Streamlit Map

---

## 📷 Snapshots

![image](https://github.com/user-attachments/assets/782e63df-ea9d-420d-bb60-0c42820b66cd)
with filters applied:
![image](https://github.com/user-attachments/assets/4707b7e6-1e34-4d86-9f22-119566f2b56e)
some analytics from the data:
![image](https://github.com/user-attachments/assets/3689d20d-1725-4d72-b946-022a9e4b4cbd)


## 🎥 Demo

[![Watch the Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=[YOUR_VIDEO_ID_HERE](https://youtu.be/i902YFKiJ4M))

> Click the image above to watch the full demo on YouTube.

---

## dependencies
Install dependencies:
- pip install -r requirements.txt
---
#note
For the sake of prototype i have limited to just one state if selected i will impletement for full country with the available data.
