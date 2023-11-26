from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read_table", methods=["POST"])
def read_table():
    print("Hello")
    data = request.get_json()
    table_data = data.get('tableData')
    print(table_data)

    # simplex_table = [[float(val) for val in row.values()] for row in table_data]
    # for row in simplex_table:
    #     print(row)

    return f"Полученные данные: {table_data}"


if __name__ == "__main__":
    app.run(debug=True)