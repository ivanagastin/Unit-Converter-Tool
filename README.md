# Intern ID : CITS1699

#  Unit Converter Tool

A modern, feature-rich **Unit Converter desktop app** built with Python and Tkinter.  
Uses the **Base-Unit Algorithm**: converts input → base unit → target unit for maximum accuracy and scalability.

---

## 🚀 Features

- ✅ **13 Categories** — Length, Weight, Temperature, Volume, Area, Speed, Time, Digital Storage, Pressure, Energy, Power, Angle, Frequency
- ✅ **100+ Units** supported
- ✅ **Live conversion** as you type
- ✅ **⇅ Swap** units instantly
- ✅ **📋 Copy** result to clipboard
- ✅ **History panel** — logs last 50 conversions
- ✅ **Dark themed** premium UI
- ✅ **Smart formatting** — scientific notation for very large/small values

---

## 🧠 Algorithm

```
Input Value  →  ×  from_unit_factor  →  Base Unit
Base Unit    →  ÷  to_unit_factor    →  Output Value
```

Temperature and Fuel Economy use dedicated non-linear formulas.

---

## 🛠️ Requirements

- Python 3.7+
- `tkinter` (included with standard Python installation)

---

## ▶️ How to Run

```bash
python unit_converter.py
```

---

## 📁 Project Structure

```
unit-converter/
│
└── unit_converter.py   # Main application (all-in-one)
```

---

## 📜 License

MIT License — free to use and modify.
