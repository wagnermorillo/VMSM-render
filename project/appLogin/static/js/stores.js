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
    SelectId = btnDelete.getAttribute("data-store-id");
    $(warningModal).modal("show");
}


// add a event click to the button of the modal (accept)
btnAccept.addEventListener("click", function () {
    // Get the necessary information from the button
    const storeId = SelectId;

    //Make the AJAX request to delete the client
    $.ajax({
        url: `/resources/deleteStore/${storeId}/`,
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
        }
    });
});

$(document).ready(function () {
    var table = $('#datatable-stores').DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        ordering: false,
        // scrollX: true,
        ajax: {
            url: '/resources/listStores/',
            dataSrc: "stores",
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
            { data: 'location' },
            {
                data: null,
                render: function (data, type, row, meta) {
                    return "(" + row.width + ", " + row.height + ", " + row.depth + ")"
                }
            },
            { data: 'totalSpace' },
            { data: 'availableSpace' },
            { data: 'recordQuantity' },
            { data: 'adress' },
            {
                data: null,
                render: function (data, type, row) {
                    // Retorna el HTML de los botones
                    return `<a class='btn btn-sm btn-secondary update-button' href="/main/stores?storeId=${row.id}"'>
                    <i class='fa-solid fa-pencil'></i>
                </a>
                <button class='btn btn-sm btn-danger delete-button' data-store-id='${row.id}' onclick='showAlert(this)'>
                    <i class='fa-solid fa-trash-can'></i>
                </button>`;
                },
            }

        ],
        columnDefs: [
            { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
            { orderable: false, targets: [] },
            { searchable: false, targets: [1, 2, 3, 4, 5, 6, 7] },
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
