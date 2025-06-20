import re
import pyperclip
from itertools import product

# === USER-DEFINED TAG ORDER ===
tag_order = [
    "FREE",
    "Smart TV",
    "SFR",
    "Orange"
]
tag_order_lower = [t.lower() for t in tag_order]

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

# Step 3: Filter only labels that exist in tag_order (case-insensitive)
filtered_pairs = [(label, time) for label, time in pairs if label.lower() in tag_order_lower]
total_time = sum(time for _, time in filtered_pairs)

# Step 4: Scale time values to sum = 5.0
scaled_values = [(time / total_time) * 5 if total_time != 0 else 0 for _, time in filtered_pairs]
labels = [label for label, _ in filtered_pairs]

# Step 5: Define allowed rounded values (0–5 by 0.25)
allowed_values = [round(x * 0.25, 2) for x in range(0, 21)]

# Step 6: Find best rounded combination with exact sum = 5.0
best_total_error = float('inf')
best_combination = None
target_sum = 5.00
epsilon = 1e-6

for candidate in product(allowed_values, repeat=len(scaled_values)):
    if abs(sum(candidate) - target_sum) < epsilon:
        total_error = sum(abs(a - b) for a, b in zip(scaled_values, candidate))
        if total_error < best_total_error:
            best_total_error = total_error
            best_combination = candidate

# Step 7: Pair and sort by tag_order (case-insensitive match)
result_with_labels = list(zip(labels, best_combination))
sorted_result = sorted(
    result_with_labels,
    key=lambda x: tag_order_lower.index(x[0].lower())
)

# Step 8: Format result (comma as decimal separator, empty for 0)
output_lines = [
    "" if val == 0 else f"{val:.2f}".replace(".", ",")
    for _, val in sorted_result
]

output_text = "\n".join(output_lines)

# Step 9: Copy result to clipboard
pyperclip.copy(output_text)
print("Final result copied to clipboard (case-insensitive tag ordering).")
