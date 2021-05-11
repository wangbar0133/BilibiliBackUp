from flask import Flask, render_template, request, redirect, session, make_response


app = Flask(__name__)

@app.route('/backup/search/video/<id>', methods=['GET'])
def search_video(id):
    pass