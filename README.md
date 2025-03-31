# 🍽️ ByteEats - The Smart Food Ordering Chatbot 🤖

## 🚀 About ByteEats

ByteEats is an intelligent **food ordering chatbot** 🍔, designed to simplify your food cravings using **FastAPI, SQLite3, and a sleek HTML/CSS frontend**. It allows users to **add, remove, track, and complete orders** with a smooth conversational experience! 🌟

---

## 🎯 Features

✅ **Natural Language Ordering** 🗣️ - Order food using simple sentences.  
✅ **Add & Remove Items** ➕➖ - Modify your order on the go.  
✅ **Order Tracking** 📦 - Check your order status anytime.  
✅ **SQLite3 Database** 🗄️ - Persistent order management.  
✅ **Ngrok/Cloudflare Tunnel** 🌍 - Expose your bot online for easy access.  
✅ **Simple Web Frontend** 🎨 - Clean and user-friendly UI for better interactions.  

---

## 🍕 Menu

ByteEats currently serves these delicious items:

- 🥘 **Pav Bhaji**
- 🍽️ **Chole Bhature**
- 🍕 **Pizza**
- 🥭 **Mango Lassi**
- 🌯 **Masala Dosa**
- 🍛 **Biryani**
- 🍔 **Vada Pav**
- 🌮 **Rava Dosa**
- 🥟 **Samosa**

---

## 🏗️ Project Structure

📂 **ByteEats/**  
├── 📁 `app/` - FastAPI Backend  
│   ├── 📄 `main.py` - API Endpoints  
│   ├── 📄 `db_helper.py` - Database functions  
│   ├── 📄 `generic_helper.py` - Utility functions  
│   ├── 📄 `requirements.txt` - Dependencies  
│   ├── 📄 `config.py` - Configuration settings  
│   ├── 📄 `static/` - HTML & CSS Frontend  
│   ├── 📁 `templates/` - HTML files  
├── 📁 `database/` - SQLite3 database  
│   ├── 📄 `food_chatbot.db` - Order storage  
│   ├── 📄 `schema.sql` - Table structure  
└── 📄 `README.md` - This file! 😎  

---

## 🛠️ Tech Stack

- **Backend:** 🐍 FastAPI
- **Database:** 🗄️ SQLite3
- **Frontend:** 🎨 HTML, CSS
- **Tunneling:** 🌍 Ngrok / Cloudflare Tunnel

---

## 🔥 Chatbot Intents & Functions

1️⃣ **Order Food** 🍽️
   - "I want to order Pav Bhaji."
   - "Add 2 Chole Bhature."
   
2️⃣ **Remove Items** ❌
   - "Remove 1 Pizza."
   - "Cancel all Mango Lassi."
   
3️⃣ **Track Orders** 📦
   - "Where is my order?"
   - "Check order #123."
   
4️⃣ **Complete Order** ✅
   - "Place my final order."

---

## 🚀 Getting Started

### 📥 Installation

1️⃣ **Clone the repository:**
```bash
   git clone https://github.com/yourusername/ByteEats.git
   cd ByteEats
```

2️⃣ **Set up a virtual environment:**
```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
```

3️⃣ **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4️⃣ **Run the FastAPI server:**
```bash
   uvicorn app.main:app --reload
```

---

## 🌍 Exposing Chatbot via Ngrok / Cloudflare Tunnel

### 🚀 Using Ngrok:
1️⃣ Install **Ngrok** and run:
```bash
   ngrok http 8000
```

### 🌩️ Using Cloudflare Tunnel:
1️⃣ Install Cloudflare CLI & authenticate.
2️⃣ Run:
```bash
   cloudflared tunnel --url http://localhost:8000
```

Your chatbot is now publicly accessible! 🌎✨

---

## 🎭 Frontend UI

ByteEats has a **simple, elegant HTML & CSS interface** for a seamless ordering experience! 🎨

1️⃣ Navigate to `frontend/index.html`
2️⃣ Open in a browser.

---

## 📌 Future Enhancements

🚀 **Payment Integration** 💳  
🚀 **Voice Commands** 🎙️  
🚀 **Multi-language Support** 🌍  
🚀 **AI-Powered Food Recommendations** 🤖  

---

## ❤️ Contribute

I will love contributions! Fork, clone & submit PRs. Let's make ByteEats even better! 🚀

---

## 📞 Contact

💌 Email: [mayankmittal29042004@gmail.com](mayankmittal29042004@gmail.com)  
🐙 GitHub: [https://github.com/mayankmittal29/](https://github.com/mayankmittal29/)  

---

💖 **Made with love & code! Happy Ordering! 🍕🤖**

