import os 
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from flask import Flask, render_template, request, send_from_directory , redirect

# Global values :
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
employee_name = ""
client_name = ""
error = ""

def connect():	
	session = cluster.connect()
	session.row_factory = dict_factory
	return session

def run_cql(session, fileName):
	f = open(fileName, 'r')
	txt = f.read()
	statement_list = txt.split(';')
	for statement in statement_list:
		stmt = statement.strip()
		if stmt != '':
			#print('Executing "' + stmt + '"')
			session.execute(stmt)



app = Flask(__name__)

@app.route('/')
def index():
	session = connect()
	run_cql(session, "Creation.cql")
	run_cql(session, "Insertions.cql")
	return render_template("index.html")


@app.route('/login_page.html', methods=['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':
		session = connect()
		query = """
			SELECT COUNT(*) FROM BD.Empleado 
			WHERE username = '""" + request.form['user_name'] + """' AND
			password = '""" + request.form['password'] + """' ALLOW FILTERING; """
		
		result = session.execute(query)[0]

		if result['count'] < 1:
			error = 'Datos incorrectos, inténtelo de nuevo'
		else:
			query2 = """ 
				SELECT nombre FROM BD.Empleado
				WHERE username = '""" + request.form['user_name'] + """'ALLOW FILTERING; """
			result2 = session.execute(query2)[0]

			global employee_name
			employee_name = result2['nombre']
			print(employee_name)
			return redirect('main_view.html')

	#if request.method == 'GET':
	#		error = None
	return render_template('login_page.html', error=error)


@app.route('/main_view.html')
def view():
	
	global employee_name
	print(employee_name)
	if employee_name != "":
		return render_template("main_view.html", employee_name = employee_name)
	else:
		error = "No ha iniciado sesión"
		return redirect('login_page.html')



@app.route('/start_sale.html', methods=['GET', 'POST'])
def login_client():
	error = None
	if request.method == 'POST':
		session = connect()
		query = """
			SELECT COUNT(*) FROM BD.Cliente 
			WHERE DNI = """ + request.form['client_DNI'] + """  ALLOW FILTERING; """
		
		result = session.execute(query)[0]

		if result['count'] < 1:
			error = 'DNI incorrecto, inténtelo de nuevo'
		else:
			query2 = """ 
				SELECT nombre FROM BD.Cliente
				WHERE DNI = """ + request.form['client_DNI'] + """  ALLOW FILTERING; """
			result2 = session.execute(query2)[0]

			global client_name
			client_name = result2['nombre']
			print(client_name)
			return redirect('main_client_view.html')

	#if request.method == 'GET':
	#		error = None
	return render_template('start_sale.html', error=error)


@app.route('/main_client_view.html', methods=['GET', 'POST'])
def client_view():
	return render_template("main_client_view.html", client_name = client_name)





@app.route('/<page>')
def web_dir(page):
	return render_template("/" + page)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), '/Images/icon.jpg')




if __name__ == '__main__':
   app.run(debug = True)