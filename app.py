import os 
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
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

def generatePDF(temp_dict):
	doc = SimpleDocTemplate("Factura.pdf")
	styles = getSampleStyleSheet()
	#Escribimos una cadena de Texto dentro del documento
	elements = []
	conection = connect()

	total = 0
	data = []
	data.append(["Id", "Nombre", "Precio", "Cantidad"])
	for item in temp_dict.keys():
		query = """
			SELECT * FROM BD.Producto
			WHERE id=""" + item
		result = conection.execute(query)[0]
		temp = [item, result['nombre'], "S/." + str(result['precio']), str(temp_dict.get(item))]
		data.append(temp)
		total += (result['precio'] * temp_dict.get(item) )

	t=Table(data)
	
	text = "          FACTURA"
	para = Paragraph(text, style=styles["Heading1"])
	text2 = "                    Total: S/." + str(total)
	para2 = Paragraph(text2, style=styles["Heading2"])
	elements.append(para)
	elements.append(t)
	elements.append(para2)

	#doc.drawString(100 , base + it, "Total: S/." + str(total))
	#Guardamos el documento
	doc.build(elements)
	return total


def insertFactura(temp_dict):
	conection = connect()
	today = datetime.today().strftime('%Y-%m-%d')
	total = 0
	for item in temp_dict.keys():
		query = """
			SELECT precio FROM BD.Producto
			WHERE id=""" + item
		result = conection.execute(query)[0]

		total += (result['precio'] * temp_dict.get(item) )

	#get the correct id of the "Factura"
	query2 = "SELECT MAX(id) as maximo from BD.factura;"
	max_id = str(conection.execute(query2)[0]['maximo'] +1)

	products = s = "".join(str(temp_dict).split("'"))
	print(products)

	query3 = """
		INSERT INTO BD.factura (id, fecha, costo, id_producto) 
		VALUES (""" + max_id + """, '""" + today + """', """ + str(total) + """, """ + products + """)"""
	conection.execute(query3)




app = Flask(__name__)
app.secret_key = 'very-secret-key'

@app.route('/')
def index():
	conection = connect()
	run_cql(conection, "Creation.cql")
	run_cql(conection, "Insertions.cql")
	#print("Inicio de web exitoso")
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



@app.route('/register_page.html', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		conection = connect()
		name = request.form.get("name")
		last_name = request.form.get("last_name")
		username = request.form.get("user")
		DNI = request.form.get("client_DNI")
		password = request.form.get("password")

		values = DNI+","+"'"+name+"'"+","+"'"+last_name+"'"+","+"'"+username+"'"+","+"'"+password+"'"

		print(values)
		#Conexión
		query = """
			INSERT INTO BD.empleado (DNI, nombre, apellidos, username, password)
			VALUES ("""+ values + """);"""
		result = conection.execute(query)

		return redirect('/')

	return render_template('register_page.html')


@app.route('/register_client_page.html', methods = ['GET', 'POST'])
def registerClient():
	
	print("Registrar cliente")

	if request.method == 'POST':
		
		conection = connect()
		name = request.form.get("name")
		last_name = request.form.get("last_name")
		DNI = request.form.get("client_DNI")
		RUC = request.form.get("client_RUC")
		credit_target = request.form.get("credit")

		values = DNI+","+"'"+last_name+"'"+","+"'"+name+"'"+","+RUC+","+credit_target

		print("POST: Register Client: ", values)

		query = """
			INSERT INTO BD.cliente (dni, apellidos, nombre, ruc,tarjeta_credito)
			VALUES ("""+ values + """);"""

		conection.execute(query)

		return redirect('/start_sale.html')

	return render_template('register_client_page.html')



@app.route('/main_view.html', methods=['GET', 'POST'])
def view():
	if request.method == 'GET':
		if 'employee_name' in session:
			if session['employee_name'] != "":
				return render_template("main_view.html", employee_name = session['employee_name'])
			else:
				error = "No ha iniciado sesión"
				return redirect('login_page.html')
		else:
			error = "No ha iniciado sesión"
			return redirect('login_page.html')

	elif request.method == 'POST':
		session.clear()
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


@app.route('/main_client_view.html', methods=['GET', 'POST'])
def client_view():
	if 'client_name' not in session:
		return redirect("main_view.html")
	else:
		if request.method == 'GET':
			if 'product_list' not in session:
				return render_template("main_client_view.html", 
					client_name = session['client_name'],
					total = "0.0")
			else:
				return render_template("main_client_view.html", 
					client_name = session['client_name'], product_list = session['product_list'],
					total = "0.0")
		
		elif request.method == 'POST':
			if 'product_list' in session:
				temp_dict = session['product_list']
				total = generatePDF(temp_dict)
				insertFactura(temp_dict)
				session.pop('product_list', None)
				return render_template("main_client_view.html", 
						client_name = session['client_name'],
						total = total)
			return render_template("main_client_view.html", 
						client_name = session['client_name'],
						total = "0.0")








@app.route('/add_product.html', methods=['GET', 'POST'])
def add_product():
	if 'client_name' not in session:
		return redirect("start_sale.html")
	else:
		if 'product_list' not in session:
			session['product_list'] = {}

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

			if stock_ > 0:
				query2 = """
					UPDATE BD.producto
  					SET stock = """ + str(stock_ -1) + """
					WHERE id=""" + str(request.form['product_id'])
				conection.execute(query2)

				temp_dict = session['product_list']
				temp_dict[request.form['product_id']] = temp_dict.get(request.form['product_id'], 0) +1
				session['product_list'] = temp_dict

			result = conection.execute(query)
			return render_template('add_product.html', products = result)




@app.route('/ask_for_product.html', methods=['GET', 'POST'])
def query_product():
	conection = connect()
	#query
	if request.method == "POST":
		search_by = request.form['search']
		if search_by == "by_id":
			query = """ 
				SELECT * FROM BD.Producto 
				WHERE ID=""" + request.form['for_search'] + " ALLOW FILTERING"
		elif search_by == "by_name":
			query = """
				SELECT * FROM BD.Producto
				WHERE nombre='""" + request.form['for_search'] +"' ALLOW FILTERING"

		print(query)
		result = conection.execute(query)[0]
		print(result)

		return render_template('ask_for_product.html',
				data = result)

	else:
		return render_template('ask_for_product.html')




@app.route('/insert_product.html', methods=['GET', 'POST'])
def insert_product():
	if request.method == 'POST':
		conection = connect()
		id_ = request.form.get("product_id")
		nombre = request.form.get("product_name")
		precio = request.form.get("product_price")
		descripcion = request.form.get("description")
		stock = request.form.get("stock")

		values = id_+","+"'"+nombre+"'"+","+"'"+descripcion+"'"+","+precio+","+stock

		#Conexión
		query = """
			INSERT INTO BD.Producto (id, nombre, descripcion, precio, stock)
			VALUES ("""+ values + """);"""
		print(query)
		result = conection.execute(query)

	return render_template('insert_product.html')


@app.route('/delete_product.html', methods=['GET', 'POST'])
def delete_product():
	if request.method == 'POST':
		query1 = """
			DELETE FROM BD.producto
			WHERE id=""" + str(request.form['product_id'])
		conection = connect()
		conection.execute(query1)

	query = "SELECT * FROM BD.Producto ALLOW FILTERING; "
	conection = connect()
	result = conection.execute(query)
	return render_template('delete_product.html', products = result)


@app.route('/<page>')
def web_dir(page):
	return render_template("/" + page)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), '/Images/icon.jpg')




if __name__ == '__main__':
   app.run(debug = True)
