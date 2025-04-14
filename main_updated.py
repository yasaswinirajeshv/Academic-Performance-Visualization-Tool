import json
import pandas as pd
import plotly.express as px

# ---------- Load JSON ----------
with open('dummy_result.json') as f:
    raw_data = json.load(f)

# ---------- Grade to Numeric Mapping ----------
grade_to_num = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6,
    "C+": 5, "C": 4, "P": 3, "F": 0, "": None
}
num_to_grade = {v: k for k, v in grade_to_num.items()}

# ---------- Flatten Data ----------
records = []
for student in raw_data:
    name = student["name"]
    prn = student["prn"]
    gpa = student["gpa"]
    for g in student["grades"]:
        records.append({
            "Name": name,
            "PRN": prn,
            "GPA": gpa,
            "Subject": g["subject"],
            "CA": g.get("ca_grade", ""),
            "ESE": g.get("ese_grade", ""),
            "Practical": g.get("practical_grade", ""),
            "Final": g.get("final_grade", "")
        })

df = pd.DataFrame(records)

# ---------- Convert Grades to Numeric ----------
for col in ["CA", "ESE", "Practical", "Final"]:
    df[f"{col}_Numeric"] = df[col].map(grade_to_num)

# -------------------- 1. Average Final Grade per Subject --------------------
avg_final = df[df["Final_Numeric"].notna()].groupby("Subject")["Final_Numeric"].mean().reset_index()
avg_final["Rounded"] = avg_final["Final_Numeric"].round()
avg_final["Rounded"] = avg_final["Rounded"].fillna(0).astype(int).map(num_to_grade)

fig1 = px.bar(
    avg_final.sort_values("Final_Numeric"),
    x="Final_Numeric",
    y="Subject",
    text="Rounded",
    orientation="h",
    color="Rounded",
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="📊 Average Final Grade per Subject"
)
fig1.update_layout(xaxis_title="Average Grade", yaxis_title="Subject", height=600)
fig1.show()

# -------------------- 2. Internal vs End Sem vs Practical Grade Averages --------------------
avg_components = df[['Subject', 'CA_Numeric', 'ESE_Numeric', 'Practical_Numeric']].copy()
avg_components = avg_components.groupby("Subject")[['CA_Numeric', 'ESE_Numeric', 'Practical_Numeric']].mean().reset_index()
avg_melt = avg_components.melt(id_vars="Subject", var_name="Component", value_name="Average Grade")

avg_melt = avg_melt[avg_melt["Average Grade"].notna()]
avg_melt["Rounded"] = avg_melt["Average Grade"].round().astype(int).map(num_to_grade)

fig2 = px.bar(
    avg_melt,
    x="Subject",
    y="Average Grade",
    color="Component",
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="📚 Internal, End Sem & Practical Grade Averages per Subject"
)
fig2.update_layout(xaxis_tickangle=45, height=600)
fig2.show()

# -------------------- 3. GPA Distribution as Bar Chart --------------------
gpa_data = [{"Name": student["name"], "PRN": student["prn"], "GPA": student["gpa"]} for student in raw_data]
df_gpa = pd.DataFrame(gpa_data)

fig3 = px.bar(
    df_gpa,
    x="Name",
    y="GPA",
    text="GPA",
    title="🎯 GPA Distribution of Students",
    color="GPA",
    color_continuous_scale="Plasma"
)
fig3.update_layout(xaxis_tickangle=45, height=600)
fig3.show()

# -------------------- 4. Line Plot per Student --------------------
line_df = df[df["Final_Numeric"].notna()].copy()
line_df["Final_Grade"] = line_df["Final_Numeric"].map(num_to_grade)

fig4 = px.line(
    line_df,
    x="Subject",
    y="Final_Numeric",
    color="Name",
    markers=True,
    line_group="PRN",
    hover_data=["PRN", "Final_Grade"],
    title="📈 Final Grade Trend per Student",
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig4.update_layout(
    yaxis=dict(dtick=1, range=[0, 10], tickmode='array', tickvals=list(range(0, 11)), ticktext=[num_to_grade.get(i, "") for i in range(0, 11)]),
    height=600
)
fig4.show()

# -------------------- 5. Topper Info in Bar Chart --------------------
topper_row = df_gpa.sort_values("GPA", ascending=False).iloc[0]
topper_name = topper_row["Name"]
topper_prn = topper_row["PRN"]

topper_data = df[df["PRN"] == topper_prn].copy()
topper_long = topper_data.melt(
    id_vars=["Subject", "PRN"],
    value_vars=["CA_Numeric", "ESE_Numeric", "Practical_Numeric", "Final_Numeric"],
    var_name="Assessment",
    value_name="Grade"
)

# Clean label names
topper_long["Assessment"] = topper_long["Assessment"].str.replace("_Numeric", "")
topper_long = topper_long[topper_long["Grade"].notna()]
topper_long["Letter Grade"] = topper_long["Grade"].round().astype(int).map(num_to_grade)

fig5 = px.bar(
    topper_long,
    x="Subject",
    y="Grade",
    color="Assessment",
    text="Letter Grade",
    barmode="group",
    hover_data=["PRN"],
    color_discrete_sequence=px.colors.qualitative.Safe,
    title=f"🏆 Topper Grades - {topper_name} (PRN: {topper_prn})"
)
fig5.update_layout(xaxis_tickangle=45, height=600)
fig5.show()
