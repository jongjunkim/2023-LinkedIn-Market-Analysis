# graph_functions.py
from pymongo import MongoClient
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

class GraphFunctions:
    def __init__(self, database):
        self.db = database

    
    def clear_figure(self, ax, canvas, text_widget):
        ax.clear()  
        canvas.draw() 
        text_widget.delete('1.0', tk.END)  

    def sponsored(self, ax, canvas, text_widget):
        self.clear_figure(ax, canvas, text_widget)  # Make sure to clear the existing figure and text widget

        count_sponsored = self.db.jobposting.count_documents({'sponsored': 1})
        count_not_sponsored = self.db.jobposting.count_documents({'sponsored': 0})
        total_count = self.db.jobposting.estimated_document_count()

        percentage = (count_sponsored / total_count) * 100 if total_count > 0 else 0

        ax.bar(["Sponsored", "Not_Sponsored"], [count_sponsored, count_not_sponsored])
        ax.set_ylabel('Number of Sponosred and Non_Sponsored')
        ax.set_title('Sponsored vs Not_Sponsored')

        text_widget.insert(tk.END, f"Percentage of documents where 'sponsored' is True: {percentage:.2f}%")

        # Redraw the canvas with the new plot
        canvas.draw_idle()

    def num_of_job(self, ax, canvas, text_widget):
        self.clear_figure(ax, canvas, text_widget)  
        
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
                "$limit": 10
            }
        ]

        results = self.db.jobposting.aggregate(pipeline)
        titles = []
        counts = []

        for result in results:
            titles.append(result['_id'])
            counts.append(result['total'])
            text_widget.insert(tk.END, f"{result['_id']} {result['total']}\n")

        # Update the existing ax with the new data
        ax.bar(titles, counts)
        ax.set_ylabel('Number of Job Postings')
        ax.set_title('Top 10 Job Titles')
        ax.set_xticklabels(titles, rotation=45, ha="right")

        # Redraw the canvas with the new plot
        canvas.draw_idle()

    def jobs_in_each_state(self, ax, canvas, text_widget):
        self.clear_figure(ax, canvas, text_widget)

        pipeline = [
            {
                "$lookup": {
                    "from": "jobposting",
                    "localField": "company_id",
                    "foreignField": "company_id",
                    "as": "jobpostings"
                }
            },
            {
                "$unwind": "$jobpostings"
            },
            {
                "$group": {
                    "_id": "$state",
                    "totalJobs": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "totalJobs": -1
                }
            },
            {
                "$limit": 10 
            }
        ]

        results = list(self.db.companies.aggregate(pipeline))

        # Process the results for visualization
        states = []
        job_counts = []
        for result in results:
            states.append(result['_id'])
            job_counts.append(result['totalJobs'])

        # Update the existing ax with the new data
        ax.barh(states, job_counts, color='skyblue')
        ax.set_xlabel('Number of Jobs')
        ax.set_ylabel('State')
        ax.set_title('Top 10 States with the Highest Number of Jobs')
        ax.invert_yaxis()  # Invert the y-axis to show the highest count on top

        # Redraw the canvas with the new plot
        canvas.draw_idle()


    def work_type(self, ax, canvas, text_widget):
        self.clear_figure(ax, canvas, text_widget)

        pipeline = [
            {
                "$lookup": {
                    "from": "companies",
                    "localField": "company_id",
                    "foreignField": "company_id",
                    "as": "company_info"
                }
            },
            {
                "$unwind": "$company_info"
            },
            {
                "$match": {"company_info.country": "US"}
            },
            {
                "$group": {
                    "_id": "$formatted_work_type",
                    "total": {"$sum": 1}
                }
            },
            {
                "$sort": {"total":-1}
            }
        ]   

        results = list(self.db.jobposting.aggregate(pipeline))

        work_type = []
        total = []
        for result in results:
            work_type.append(result['_id'])
            total.append(result['total'])
        
        print(work_type)
        print(total)


        plt.pie(total, labels=work_type, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        # Show the pie chart
        plt.show()



    def num_of_companies_each_state(self, ax, canvas, text_widget):
        
        self.clear_figure(ax, canvas, text_widget)

        pipeline = [
            {
                "$match": {"country": "US"}
            },
            {
                "$group": {
                    "_id": "$state",
                    "total": {"$sum": 1}
                }
            },
            {
                "$sort": {"total": -1}
            }
        ]

        results = self.db.companies.aggregate(pipeline)
        
        states = []
        total = []
        for result in results:
            states.append(result['_id'])
            total.append(result['total'])
        
       
        ax.barh(states, total, color='skyblue')
        ax.set_xlabel('Number')
        ax.set_ylabel('State')
        ax.set_title('Number of Companies in Each State')

      
        canvas.draw_idle()

       