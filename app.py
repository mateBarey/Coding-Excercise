from flask_api import FlaskAPI, status
from dummyapi import token 
import models
from models import Token 
from flask import  jsonify, request
from database import SessionLocal, engine, sqlalchemy_db_url
import pandas as pd 


app = FlaskAPI(__name__)


#sqlalchemy Build Models Table
models.Base.metadata.create_all(bind=engine)


#Create A Session object to initiate Queries in a db
db = SessionLocal()


@app.route("/token", methods=["GET"])
def get_token():
    """
    Generate and store a new token.
    """
    new_token: str = token.generate_token()

    #store token  into db 
    db.add(Token(token=f'{new_token}'))
    db.commit()
    db.close()

    retJson = {
                    "status":200,
                    "msg":"Token generated succesfully!" ,
                    "token":new_token
                }

    #uncomment to visualize Token Table 
    #df = pd.read_sql_table('tokens',sqlalchemy_db_url)
    #print(df.head())
    return jsonify(retJson)


@app.route("/verify", methods=["POST"])
def verify_token():
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


@app.route(
    "/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
)
def catch_all(path):
    """
    Return errors for all invalid paths or request methods.
    """
    return (
        {"status": "error"},
        status.HTTP_404_NOT_FOUND,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
