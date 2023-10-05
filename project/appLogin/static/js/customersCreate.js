// remove the mask
const form = document.getElementById("form");
form.addEventListener('submit', function (event) {

    // Prevenir el envío del formulario para que podamos manipular los datos primero
    event.preventDefault();

    // Quitar la máscara del campo de teléfono
    const phoneInput = document.getElementById('id_phone');
    let phoneNumber = phoneInput.value;
    phoneNumber = phoneNumber.replace(/-/g, '');
    phoneInput.value = phoneNumber;

    // Quitar la máscara del campo de cédula
    const cedulaInput = document.getElementById('id_cedula');
    let cedulaNumber = cedulaInput.value;
    cedulaNumber = cedulaNumber.replace(/-/g, '');
    cedulaInput.value = cedulaNumber;

    // Ahora puedes enviar el formulario
    form.submit();
});


// trying read success variable
var success = document.querySelector('meta[name="success"]').getAttribute('content');
console.log(success);
console.log(typeof success);

if (success) {
    $(document).ready(function () {
        $('#successModal').modal('show');
    });
}