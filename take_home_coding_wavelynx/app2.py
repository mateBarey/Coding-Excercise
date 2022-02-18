from dummyapi import token 
import models
from models import Token 
from database import SessionLocal, engine, sqlalchemy_db_url
from flask import Flask, request , jsonify
import pandas as pd 
from flask_restful import Api , Resource

app = Flask(__name__)
api = Api(app,catch_all_404s=True)

#Make db table  and create a db session
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

class GetToken(Resource):
    def get(self):
        """
        Generate and store a new token.
        """
        new_token: str = token.generate_token()
        #Store tokens into session db
        db.add(Token(token=f'{new_token}'))
        db.commit()
        db.close()
        retJson = {
                        "status":200,
                        "msg":"Token generated successfully!" ,
                        "token":new_token
                    }

        #uncomment to visualize Token Table 
        df = pd.read_sql_table('tokens',sqlalchemy_db_url)
        print(df)
        return jsonify(retJson)

class Verify(Resource):
    def post(self):
        """
        Verify that the provided token has been previously generated.
        """
        if request:
            postedData = request.get_json(force=True)
            reqToken = postedData["token"]
            if len(reqToken) >= 8 and len(reqToken) <= 32:
                query = db.query(Token).filter(Token.token == f'{reqToken}').first()
                if query:
                    retJson = {
                            "status":200,
                            "msg":"Token already saved once" 
                        }
                    return jsonify(retJson)
                else:
                    retJson = {
                        "status": 200,
                        "msg": "Token not found!"}
                    return jsonify(retJson)
            else:
                retJson = {
                    "status": 200,
                    "msg": "Invalid Token Length!"}
                return jsonify(retJson)
        else:
            retJson = {
                "status":400,
                "msg": "Invalid JSON Request"
            }
            return jsonify(retJson)

api.add_resource(GetToken, '/getToken')
api.add_resource(Verify, '/verifyToken')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
