#!/usr/bin/env python3.7
import os, sys
sys.path.insert(0, '/home/tomsmith/webapps/redblue/htdocs/redblue/env/lib/python3.7/site-packages') #server path

from flask import Flask
from flask import request,render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "redblue.db"))

app = Flask(__name__, 
    static_folder='static', 
    static_url_path='/static',
    template_folder='views')

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        print(request.form)
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()

    books = Book.query.all()
    return render_template("home.html", books=books)
    

@app.route("/test")
def test():
    return "My flask app"

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    #print(book)
  
    db.session.delete(book)
    db.session.commit()
    

    return redirect("/")

### GET !
@app.route('/api', methods=['GET', 'POST'])
def get():

    id = request.args['id']
    print(id)
  
    return jsonify({'status':"OK", 'events':["stroke('#FF0038')", "strokeWeight(20)","line(0,0,0, 0)"] })


### PUT !
@app.route('/api_put', methods=[ 'POST'])
def put():
 
    id = request.args['id']
    data = request.get_json()
    
    print("id", id, type(data), data.keys())
    print("request", request)
    result = {'status':"OK", 'events':data['events']}
    return jsonify(result)

if __name__ == '__main__':
    app.run()





