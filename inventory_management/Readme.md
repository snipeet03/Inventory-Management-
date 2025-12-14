# 📦 Inventory & Assembly Management System (Django)

## 📌 Overview
The **Inventory & Assembly Management System** is a Django-based web application developed to digitize and automate warehouse inventory operations.  
It replaces manual record-keeping with a **real-time, database-driven platform** that enables accurate stock tracking, assembly validation, and analytical dashboards.

The system is designed for industrial use cases where components such as **needles** and **nozzles** are uniquely identified using **BAP numbers** and **Alpha numbers**, ensuring precise traceability and operational efficiency.

---

## 🎯 Problem Statement
Traditional inventory systems rely on manual data entry, which leads to:
- Delayed and non-real-time inventory updates
- Human errors in stock management
- No analytical insights for decision-making
- Difficulty in validating assembled components

This project addresses these challenges by providing a **centralized, scalable, and real-time inventory management solution**.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python 3.9)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** PostgreSQL / SQLite (development)
- **Data Processing:** Pandas
- **Visualization:** Plotly
- **Server:** Django Development Server
- **Version Control:** Git & GitHub

---

## ⚙️ Key Features
- 🔐 User authentication and role-based access
- 📥 Inventory add, update, and remove functionality
- 🧩 Assembly validation using BAP and Alpha numbers
- 📊 Real-time inventory dashboards
- 📈 Data analysis and visualization using Plotly
- 📄 Excel-based master data integration
- 🔄 Live stock status tracking
- 🗂️ Modular and scalable Django architecture

---

## 🏗️ System Architecture
- **Models:** Structured schemas for inventory, assembly, and user data
- **Views:** Business logic for inventory and assembly workflows
- **Templates:** Responsive UI built with Bootstrap
- **Database Layer:** PostgreSQL for reliable and scalable storage
- **Data Flow:**  
  Inventory Entry → Django Models → Database → Pandas Processing → Plotly Visualization

---

## 🧪 Testing & Validation
- Django form and model validation
- Database integrity checks
- Excel file and data consistency validation
- Manual functional testing of inventory workflows

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/snipeet03/Inventory-management-.git
cd inventory_management
