# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session,url_for

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def top():
    if request.method == "GET":
        return render_template("index.html")
    else:
        theme = request.form.get("theme")
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into themes values(null,?)", (theme,) )
        c.execute("select id from themes where theme = ?",(theme,))
        theme = c.fetchone()
        conn.commit()
        conn.close()
        return redirect("/shiritori")

@app.route('/shiritori',methods=["GET","POST"])
def shiritori():
    if request.method == "GET":
        return render_template("shiritori.html")
    else:
        return redirect("/association")



## おまじない
if __name__ == "__main__":
    app.run(debug=True)