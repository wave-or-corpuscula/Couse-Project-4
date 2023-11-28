from flask import Flask, render_template, request, flash, redirect, url_for, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = "sjdFODJdsojfsodfjPFJdjs546sdfsoidfjPfj"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simplex_solve", methods=["POST", "GET"])
def read_table():
    if request.method == "POST":
        print(request.form)
    print(request.method)
    # data = request.get_json()
    # table_data = data.get('tableData')

    # targer_func = table_data.get("targetFunction")
    # constraints = table_data.get("constraintsData")
    # print(targer_func)
    # for c in constraints:
    #     print(c)

    # for k, v in table_data.items():
    #     print(f"{k}: {v}")

    return render_template("index.html", simplex_solution=True)


if __name__ == "__main__":
    app.run(debug=True)
