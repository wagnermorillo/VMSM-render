// for animations un hover
$(document).ready(function () {
    $(".sidebar ul li").on("mouseover", function () {
        $(".sidebar ul li.active").removeClass("active");
        $(this).addClass("active");
    });

    $(".sidebar ul li").on("mouseleave", function () {
        $(this).removeClass("active");
    });
});


// for datatable
let dataTable;
let dataTableisInit = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
        { orderable: false, targets: [4, 5, 6, 7] },
        { searchable: false, targets: [0, 3, 6, 7] },
        { targets: [4, 5], type: 'formatted-phone' }
    ],
    pageLength: 5,
    destroy: true
};

$.fn.dataTable.ext.type.search['formatted-phone'] = function (data) {
    // Eliminar guiones para la búsqueda
    return data.replace(/[-\s()]/g, '');
};

const initDataTable = async () => {
    if (dataTableisInit) {
        dataTable.destroy();
    }
    await listClients();
    dataTable = $("#datatable-clients").DataTable(dataTableOptions);
    dataTableisInit = true;

};


const listClients = async () => {
    try {
        const response = await fetch("/resources/listClients/");
        const data = await response.json();
        let content = "";
        data.clients.forEach((client, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${client.names}</td>
                    <td>${client.lastNames}</td>
                    <td>${client.email}</td>
                    <td>(${client.phone.slice(0, 3)})-${client.phone.slice(3, 6)}-${client.phone.slice(6)}</td>
                    <td>${client.cedula.slice(0, 3)}-${client.cedula.slice(3, 10)}-${client.cedula.slice(10)}</td>
                    <td>${client.birthdate}</td>
                    <td>

                        <a class='btn btn-sm btn-secondary update-button' href="/main/customers?clientId=${client.id}"'>
                            <i class='fa-solid fa-pencil'></i>
                        </a>
                        <button class='btn btn-sm btn-danger delete-button'  data-client-id='${client.id}'>
                            <i class='fa-solid fa-trash-can'></i>
                        </button>
                    </td>
                </tr>
            `;
        })
        tableBodyClients.innerHTML = content;



        // to delete a costumer
        // get the elements id
        let SelectId = null;
        const btnDeleteList = document.querySelectorAll(".delete-button");
        const btnRefresh = document.getElementById("refresh-button");
        const warningModal = document.getElementById("warningModal");
        const infoModal = document.getElementById("infoModal");
        const btnAccept = document.getElementById("accept-button");
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');


        // Add a click event to the button
        btnDeleteList.forEach(function (btnDelete) {
            btnDelete.addEventListener('click', function () {
                SelectId = btnDelete.getAttribute("data-client-id");
                $(warningModal).modal("show");
            });
        });

        // add a event click to the button of the modal (accept)
        btnAccept.addEventListener("click", function () {
            // Get the necessary information from the button
            const clientId = SelectId;
            console.log(clientId);

            //Make the AJAX request to delete the client
            $.ajax({
                url: `/resources/deleteClient/${clientId}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken // Add CSRF token as header
                },
                success: function (response) {
                    // Handle Django response if necessary

                    // hidden the modal
                    $(warningModal).modal('hide');

                    // show the new modal
                    $(infoModal).modal("show");

                    // refresh the page the finish process
                    btnRefresh.addEventListener("click", function () {
                        location.reload();
                    });
                },
                error: function (error) {
                    // Manejar errores si es necesario
                    console.error('Error al eliminar el cliente:', error);
                }
            });
        });



    } catch (ex) {
        alert(ex);
    }
};
window.addEventListener("load", async () => {
    await initDataTable();
})
