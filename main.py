import re
import pyperclip
from itertools import product

# === USER-DEFINED TAG ORDER ===
tag_order = [
    "FREE",
    "Smart TV",
    "SFR",
    "Orange",
    "rapport"
]

# Step 1: Get text from clipboard
text = pyperclip.paste()

# Step 2: Parse label/time pairs
lines = text.strip().splitlines()
pairs = []
i = 0
while i < len(lines) - 1:
    label = lines[i].strip()
    time_line = lines[i + 1].strip()
    if re.match(r"^\d+(\.\d+)?\s*h$", time_line):
        time = float(time_line.replace("h", "").strip())
        pairs.append((label, time))
        i += 2
    else:
        i += 1

# Step 3: Filter out 'Par défaut'
filtered_pairs = [(label, time) for label, time in pairs if label.lower() != "par défaut"]
total_time = sum(time for _, time in filtered_pairs)

# Step 4: Get scaled values
scaled_values = [(time / total_time) * 5 if total_time != 0 else 0 for _, time in filtered_pairs]
labels = [label for label, _ in filtered_pairs]

# Step 5: Define allowed values (0 to 5 in 0.25 steps)
allowed_values = [round(x * 0.25, 2) for x in range(0, 21)]

# Step 6: Find combinations that sum to 5.00 and minimize total distance
best_total_error = float('inf')
best_combination = None
target_sum = 5.00
epsilon = 1e-6  # for floating point comparison

for candidate in product(allowed_values, repeat=len(scaled_values)):
    if abs(sum(candidate) - target_sum) < epsilon:
        total_error = sum(abs(a - b) for a, b in zip(scaled_values, candidate))
        if total_error < best_total_error:
            best_total_error = total_error
            best_combination = candidate

# Step 7: Pair and sort by tag_order
result_with_labels = list(zip(labels, best_combination))
sorted_result = sorted(result_with_labels, key=lambda x: tag_order.index(x[0]) if x[0] in tag_order else float('inf'))

# Step 8: Format values with comma
output_text = "\n".join(f"{val:.2f}".replace(".", ",") for _, val in sorted_result)

# Step 9: Copy to clipboard
pyperclip.copy(output_text)
print("Final result copied to clipboard with sum = 5.0 and comma decimal format.")
