from flask import Flask,render_template,redirect,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
import random
import pandas as pd 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///MyExpenses.db"
db = SQLAlchemy(app)

class Expenses(db.Model):
    sno = db.Column(db.Integer,primary_key =  True)
    date = db.Column(db.DateTime, default=date.today())
    category = db.Column(db.String(100),nullable= False)
    amount = db.Column(db.Integer)

    def __repr__(self)->str:
        return f'{self.category}-{self.amount}'


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        exp = Expenses(
            sno = int(random.random()*10000),
            date= datetime.strptime(request.form.get("date"),'%Y-%m-%d') ,
            category=request.form.get("category"),
            amount=request.form.get("amount")
        )
        db.session.add(exp)
        db.session.commit()
        print(exp)
        items = Expenses()
        expense_items = items.query.all()
        return render_template('index.html',myTable = expense_items)
    
    items = Expenses()
    expense_items = items.query.all()
    list_form = []
    for d in expense_items:
        list_form.append({'category':d.category,'amount':d.amount})
    pandas_df = pd.DataFrame(list_form)
    if len(pandas_df)>0:
        grouped_df = pandas_df.groupby('category')['amount'].sum().reset_index()
        return render_template('index.html',myTable = expense_items , data=grouped_df.to_json(orient='records', index=False))
    return render_template('index.html',myTable = expense_items)


@app.route("/AddExpense", methods=["GET", "POST"])
def expense_create():
    if request.method == "POST":
        exp = Expenses(
            sno = int(random.random()*10000),
            date= datetime.strptime(request.form.get("date"),'%Y-%m-%d') ,
            category=request.form.get("category"),
            amount=request.form.get("amount")
        )
        db.session.add(exp)
        db.session.commit()
        print(exp)
        return redirect('/')

    return redirect('/')

@app.route("/delete/<int:sno>", methods=["GET", "POST"])
def delete(sno):
    data = Expenses.query.get(sno)
    query = db.session.delete(data)
    db.session.commit()
    items = Expenses()
    expense_items = items.query.all()
    return redirect('/')
   

if __name__=='__main__':
    app.run(debug=True,port=8000)
