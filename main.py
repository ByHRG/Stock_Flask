from flask import Flask, render_template, request, jsonify, send_file, redirect
from flask_restx import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.documentation
def custom_ui():
    return render_template(
        "swagger-ui.html", title=api.title, specs_url="/static/swagger.json"
    )

