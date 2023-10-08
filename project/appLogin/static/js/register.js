let editable = false;
       const items = {}; // Objeto para almacenar los cubos

        function crearMatriz() {
            const matrizContainer = document.getElementById("matriz");
            matrizContainer.innerHTML = "";
            const sizeX = parseInt(document.getElementById("inputX").value);
            const sizeY = parseInt(document.getElementById("inputY").value);
            const numCajas = parseInt(document.getElementById("numCajas").value);
            const tamanoCajas = parseInt(document.getElementById("tamanoCajas").value);

            matrizContainer.style.gridTemplateColumns = `repeat(${sizeX}, ${tamanoCajas}px)`;

            for (let y = 0; y < sizeY; y++) {
                for (let x = 0; x < sizeX; x++) {
                    const square = document.createElement("div");
                    const uniqueId = `square_${x}_${y}`;
                    square.id = uniqueId; // Asigna un ID único
                    square.classList.add("square");
                    matrizContainer.appendChild(square);

                    // Crea un elemento de texto para mostrar el nombre de la variable
                    const textElement = document.createElement("span");
                    textElement.classList.add("text");
                    textElement.textContent = uniqueId;
                    square.appendChild(textElement);

                    square.addEventListener("click", () => {
                        if (editable) {
                            square.classList.toggle("editable");
                            cambiarColorPorId(uniqueId); // Cambia el color basado en el ID
                        }
                    });

                    // Almacena el cubo en el objeto cubos
                    items[uniqueId] = square;
                }
            }

            // Establecer cuadrados editables
            const squares = document.querySelectorAll(".square");
            for (let i = 0; i < numCajas; i++) {
                squares[i].classList.add("editable");
                cambiarColorPorId(squares[i].id); // Cambia el color basado en el ID
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
            return "#" + Math.floor(Math.random()*16777215).toString(16);
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


        // Llama a la función inicialmente para crear la matriz predeterminada.
        crearMatriz();