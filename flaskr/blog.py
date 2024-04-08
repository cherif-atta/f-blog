
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM user u JOIN post p ON u.id=p.author_id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if title is None:
            error = 'title can\'t be empty'
        elif body is None:
            error = 'body is required'

        if error is None:
            try:
                db = get_db()
                db.execute(
                    'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)',
                    (title, body, g.user['id']),
                )
                db.commit()
            except db.IntegrityError:
                pass
            else:
                return redirect(url_for('index'))
        flash(error, 'error')

    return render_template('blog/create.html')