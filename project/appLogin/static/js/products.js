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
    SelectId = btnDelete.getAttribute("data-produt-id");
    $(warningModal).modal("show");
}


// add a event click to the button of the modal (accept)
btnAccept.addEventListener("click", function () {
    // Get the necessary information from the button
    const productId = SelectId;
    console.log(productId);

    //Make the AJAX request to delete the client
    $.ajax({
        url: `/resources/deleteProduct/${productId}/`,
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
            console.error(error);
        }
    });
});

$(document).ready(function () {
    var table = $('#datatable-products').DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        ordering: false,
        ajax: {
            url: '/resources/listProducts/',
            dataSrc: "products",
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
            { data: 'name' },
            { data: 'descriptions' },
            {
                data: null,
                render: function (data, type, row) {
                    // Retorna el HTML de los botones
                    return `<a class='btn btn-sm btn-secondary update-button' href="/main/products?productId=${row.id}"'>
                    <i class='fa-solid fa-pencil'></i>
                </a>
                <button class='btn btn-sm btn-danger delete-button' data-produt-id='${row.id}' onclick='showAlert(this)'>
                    <i class='fa-solid fa-trash-can'></i>
                </button>`;
                },
            }

        ],
        columnDefs: [
            { className: "centered", targets: [0,1,2,3] },
            { orderable: false, targets: [] },
            { searchable: false, targets: [0, 3] },
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
