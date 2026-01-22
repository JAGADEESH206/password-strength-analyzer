#  Password Strength Analyser (Python)

A simple Password Strength Analyser built in Python.  
It checks how strong your password is based on multiple factors and gives you a detailed breakdown of bonuses, penalties, and tips for improvement.

---

# Features

- Checks password length, character variety, and complexity
- Detects repeated, consecutive, and sequential characters
- Penalises over-reliance on one character type
- Rewards balanced and unique passwords  
- Gives a clear rating
- Provides tips to help improve weak passwords  

---

# How It Works

The program calculates a raw score by:
- Adding bonuses for:
  - Length
  - Mixed uppercase/lowercase
  - Numbers and symbols
  - Meeting all 5 password requirements
  - Uniqueness and balance

- Deducting points for:
  - Repeated or consecutive characters
  - Sequential patterns
  - Too many of one character type
  - Using only one type

Finally, it scales your score to a 0–100 range and gives a verdict

---

# How to Run 

1. Hit "Run" at main.py  
2. Enter a password and see the breakdown!

