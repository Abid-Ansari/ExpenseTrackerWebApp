from flask import Flask,render_template,redirect,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
import random
import pandas as pd 
from datetime import datetime


app = Flask(__name__)
# Setting up the database
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///MyExpenses.db"
# Creating an object of Falsk SQL Alchemy class
db = SQLAlchemy(app)

# Creating the databse using Class

class Expenses(db.Model):
    sno = db.Column(db.Integer,primary_key =  True)
    date = db.Column(db.DateTime, default=date.today())
    category = db.Column(db.String(100),nullable= False)
    amount = db.Column(db.Integer)

    def __repr__(self)->str:
        return f'{self.category}-{self.amount}'


@app.route("/", methods=["GET", "POST"])
def main_function():
    items = Expenses()
    # retreive all the records
    expense_items = items.query.all()
    pi_graph = []
    bar_graph = []
    for d in expense_items:
        pi_graph.append({'category':d.category,'amount':d.amount})
        bar_graph.append({'date':d.date,'amount':d.amount})
    pi_graph_df = pd.DataFrame(pi_graph)
    bar_graph_df = pd.DataFrame(bar_graph)
    if len(pi_graph_df)>0:
        pi_graph_df = pi_graph_df.groupby('category')['amount'].sum().reset_index()
        bar_graph_df = bar_graph_df.groupby('date')['amount'].sum().reset_index()
        bar_graph_df['date'] = bar_graph_df['date'].apply(lambda x:x.date())
        # sending the data to plot bar and pi - graphs
        return render_template('index.html',myTable = expense_items , data=pi_graph_df.to_json(orient='records', index=False,date_format='iso') ,
                               bar_graph_data = bar_graph_df.to_json(orient='records', index=False,date_format='iso'))
    return render_template('index.html',myTable = expense_items)


@app.route("/AddExpense", methods=["GET", "POST"])
def expense_create():
    if request.method == "POST":
        # retreiving the response from user
        exp = Expenses(
            sno = int(random.random()*10000),
            date= datetime.strptime(request.form.get("date"),'%Y-%m-%d') ,
            category=request.form.get("category"),
            amount=request.form.get("amount")
        )
        #adding into our databse
        db.session.add(exp)
        db.session.commit()
        return redirect('/')

    return redirect('/')

@app.route("/delete/<int:sno>", methods=["GET", "POST"])
def delete(sno):
    # this function receives request when delete button is clicked and then delete that entry
    data = Expenses.query.get(sno)
    print(data)
    query = db.session.delete(data)
    db.session.commit()
   
    return redirect('/')
   

if __name__=='__main__':
    app.run(debug=True,port=8000)
