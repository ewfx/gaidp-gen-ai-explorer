# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This project was inspired by the need to automate data validation and filtering based on predefined rules without requiring exact matches. Many organizations deal with large datasets in Excel, where specific fields must adhere to certain compliance or formatting rules.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

Added to PPT

## 💡 Inspiration
This project was inspired by the need to automate data validation and filtering based on predefined rules without requiring exact matches. Many organizations deal with large datasets in Excel, where specific fields must adhere to certain compliance or formatting rules.

## ⚙️ What It Does
Problem Being Solved:
Manual Data Validation is Time-Consuming

Checking each row for compliance with rules takes significant time.

Exact Matches Are Too Strict

Traditional filtering methods require exact text matches, which may miss slight variations.

Rules Are Dynamic & Change Frequently

Hardcoding rules isn't scalable; the system must adapt to new rules dynamically.
## 🛠️ How We Built It
✅ Uses Fuzzy Matching (Levenshtein Distance) to identify similar rule violations.
✅ Gemini LLM Model
✅ Dynamically Loads Rules from an external Excel file, allowing easy updates.
✅ Enables Column Selection, so users can specify which column(s) to validate.
✅ Automates Filtering & Saves Output, reducing manual work.

Python
Gemini LLM model
Python Libraries ( Panda, Flask APIs, Logging, RapidFuzz)
Jquery DataTable
HTML,CSS Bootstrep
Test Cases 
Logging


## 🚧 Challenges We Faced
Reading data based on Rules

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: HTML / CSS/ bootstrep
- 🔹 Backend: Flask API
- 🔹 Database: NA
- 🔹 Other: Gemini Model

## 👥 Team
- **Your Name** - Munesh Sharma
- **Teammate 2** - Shivam Srivastava
- - **Teammate 3** - Aditya Kashyap

