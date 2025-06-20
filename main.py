import re
import pyperclip
from itertools import product

# === USER-DEFINED TAG ORDER ===
# Tags should match the labels exactly (case-sensitive)
tag_order = [
    "FREE",
    "Smart TV",
    "SFR",
    "Orange",
    "rapport"
]
"""France.TV_Free_Mai/Juin_2025
France.TV_SmartTV_Mai/Juin_2025
France.TV_SFR_Mai/Juin_2025
France.TV_Orange_Mai/Juin_2025
rapport"""

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
        i += 1  # Skip malformed entries

# Step 3: Filter out 'Par défaut'
filtered_pairs = [(label, time) for label, time in pairs if label.lower() != "par défaut"]
total_time = sum(time for _, time in filtered_pairs)

# Step 4: Get scaled values
scaled_values = [(time / total_time) * 5 if total_time != 0 else 0 for _, time in filtered_pairs]
labels = [label for label, _ in filtered_pairs]

# Step 5: Define allowed quantized values
allowed_values = [round(x * 0.25, 2) for x in range(0, 21)]

# Step 6: Brute-force search for best match
best_total_error = float('inf')
best_combination = None

for candidate in product(allowed_values, repeat=len(scaled_values)):
    total_error = sum(abs(a - b) for a, b in zip(scaled_values, candidate))
    if total_error < best_total_error:
        best_total_error = total_error
        best_combination = candidate

# Step 7: Pair results with labels and sort by tag_order
result_with_labels = list(zip(labels, best_combination))
sorted_result = sorted(result_with_labels, key=lambda x: tag_order.index(x[0]) if x[0] in tag_order else float('inf'))

# Step 8: Prepare output (just the values)
output_text = "\n".join(f"{val:.2f}" for _, val in sorted_result)
pyperclip.copy(output_text)

print("Sorted and rounded values have been copied to the clipboard.")
