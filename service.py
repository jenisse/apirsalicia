from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from sqlalchemy import create_engine



class Recommendations(Resource):
    def get(self, dato):
        db_connect = create_engine('postgres://dhkuugcsguuvmc:72aae72895616c0a4afcb2fbc3ffdb9da9d5cf6a33373d3ed93b1490d32183b1@ec2-54-243-213-188.compute-1.amazonaws.com:5432/d1i8j5vuaca7m0')
        conn = db_connect.connect()
        rese_id ='id_investigador='+str(dato)
        query=conn.execute( """select Similar_Orcid.title, Similar_Orcid.similarity_percentage, Publicacion_Alicia.url, Publicacion_Alicia.title as titulo_alicia from Similar_Orcid  INNER JOIN Publicacion_Alicia on Similar_Orcid.identifier=Publicacion_Alicia.identifier where link_dina like ('%' || ? || '%')""", (rese_id,))
        result = {'recommendations': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
class RandomRecommendation(Resource):
    def get(self, dato):
        db_connect = create_engine('postgres://dhkuugcsguuvmc:72aae72895616c0a4afcb2fbc3ffdb9da9d5cf6a33373d3ed93b1490d32183b1@ec2-54-243-213-188.compute-1.amazonaws.com:5432/d1i8j5vuaca7m0')
        conn = db_connect.connect()
        rese_id ='id_investigador='+str(dato)
        query=conn.execute( """select Similar_Orcid.title, Similar_Orcid.similarity_percentage, Publicacion_Alicia.url, Publicacion_Alicia.title as titulo_alicia from Similar_Orcid  INNER JOIN Publicacion_Alicia on Similar_Orcid.identifier=Publicacion_Alicia.identifier where link_dina like ('%' || ? || '%') ORDER BY RANDOM() LIMIT 1""", (rese_id,))
        result = {'recommendation': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
class Shutdown(Resource):
    def get(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

class Service:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        
        #self.api.add_resource(Prueba, '/prueba') #'/employees/<employee_id>'
        self.api.add_resource(Recommendations, '/recomendaciones/<dato>')
        self.api.add_resource(RandomRecommendation, '/recomendacion_aleatoria/<dato>')
        self.api.add_resource(Shutdown, '/shutdown')

        
    def run(self):
        self.app.run(port=5002)
        
        
if __name__ == '__main__':
    print("ANTES")
    servicio=Service()
    servicio.run()
    print("HOLA")




