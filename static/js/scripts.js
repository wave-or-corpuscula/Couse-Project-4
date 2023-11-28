
function collectFormData() {

  const formData = {
    variables: parseInt(document.getElementById("variables").value),
    constraints: parseInt(document.getElementById("constraints").value),
    targetFunction: {},
    optimizationDirection: document.getElementById("optimization-direction").value
  };

  // Собираем данные целевой функции
  for (let i = 1; i <= formData.variables; i++) {
    const inputValue = parseFloat(document.getElementById(`variable-${i}`).value);
    formData.targetFunction[`x${i}`] = inputValue;
  }

  // Собираем данные ограничений
  formData.constraintsData = [];
  for (let i = 1; i <= formData.constraints; i++) {
    const constraintData = {
      variables: {}
    };

    for (let j = 1; j <= formData.variables; j++) {
      const inputValue = parseFloat(document.querySelector(`.constraint-${i}-variable-${j}`).value);
      constraintData.variables[`x${j}`] = inputValue;
    }

    const comparisonValue = document.querySelector(`.constraint-${i}-comparison`).value;
    const freeTermValue = parseFloat(document.querySelector(`.constraint-${i}-free-term`).value);

    constraintData.comparison = comparisonValue;
    constraintData.freeTerm = freeTermValue;

    formData.constraintsData.push(constraintData);
  }

  return formData;
}

function sendDataToBackend() {
  const data = collectFormData();

  fetch('/simplex_solve', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ tableData: data }),
  })
  .then(response => {
    if (response.ok) {
      // Обработка успешного ответа от сервера
      console.log('Данные успешно отправлены на сервер');
    } else {
      // Обработка ошибки
      console.error('Ошибка отправки данных на сервер');
    }
  })
  .catch(error => {
    console.error('Произошла ошибка:', error);
  });
}

document.getElementById("simplex-solve").addEventListener("click", function() {
  fetch('/simplex_solve', {
    method: 'POST',
    body: JSON.stringify({}),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.text())
  .then(data => {
    // Обновление содержимого страницы в соответствии с ответом от сервера
    document.getElementById("solution-content").innerHTML += data["simplex_solution"];
  })
  .catch(error => {
    console.error('Произошла ошибка:', error);
  });
});


document.addEventListener("DOMContentLoaded", function() {

  document.getElementById("simplex-solve").addEventListener("click", sendDataToBackend);

});