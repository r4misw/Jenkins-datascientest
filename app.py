from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/api/hello")
def hello():
    return jsonify({"hello": "world"})


@app.route("/api/hello/<name>")
def hello_name(name):
    return jsonify({"hello": name})


@app.route("/api/whoami")
def whoami():
    return jsonify(
        name=request.remote_addr,
        ip=request.remote_addr,
        useragent=request.user_agent.string,
    )


@app.route("/api/whoami/<name>")
def whoami_name(name):
    return jsonify(
        name=name,
        ip=request.remote_addr,
        useragent=request.user_agent.string,
    )


if __name__ == "__main__":
    app.run()