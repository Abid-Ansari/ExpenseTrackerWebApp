from flask import Flask,render_template,redirect,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
import random
import pandas as pd 
from datetime import datetime

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
    items = Expenses()
    expense_items = items.query.all()
    list_form = []
    list_form2 = []
    for d in expense_items:
        list_form.append({'category':d.category,'amount':d.amount})
        list_form2.append({'date':d.date,'amount':d.amount})
    pandas_df = pd.DataFrame(list_form)
    pandas_df2 = pd.DataFrame(list_form2)
    if len(pandas_df)>0:
        grouped_df = pandas_df.groupby('category')['amount'].sum().reset_index()
        grouped_df2 = pandas_df2.groupby('date')['amount'].sum().reset_index()
        print(grouped_df2.dtypes['date'])
        grouped_df2['date'] = grouped_df2['date'].apply(lambda x:x.date())
        print(grouped_df2.dtypes['date'])
        print(grouped_df2)
        return render_template('index.html',myTable = expense_items , data=grouped_df.to_json(orient='records', index=False) ,
                               bar_graph_data = grouped_df2.to_json(orient='records', index=False))
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
    print(data)
    query = db.session.delete(data)
    db.session.commit()
    items = Expenses()
    expense_items = items.query.all()
    return redirect('/')
   

if __name__=='__main__':
    app.run(debug=True,port=8000)
