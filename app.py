import os 
from cassandra.cluster import Cluster
from flask import Flask, render_template, request, send_from_directory  


def connect():
	cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
	session = cluster.connect()
	return session

def create_keyspace(session):
	session.execute("""CREATE KEYSPACE bd WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} 
				AND durable_writes = 'true';""")



app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/<page>')
def HTML(page):
	return render_template("/" + page)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), '/Images/icon.jpg')




if __name__ == '__main__':
   app.run(debug = True)