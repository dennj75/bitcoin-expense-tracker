# ₿ Bitcoin Expense Tracker (₿-ET)

A personal finance tracker built specifically for **Bitcoiners**. Track your expenses in EUR while automatically calculating real-time Bitcoin (**BTC**) equivalents, with full support for the Lightning Network and on-chain transactions.

[![GitHub license](https://img.shields.io/github/license/dennj75/bitcoin-expense-tracker?style=flat-square)](LICENSE)
[![GitHub stars](https://imgpl.io/github/stars/dennj75/bitcoin-expense-tracker?style=flat-square)](https://github.com/dennj75/bitcoin-expense-tracker/stargazers)

---

## 🌟 Why This Project?

Most expense trackers treat Bitcoin as just another "crypto asset." Bitcoin Expense Tracker is different:

- ⚡ **Native Lightning Network:** Track your Lightning transactions separately with satoshi precision.
- 🔗 **On-chain Transaction Tracking:** Full support for regular Bitcoin transactions and fee management.
- 💱 **Automatic BTC/EUR Conversion:** Uses historical BTC prices for accurate expense tracking.
- 🔐 **Privacy-First:** Your data stays local, stored in an SQLite database on your machine.
- 🆔 **Nostr Authentication:** Log in with your Nostr identity (via nos2x browser extension).
- 👥 **Multi-user Support:** Complete data isolation between different users.
- 🌐 **Open Source:** Built in public, contributions are welcome.

---

## 📸 Screenshots

Here are some views of the Bitcoin Expense Tracker interface:

### Dashboard & EUR Tracking

![Screenshot of the main dashboard showing EUR transactions and Bitcoin conversion.](static/dashboard.png)

### Lightning Transaction View

![Screenshot of the Lightning Transaction input screen.](static/lightning.png)

---

## ✨ Features

### 💰 Multi-Currency Tracking

- **EUR** - Traditional fiat transactions.
- **Bitcoin (On-chain)** - Regular BTC transactions with fee tracking.
- **Lightning Network** - Satoshi-level precision for Lightning payments.

### 🔐 Flexible Authentication

- **Traditional Login** - Standard Username/Password authentication.
- ⚡ **Nostr Login** - Decentralized authentication using NIP-07 (nos2x extension):
  - Sign in with your existing Nostr identity.
  - Schnorr signature verification (BIP340).
  - No password needed.

### 📊 Financial Management

- **Detailed Categorization:** 10+ categories with custom subcategories.
- **Automatic BTC Conversion:** Fetches historical BTC prices via CoinGecko API.
- **Real-time Balance:** View your balance in EUR, BTC, and satoshis.
- **CSV Export:** Export transactions by month or all-time.

### 🛡️ Security & Privacy

- **Local-First:** Your financial data never leaves your computer.
- **User Data Isolation:** Complete separation between user accounts.
- **SQL Injection Protection:** Uses parameterized queries.

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8+
- **pip** (Python package manager)
- _Optional:_ **nos2x** browser extension for Nostr login.

### Installation

1.  Clone the repository

```bash
git clone https://github.com/yourusername/EE.git
cd EE
```

2. Create virtual environment:

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

inux / Mac:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python app.py
```

5. Open your browser  
   Access the application at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 📖 Usage WorkflowFirst Time SetupCreate an Account:

Click **_"Registrati"_** for a traditional account OR Click **_"Login with Nostr"_** if you have the nos2x extension installed.

- Start Tracking:Use **_"Nuova Transazione"_** for EUR expenses.
- Use **_"Transazioni Lightning"_** for Lightning payments.
- Use **_"Transazioni On-chain"_** for regular Bitcoin transactions.
- Adding EUR Transactions (Automatic Conversion)Go to "Nuova Transazione".
  - Select date, category, and amount in EUR.The system automatically converts to BTC based on the historical price for that date.

### Adding Lightning / On-chain

- TransactionsLightning:  
  Navigate to "Transazioni Lightning" and enter the amount in satoshis. The system calculates the EUR equivalent.On-chain: Go to "Transazioni On-chain" and enter transaction details, including fees.

### Exporting DataExport all transactions:

- Click "Scarica CSV."Export by month: Select the month in YYYY-MM format.

## ⚡ Nostr Login Details

Bitcoin Expense Tracker leverages the Nostr protocol for decentralized authentication:FeatureDescriptionPassword-lessAuthentication based on the cryptographic signature of your Nostr key.Unified IdentityUse the same Nostr identity you use for other Nostr-enabled apps.  
NIP-07 StandardUses browser extensions (like nos2x) to sign requests without exposing your private key.  
How to Use Nostr LoginInstall nos2x:

- Install the nos2x extension (Chrome/Brave/Firefox).
- Set up Keys: Generate new keys or import your existing Nostr keys (NPUB/NSEC) in the extension.

### Log in to App 🚀:

- On the login page, click "Login with Nostr.  
  The nos2x extension will prompt you to approve the signature of a challenge.Approve the request, and you are logged in!

### 🧪 TestingRunning

Multi-user Tests (E2E)Verify that user data isolation works correctly by running the End-to-End test script:Bashpython test_multiuser_e2e.py  
 This automated script performs the following checks:Creates multiple test users.Inserts transactions for each user.Verifies that each user only sees their own data.Tests ownership checks during delete/modify operations.

### 📁 Project Structure bitcoin-expense-tracker/

```
├── app.py # Main Flask web application
├── auth.py # Authentication blueprint (traditional & Nostr)
├── requirements.txt # Python dependencies
├── db/
│ └── db_utils.py # SQLite database utilities
├── utils/
│ ├── crypto.py # BTC price fetching (CoinGecko) and conversion
│ └── export.py # CSV export logic
├── templates/ # HTML templates (login, index, transactions, etc.)
└── static/ # CSS, JavaScript, images
```

### 🛠️ TechStack

Component Technology Role

- **Backend**: Flask (Python)
- **Database**: SQLite
- **API**: CoinGecko (BTC prices)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **_Authentication_** Flask-Login + Nostr (NIP-07)Session management and Nostr login Cryptography coincurve BIP340/Schnorr signatures implementation External

## 🔄 Change Log v2.0

### 🦤Nostr Authentication (Latest)

⚡ Nostr login implemented with nos2x extension support.  
🔐 BIP340 Schnorr signature verification.  
📝 Database separation: transazioni.db (transactions) and database.db (users).v1.5 - Multi-user Support  
👥 Each transaction linked by user_id.  
🔒 Ownership checks for delete/modify operations enforced.  
📊 Per-user data isolation and filtered CSV exports.v1.0 - Core Features  
💰 EUR, Lightning, and on-chain tracking.💱 Automatic BTC conversion via CoinGecko.  
🏷️ Category and subcategory management.

## 🗺️ Roadmap

### 🎯 Priority Goal

### Short Term

- [ ] Mobile responsive design improvements and Dark Mode support.
- [ ] Transaction search and advanced filtering functionality.

### Medium Term

- [ ] Charts & analytics dashboard for financial insights.
- [ ] Recurring transaction support and tax report generation.

### Long Term

- [ ] Integration with Lightning wallet APIs (automatic import).

## 🤝 Contributing

### Contributions are welcome!

This is a learning project built in public! Contributions, issues, and feature requests are welcome.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

Always use parameterized SQL queries to prevent SQL injection.  
 Always check current_user.id for data modification operations.  
 Add tests for new features.

## ⚠️ Disclaimer and Security

This is an early-stage project built for learning purposes. Use at your own risk.

## ⚠️ Backup:

Always backup your transazioni.db and database.db files regularly.  
 🔒 Nostr Keys: Never share your Nostr private keys (NSEC).  
 ⚙️ Production: For production deployment, use a strong app.secret_key, enable HTTPS, and consider using a WSGI server (e.g., Gunicorn/uWSGI).  
 📬 Contact & SupportIssues: GitHub IssuesDiscussions: GitHub

Discussions Building in public 🚀 | Stay humble, stack sats ⚡
