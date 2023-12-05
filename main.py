from flask import (Flask, 
                    render_template, 
                    request, 
                    flash, 
                    redirect, 
                    url_for, 
                    jsonify,
                    make_response)


from solve_algorithms import SimplexMethod

material_tables = [
    [
        [2, 4],
        [1, 1],
        [2, 1]
    ],
    [
        [2, 4, 5],
        [1, 8, 6],
        [7, 4, 5],
        [4, 6 ,7]
    ],
    [
        [0.8, 0.5, 1, 2, 1.1],
        [0.2, 0.1, 0.1, 0.1, 0.2],
        [0.3, 0.4, 0.6, 1.3, 0.05],
        [0.2, 0.3, 0.3, 0.7, 0.5],
        [0.7, 0.1, 0.9, 1.5, 0]
    ],
    [
        [0.1, 0.4],
        [0.01, 0.04]
    ],
    [
        [3, 2],
        [2, 5]
    ]
]

reserves = [
    [560, 170, 300],
    [120, 280, 240, 360],
    [1411, 149, 815.5, 466, 1080],
    [160, 24],
    [18, 20]
]

profits = [
    [4, 5],
    [10, 14, 12],
    [1, 0.7, 1, 2, 0.6],
    [1, 3],
    [-2, -3]
]

app = Flask(__name__)
app.config["SECRET_KEY"] = "sjdFODJdsojfsodfjPFJdjs546sdfsoidfjPfj"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simplex_test")
def simplex_test():
    task_index = 2
    method = SimplexMethod(material_tables[task_index], 
                           reserves[task_index], 
                           profits[task_index], 
                           'max')
    for iter in method.solution["iterations"]:
        print(iter)
        print()
    return render_template('simplex_solution.html', solution=method.solution)



@app.route("/simplex_solve", methods=["POST"])
def read_table():
    if request.method == "POST":
        response = { 'ok': True, 'html': None }

        data = request.get_json()
        form_data = data.get('formData')

        try:
            form_data = format_form_data(form_data)
        except:
            print("Error!")
            return jsonify(response)

        method = SimplexMethod(materials=form_data["tableData"],
                               reserve=form_data["reserves"],
                               profit=form_data["profits"])


        response['html'] = render_template('simplex_solution.html', solution=method.solution)
        return jsonify(response)
    

def format_form_data(form_data: list):
    form_data["tableData"] = [[float(el) for el in row] for row in form_data["tableData"]]
    form_data["reserves"] = [float(res) for res in form_data["reserves"]]
    form_data["profits"] = [float(prof) for prof in form_data["profits"]]
    return form_data


if __name__ == "__main__":
    app.run(debug=True)
