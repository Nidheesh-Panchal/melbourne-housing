# Melbourne Housing: Price Prediction

Using the [Melbourne Housing dataset](https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot) from kaggle, generated a linear regression model to predict the house prices of Melbourne using the predictors: type of the house, suburb house is located in, distance of the house from CBD, number of bathrooms and rooms in the house, total landsize for the house.

Detailed analysis located in the jupyter notebook in the src folder.

<!-- ### Tools Used:
1. [Github](https://github.com)
2. [VSCode](https://code.visualstudio.com)
3. [GitCLI](https://git-scm.com/downloads) -->

### Setup:
Create new environment for the application using Anaconda at the root project folder and install the required packages for python

```
$ conda create -p venv python==3.7 -y
$ conda activate venv
$ pip install -r requirements.txt
```

### Run:
Use the following command to run the Flask server on localhost

```
$ python ./src/n1.py
```

### Website
Open the following URL in the browser of your choice
```
http://localhost:{port}/
```

### API route:
Use the postman collection placed in the Resources folder to use the API
```
http://localhost:{port}/api/predict
```

### Screenshot
![Image](./Resources/melb.png)

### Future work
The flask app can be hosted on any cloud platform or can be containerized. Can deploy the app as backend and use a separate Angular or React frontend for better user experience.