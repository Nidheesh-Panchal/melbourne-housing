from flask import Flask, request, app, url_for, render_template, jsonify
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)
model = pickle.load(open("./src/model/model.pkl", "rb"))
scaler = pickle.load(open("./src/model/scaler.pkl", "rb"))
labeller = pickle.load(open("./src/model/labeller.pkl", "rb"))

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/api/predict", methods = ["POST"])
def api_predict():
	data = request.json["data"]
	print(data)

	# Now we need to get the data, we have 2 categorical variables, Type is just a one hot encoding
	# so we can convert that easily, we need to use the labeller for the suburb

	house_type = data["type"]
	suburb = data["suburb"]
	rooms = data["rooms"]
	distance = data["distance"]
	bathroom = data["bathroom"]
	landsize = data["landsize"]

	house_type_u=0
	house_type_t=0

	if(house_type == "u"):
		house_type_u = 1
	elif(house_type == "t"):
		house_type_t = 1

	suburb_1 = labeller.transform([suburb])[0]

	x = np.array([house_type_u, house_type_t, suburb_1, rooms, distance, bathroom, landsize])
	print(x.shape)

	# now scale the input

	x_scaled = scaler.transform(x.reshape(1,-1))
	print(x_scaled.shape)

	y_pred = model.predict(x_scaled)
	print(y_pred)

	return jsonify(round(y_pred[0], 2))

if __name__ == "__main__":
	app.run(debug=True)