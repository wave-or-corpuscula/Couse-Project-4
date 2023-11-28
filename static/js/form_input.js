const maxConstraintsAmount = 10;
const minConstraintsAmount = 2;
const maxVariablesAmount = 10;
const minVariablesAmount = 2;

const values = {
  variables: {},
  constraints: {}
};

function fillConstraintsSelect() {
  const constraintsSelect = document.getElementById("constraints");
  constraintsSelect.innerHTML = "";

  for (let i = minConstraintsAmount; i <= maxConstraintsAmount; i++) {
    var opt = document.createElement("option");
    opt.text = i;
    opt.value = i;
    constraintsSelect.appendChild(opt);
  }
}

function fillVariablesSelect() {
  const constraintsSelect = document.getElementById("variables");
  constraintsSelect.innerHTML = "";

  for (let i = minVariablesAmount; i <= maxVariablesAmount; i++) {
    var opt = document.createElement("option");
    opt.text = i;
    opt.value = i;
    constraintsSelect.appendChild(opt);
  }
}


function createVariableInputs() {
  const numVariables = parseInt(document.getElementById("variables").value);
  const targetFunctionDiv = document.getElementById("targetFunction");
  targetFunctionDiv.innerHTML = ""; // Очищаем содержимое

  // Сохраняем текущие значения переменных
  for (let i = 1; i <= numVariables; i++) {
    const input = document.querySelector(`#variable${i}`);
    values.variables[`variable-${i}`] = input ? input.value : '';
  }

  const label = document.createElement("label");
  label.textContent = "F = ";
  targetFunctionDiv.appendChild(label);

  for (let i = 1; i <= numVariables; i++) {
    const label = document.createElement("label");
    label.textContent = `x${i}`;
    if (i != numVariables) {
      label.textContent += ' + ' 
    }
    const input = document.createElement("input");
    input.id = `variable-${i}`;
    input.value = values.variables[`variable-${i}`] || '';

    targetFunctionDiv.appendChild(input);
    targetFunctionDiv.appendChild(label);
  }

  const arrow_lb = document.createElement("label");
  arrow_lb.textContent = " -> ";
  targetFunctionDiv.appendChild(arrow_lb);

  const select = document.createElement("select");
    select.classList.add("optimization-direction");
    select.id = "optimization-direction";
    const options = ["max", "min"];
    for (const option of options) {
      const optionElement = document.createElement("option");
      optionElement.value = option;
      optionElement.textContent = option;
      select.appendChild(optionElement);
    }

    targetFunctionDiv.appendChild(select);
}

function createConstraintInputs() {
  const numVariables = parseInt(document.getElementById("variables").value);
  const numConstraints = parseInt(document.getElementById("constraints").value);
  const constraintsDiv = document.getElementById("constraintsDiv");
  constraintsDiv.innerHTML = ""; // Очищаем содержимое
  
  // Сохраняем текущие значения переменных
  for (let i = 1; i <= numVariables; i++) {
    const input = document.querySelector(`#variable-${i}`);
    values.variables[`variable-${i}`] = input ? input.value : '';
  }


  for (let i = 1; i <= numConstraints; i++) {
    const constraintDiv = document.createElement("div");

      // Сохраняем текущие значения ограничений
    for (let j = 1; j <= numVariables; j++) {
      const input = document.querySelector(`#constraint-${i}-variable-${j}`);
      values.constraints[`constraint-${i}-variable-${j}`] = input ? input.value : '';
    }

    for (let j = 1; j <= numVariables; j++) {
      const label = document.createElement("label");
      label.textContent = `x${j} + `;
      const input = document.createElement("input");
      input.type = "number";
      input.classList.add(`constraint-${i}-variable-${j}`);
      input.value = values.constraints[`constraint-${i}-variable-${j}`] || ''; // Восстанавливаем сохраненное значение, если есть
      input.step = "any";
      constraintDiv.appendChild(label);
      constraintDiv.appendChild(input);
    }

    const select = document.createElement("select");
    select.classList.add(`constraint-${i}-comparison`);
    const options = [">=", "<=", "="];
    for (const option of options) {
      const optionElement = document.createElement("option");
      optionElement.value = option;
      optionElement.textContent = option;
      select.appendChild(optionElement);
    }
    constraintDiv.appendChild(select);

    const freeTermInput = document.createElement("input");
    freeTermInput.type = "number";
    freeTermInput.classList.add(`constraint-${i}-free-term`);
    freeTermInput.step = "any";
    constraintDiv.appendChild(freeTermInput);

    constraintsDiv.appendChild(constraintDiv);
  }
}

function startup() {
    fillConstraintsSelect();
    fillVariablesSelect();
    createVariableInputs()
    createConstraintInputs()
}

document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("variables").addEventListener("change", createVariableInputs);
    document.getElementById("variables").addEventListener("change", createConstraintInputs);
    document.getElementById("constraints").addEventListener("change", createConstraintInputs);
    // document.getElementById("simplex-solve").addEventListener("click", sendDataToBackend);
    startup();

});