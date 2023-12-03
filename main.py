from flask import (Flask, 
                    render_template, 
                    request, 
                    flash, 
                    redirect, 
                    url_for, 
                    jsonify,
                    make_response)

from scipy.optimize import linprog
from cvxpy import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "sjdFODJdsojfsodfjPFJdjs546sdfsoidfjPfj"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simplex_solve", methods=["POST"])
def read_table():
    if request.method == "POST":
        response = { 'ok': True, 'html': None }

        data = request.get_json()
        table_data = data.get('tableData')

        # try:
        simplex_data = reformate_form_data(table_data)
        for key, val in simplex_data.items():
            print(f"{key}: {val}")
        iterations = []
        res = linprog(c=simplex_data['func'], 
                        A_ub=simplex_data['constraints'], 
                        b_ub=simplex_data['free_coefs'], 
                        bounds=simplex_data['bounds'],
                        method="simplex", 
                        options={"disp": True},
                        callback=lambda xk: iterations.append(xk)
                        )
        # print(iterations)
        # print(res)
        response['html'] = render_template("simplex_solution.html", solution=res, iterations=None)
        # except:
        #     response['html'] = render_template("error_message.html", messages=["Ошибка при решении!",
        #                                                                        "Провеврьте корректность введенных данных"])
        #     response["ok"] = False
        return jsonify(response)
    

# def save_callback(iterations: list, xk, **kwargs):
#     iterations.append(xk)


def reformate_form_data(form_data):
    # print(form_data)
    try:
        objective = form_data['optimizationDirection']
        k = 1 if objective == 'min' else -1
        func_coefs = [k * float(x) for x in form_data.get('targetFunction').values()]
        constraint_coefs = []
        free_coefs = []

        for constraint_line in form_data['constraintsData']:
            # Если знак >= то меняем знак с обеих сторон
            ck = 1 if constraint_line['comparison'] == '<=' else -1
            constraint_coefs.append([ck * float(coef) if coef != '' else 0 for coef in constraint_line['variables'].values()])
            free_coefs.append(ck * float(constraint_line['freeTerm']) if constraint_line['freeTerm'] != '' else 0 )
        
        
        bounds = [(0, None) if form_data.get('positiveSolutions') else (None, None) for _ in form_data.get('targetFunction').keys()]
        return {
            'func': func_coefs,
            'constraints': constraint_coefs,
            'free_coefs': free_coefs,
            'bounds': bounds
        }
    except:
        raise


if __name__ == "__main__":
    app.run(debug=True)
