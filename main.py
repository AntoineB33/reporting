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

def round_to_nearest_0_25(x):
    return round(x * 4) / 4

def adjust_to_target_sum(values, target_sum=5.0):
    rounded = [round_to_nearest_0_25(v) for v in values]
    delta = round(target_sum - sum(rounded), 6)
    steps = int(abs(delta) / 0.25)

    if steps == 0:
        return rounded

    direction = 1 if delta > 0 else -1

    # Compute deviation for sorting (lowest impact first)
    diffs = [
        (i, abs(rounded[i] + direction * 0.25 - values[i]))
        for i in range(len(values))
        if 0 <= rounded[i] + direction * 0.25 <= 5
    ]
    diffs.sort(key=lambda x: x[1])  # sort by minimal distortion

    # Apply the best N smallest adjustments
    for i in range(steps):
        if i < len(diffs):
            idx = diffs[i][0]
            rounded[idx] += direction * 0.25

    return rounded

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

# Step 3: Filter using tag_order
filtered_pairs = [(label, time) for label, time in pairs if label.lower() in tag_order_lower]
total_time = sum(time for _, time in filtered_pairs)

# Step 4: Compute scaled values
scaled_values = [(time / total_time) * 5 if total_time != 0 else 0 for _, time in filtered_pairs]
labels = [label for label, _ in filtered_pairs]

# Step 5: Adjust values with heuristic
rounded_values = adjust_to_target_sum(scaled_values)

# Step 6: Pair and sort by tag_order
result_with_labels = list(zip(labels, rounded_values))
sorted_result = sorted(result_with_labels, key=lambda x: tag_order_lower.index(x[0].lower()))

# Step 7: Format output
output_lines = ["" if val == 0 else f"{val:.2f}".replace(".", ",") for _, val in sorted_result]
output_text = "\n".join(output_lines)

# Step 8: Copy to clipboard
pyperclip.copy(output_text)
print("Rounded and adjusted result copied to clipboard.")