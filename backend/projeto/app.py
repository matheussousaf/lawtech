from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = 'cadastro'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    adress = db.Column(db.String)
    cpf = db.Column(db.String)
    birth_date = db.Column(db.Date)
    lat = db.Column(db.Integer)
    long = db.Column(db.Integer)
    url_certificate = db.Column(db.String)
    rating = db.Column(db.Float)

    def __init__(self, name, description, adress, cpf, birth_date, lat, long, url_certificate, rating):
        self.name = name
        self.description = description
        self.adress = adress
        self.cpf = cpf
        self.birth_date = birth_date
        self.lat = lat
        self.long = long
        self.url_certificate = url_certificate
        self.rating = rating

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        description = request.form.get('description')
        adress = request.form.get('adress')
        cpf = request.form.get('cpf')
        birth_date = request.form.get('birth_date')
        lat = request.form.get('lat')
        long = request.form.get('long')
        url_certificate = request.form.get('url_certificate')
        rating = request.form.get('rating')
        email = request.form.get('email')

        if nome and cpf and adress and birth_date and lat and long and url_certificate and rating and email and description:
            p = Pessoa(nome,description, adress, cpf,birth_date,lat,long,url_certificate,rating,email)
            db.session.add(p)
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/lista')
def lista():
    listaCadastro = Pessoa.query.all()
    return render_template('lista.html', add = listaCadastro)

@app.route('/deletar/<int:id>')
def deletar(id):
    pessoa = Pessoa.query.filter_by(_id = id).first()
    db.session.delete(pessoa)
    db.session.commit()

    listaCadastro = Pessoa.query.all()
    return render_template('lista.html', pessoas = listaCadastro)

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id = id).first()

    if request.method == 'POST':
        nome = request.form.get('nome')
        description = request.form.get('description')
        adress = request.form.get('adress')
        cpf = request.form.get('cpf')
        birth_date = request.form.get('birth_date')
        lat = request.form.get('lat')
        long = request.form.get('long')
        url_certificate = request.form.get('url_certificate')
        rating = request.form.get('rating')
        email = request.form.get('email')

        if nome and cpf and adress and birth_date and lat and long and url_certificate and rating and email and description:
            p = Pessoa(nome, description, adress, cpf, birth_date, lat, long, url_certificate, rating, email)
            db.session.add(p)
            db.session.commit()
            return jsonify({'message': 'sucessfuly fetched','data': result.data}),201
    return jsonify({'message': "user don't exist", 'data': {}}),404

if __name__ == '__main__':
    app.run()
