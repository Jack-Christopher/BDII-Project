import os 
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from flask import Flask, render_template, request, send_from_directory , redirect, session

# Global values :
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)

def connect():	
	conection = cluster.connect()
	conection.row_factory = dict_factory
	return conection

def run_cql(conection, fileName):
	f = open(fileName, 'r')
	txt = f.read()
	statement_list = txt.split(';')
	for statement in statement_list:
		stmt = statement.strip()
		if stmt != '':
			#print('Executing "' + stmt + '"')
			conection.execute(stmt)



app = Flask(__name__)
app.secret_key = 'very-secret-key'


@app.route('/')
def index():
	conection = connect()
	run_cql(conection, "Creation.cql")
	run_cql(conection, "Insertions.cql")
	print("ok")
	return render_template("index.html")


@app.route('/login_page.html', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		conection = connect()
		query = """
			SELECT COUNT(*) FROM BD.Empleado 
			WHERE username = '""" + request.form['user_name'] + """' AND
			password = '""" + request.form['password'] + """' ALLOW FILTERING; """
		
		result = conection.execute(query)[0]

		if result['count'] < 1:
			error = 'Datos incorrectos, inténtelo de nuevo'
		else:
			query2 = """ 
				SELECT nombre FROM BD.Empleado
				WHERE username = '""" + request.form['user_name'] + """'ALLOW FILTERING; """
			result2 = conection.execute(query2)[0]

			session['employee_name'] = result2['nombre']
			return redirect('main_view.html')

	elif request.method == 'GET':
		if 'employee_name' in session:
			return redirect('main_view.html')
	return render_template('login_page.html', error=error)


@app.route('/main_view.html')
def view():
	if session['employee_name'] != "":
		return render_template("main_view.html", employee_name = session['employee_name'])
	else:
		error = "No ha iniciado sesión"
		return redirect('login_page.html')



@app.route('/start_sale.html', methods=['GET', 'POST'])
def login_client():
	if request.method == 'POST':
		conection = connect()
		query = """
			SELECT COUNT(*) FROM BD.Cliente 
			WHERE DNI = """ + request.form['client_DNI'] + """  ALLOW FILTERING; """
		
		result = conection.execute(query)[0]

		if result['count'] < 1:
			error = 'DNI incorrecto, inténtelo de nuevo'
		else:
			query2 = """ 
				SELECT nombre FROM BD.Cliente
				WHERE DNI = """ + request.form['client_DNI'] + """  ALLOW FILTERING; """
			result2 = conection.execute(query2)[0]

			session['client_name'] = result2['nombre']
			return redirect('main_client_view.html')

	if request.method == 'GET':
		error = None
	return render_template('start_sale.html', error=error)


@app.route('/main_client_view.html')
def client_view():
	if 'client_name' not in session:
		#error = "No ha seleccionado a un cliente"
		return redirect("start_sale.html")
	else:
		if 'bought_products' not in session:
			return render_template("main_client_view.html", 
				client_name = session['client_name'])
		else:
			return render_template("main_client_view.html", 
				client_name = session['client_name'], bought_products = session['bought_products'])




@app.route('/add_product.html', methods=['GET', 'POST'])
def add_product():
	if 'client_name' not in session:
		return redirect("start_sale.html")
	else:
		query = "SELECT * FROM BD.Producto ALLOW FILTERING; "

		if request.method == 'GET':
			conection = connect()
			result = conection.execute(query)
			return render_template('add_product.html', products = result)
		if request.method == 'POST':
			query1 = """
				SELECT stock FROM BD.producto
				WHERE id=""" + str(request.form['product_id'])
			conection = connect()
			stock_ = conection.execute(query1)[0]['stock']

			query2 = """
				UPDATE BD.producto
  				SET stock = """ + str(stock_ -1) + """
				WHERE id=""" + str(request.form['product_id'])
			conection.execute(query2)

			result = conection.execute(query)
			return render_template('add_product.html', products = result)




@app.route('/<page>')
def web_dir(page):
	return render_template("/" + page)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), '/Images/icon.jpg')




if __name__ == '__main__':
   app.run(debug = True)