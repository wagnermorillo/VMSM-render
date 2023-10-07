var success = document.querySelector('meta[name="success"]').getAttribute('content');

if (success) {
    $(document).ready(function () {
        $('#successModal').modal('show');
    });
}