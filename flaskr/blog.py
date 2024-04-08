

from flask import Blueprint, render_template

from flaskr.db import get_db


bp = Blueprint('blog', __name__)

bp.route('/index')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        'FROM user u JOIN post p ON u.id=p.author_id'
        'ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)