#!/bin/bash

file="$1"

# Extract the entire text from PDF
text=$(pdftotext "$file" -)

# Extract name, PRN, seat number, and GPA
name=$(echo "$text" | grep -oP 'NAME\s+: \K.*')
prn=$(echo "$text" | grep -oP 'PRN: \K\d+')
seat_no=$(echo "$text" | grep -oP 'SEAT NO. : \K\d+')
gpa=$(echo "$text" | grep -oP 'GPA: \K[\d.]+')

# Extract grade lines from between COURSE and RESULT DATE
grades=$(echo "$text" | awk '/COURSE/,/RESULT DATE/' | grep -E '[0-9]{4}' | \
  sed 's/^[[:space:]]*//; s/[[:space:]]\{2,\}/ /g' | \
  while read -r line; do
    code=$(echo "$line" | awk '{print $1}')
    rest=$(echo "$line" | cut -d' ' -f2-)

    parts=($rest)
    n=${#parts[@]}

    final=""
    practical=""
    ese=""
    ca=""
    subject_parts=()

    if [[ $n -ge 1 ]]; then final="${parts[$((n-1))]}"; fi
    if [[ $n -ge 2 ]]; then practical="${parts[$((n-2))]}"; fi
    if [[ $n -ge 3 ]]; then ese="${parts[$((n-3))]}"; fi
    if [[ $n -ge 4 ]]; then ca="${parts[$((n-4))]}"; fi

    subject_len=$((n-4))
    if [[ $subject_len -gt 0 ]]; then
      subject_parts=("${parts[@]:0:$subject_len}")
    fi
    subject="${subject_parts[*]}"

    echo "{ \"subject\": \"${subject}\", \"ca_grade\": \"${ca}\", \"ese_grade\": \"${ese}\", \"practical_grade\": \"${practical}\", \"final_grade\": \"${final}\" },"
  done
)

# Combine into a single JSON object
student_json=$(cat <<EOF
{
  "name": "$name",
  "prn": "$prn",
  "seat_no": "$seat_no",
  "gpa": $gpa,
  "grades": [
$(echo "$grades" | sed '$ s/,$//')
  ]
}
EOF
)

echo "$student
