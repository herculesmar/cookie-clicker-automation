# 🍪 Cookie Clicker Automation & Strategy Toolkit

A professional **Python + JavaScript injection toolkit** for automating and optimizing gameplay in the browser game **Cookie Clicker**.

This project connects to an existing Chrome session and injects controlled JavaScript logic directly into the game to:

* Automate repetitive actions
* Analyze ascension progress
* Optimize late-game dragon upgrades

⚠️ **Educational & personal-use project**. Not affiliated with Orteil or Cookie Clicker.

---

## 📦 Included Programs

### 🧠 `cookie.py` — Full Automation Bot

A real-time automation engine with modular control.

**Features**

* Ultra-fast big cookie clicking
* Golden cookie detection with delay handling
* Smart upgrade purchasing (ignores toggles & tech switches)
* CPS-efficient building buying strategy
* Automatic wrinkler popping
* Global pause / resume system
* Individual loop toggles via terminal UI

**Design highlights**

* Uses a single global switch: `window.botActive`
* Prevents duplicate intervals
* Safe attach to existing Chrome profile

---

### 📊 `list.py` — Ascension Analyzer

Extracts ascension data for strategic planning.

**Outputs**

* All bought prestige upgrades
* Current heavenly chips
* Total prestige level

Perfect for exporting data to tools (or ChatGPT) to calculate **optimal ascension paths**.

---

### 🐉 `dragon.py` — Final Dragon Upgrade Calculator

Late-game optimization tool for the **"Train Your Dragon"** phase.

**What it does**

* Calculates:

  * Cookie gain from selling buildings above 200
  * Cost to raise buildings below 200
* Determines if the final dragon upgrade is possible
* Shows a clear profit/loss projection
* Executes the strategy **only after user confirmation**

Uses Cookie Clicker’s internal pricing formulas (`getSumPrice`, `getReverseSumPrice`) for accuracy.

---

## 🛠️ Requirements

* Python **3.9+**
* Google Chrome
* Cookie Clicker (official site)

### Python dependencies

```bash
pip install selenium webdriver-manager
```

---

## ▶️ How to Use

### 1️⃣ Start Chrome in debug mode

```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="cc-profile"
```

### 2️⃣ Open Cookie Clicker

Make sure the game is **fully loaded**.

### 3️⃣ Run any script

```bash
python cookie.py
python list.py
python dragon.py
```

---

## ⚠️ Disclaimer

* This project modifies gameplay behavior
* Intended for **learning automation, scripting, and optimization**
* Use only on personal saves

---

## 📄 License

MIT License
