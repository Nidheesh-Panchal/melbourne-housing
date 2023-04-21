import pickle

import numpy as np
import pandas as pd
from flask import Flask, app, jsonify, render_template, request, url_for

app = Flask(__name__)
model = pickle.load(open("./src/model/model.pkl", "rb"))
scaler = pickle.load(open("./src/model/scaler.pkl", "rb"))
labeller = pickle.load(open("./src/model/labeller.pkl", "rb"))
model_rf = pickle.load(open("./src/model/randomforest.pkl", "rb"))

df = pd.read_csv("./src/data/melb_data.csv")
suburb_list = list(df["Suburb"].unique())
suburb_list.sort()

default = {"rooms": 2, "bathroom": 2, "landsize": 1000, "distance": 12, "car": 2}

def predict(data):
	house_type = data["type"]
	suburb = data["suburb"]
	rooms = data["rooms"]
	distance = data["distance"]
	bathroom = data["bathroom"]
	landsize = data["landsize"]
	car = data["car"]

	# Now we need to get the data, we have 2 categorical variables, Type is just a one hot encoding
	# so we can convert that easily, we need to use the labeller for the suburb

	house_type_h=0
	house_type_u=0
	house_type_t=0

	if(house_type == "u"):
		house_type_u = 1
	elif(house_type == "t"):
		house_type_t = 1
	else:
		house_type_h=1

	suburb_1 = labeller.transform([suburb])[0]

	x = np.array([house_type_u, house_type_t, suburb_1, rooms, distance, bathroom, landsize])
	print(x.shape)

	x_rf = np.array([house_type_h, house_type_u, house_type_t, suburb_1, rooms, distance, bathroom, landsize, car]).reshape(1,-1)

	# now scale the input

	x_scaled = scaler.transform(x.reshape(1,-1))
	print(x_scaled.shape)

	y_pred_lm = round(model.predict(x_scaled)[0], 2)
	print(y_pred_lm)

	y_pred_rf = round(model_rf.predict(x_rf)[0], 2)

	return {"lm": y_pred_lm, "rf": y_pred_rf}

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)

@app.route("/")
def home():
	return render_template("home.html", suburb_list = suburb_list, default = default)

@app.route("/api/predict", methods = ["POST"])
def api_predict():
	data = request.json["data"]
	print(data)

	return jsonify(predict(data))

@app.route("/predict", methods = ["POST"])
def home_predict():
	data = request.form
	print(data)

	y_pred = predict(data)

	return render_template("home.html", suburb_list = suburb_list, default=data, price=y_pred)

if __name__ == "__main__":
	app.run(debug=True)