#IMPORTAR LIBRERIAS
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config[
	'SQLALCHEMY_DATABASE_URI'
] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(
		db.Integer,
		primary_key = True
	)
	content = db.Column(
		db.String(200),
		nullable = False
	)
	completed = db.Column(
		db.Integer,
		default = 0
	)
	date_created = db.Column(
		db.DateTime,
		default = datetime.utcnow
	)

	def __repr__(self):
		return '<Task %r>' % self.id

#creación de routes
@app.route('/', methods=['POST', 'GET'])
def index():
	#return "Hola mundo"
	#return render_template('index.html')
	if request.method == 'POST':
		contenido_tarea = request.form['content']
		tarea = Todo(content = contenido_tarea)

		try:
			db.session.add(tarea)
			db.session.commit()
			return redirect('/')
		except:
			return 'Hubo un error al registrar la tarea'
	else:
		tareas = Todo.query.order_by(
			Todo.date_created
		).all()
		return render_template('index.html', tareas = tareas)

@app.route('/delete/<int:id>')
def delete(id):
	tarea_a_eliminar = Todo.query.get_or_404(id)

	try:
		db.session.delete(tarea_a_eliminar)
		db.session.commit()
		return redirect('/')
	except:
		return 'Hubo un problema al borrar la tarea'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	tarea = Todo.query.get_or_404(id)
	if request.method == 'POST':
		tarea.content = request.form['content']

		try:
			db.session.commit()
			return redirect('/')
		except:
			return "Hubo un problema al actualizar la tarea"
	else:
		return render_template(
			'actualizar.html',
			tarea = tarea
		)

if __name__ == "__main__":
	app.run(debug = True)