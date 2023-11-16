import tkinter as tk
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


client = MongoClient('mongodb://localhost:27017/')
db = client['MarketAnalysis']
jobposting = db['jobposting']

#analysis of sponsored job
def Sponsored():

    count_sponsored = jobposting.count_documents({'sponsored': 1})
    count_not_sponsored = jobposting.count_documents({'sponsored': 0})
    total_count = jobposting.estimated_document_count()

    percentage = (count_sponsored / total_count) * 100 if total_count > 0 else 0

    fig, ax = plt.subplots()
    ax.bar(["Sponsored", "Not_Sponsored"], [count_sponsored, count_not_sponsored])
    ax.set_ylabel('Number of Documents')
    ax.set_title('Documents Count: Sponsored vs Not_Sponsored')
  
    canvas = FigureCanvasTkAgg(fig, master=root)  # root는 Tkinter의 메인 윈도우
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, f"Percentage of documents where 'sponsored' is 1: {percentage:.2f}%")

#analysis of Top 10 Most Frequent Job titles
def numofJob():
    pipeline = [
        {
            "$group": {
                "_id": "$title",
                "total": {"$sum": 1}
                }
        },
        {
            "$sort": {"total": -1}
        },
        {
            "$limit" : 10
        }
    ]

    results = jobposting.aggregate(pipeline)
    titles = []
    counts = []

    for result in results:
        titles.append(result['_id'])
        counts.append(result['total'])
        text_area.insert(tk.END, f"{result['_id']} {result['total']}\n")

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(titles, counts)
    ax.set_ylabel('Number of Job Postings')
    ax.set_title('Top 10 Job Titles')
    ax.set_xticklabels(titles, rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

#anaylsis of number of job tiltes in each state in US
#Data anylsis 
#Percentage of Work Type
    

root = tk.Tk()
root.title("2023 Linkedin Market Analysis")

run_button = tk.Button(root, text="Calculate Sponsored Percentage", command=Sponsored)
run_button.pack()

run_button1 = tk.Button(root, text="Top 10 Most Frequent Job titles ", command=numofJob)
run_button1.pack()

text_area = tk.Text(root, height=10, width=100)
text_area.pack()


def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
