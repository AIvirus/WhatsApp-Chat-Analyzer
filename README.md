# 📜 WhatsApp Chat Analyzer

## 📌 Overview
The **WhatsApp Chat Analyzer** is a Streamlit-based web application that provides deep insights into WhatsApp chat data. Users can upload a chat file, analyze message statistics, activity trends, and even visualize common words and emoji usage. 📊  

## 🚀 Features
- 📁 Upload WhatsApp chat text files for analysis  
- 📊 Generate statistics (messages, words, media, and links count)  
- 📆 View monthly and daily activity trends  
- 📅 Weekly activity heatmaps  
- 🔥 Identify the most active users in a group chat  
- ☁️ WordCloud and common words visualization  
- 😀 Emoji usage analysis  

## 📂 Folder Structure
```
WhatsAppChatAnalyzer/
│── app.py                    # Main Streamlit app
│── helper.py                  # Helper functions for data processing
│── preprocessor.py            # Data cleaning and preprocessing
│── requirements.txt           # Dependencies
│── stop_hinglish.txt          # Stopwords for text processing
│── testing.py                 # Test script
│── .devcontainer/             # VS Code dev container configuration
│── __pycache__/               # Compiled Python files
```

## ⚡ Installation

### 📥 Clone this repository
```sh
https://github.com/AIvirus/WhatsApp-Chat-Analyzer.git
cd WhatsApp-Chat-Analyzer
```

### 📦 Install dependencies
```sh
pip install -r requirements.txt
```

## 🎯 Usage

### ▶️ Run the Application
```sh
streamlit run app.py
```

### 📤 Upload a WhatsApp Chat File
1. Export a chat from WhatsApp (without media).  
2. Upload the exported `.txt` file in the sidebar.  
3. Click "Show Analysis" to generate insights.  

## 📊 Analysis Features

### 📌 Message Statistics
- 📝 **Total messages**  
- 🔤 **Total words**  
- 🖼 **Media files shared**  
- 🔗 **Links shared**  

### 🗓 Time-based Analysis
- 📆 **Monthly & Daily timeline**  
- 📊 **Most active days & months**  
- 📅 **Weekly activity heatmap**  

### 🔥 Most Active Users (Group Chats)
- Identifies the most engaged members  
- Displays activity distribution  

### 🌟 WordCloud & Common Words
- Shows the most frequently used words in chat  

### 😂 Emoji Analysis
- Displays most used emojis and their frequency  

## ⚖️ License
🔒 **All rights reserved by the author.**  
- 📚 Free for educational and research purposes.  
- 🚫 Commercial use requires permission.  
