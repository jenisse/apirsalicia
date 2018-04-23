from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from sqlalchemy import create_engine
import os

app = Flask(__name__)

@app.route('/recomendaciones/<dato>')
def recommendations(dato):
    db_connect = create_engine('postgres://dhkuugcsguuvmc:72aae72895616c0a4afcb2fbc3ffdb9da9d5cf6a33373d3ed93b1490d32183b1@ec2-54-243-213-188.compute-1.amazonaws.com:5432/d1i8j5vuaca7m0')
    conn = db_connect.connect()
    rese_id ='id_investigador='+str(dato)
    #query=conn.execute( """select Similar_Orcid.title, Similar_Orcid.similarity_percentage, Publicacion_Alicia.url, Publicacion_Alicia.title as titulo_alicia from Similar_Orcid  INNER JOIN Publicacion_Alicia on Similar_Orcid.identifier=Publicacion_Alicia.identifier where link_dina like ('%' || ? || '%')""", (rese_id,))
    query=conn.execute("select * from Investigador")
    result = {'recommendations': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

@app.route('/recomendacion_aleatoria/<dato>') 
def randomRecommendation(dato):
    db_connect = create_engine('postgres://dhkuugcsguuvmc:72aae72895616c0a4afcb2fbc3ffdb9da9d5cf6a33373d3ed93b1490d32183b1@ec2-54-243-213-188.compute-1.amazonaws.com:5432/d1i8j5vuaca7m0')
    conn = db_connect.connect()
    rese_id ='id_investigador='+str(dato)
    query=conn.execute( """select Similar_Orcid.title, Similar_Orcid.similarity_percentage, Publicacion_Alicia.url, Publicacion_Alicia.title as titulo_alicia from Similar_Orcid  INNER JOIN Publicacion_Alicia on Similar_Orcid.identifier=Publicacion_Alicia.identifier where link_dina like ('%' || ? || '%') ORDER BY RANDOM() LIMIT 1""", (rese_id,))
    result = {'recommendation': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

@app.route('/shutdown')        
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




