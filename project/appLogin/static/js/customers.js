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


function formatPhoneNumber(phone) {
    if (!phone) return '';
    const cleaned = ('' + phone).replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return match[1] + '-' + match[2] + '-' + match[3];
    }
    return phone;
}


// to delete a costumer
// get the elements id
let SelectId = null;
const btnRefresh = document.getElementById("refresh-button");
const warningModal = document.getElementById("warningModal");
const infoModal = document.getElementById("infoModal");
const btnAccept = document.getElementById("accept-button");
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');

// Add a click function to the button
function showAlert(btnDelete) {
    SelectId = btnDelete.getAttribute("data-client-id");
    $(warningModal).modal("show");
}


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

$(document).ready(function () {
    var table = $('#datatable-clients').DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        ordering: false,
        ajax: {
            url: '/resources/listClients/',
            dataSrc: "clients",
            type: "GET",
            data: function (d) {
                return {
                    start: d.start,
                    length: d.length,
                    draw: d.draw,
                    search: d.search.value
                }
            }
        },
        columns: [
            {
                data: null,
                render: function (data, type, row, meta) {

                    return meta.row + meta.settings._iDisplayStart + 1;
                },
                orderable: true,
                serverSide: false
            },
            { data: 'names' },
            { data: 'lastNames' },
            { data: 'email' },
            {
                data: 'phone',
                render: function (data, type, row) {
                    if (type === 'display' && data.length === 11) {
                        return '(' + data.substring(0, 3) + ')-' + data.substring(3, 6) + '-' + data.substring(6, 10);
                    }
                    return data;
                }
            },
            {
                data: 'cedula',
                render: function (data, type, row) {
                    if (type === 'display' && data.length === 11) {
                        // Formatea la cédula como XXX-XXXXXXX-X
                        return data.substring(0, 3) + '-' + data.substring(3, 10) + '-' + data.substring(10);
                    }
                    return data;
                },
                orderable: true
            },
            { data: 'birthdate' },
            {
                data: null,
                render: function (data, type, row) {
                    // Retorna el HTML de los botones
                    return `<a class='btn btn-sm btn-secondary update-button' href="/main/customers?clientId=${row.id}"'>
                    <i class='fa-solid fa-pencil'></i>
                </a>
                <button class='btn btn-sm btn-danger delete-button' data-client-id='${row.id}' onclick='showAlert(this)'>
                    <i class='fa-solid fa-trash-can'></i>
                </button>`;
                },
            }

        ],
        columnDefs: [
            { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
            { orderable: false, targets: [] },
            { searchable: false, targets: [0, 6, 7] },
        ],
        pageLength: 5,

    });

    // Turn off automatic search every time you type in the search box
    $('input[type="search"]').off('keyup search input').on('keypress', function (e) {
        if (e.which == 13) {
            table.search(this.value).draw();
        }
    });
});
