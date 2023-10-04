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

// for names and lastnames
$(document).ready(function() {
    $('#btnBuscar').on('click', function(e) {
        e.preventDefault();
        var names = $('#inputNames').val();
        var lastNames = $('#inputLastNames').val();
        $.ajax({
            url: 'clients',
            data: {
                'names': names,
                'lastNames': lastNames
            },
            dataType: 'json',
            success: function(data) {
                var resultados = $('#resultados');
                resultados.empty();
                if (data.clients.length) {
                    data.clients.forEach(function(client) {
                        resultados.append('<p>' + client.names + ' ' + client.lastNames + '</p>');
                    });
                } else {
                    resultados.append('<p>No se encontraron clientes con esos nombres y apellidos.</p>');
                }
            }
        });
    });
});