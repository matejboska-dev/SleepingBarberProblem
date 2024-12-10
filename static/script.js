document.addEventListener("DOMContentLoaded", function() {
    const addCustomerBtn = document.getElementById("add-customer-btn");
    const configForm = document.getElementById("config-form");
    const messageDiv = document.getElementById("message");
    const customersList = document.getElementById("customers-list");

    addCustomerBtn.addEventListener("click", function() {
        fetch('/add_customer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                num_chairs: document.getElementById('num_chairs').value,
                max_customers: document.getElementById('max_customers').value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                updateCustomerList();
            } else {
                showMessage(data.message);
            }
        });
    });

    configForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const numChairs = document.getElementById('num_chairs').value;
        const maxCustomers = document.getElementById('max_customers').value;

        fetch('/save_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ num_chairs: numChairs, max_customers: maxCustomers })
        })
        .then(response => response.json())
        .then(data => {
            showMessage(data.message);
        });
    });

    function updateCustomerList() {
        fetch('/get_customers')
        .then(response => response.json())
        .then(data => {
            customersList.innerHTML = '';
            data.customers.forEach(customer => {
                const li = document.createElement('li');
                li.textContent = `Zákazník ${customer}`;
                customersList.appendChild(li);
            });
        });
    }

    function showMessage(message) {
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
});
