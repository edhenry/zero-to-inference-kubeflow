import flask
import numpy as np
import mnist
import uuid

app = flask.Flask(__name__, template_folder="")
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "dev"

@app.route("/", methods=["GET","POST"])
def index():
    #Initialize session id and counter
    if "id" not in flask.session:
        flask.session["id"] = uuid.uuid1()
    if "num_data" not in flask.session:
        flask.session["num_data"] = 0
    if "prediction" not in flask.session:
        flask.session["prediction"] = ""

    #Handle POST requests
    if flask.request.method=="POST":
        data = flask.request.data
        handle=mnist.handle(data)
        if(handle==1):
            flask.session["num_data"] = flask.session["num_data"] + 1
            mnist.process_data(data, flask.session["id"], flask.session["num_data"])
        elif(handle==2):
            flask.session["prediction"]=mnist.predict(data).tolist()
        elif(handle==3):
            if flask.session["num_data"] > 0:
                mnist.delete(flask.session["id"], flask.session["num_data"],1)
                flask.session["num_data"] = flask.session["num_data"] - 1
        elif(handle==4):
            #Convert to string
            data = data.decode("utf-8")
            #Create numpy array from string and reshape to 2D
            data = np.array(data.split('/'))
            ground=data[0]
            ground = ground.replace("\"", "")
            ground = int(ground)
            mnist.train(flask.session["id"], flask.session["num_data"],ground)
            flask.session["num_data"]=0

    return flask.render_template("./index.html", 
            num_data=flask.session["num_data"], 
            prediction=flask.session["prediction"],
            user_id=flask.session["id"])


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000, debug = True)