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
                render: function(data, type, row){
                    return `<a class="clientname" href="#"> ${data} </a>`;
                }
            },
            { data: 'storeName' },
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
                render: function(data, type, row){
                    if (type === "display") {
                        if (data) {
                            // if is true, show the icon check
                            return '<i class="fas fa-check-circle" style="color: green;"></i>';
                        }else{
                            // if is false, show the icon X
                            return '<i class="fas fa-times-circle" style="color: red;"></i>';
                        }
                    }
                }
            },

        ],
        columnDefs: [
            { className: "centered", targets: [0,1,2,3,4,5,6,7,8] },
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