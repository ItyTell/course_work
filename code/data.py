import pandas as pd
import matplotlib.pyplot as plt




file = pd.ExcelFile(r"C:\Users\nickk\course_work\code\owid-covid-data.xlsx")
df = file.parse("Sheet1")




f = open(r"C:\Users\nickk\course_work\code\hosp_patients.txt", "w")
s = ""
for data in df["hosp_patients"]:
    s += str(int(data)) + " "

f.write(s)
f.close()
