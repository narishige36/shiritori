# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session,url_for
#時間ごとに処理する
import time
import re

app = Flask(__name__)

app.secret_key = 'sunabakoza'

#正規表現
def word_re(word):
    re_hiragana = re.compile(r'^[あ-ん]+$')
    return re_hiragana.fullmatch(word)

@app.route('/',methods=["GET", "POST"])
def top():
    if request.method == "GET":
        return render_template("index.html")
    else:
        #テーマ名を入力してDBに保存
        theme = request.form.get("theme")
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into themes values(null,?)", (theme,) )
        #テーマIDをthemeに代入
        c.execute("select id from themes where theme = ?",(theme,))
        theme_id = c.fetchone()
        conn.commit()
        conn.close()
        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if theme_id is None:
            # ログイン失敗すると、ログイン画面に戻す
            return render_template("index.html")
        else:
            session['theme_id'] = theme_id[0]
            return redirect("/shiritori")
        

@app.route('/shiritori',methods=["GET","POST"])
def shiritori():
    if request.method == "GET":
        return render_template("shiritori.html")
    else:
        # １　開始ボタンを押すとしりとりゲームが始まる
        # 2 60秒のカウントダウン
        # 3 しりとりのデータを入れる
        #sessionからtheme_idを取得
        theme_id = session['theme_id']
        word = request.form.get("words")
        if not word_re(word):
            error_text = "ひらがなで入力してください"
            return render_template('shiritori.html',error_text = error_text)
        else:
            error_text = ""
            conn = sqlite3.connect('service.db')
            c = conn.cursor()
            #db shiritori に theme_idと単語をインサート
            c.execute("insert into shiritori values(?,?,null)", (theme_id,word,) )
            conn.commit()
            #db から最初に入力したテーマと紐づいている単語を取得
            c.execute("select word from shiritori where theme_id = ?",(theme_id,))
            words = []
            word_list = []
            for row in c.fetchall():
                words.append(row[0])
            for i in range(len(words)):
                list_item = words[i]
                word_list.append({"id":i,"word":list_item})

            conn.close()
            return render_template('shiritori.html',word_list = word_list,error_text = error_text)




## おまじない
if __name__ == "__main__":
    app.run(debug=True)