from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app=Flask(__name__)


@app.route("/", methods=["POST","GET"])
def login():
	if request.method=="POST":
		code=request.form["code"]
		return redirect(url_for("result",code=code))
	else:
		return render_template('base.html')

@app.route("/<code>")
def result(code):
		return render_template("result.html")

if __name__=="__main__":
	app.run(debug=True)




