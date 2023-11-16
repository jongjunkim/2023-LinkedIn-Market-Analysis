import tkinter as tk
from pymongo import MongoClient
from tkinter import messagebox


#first analysis
def run_query():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Project2']  
   
    pipeline = [
        {
            "$match": {
                "description": {"$regex": "Python|SQL", "$options": "i"},
                "formatted_experience_level": {"$ne": None}
            }
        },
        {
            "$lookup": {
                "from": "companies",
                "localField": "company_id",
                "foreignField": "company_id",
                "as": "company_info"
            }
        },
        {"$unwind": "$company_info"},
        {
            "$match": {
                "company_info.country": "US"
            }
        },
        {
            "$lookup": {
                "from": "salaries",
                "localField": "job_id",
                "foreignField": "job_id",
                "as": "salary_info"
            }
        },
        {"$unwind": "$salary_info"},
        {
            "$group": {
                "_id": {
                    "state": "$company_info.state",
                    "experienceLevel": "$formatted_experience_level"
                },
                "averageMedSalary": {"$avg": "$salary_info.med_salary"}
            }
        },
        {
            "$group": {
                "_id": "$_id.state",
                "experienceLevels": {
                    "$push": {
                        "experienceLevel": "$_id.experienceLevel",
                        "averageMedSalary": {"$round": ["$averageMedSalary", 2]}
                    }
                }
            }
        }
    ]

    try:
        results = db.jobposting.aggregate(pipeline)
        display_results(results)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# first analyis print format
def display_results(results):
   
    text_area.delete('1.0', tk.END) 

    
    header = f"{'State':<20} {'Experience Level':<20} {'Avg Med Salary ($)':<20}\n"
    text_area.insert(tk.END, header)
    text_area.insert(tk.END, "-" * 60 + "\n") 

 
    for result in results:
        state = result['_id']
        for exp_level in result['experienceLevels']:
            exp = exp_level['experienceLevel']
            avg_salary = exp_level['averageMedSalary']
            line = f"{state:<20} {exp:<20} {avg_salary:<20}\n"
            text_area.insert(tk.END, line)

      
        text_area.insert(tk.END, "-" * 60 + "\n")


#second analysis
def run_query2():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Project2']

   
    pipeline2 = [
        {"$lookup": {
            "from": "companies",
            "localField": "company_id",
            "foreignField": "company_id",
            "as": "company_info"}},
        {"$unwind": "$company_info"},
        {"$match": {
            "company_info.country": "US",
            "company_info.description": {"$regex": "software|engineer|hardware", "$options": "i"}}},
        {"$addFields": {
            "dayMonthYear": {"$dateToString": {"format": "%Y-%m-%d", "date": {"$toDate": "$listed_time"}}}}},
        {"$group": {
            "_id": {"applicationType": "$application_type", "dayMonthYear": "$dayMonthYear"},
            "totalApplies": {"$sum": "$applies"},
            "totalViews": {"$sum": "$views"}}},
        {"$sort": {"_id.dayMonthYear": 1, "_id.applicationType": 1}}
    ]

    try:
        results = db.jobposting.aggregate(pipeline2)
        display_results2(results)
    except Exception as e:
        messagebox.showerror("Error", str(e))

#second analysis print format
def display_results2(results):
   
    text_area.delete('1.0', tk.END) 

    
    header = f"{'Application Type':<20} {'DayMonthYear':<20} {'Total Applies':<20} {'Total Views':<20}\n"
    text_area.insert(tk.END, header)
    text_area.insert(tk.END, "-" * 80 + "\n")  

    
    for result in results:
        app_type = result['_id']['applicationType']
        day_month_year = result['_id']['dayMonthYear']
        total_applies = result['totalApplies']
        total_views = result['totalViews']
        line = f"{app_type:<20} {day_month_year:<20} {total_applies:<20} {total_views:<20}\n"
        text_area.insert(tk.END, line)

        text_area.insert(tk.END, "-" * 80 + "\n")


root = tk.Tk()
root.title("MongoDB Query GUI")

#Changes in salary offers by experience_level for jobs at each State in US that require Python and SQL skills
run_button = tk.Button(root, text="Changes in salary offers", command=run_query)
run_button.pack()

#Changes in applies and views by application type throughout the day in August for the U.S companies related to 'software', 'engineer', and 'hardware'
button2 = tk.Button(root, text="Changes in applies and views", command=run_query2)
button2.pack()

text_area = tk.Text(root, height=50, width=100)
text_area.pack()

root.mainloop()
