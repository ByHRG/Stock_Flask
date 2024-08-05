from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource
from flask_cors import CORS
from Utills.Stock.kasina import KASINA
from Utills.Stock.abc import ABCMART


app = Flask(__name__)
CORS(app)
api = Api(app)


@api.documentation
def custom_ui():
    return render_template(
        "swagger-ui.html", title=api.title, specs_url="/static/swagger.json"
    )

@api.route("/kasina")
class Kasina(Resource):
    def get(self):
        data = request.args.to_dict()["product_code"]
        output = KASINA().run(data)
        return jsonify(output)


@api.route("/abcmart")
class Abc(Resource):
    def get(self):
        data = request.args.to_dict()
        output = ABCMART().run(data)
        return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="6452", debug=True)
