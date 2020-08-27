# -*- coding: utf-8 -*-
import click

from watchlist import app, db
from watchlist.models import User, Triple


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Chris'
    triples = [
        {'entity': 'Material Resource', 'relation': 'has subclass', 'attribute': 'Workpiece'},
        {'entity': 'Equipment Resource', 'relation': 'has subclass', 'attribute': 'Processing Equipment'},
        {'entity': '设备资源', 'relation': '包含', 'attribute': '仪器仪表'},
        {'entity': '刀具', 'relation': '包含', 'attribute': '铣刀'},
        {'entity': '夹具', 'relation': '包含', 'attribute': '通用夹具'},
        {'entity': '刀具', 'relation': '属于', 'attribute': '消耗性资源'},
        {'entity': '人力资源', 'relation': '包含', 'attribute': '一线人员'},
        {'entity': 'Machining Staff', 'relation': 'is a', 'attribute': 'Frontline Staff'},
        {'entity': 'ERP', 'relation': 'is a', 'attribute': 'Application System Resource'},
        {'entity': 'TRIZ', 'relation': '属于', 'attribute': '创新方法'},

    ]

    user = User(name=name)
    db.session.add(user)
    for m in triples:
        triple = Triple(entity=m['entity'], relation=m['relation'], attribute=m['attribute'])
        db.session.add(triple)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
