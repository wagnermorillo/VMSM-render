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
        return "(" + match[1] + ")" + '-' + match[2] + '-' + match[3];
    }
    return phone;
}

function formatCedula(cedula) {
    if (!cedula) return '';
    const cleaned = ('' + cedula).replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{7})(\d{1})$/);
    if (match) {
        return match[1] + '-' + match[2] + '-' + match[3];
    }
    return cedula;
}



$(document).ready(function () {
    var table = $('#datatable-records').DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        ordering: false,
        // scrollX: true,
        ajax: {
            url: '/resources/listRecords/',
            dataSrc: "records",
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
            {
                data: 'clientFullName',
                render: function (data, type, row) {
                    return `<button class="btnClient" data-idClient="${row.idClient}"> ${data} </button>`;
                }
            },
            {
                data: 'storeName',
                render: function (data, type, row) {
                    return `<button class="btnStore" data-idStore="${row.idStore}"> ${data} </button>`;
                }
            },
            { data: 'dateIn' },
            { data: 'dateOut' },
            {
                data: null,
                render: function (data, type, row, meta) {
                    return "(" + row.width + ", " + row.height + ", " + row.depth + ")"
                }
            },
            { data: 'totalVolume' },
            { data: 'totalWeight' },
            {
                data: 'isFragile',
                render: function (data, type, row) {
                    if (type === "display") {
                        if (data) {
                            // if is true, show the icon check
                            return '<i class="fas fa-check-circle" style="color: green;"></i>';
                        } else {
                            // if is false, show the icon X
                            return '<i class="fas fa-times-circle" style="color: red;"></i>';
                        }
                    }
                }
            },

        ],
        columnDefs: [
            { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
            { orderable: false, targets: [] },
            { searchable: false, targets: [] },
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



// ajax to complete content of client
$(document).on("click", ".btnClient", function () {
    var idClient = $(this).attr("data-idClient");

    $.ajax({
        url: `/resources/listClients/${idClient}`,
        type: "GET",
        dataType: 'json',
        success: function (data) {

            // refill data of the fields
            $('#clientName').text(data.client.names);
            $('#clientLastName').text(data.client.lastNames);
            $('#clientEmail').text(data.client.email);
            $('#clientAddress').text(data.client.adress);
            $('#clientPhone').text(formatPhoneNumber(data.client.phone));
            $('#clientCedula').text(formatCedula(data.client.cedula));
            $('#clientBirthdate').text(data.client.birthdate);


            // show the modal
            $("#infoClient").modal("show");
        },
        error: function (error) {
            console.log(error);
        }
    });
});



// ajax to complete content of store
$(document).on("click", ".btnStore", function () {
    var idStore = $(this).attr("data-idStore");

    $.ajax({
        url: `/resources/listStores/${idStore}`,
        type: "GET",
        dataType: 'json',
        success: function (data) {
            console.log(data.store.location);

            // refill data of the fields
            $('#storeLocation').text(data.store.location);
            $('#storeName').text(data.store.name);
            $('#storeDimensions').text(
                `(${data.store.width}, ${data.store.width}, ${data.store.width})`
            );
            $('#storeTotalSpace').text(data.store.totalSpace);
            $('#storeAvailableSpace').text(data.store.availableSpace);
            $('#storeRecordQuantity').text(data.store.recordQuantity);
            $('#storeAddress').text(data.store.adress);


            // show the modal
            $("#infoStore").modal("show");
        },
        error: function (error) {
            console.log(error);
        }
    });
});