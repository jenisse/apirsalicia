from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from sqlalchemy import create_engine



class Recommendations(Resource):
    def get(self, dato):
		host = "ec2-50-16-196-238.compute-1.amazonaws.com:5432"
		db = "de925n6fc4qpge"
		user = "aaiekzlymkmulx"
		pw = "688099ba64af630040260c2d81a5354098b4773ca07fb0163d49ee36928fa342"
        db_connect = create_engine('postgres://'+user+':'+pw+'@'+host+'/'+db)
		rese_id ='https://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador='+str(dato)
		s=text("(select a.title, t.similarity_percentage, a.link from alicia a, scopus_similar t where t.link_dina=:dato and a.identifier=t.identifier) union (select a.title, t.similarity_percentage, a.link from alicia a, orcid_similar t where t.link_dina=:dato and a.identifier=t.identifier) order by similarity_percentage desc limit 10;")
		query=conn.execute( s, dato=rese_id)
		result = {'recommendations': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		conn.close()
		db_connect.dispose()	
        return jsonify(result)
class RandomRecommendation(Resource):
    def get(self, dato):
        host = "ec2-50-16-196-238.compute-1.amazonaws.com:5432"
		db = "de925n6fc4qpge"
		user = "aaiekzlymkmulx"
		pw = "688099ba64af630040260c2d81a5354098b4773ca07fb0163d49ee36928fa342"
        db_connect = create_engine('postgres://'+user+':'+pw+'@'+host+'/'+db)
		rese_id ='https://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador='+str(dato)
		s=text("(select a.title, t.similarity_percentage, a.link from alicia a, scopus_similar t where t.link_dina=:dato and a.identifier=t.identifier order by random()) union (select a.title, t.similarity_percentage, a.link from alicia a, orcid_similar t where t.link_dina=:dato and a.identifier=t.identifier order by random())  limit 1;")
        result = {'recommendation': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        conn.close()
		db_connect.dispose()
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
