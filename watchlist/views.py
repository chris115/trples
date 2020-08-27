# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Triple


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        entity = request.form['entity']
        relation = request.form['relation']
        attribute = request.form['attribute']

        if not entity or not relation or not attribute or len(entity) > 40 or len(relation) > 40 or len(attribute) > 40:
            flash('Invalid input.')
            return redirect(url_for('index'))

        triple = Triple(entity=entity, relation=relation, attribute=attribute)
        db.session.add(triple)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    triples = Triple.query.all()
    return render_template('index.html', triples=triples)


@app.route('/triple/edit/<int:triple_id>', methods=['GET', 'POST'])
@login_required
def edit(triple_id):
    triple = Triple.query.get_or_404(triple_id)

    if request.method == 'POST':
        entity = request.form['entity']
        relation = request.form['relation']
        attribute = request.form['attribute']

        if not entity or not relation or not attribute or len(entity) > 40 or len(relation) > 40 or len(attribute) > 40:
            flash('Invalid input.')
            return redirect(url_for('edit', triple_id=triple_id))

        triple.entity = entity
        triple.relation = relation
        triple.attribute = attribute
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', triple=triple)


@app.route('/triple/delete/<int:triple_id>', methods=['POST'])
@login_required
def delete(triple_id):
    triple = Triple.query.get_or_404(triple_id)
    db.session.delete(triple)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
