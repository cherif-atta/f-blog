
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
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
        if not title:
            error = 'title cant be empty'
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


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        updated_title = request.form['title']
        updated_body = request.form['body']
        error = None
        if not updated_title:
            error = 'Title is required.'
        
        if not error:
            db = get_db()
            db.execute(
                'UPDATE post SET title=?, body=? WHERE id=?',
                (updated_title, updated_body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

        flash(error, 'error')

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id=?',
        (id,)
    )
    db.commit()
    
    return redirect(url_for('blog.index'))