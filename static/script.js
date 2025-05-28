document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded");
});

function validateOrderForm() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let address = document.getElementById("address").value;
    let medicine = document.getElementById("medicine_name").value;
    let contact = document.getElementById("contact_no").value;
    
    if (name === "" || email === "" || address === "" || medicine === "" || contact === "") {
        alert("All fields must be filled out");
        return false;
    }
    return true;
}

function validateAppointmentForm() {
    let patientName = document.getElementById("patient_name").value;
    let email = document.getElementById("email").value;
    let contact = document.getElementById("contact_no").value;
    let age = document.getElementById("age").value;
    
    if (patientName === "" || email === "" || contact === "" || age === "") {
        alert("All fields must be filled out");
        return false;
    }
    return true;
}