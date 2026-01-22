import math
import string
import sys

print("Password Strength Analyser")

print("\nRecommended Password Rules:")
print(" - At least 14 characters long")
print(" - At least 1 lowercase character")
print(" - At least 1 uppercase character")
print(" - At least 1 number")
print(" - At least 1 symbol\n")


# === password input + validation check ===
pw = input("Enter your password: ")

if not pw.strip():
    print("Error: Password cannot be empty or consisting of only spaces/tabs.")
    sys.exit(1)
elif not pw.isascii():
    print("Error: Unsupported characters detected. Use standard ASCII letters/digits/symbols.")
    sys.exit(1)


s = pw
pw = pw.strip()
length = len(pw)
lowered = pw.lower()


# Analyse password
n_alpha = sum(1 for ch in pw if ch.isalpha())
n_upper = sum(1 for ch in pw if ch.isupper())
n_lower = sum(1 for ch in pw if ch.islower())
n_digit = sum(1 for ch in pw if ch.isdigit())
n_symbol = sum(1 for ch in pw if not ch.isalnum())


# === ADDITIONS ===
adds = 0

# 1) Length
base = length * 4
if length >= 20:
    base += 10
elif length >= 16:
    base += 5
adds += base

# 2) Uppercase letters
if n_upper == length:
    up_bonus = 0
elif n_alpha == length:
    up_bonus = n_upper
    adds += up_bonus
else:
    up_bonus = n_upper * 2
    adds += up_bonus 

# 3) Lowercase letters
if n_lower == length:
    low_bonus = 0
elif n_alpha == length:
    low_bonus = n_lower
    adds += low_bonus
else:
    low_bonus = n_lower * 2
    adds += low_bonus

# 4) Numbers
if n_digit == length:
    dig_bonus = 0
else:
    dig_bonus = n_digit * 2
    adds += dig_bonus

# 5) Symbols
if n_symbol == length:
    sym_bonus = 0
else:
    sym_bonus = n_symbol * 3
    adds += sym_bonus

# 6) Unique characters
unique = len(set(pw))
adds += unique

# 7) Requirements met
req_len = 1 if length >= 14 else 0
req_up = 1 if n_upper > 0 else 0
req_low = 1 if n_lower > 0 else 0
req_dig = 1 if n_digit > 0 else 0
req_sym = 1 if n_symbol > 0 else 0

req_met = req_len + req_up + req_low + req_dig + req_sym
req_bonus = req_met * 2
adds += req_bonus
if req_met == 5:
    req_bonus += 10
    adds += 10
elif n_upper and n_lower and n_digit and n_symbol:
    req_bonus += 3
    adds += 3


# === DEDUCTIONS ===
deds = 0
# 1) Letters only / too many letters
if n_alpha == length:
    letter_penalty = length * 2
    deds += letter_penalty
elif n_alpha / length >= 0.7:
    letter_penalty = n_alpha
    deds += letter_penalty

# 2) Numbers only / too many digits
if n_digit == length:
    dig_penalty = length * 2
    deds += dig_penalty
elif n_digit / length >= 0.7:
    dig_penalty = n_digit
    deds += dig_penalty

# 3) Symbols only / too many symbols
if n_symbol == length:
    sym_penalty = length * 2
    deds += sym_penalty
elif n_symbol / length >= 0.7:
    sym_penalty = n_symbol
    deds += sym_penalty


# 4) Repeated characters (case insensitive)
repeat_count = 0
for i in range(length-1):
    if lowered[i] == lowered[i+1]:
        repeat_count += 1
repeat_penalty = repeat_count ** 2
deds += repeat_penalty

# 5) Consecutive uppercase characters
cons_upper = sum(1 for i in range(length-1) if pw[i].isupper() and pw[i+1].isupper())
cons_upper_penalty = cons_upper * 2
deds += cons_upper_penalty

# 6) Consecutive lowercase characters
cons_lower = sum(1 for i in range(length-1) if pw[i].islower() and pw[i+1].islower())
cons_lower_penalty = cons_lower * 2
deds += cons_lower_penalty

# 7) Consecutive numbers
cons_digit = sum(1 for i in range(length-1) if pw[i].isdigit() and pw[i+1].isdigit())
cons_digit_penalty = cons_digit * 2
deds += cons_digit_penalty

# 8) Consecutive symbols
cons_symbol = sum(1 for i in range(length-1) if not pw[i].isalnum() and not pw[i+1].isalnum())
cons_symbol_penalty = cons_symbol * 2
deds += cons_symbol_penalty

# 9) Sequential 
letters = string.ascii_lowercase
digits = string.digits
symbols = "!@#$%^&*()-_=+[]{}\\|;:'\",<.>/?~"

def find_seq(password, alphabet):
    seqs = 0
    
    for i in range(len(password) - 2):
        seq_len = 1
        for j in range(i+1, length):
            if pw[j] in alphabet and pw[j-1] in alphabet:
                diff = alphabet.index(pw[j]) - alphabet.index(pw[j-1])
                if diff == 1 or diff == -1:
                    seq_len += 1
                else:
                    break
            else:
                break
        if seq_len >= 3:
            seqs += 1
    return seqs

letter_seq = find_seq(lowered, letters)
digit_seq = find_seq(pw, digits)
symbol_seq = find_seq(pw, symbols)
letter_seq_penalty = letter_seq * 3
digit_seq_penalty = digit_seq * 3
symbol_seq_penalty = symbol_seq * 3
deds += letter_seq_penalty + digit_seq_penalty + symbol_seq_penalty


# === FINAL SCORE CALCULATION ===
raw_score  = adds - deds
if raw_score >= 150:
    score = 100
elif raw_score < 0:
    score = 0
else:
    score = round((raw_score / 150 * 100))

if score >= 85:
    meter = "Very Strong"
elif score >= 65:
    meter = "Strong"
elif score >= 50:
    meter = "Warning"
else:
    meter = "Weak"


# === OUTPUT ===
print("\n\n---- Password Strength Analysis ----")
print(f"Password: {s}")
print(f"Length: {length}")

print("\nBonuses:")
print(f" - Base characters (count {length}): +{base}")
if up_bonus:
    print(f" - Uppercase bonus (count {n_upper}): +{up_bonus}")
if low_bonus:
    print(f" - Lowercase bonus (count {n_lower}): +{low_bonus}")
if dig_bonus:
    print(f" - Numbers (count {n_digit}): +{dig_bonus}")
if sym_bonus:
    print(f" - Symbols (count {n_symbol}): +{sym_bonus}")
if unique:
    print(f" - Unique characters (count {unique}): +{unique}")
if req_bonus:
    print(f" - Requirements met (count {req_met}): +{req_bonus}")
print(f"Total bonuses: {adds}")

print("\nPenalties:")
if n_alpha == length:
    print(f" - Letters only (count {length}): -{letter_penalty}")
elif n_alpha / length >= 0.7:
    print(f" - Too many letters (count {n_alpha}): -{letter_penalty}")
if n_digit == length:
    print(f" - Numbers only (count {length}): -{dig_penalty}")
elif n_digit / length >= 0.7:
    print(f" - Too many digits (count {n_digit}): -{dig_penalty}")
if n_symbol == length:
    print(f" - Symbols only (count {length}): -{sym_penalty}")
elif n_symbol / length >= 0.7:
    print(f" - Too many symbols (count {n_symbol}): -{sym_penalty}")
if repeat_penalty:
    print(f" - Repeated characters (count {repeat_count}): -{repeat_penalty}")
if cons_upper_penalty:
    print(f" - Consecutive uppercase (count {cons_upper}): -{cons_upper_penalty}")
if cons_lower_penalty:
    print(f" - Consecutive lowercase (count {cons_lower}): -{cons_lower_penalty}")
if cons_digit_penalty:
    print(f" - Consecutive numbers (count {cons_digit}): -{cons_digit_penalty}")
if cons_symbol_penalty:
    print(f" - Consecutive symbols (count {cons_symbol}): -{cons_symbol_penalty}")
if letter_seq_penalty:
    print(f" - Sequential letters (count {letter_seq}): -{letter_seq_penalty}")
if digit_seq_penalty:
    print(f" - Sequential numbers (count {digit_seq}): -{digit_seq_penalty}")
if symbol_seq_penalty:
    print(f" - Sequential symbols (count {symbol_seq}): -{symbol_seq_penalty}")
print(f"Total penalties: {deds}")

print(f"\nRaw score = {raw_score}")
print(f"Scaled score = {score} => {meter}")

print("\nNotes/Requirements")
print(f" - Length ≥ 14? {'✔' if req_len else '✘'}")
print(f" - Has uppercase? {'✔' if req_up else '✘'}")
print(f" - Has lowercase? {'✔' if req_low else '✘'}")
print(f" - Has digit? {'✔' if req_dig else '✘'}")
print(f" - Has symbol? {'✔' if req_sym else '✘'}")
print(f"Requirements met: {req_met}/5\n")

if meter == "Very Strong":
    print("\n---- Verdict ----")
    print("✅ VERY STRONG — exceeds minimum standards. Good job.")
    print("\nTips:")
    print(" - Superb! Your password is highly resistant to brute force and guessing attacks.")
    print(" - Make sure it's unique — don’t reuse it across different sites.")
    print(" - Store it safely in a password manager.")

elif meter == "Strong":
    print("\n---- Verdict ----")
    print("✔ STRONG — meets minimum standards. Good but can improve.")
    print("\nTips:")
    print(" - Acceptable for most accounts, but not ideal for critical ones (e.g. bank account).")
    print(" - Add more symbols or random characters to increase strength.")
    print(" - Avoid using words or patterns that could be guessed.")

elif meter == "Warning":
    print("\n---- Verdict ----")
    print("⚠️ WARNING — advisory against bad practices. Consider improving.")
    print("\nTips:")
    print(" - May resist casual guessing but still vulnerable to brute-force attacks.")
    print(" - Increase password length (14+ characters minimum).")
    print(" - Mix uppercase, lowercase, numbers, and symbols.")
    print(" - Avoid using personal info or predictable sequences.")

else:
    print("\n---- Verdict ----")
    print("❌ WEAK — does not meet minimum standards. Change your password.")
    print("\nTips:")
    print(" - Do NOT use this for any important account.")
    print(" - Make it longer — at least 14 characters.")
    print(" - Include uppercase, lowercase, numbers, and symbols.")
    print(" - Avoid simple words, patterns, or repeating characters.")
    print(" - Consider using a passphrase made of 4+ random words or a password manager.")


print("\n\nQuick tips:")
print("- Make it longer (length helps a lot)")
print("- Use a mix of uppercase, lowercase, digits and symbols")
print("- Avoid sequential characters like 'abcd' or '1234' or repeated letters like 'aaaa'")
print("- Use unrelated words or a password manager for best security")
