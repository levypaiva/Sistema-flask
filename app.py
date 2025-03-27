from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deposito.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    localizacao = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    itens = Item.query.all()
    return render_template('index.html', itens=itens)

@app.route('/add', methods=['POST'])
def add_item():
    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']
    localizacao = request.form['localizacao']
    novo_item = Item(nome=nome, categoria=categoria, quantidade=quantidade, localizacao=localizacao)
    db.session.add(novo_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
