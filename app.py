from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                      (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template('home.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return render_template('post.html', post=post)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
