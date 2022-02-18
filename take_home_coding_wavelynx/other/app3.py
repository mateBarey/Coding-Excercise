from flask_api import FlaskAPI, status
from dummyapi import token 
import models
from models import Token 
from flask import jsonify, request, _app_ctx_stack
from database import SessionLocal, engine 
from sqlalchemy.orm import scoped_session
import pandas as pd 


app = FlaskAPI(__name__)
app.tokens = []

#sqlalchemy stuff
models.Base.metadata.create_all(bind=engine)

db_session= scoped_session(SessionLocal,scopefunc=_app_ctx_stack.__ident_func__)

@app.route("/token", methods=["GET"])
def get_token():
    """
    Generate and store a new token.
    """
    new_token: str = token.generate_token()
    app.tokens.append(new_token)
    #store token here into db
    db_session.add(Token(token=f'{new_token}'))
    db_session.commit()
    db_session.close()
    #fix this part
    # 
    retJson = {
                    "status":200,
                    "msg":"Token generated successfully!" ,
                    "token":new_token
                }

    #df = pd.read_sql_table('tokens',sqlalchemy_db_url)
    #print(df)
    return jsonify(retJson)

@app.route("/verify", methods=["POST"])
def verify_token():
    """
    Verify that the provided token has been previously generated.
    """
    if request:
        postedData = request.get_json()

        reqToken = postedData["token"]

        if len(reqToken) >= 8 and len(reqToken) <= 32:
            query = db_session.query(Token).filter(Token.token == f'{reqToken}').first()
            
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
