let timerInterval;

function fetchStatus() {
    fetch("/api/status")
        .then((response) => response.json())
        .then((data) => {
            // Update barber status
            const barberStatus = document.getElementById("barber-status");
            const barberImg = document.getElementById("barber-img");
            barberStatus.textContent = `Status: ${data.barber_status}`;
            barberImg.src =
                data.barber_status === "Sleeping"
                    ? "img\barber inactive.png"
                    : "img\barber active.png";

            // Update waiting room
            const seats = document.querySelectorAll(".seat");
            seats.forEach((seat, index) => {
                seat.src =
                    index < data.waiting_customers.length
                        ? "img\waitingroom-occupiedchair.png"
                        : "img\waitingroom-emptychair.png";
            });

            // Update incoming customers
            const entrance = document.getElementById("incoming-customers");
            entrance.innerHTML = ""; // Clear previous
            data.waiting_customers.forEach((customer) => {
                const img = document.createElement("img");
                img.src = "static\img\waiting stickman.png";
                img.alt = customer.name;
                img.title = customer.name;
                img.style.width = "50px";
                entrance.appendChild(img);
            });
        });
}

function fetchTimeRemaining() {
    fetch("/api/time_remaining")
        .then((response) => response.json())
        .then((data) => {
            const timerElement = document.getElementById("timer");
            if (data.time_remaining > 0) {
                timerElement.textContent = `Time Remaining: ${data.time_remaining}s`;
                clearInterval(timerInterval);
                startTimer(data.time_remaining);
            } else {
                timerElement.textContent = "";
            }
        });
}

function startTimer(seconds) {
    let timeLeft = seconds;
    timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            document.getElementById("timer").textContent = `Time Remaining: ${timeLeft}s`;
        } else {
            clearInterval(timerInterval);
        }
    }, 1000);
}

setInterval(() => {
    fetchStatus();
    fetchTimeRemaining();
}, 1000);
