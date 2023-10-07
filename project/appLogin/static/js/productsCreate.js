// trying read success variable
var success = document.querySelector('meta[name="success"]').getAttribute('content');
console.log(success);
console.log(typeof success);

if (success) {
    $(document).ready(function () {
        $('#successModal').modal('show');
    });
}