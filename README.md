# 🧮 Premium Python Calculator

> A clean, modern, responsive desktop calculator built entirely with Python, focused on simplicity, usability, and polished light-theme UI design.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/UI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![Tests](https://img.shields.io/badge/Tests-Passing-success.svg)](#running-tests)

---

## 📸 Preview

*A screenshot placeholder for the clean light-theme interface. (To add a screenshot, place your image file in the repository and reference it here).*

---

## ✨ Features

- **➕ Addition:** Add numbers quickly and accurately.
- **➖ Subtraction:** Perform precise subtraction.
- **✖️ Multiplication:** Multiply integers and decimals.
- **➗ Division:** Handle standard division and protect against division by zero.
- **🔢 Decimal Support:** Full support for floating-point calculations.
- **⌨️ Keyboard Input:** Full keyboard support (`0-9`, `.`, `+`, `-`, `*`, `/`, `Enter`/`=`, `Backspace`, `Escape`).
- **🧹 Clear & Backspace:** Easy error recovery and resetting.
- **📱 Responsive Interface:** Intelligently scales and adapts across various window sizes.
- **🛡️ Robust Error Handling:** Graceful handling of edge cases and invalid states without crashing.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application logic and calculation engine |
| **Tkinter** | Native Python GUI framework for the modern light-theme interface |
| **Unittest** | Automated unit testing framework for robust verification |

---

## 📁 Project Structure

```text
python-calculator/
│
├── calculator.py       # Main application & graphical user interface
├── test_calculator.py  # Comprehensive automated unit test suite
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed on your system. (`tkinter` is included with standard Python installations on Windows, macOS, and Linux).

### Running the Application

Clone or download the repository, navigate to the project directory, and run:

```bash
python calculator.py
```

---

## 🧪 Running Tests

To verify the calculator's calculation logic, error handling, and core operations, run the unit test suite:

```bash
python test_calculator.py
```
