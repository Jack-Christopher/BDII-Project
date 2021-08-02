import os 
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table
from reportlab.lib.styles import getSampleStyleSheet
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


@app.route('/register_page.html', methods=['GET', 'POST'])
def register():
	error = None
	print("b")
	if request.method == 'POST':
		print("d")
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
			INSERT INTO BD.empleado (DNI, nombre, apellidos, username,password)
			VALUES ("""+ values + """);"""
		result = conection.execute(query)

		return redirect('/')

	return render_template('register_page.html')


@app.route('/main_view.html', methods=['GET', 'POST'])
def view():
	if request.method == 'GET':
		if session['employee_name'] != "":
			return render_template("main_view.html", employee_name = session['employee_name'])
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
		return redirect("start_sale.html")
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
			temp_dict = session['product_list']
			total = generatePDF(temp_dict)
			session.pop('product_list', None)
			return render_template("main_client_view.html", 
					client_name = session['client_name'],
					total = total)







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




@app.route('/<page>')
def web_dir(page):
	return render_template("/" + page)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), '/Images/icon.jpg')




if __name__ == '__main__':
   app.run(debug = True)
