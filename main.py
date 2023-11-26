from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read_table", methods=["POST"])
def read_table():
    data = request.get_json()
    table_data = data.get('tableData')

    targer_func = table_data.get("targetFunction")
    constraints = table_data.get("constraintsData")
    print(targer_func)
    for c in constraints:
        print(c)
        


    return f"Полученные данные: {table_data}"


if __name__ == "__main__":
    app.run(debug=True)