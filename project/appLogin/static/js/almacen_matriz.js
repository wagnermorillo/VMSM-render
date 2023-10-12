let editable = false;
const items = {}; // Objeto para almacenar los cubos

function crearMatriz(height, width, numCajas) {
    const tamanoCajas = 55;
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

    const containerWidth = width * (tamanoCajas + 1); 
    const containerHeight = height * (tamanoCajas + 1);

    // Establece el ancho y alto calculados en el .container
    const container = document.querySelector(".container");
    container.style.width = `calc(${containerWidth}px + 5px)`;
    container.style.height = `calc(${containerHeight}px + 5px)`;

    // Crea la cuadrícula
    for (let y = 1; y <= height; y++) {
        for (let x = 1; x <= width; x++) {
            const square = document.createElement("div");
            const uniqueId = `cell_${y}_${x}`;
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

function asignarRegistroALaMatriz(record) {
    const matrizContainer = document.getElementById("matriz");
    const uniqueId = `${record.id}`;
    const square = items[uniqueId];

    if (square) {
        obtenerDatosDeRegistro(record.id, (registroData) => {
            if (registroData) {
                // Modifica el color o la representación visual según los datos del registro
                square.style.backgroundColor = "green"; // Puedes ajustar el color o marcador según tus necesidades
                // También puedes mostrar información adicional en el hover.
                square.title = `Cliente: ${registroData.client.names}, Producto: ${record.products.join(', ')}`;
            } else {
                console.error("Error al obtener datos del registro");
            }
        });
    }
}

function obtenerDatosDeRegistro(recordId, callback) {
    fetch(`/get_record_data/${recordId}/`)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                console.error('Error fetching record data');
                callback(null);
            }
        })
        .then((data) => {
            if (data.error) {
                console.error(data.error);
                callback(null);
            } else {
                console.log('Datos del registro:', data);
                callback(data);
            }
        })
        .catch((error) => {
            console.error('Error fetching record data:', error);
            callback(null);
        });
}

// Luego, dentro de tu función cargarMatriz, después de obtener el store y antes de asignar el registro a la matriz, llama a obtenerDatosDeRegistro con el ID del registro que deseas obtener.



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

                fetch(`/get_records_in_store/${selectedStoreId}/`)
                    .then((response) => response.json())
                    .then((data) => {
                        if (data === null) {
                            data = { records: [] };
                        }

                        if (Array.isArray(data.records)) {
                            data.records.forEach((record) => {
                                // Procesa los registros aquí
                                representarValoresEnMatriz(record); // Invoca la función para representar los valores en la matriz
                            });
                        } else {
                            console.error("Los registros no son un array válido:", data.records);
                        }
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
    const uniqueId = `${record.id}`;
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
    const cargarMatrizButton = document.getElementById("cargarMatrizButton"); // Asegúrate de ajustar el ID de tu botón

    // Asigna un evento al botón para cargar la matriz
    cargarMatrizButton.addEventListener("click", function () {
        const selectedStoreId = storeSelect.value;
        if (selectedStoreId) {
            // Llama a la función para cargar la matriz
            cargarMatriz(selectedStoreId);

            // Realiza una solicitud AJAX para obtener los registros
            fetch(`/get_records_in_store/${selectedStoreId}/`)
                .then((response) => response.json())
                .then((data) => {
                    if (data === null) {
                        // Asignar 0 en lugar de null
                        data = { records: [] }; // Crear un objeto con una propiedad "records" que sea un array vacío
                    }
                    
                    if (Array.isArray(data.records)) {
                        data.records.forEach((record) => {
                            // Procesa los registros aquí
                            asignarRegistroALaMatriz(record);
                        });
                    } else {
                        console.error("Los registros no son un array válido:", data.records);
                    }
                    console.log(data.records)
                })
                .catch((error) => console.error("Error al obtener registros del almacén:", error));



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



function establecerColorDeFondo(record, color) {
    const heightPosition = record.heightPosition || 1;
    const widthPosition = record.widthPosition || 1;
    const height = record.height || 1;
    const width = record.width || 1;

    for (let y = heightPosition; y < heightPosition + height; y++) {
        for (let x = widthPosition; x < widthPosition + width; x++) {
            const square = document.getElementById(`cell_${y}_${x}`);

            if (square) {
                square.style.backgroundColor = color;
            }
        }
    }
}

function representarValoresEnMatriz(record) {
    const idClientNames = record.idClient__names;
    const products = record.products || [];

    // Utiliza la función para establecer el color de fondo en lugar de hacerlo directamente
    establecerColorDeFondo(record, "red");

    // Luego, si es necesario, puedes agregar un título o información adicional
    const info = `Cliente: ${idClientNames}, Producto: ${products.join(', ')}`;
    establecerTituloEnCeldas(record, info);
}

function establecerTituloEnCeldas(record, info) {
    const heightPosition = record.heightPosition || 1;
    const widthPosition = record.widthPosition || 1;
    const height = record.height || 1;
    const width = record.width || 1;

    for (let y = heightPosition; y < heightPosition + height; y++) {
        for (let x = widthPosition; x < widthPosition + width; x++) {
            const square = document.getElementById(`cell_${y}_${x}`);

            if (square) {
                square.title = info;
            }
        }
    }
}


