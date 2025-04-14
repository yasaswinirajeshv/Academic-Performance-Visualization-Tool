#!/bin/bash

input_pdf="$1"

# Check file validity
if [ -z "$input_pdf" ] || [ ! -f "$input_pdf" ]; then
  echo "Usage: $0 <PDF File>"
  exit 1
fi

# Extract name and GPA
text=$(pdftotext -layout "$input_pdf" -)
student_name=$(echo "$text" | grep -i "NAME" | head -n 1 | sed -E 's/.*NAME[[:space:]]*:[[:space:]]*(.*)/\1/' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
prn=$(echo "$text" | grep -oP 'PRN: \K\d+')
seat_no=$(echo "$text" | grep -oP 'SEAT NO. : \K\d+')
gpa=$(echo "$text" | grep -i "GPA" | head -n 1 | sed -E 's/.*GPA[:[:space:]]*([0-9.]+).*/\1/')

# Fallbacks
student_name_clean=$(echo "$student_name" | tr -cd '[:alnum:]_')
[ -z "$student_name_clean" ] && student_name_clean="Unknown_Student"

# Convert to text
pdftotext -layout "$input_pdf" results.txt

# Start JSON
echo "{" 
echo "  \"name\": \"${student_name}\","
echo "  \"prn\": \"${prn}\","
echo "  \"seat_no\": \"${seat_no}\","
echo "  \"gpa\": $gpa,"
echo "  \"grades\": ["

awk '
BEGIN { first = 1 }
/^[[:space:]]*[0-9]{4}/ {
    if (!first) print ","
    first = 0

    code = $1
    subject = ""
    ca = ""
    ese = ""
    practical = ""
    final = ""

    # Extract subject name
    for (i = 2; i <= NF; i++) {
        if ($i ~ /^(A\+?|B\+?|C\+?|O|P|F|D)$/) break
        subject = subject " " $i
    }
    subject = substr(subject, 2)

    # Edge case: subject might be "PROGRAMMING IN C" or "PROGRAMMING IN C LAB"
    if (subject == "PROGRAMMING IN" && $i == "C") {
        subject = subject " C"
        i++
        if ($i == "LAB") {
            subject = subject " LAB"
            i++
        }
    }

    n_grades = 0
    for (j = i; j <= NF; j++) {
        grades[n_grades++] = $j
    }

    if (n_grades == 4) {
        ca = grades[0]
        ese = grades[1]
        practical = grades[2]
        final = grades[3]
    } else if (n_grades == 3) {
        ca = grades[0]
        ese = grades[1]
        final = grades[2]
    } else if (n_grades == 2) {
        practical = grades[0]
        final = grades[1]
    } else if (n_grades == 1) {
        final = grades[0]
    }

    printf "    { \"subject\": \"%s\", \"ca_grade\": \"%s\", \"ese_grade\": \"%s\", \"practical_grade\": \"%s\", \"final_grade\": \"%s\" }", subject, ca, ese, practical, final
    delete grades
}
' results.txt


echo ""
echo "  ]"
echo "}"
