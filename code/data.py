import pandas as pd
import matplotlib.pyplot as plt




file = pd.ExcelFile(r"C:\Users\nickk\course_work\code\owid-covid-data.xlsx")
df = file.parse("Sheet1")




f = open(r"C:\Users\nickk\course_work\code\data.txt", "w")
s = ""
for data in df["total_cases"]:
    s += str(data) + " "

f.write(s)
f.close()
