⭐ Overview

Project: Bitcoin Expense Tracker — simple expense tracker in EUR, Lightning, and on-chain with multi-user support.

Status: Functional for development — Flask authentication + per-user data isolation, filtered CSV export.

🧪 Quick tests (end-to-end)

Run the multi-user verification script:

python test_multiuser_e2e.py

This script recreates transazioni.db (removes it if present) and checks that two separate users only see their own transactions and that delete/modify operations require ownership.

🔄 Recent major changes
👥 Multi-user support: each transaction now includes user_id; read/save functions filter by user.

Involved files: db/db_utils.py, app.py, utils/export.py.

🔐 Security improvements:
Added ownership checks for delete/modify on the tables (transazioni, transazioni_lightning, transazioni_onchain). Functions raise PermissionError on unauthorized access.

📤 Improved CSV export:
CSV export functions now accept user_id and generate files containing only the authenticated user’s transactions.

🐞 Bugfixes:
Fixed parameterized SQL queries (various string/tuple issues in SELECT and LIKE queries).

💾 **Relevant files**
app.py: updated routes to pass current_user.id to DB functions.

db/db_utils.py: updated CRUD functions (accept/check user_id).

utils/export.py: CSV exports filtered by user.

test_multiuser_e2e.py: end-to-end test script (creates users, inserts transactions, verifies isolation).

🧠**Good practices and notes**
Always use current_user.id for DB operations in protected routes.

Queries are parameterized (?) to avoid SQL injection.

In production, replace app.secret_key with a secure value and use a WSGI server (gunicorn/uwsgi) and persistent/backup-enabled DB.

🎯**Recommended roadmap**
Make user_id mandatory in export functions to avoid unintended exports.

Add unit tests and CI (GitHub Actions) to run pytest on each PR.

Improve input validation in forms and refine UX error messages.

Consider rate-limiting or caching for external requests (e.g., CoinGecko) if you add historical BTC conversion.

## 📞Contacts / contributions

Open an issue or PR on the GitHub repository for suggestions, bugs, or contributions.

Automatically updated after local changes: db/db_utils.py, app.py, utils/export.py.

# EE - Bitcoin & Euro Expense Tracker

A personal finance tracker built specifically for Bitcoiners. Track your expenses in EUR while automatically calculating Bitcoin (BTC) equivalents, including Lightning Network and on-chain transactions.

## 🌟 Why EE?

Most expense trackers treat Bitcoin as just another "crypto asset". EE is different:

- **Native Lightning Network support** - Track your Lightning transactions separately
- **On-chain transaction tracking** - Full support for regular Bitcoin transactions
- **Automatic BTC/EUR conversion** - Uses historical BTC prices for accurate tracking
- **Privacy-first** - Your data stays local, SQLite database on your machine
- **Open Source** - Built in public, contributions welcome

## ✨ Features

- 📊 **Multi-currency tracking**: EUR, Bitcoin (on-chain), Lightning Network (satoshis)
- 🏷️ **Detailed categorization**: 10+ categories with custom subcategories
- 💱 **Automatic BTC conversion**: Fetches historical BTC prices via CoinGecko API
- 📈 **Balance tracking**: Real-time balance in EUR, BTC, and satoshis
- 📤 **CSV Export**: Export transactions by month or all-time
- 🌐 **Web Interface**: Clean Flask-based UI (plus CLI for power users)
- 🔐 **Local-first**: Your financial data never leaves your computer

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/EE.git
cd EE
```

2. Create virtual environment:

```bash
python -m venv .venv
```

3. Activate virtual environment:

- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the web app:

```bash
python app.py
```

6. Open browser at `http://127.0.0.1:5000`

### CLI Usage

For command-line interface:

```bash
python main.py
```

## 📸 Screenshots

_Coming soon - adding screenshots of the web interface_

## 🗂️ Project Structure

```
EE/
├── app.py              # Flask web application
├── main.py             # CLI interface
├── cli.py              # CLI utilities
├── requirements.txt    # Python dependencies
├── db/                 # Database utilities
│   └── db_utils.py    # DB functions
├── utils/             # Helper modules
│   ├── crypto.py      # BTC price fetching & conversion
│   ├── export.py      # CSV export functions
│   └── helpers.py     # General utilities
├── templates/         # HTML templates
└── static/           # CSS, JS, images
```

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **API**: CoinGecko (BTC prices)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## 📝 Usage Examples

### Adding a Transaction (Web)

1. Navigate to "Nuova Transazione"
2. Select date, category, amount in EUR
3. Automatic BTC conversion happens based on historical price

### Adding Lightning Transaction

1. Go to "Transazioni Lightning"
2. Enter amount in satoshis
3. System calculates EUR equivalent

### Exporting Data

- Export all transactions: `/scarica-csv`
- Export by month: `/scarica-csv-mese` (format: YYYY-MM)

## 🎯 Roadmap

- [x] Multi-user support with authentication
- [ ] Cloud deployment option
- [ ] Mobile-responsive design improvements
- [ ] Tax report generation for crypto transactions
- [ ] Budget planning & forecasting
- [ ] Recurring transaction support
- [ ] Charts & analytics dashboard
- [ ] Integration with wallet APIs (auto-import)

## 🤝 Contributing

This is a learning project built in public! Contributions, issues, and feature requests are welcome.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CoinGecko API for BTC price data
- Flask framework
- The Bitcoin community

## 📧 Contact

Building in public - follow the journey!

---

**Note**: This is an early-stage project. Use at your own risk. Always backup your `transazioni.db` file regularly.
