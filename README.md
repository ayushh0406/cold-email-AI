# 📧 Cold Email Generator

**Cold Email Generator** is an AI-powered tool that helps service companies generate personalized cold emails. It extracts job listings from a company's careers page and crafts outreach emails, including relevant portfolio links fetched from a vector database.

---

## 🚀 **How It Works?**

**Example Scenario:**

Imagine **TechSoft Solutions** (a software services company) wants to offer its development expertise to **FinCorp** (a finance company hiring software engineers). Instead of sending generic outreach emails, TechSoft can use this tool to:

✅ Scrape **FinCorp's Careers Page** for job listings.
✅ Use **AI (Groq + LangChain)** to craft personalized cold emails.
✅ Include **Portfolio Links** relevant to the job descriptions.

---

## 🏗 **Project Architecture**

![Architecture](cold-email-AI/imgs/architecture.png)

The system consists of:
- **Streamlit UI** for user interaction.
- **Groq AI Model** for email generation.
- **LangChain + ChromaDB** for vector-based portfolio matching.
- **Web Scraper** to extract job listings.

---

## 🔧 **Setup Instructions**

### **1️⃣ API Key Configuration**
- Get your **Groq API Key** from: [Groq Console](https://console.groq.com/keys)
- Create a `.env` file inside `app/` and add:
  ```env
  GROQ_API_KEY=your_api_key_here
  ```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Run the Application**
```sh
streamlit run app/main.py
```

---

## 📸 **Screenshots**

### **Cold Email Preview:**
![Cold Email Screenshot](cold-email-AI/imgs/img.png).

---

## 📌 **Features**
✅ **Automated Job Listing Extraction** – Scrapes careers pages for openings.
✅ **AI-Powered Email Generation** – Uses Groq + LangChain for personalized outreach.
✅ **Portfolio Matching** – Integrates with ChromaDB to suggest relevant portfolio links.
✅ **User-Friendly Interface** – Built with Streamlit for easy usage.

---

## 🤝 **Contributing**
Want to improve this project? Feel free to fork the repo and create a pull request!

### **Steps to Contribute:**
1. Fork the repository.
2. Clone it to your local system:
   ```sh
   git clone https://github.com/your-username/cold-email-AI.git
   ```
3. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
4. Make your changes and commit:
   ```sh
   git add .
   git commit -m "Added new feature"
   ```
5. Push and open a pull request:
   ```sh
   git push origin feature-branch
   ```

---



