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
        { targets: [4,5], type: 'formatted-phone'}
    ],
    pageLength: 5,
    destroy: true
};

$.fn.dataTable.ext.type.search['formatted-phone'] = function (data) {
    // Eliminar guiones para la búsqueda
    return data.replace(/[-\s()]/g, '');
};

const initDataTable = async()=>{
    if (dataTableisInit) {
        dataTable.destroy();
    }
    await listClients();
    dataTable = $("#datatable-clients").DataTable(dataTableOptions);
    dataTableisInit = true;

};


const listClients = async()=>{
        try{
            const response = await fetch("/resources/listClients/");
            const data = await response.json();
            let content = "";
            data.clients.forEach((client, index)=>{
                content += `
                <tr>
                    <td>${index+1}</td>
                    <td>${client.names}</td>
                    <td>${client.lastNames}</td>
                    <td>${client.email}</td>
                    <td>(${client.phone.slice(0, 3)})-${client.phone.slice(3, 6)}-${client.phone.slice(6)}</td>
                    <td>${client.cedula.slice(0, 3)}-${client.cedula.slice(3, 10)}-${client.cedula.slice(10)}</td>
                    <td>${client.birthdate}</td>
                    <td>
                        <button class='btn btn-sm btn-secondary'><i class='fa-solid fa-pencil'></i></button>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                </tr>
            `;
            })
            console.log(content);
            tableBodyClients.innerHTML = content;

        }catch(ex){
            alert(ex);
        }
};
window.addEventListener("load", async()=>{
    await initDataTable();
})

// hidden components
const tableData = document.getElementById("tableData");
const activeForm = document.getElementById("activeForm");
const formCustomer = document.getElementById("formCustomer");
const activeTable = document.getElementById("activeTable");

// hidden table and show forms
activeForm.addEventListener('click', function(){
    // hidden the table
    tableData.style.display = "none";
    // show the forms
    formCustomer.style.display = "block";
});

// hidden forms and show table
activeTable.addEventListener('click', function(){
    
    formCustomer.style.display = "none";
    tableData.style.display = "block";
});