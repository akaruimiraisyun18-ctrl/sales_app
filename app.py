from flask import Flask,render_template,request
import sqlite3
import matplotlib.pyplot as plt 
import os
app = Flask(__name__)
weekdays=["月","火","水","木","金","土","日"]
def init_db():
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_number INTEGER,
        weekday INTEGER,
        hour INTEGER,
        sale INTEGER
    )
    """)
    conn.commit()
    conn.close()
init_db()
@app.route("/")
def index():
    return render_template("index.html", weekdays=weekdays)
@app.route("/input", methods=["POST"])
def input_sales():
    start_hour = int(request.form["start_hour"])
    end_hour = int(request.form["end_hour"])
    days = int(request.form["days"])
    start_day = int(request.form["start_day"])
    hours = list(range(start_hour,end_hour))
    day_list = list(range(days))
    return render_template(
        "input_sales.html",
        start_hour=start_hour,
        end_hour=end_hour,
        days=day_list,
        start_day=start_day,
        hours=hours,
        weekdays=weekdays,
    )
@app.route("/result",methods=["POST"])
def result():
    start_hour = int(request.form["start_hour"])
    end_hour = int(request.form["end_hour"])    
    days_count= int(request.form["days_count"])
    start_day = int(request.form["start_day"])
    hours_count = end_hour-start_hour
    hours = list(range(start_hour,end_hour))
    sales_table = []
    count_table = []
    for kinako in range(7):
        sales_row = []
        count_row = []
        for kenako in range(hours_count):
            sales_row.append(0)
            count_row.append(0)
        sales_table.append(sales_row)    
        count_table.append(count_row)
    conn = sqlite3.connect("sales.db")    
    cur = conn.cursor()
    for kinako in range(days_count):
        weekday = ( start_day + kinako )%7
        for kenako in range(start_hour,end_hour):
            form_name="sale_"+str(kinako)+"_"+str(kenako)
            sale = int(request.form[form_name])
            hour_index = kenako-start_hour
            now_sale = sales_table[weekday][hour_index]
            new_sale = now_sale+sale
            sales_table[weekday][hour_index]=new_sale
            now_count=count_table[weekday][hour_index]
            new_count=now_count+1
            count_table[weekday][hour_index]=new_count
            cur.execute(
                "INSERT INTO sales (day_number,weekday,hour,sale)VALUES(?,?,?,?)",
                (kinako+1,weekday,kenako,sale)
            )
    conn.commit()  
    conn.close()
    average_table = []
    for kinako in range(7):
        average_row = []
        for kenako in range(hours_count):
            if count_table[kinako][kenako] !=0:
                average = sales_table[kinako][kenako]/count_table[kinako][kenako]
            else:
                average = 0
            average_row.append(average)  
        average_table.append(average_row)    
    if not os.path.exists("static"):
        os.makeddirs("static")      
    plt.figure(figsize=(10,5))   
    plt.imshow(average_table)    
    plt.xticks(range(hours_count),hours)
    plt.yticks(range(7),weekdays)
    plt.colorbar()
    plt.title("曜日・時間帯別　平均売上")
    plt.savefig("static/heatmap.png")
    plt.close()
    weekday_total = []
    for kinako in range(7):
        total = 0
        for kenako in range(hours_count):
            total = total + sales_table[kinako][kenako]
        weekday_total.append(total)    
    plt.figure(figsize=(8,5))    
    plt.bar(weekdays,weekday_total)
    plt.title("曜日別　合計売上")
    plt.savefig("static/bar.png")
    plt.close()
    return render_template(
        "result.html",
        average_table=average_table,
        weekdays=weekdays,
        hours=hours,
        heatmap_image="heatmap.png",
        bar_image="bar.png"
    )    
if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
