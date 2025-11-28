# 🍺 **BrewBuddy – Beverage Manager for Student Houses**

## 📌 **Overview**

BrewBuddy is a website designed to help students living together manage their shared drink inventory.
It solves common house issues like:

* *“Who drank the last beer?”*
* *“Do we still have drinks left?”*
* *“Who needs to restock?”*

With BrewBuddy, housemates can track drinks, see what's in stock, add favorites, create a shopping list, view their profile, and log in using either a normal account or Google authentication.

---

## ⭐ **Features**

### 🏠 General

* Clean homepage with hero section, about section, team section & contact form
* EmailJS-powered contact system (no backend needed)

### 🔐 Authentication

* Standard login & signup
* Strong password validation
* Google login (OAuth2)
* Session-based authentication

### 🍺 Inventory & Drinks

* Drinks displayed with image, description & count
* Add/remove favorite beers
* Dashboard shows available beers

### 🧑‍💻 User Profile

* Update name, email, phone number, date of birth
* Upload profile picture
* View personal info

### 🧾 Database Tables (SQLite)

* Users
* Drinks
* Consumption
* Shopping List
* Expenses
* Favorites

---

## 🧱 **Tech Stack**

| Layer          | Technology            |
| -------------- | --------------------- |
| Frontend       | HTML, CSS, JavaScript |
| Backend        | Flask (Python)        |
| Authentication | Google OAuth 2.0      |
| Contact System | EmailJS               |
| Database       | SQLite                |
| Templates      | Jinja HTML Templates  |
| Tools          | VSCode, Git/GitHub    |

---

## 📁 **Project Structure**

```
BrewBuddy/
│── app.py
│── models.py
│── brewbuddy.db
│── .env
│── static/
│     ├── style.css
│     ├── BeerIcons/
│     ├── uploads/
│── templates/
│     ├── home.html
│     ├── dashboard.html
│     ├── favourites.html
│     ├── profile.html
│     ├── basket.html
│── README.md
```

---

## ⚙️ **Installation & Setup**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/BrewBuddy.git
cd BrewBuddy
```

### 2️⃣ Install Dependencies

```bash
pip install flask flask_sqlalchemy google-auth google-auth-oauthlib python-dotenv werkzeug
```

### 3️⃣ Create `.env` File

Add your keys:

```
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 4️⃣ Run the App

```bash
python app.py
```

Visit: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🗄️ **Database Overview**

SQLite database: `brewbuddy.db`

### 📌 Tables:

| Table        | Purpose                                 |
| ------------ | --------------------------------------- |
| User         | Stores account data & login info        |
| Drink        | Beer name, description, image, quantity |
| Favourite    | Users’ favorite drinks                  |
| ShoppingList | What the house needs to buy             |
| Expense      | Tracks spending                         |
| Consumption  | Who drank what & when                   |

---

## 📧 **EmailJS Setup (Contact Form)**

1. Create an EmailJS account
2. Create a service
3. Create a template
4. Add your **public key**, **template ID**, and **service ID** in `home.html`

Example:

```js
emailjs.send("service_xxx", "template_xxx", params)
```

---

## 🔐 **Google Login Setup**

Follow steps at:
[https://developers.google.com/identity/protocols/oauth2](https://developers.google.com/identity/protocols/oauth2)

Required:

* OAuth 2.0 Client ID
* Client Secret
* Redirect URI:
  `http://127.0.0.1:5000/login/google/callback`

---

## 📸 **Screenshots**
<img width="1898" height="1017" alt="image" src="https://github.com/user-attachments/assets/2b76a357-4e9d-4d91-b150-283a5d46294f" />
<img width="1888" height="1035" alt="image" src="https://github.com/user-attachments/assets/0f17a6a6-2a1e-40f5-8f73-fbbf381d4ba8" />
<img width="1919" height="610" alt="image" src="https://github.com/user-attachments/assets/aa71eecf-ad97-468d-b563-8a74b3d7d50b" />
<img width="1902" height="1031" alt="image" src="https://github.com/user-attachments/assets/831eddab-998f-4587-afaa-490fa8ba12f9" />

---

## 👥 **Team**

| Name    | Role                             |
| ------- | -------------------------------- |
| Hasan   | Backend                          |
| Mirthe  | Designer                         |
| Lucas   | Backend                          |
| Enas    | Frontend + Backend + Git Manager |
| Sueda   | Frontend                         |
| Daniela | Frontend + Backend               |

---

## 📝 **License**

This project is created for educational purposes by students at **Fontys ICT**.

Just tell me!
