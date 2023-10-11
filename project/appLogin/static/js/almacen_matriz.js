let editable = false;
const items = {}; // Objeto para almacenar los cubos

function crearMatriz(height, width, numCajas) {
    const tamanoCajas = 50;
    const matrizContainer = document.getElementById("matriz");
    matrizContainer.innerHTML = ""; // Limpia cualquier contenido anterior

    // Verifica que height y width sean valores válidos
    if (height <= 0 || width <= 0 || tamanoCajas <= 0) {
        console.error("Dimensiones no válidas.");
        return;
    }

    // Establece las columnas y filas de la cuadrícula
    matrizContainer.style.gridTemplateColumns = `repeat(${width}, ${tamanoCajas}px)`;
    matrizContainer.style.gridTemplateRows = `repeat(${height}, ${tamanoCajas}px)`;

    // Crea la cuadrícula
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const square = document.createElement("div");
            const uniqueId = ``;
            square.id = uniqueId;
            square.classList.add("square");
            matrizContainer.appendChild(square);

            const textElement = document.createElement("span");
            textElement.classList.add("text");
            textElement.textContent = uniqueId;
            square.appendChild(textElement);
            //console.log("matriz es:")
            square.addEventListener("click", () => {
                if (editable) {
                    square.classList.toggle("editable");
                    cambiarColorPorId(uniqueId);
                }
            });

            items[uniqueId] = square;
        }
    }

    // Establece cuadrados editables
    const squares = document.querySelectorAll(".square");
    for (let i = 0; i < numCajas; i++) {
        squares[i].classList.add("editable");
        cambiarColorPorId(squares[i].id);
    }
}


function cambiarColorPorId(id) {
    const square = items[id];
    if (square) {
        const color = getRandomColor(); // Genera un color aleatorio
        square.style.backgroundColor = color;
    }
}

function getRandomColor() {
    // Genera un color aleatorio en formato hexadecimal
    return "#" + Math.floor(Math.random() * 16777215).toString(16);
}

function editarMatriz() {
    editable = !editable;
    const editButton = document.getElementById("editboton");
    if (editable) {
        editButton.textContent = "Guardar Edición";
    } else {
        editButton.textContent = "Editar Matriz";
    }
}

function cargarMatriz() {
    const storeSelect = document.getElementById("storeSelect");
    const selectedStoreId = storeSelect.value;

    if (selectedStoreId) {
        fetch(`/get_store_dimensions/${selectedStoreId}/`)
            .then((response) => response.json())
            .then((data) => {
                const height = data.height;
                const width = data.width;

                // Llama a la función para crear la matriz
                crearMatriz(height, width);

                // Luego, obtén la información de los registros en este almacén y colócalos en la matriz.
                fetch(`/get_records_in_store/${selectedStoreId}/`)
                    .then((response) => response.json())
                    .then((records) => {
                        // Itera sobre los registros y coloca visualmente cada uno en la matriz.
                        records.forEach((record) => {
                            asignarRegistroALaMatriz(record);
                        });
                    })
                    .catch((error) => console.error("Error al obtener registros del almacén:", error));
            })
            .catch((error) => console.error("Error al obtener dimensiones del almacén:", error));
    } else {
        console.error("No se ha seleccionado un almacén");
    }
}

// Función para asignar visualmente un registro a la matriz
function asignarRegistroALaMatriz(record) {
    const matrizContainer = document.getElementById("matriz");
    const uniqueId = `square_${record.widthPosition}_${record.heightPosition}`;
    const square = items[uniqueId];
    if (square) {
        // Modifica el color de la celda o agrega un marcador para representar el registro
        square.style.backgroundColor = "green"; // Puedes ajustar el color o el marcador según tus necesidades
        // También puedes mostrar información adicional, como el nombre del cliente o el producto, en el hover.
        square.title = `Cliente: ${record.idClient.names}, Producto: ${record.products.join(', ')}`;
    }
}

  document.addEventListener("DOMContentLoaded", function () {
    // Obtén la referencia al elemento <select> con id "storeSelect"
    const storeSelect = document.getElementById("storeSelect");
    const cargarMatrizButton = document.getElementById("cargarMatrizButton"); // Agrega el id a tu botón
  
    // Asigna un evento al botón para cargar la matriz
    cargarMatrizButton.addEventListener("click", function () {
      const selectedStoreId = storeSelect.value;
      if (selectedStoreId) {
        // Llama a la función para cargar la matriz
        cargarMatriz(selectedStoreId);
      }
    });
  
    // Realiza una solicitud AJAX para obtener la lista de almacenes disponibles
    fetch("/api/obtener_almacenes/") // Asegúrate de ajustar la URL según tu estructura de URL
      .then((response) => response.json())
      .then((data) => {
        // Llena las opciones del elemento <select> con los almacenes disponibles
        data.almacenes.forEach(function (almacen) {
          const option = document.createElement("option");
          option.value = almacen.id;
          option.textContent = almacen.name;
          storeSelect.appendChild(option);
        });
      })
      .catch((error) => console.error("Error al obtener almacenes:", error));
  });