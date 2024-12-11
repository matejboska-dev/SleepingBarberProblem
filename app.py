from flask import Flask, render_template, jsonify
from threading import Thread, Lock, Event
import time
import random

app = Flask(__name__)

# Mutex for thread synchronization
mutex = Lock()

# Configuration
customer_interval_min = 5
customer_interval_max = 15
haircut_duration_min = 3
haircut_duration_max = 15

# Global variables for barber and waiting room status
barber_status = "Sleeping"
waiting_customers = []
current_customer = None
time_remaining = 0
barber_working_event = Event()

class Customer:
    def __init__(self, name):
        self.name = name


class Barber:
    def sleep(self):
        global barber_status
        barber_status = "Sleeping"
        barber_working_event.wait()

    def wake_up(self):
        global barber_status
        barber_status = "Awake"
        barber_working_event.set()

    def cut_hair(self, customer):
        global barber_status, time_remaining, current_customer
        barber_status = f"Cutting hair: {customer.name}"
        time_remaining = random.randint(haircut_duration_min, haircut_duration_max)
        current_customer = customer.name

        while time_remaining > 0:
            time.sleep(1)
            time_remaining -= 1

        barber_status = f"Finished haircut: {customer.name}"
        time.sleep(1)  # Simulate short pause after haircut
        barber_status = "Sleeping"
        current_customer = None


class BarberShop:
    def __init__(self, barber, num_seats):
        self.barber = barber
        self.num_seats = num_seats
        print(f"BarberShop initialized with {num_seats} seats.")

    def barber_go_to_work(self):
        while True:
            mutex.acquire()
            if waiting_customers:
                customer = waiting_customers.pop(0)
                mutex.release()
                self.barber.cut_hair(customer)
            else:
                mutex.release()
                self.barber.sleep()

    def enter_shop(self, customer):
        global barber_status
        mutex.acquire()
        if len(waiting_customers) >= self.num_seats:
            print(f"Waiting room full. {customer.name} is leaving.")
            mutex.release()
        else:
            print(f"{customer.name} sat in the waiting room.")
            waiting_customers.append(customer)
            mutex.release()
            self.barber.wake_up()


# Flask routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({
        "barber_status": barber_status,
        "waiting_customers": [{"name": c.name} for c in waiting_customers],
    })


@app.route("/api/time_remaining")
def timer():
    return jsonify({"time_remaining": time_remaining})


def generate_customers(barber_shop):
    customers = [
        "Bragi", "Auja", "Iris"
    ]

    while customers:
        customer_name = customers.pop(0)
        customer = Customer(customer_name)
        barber_shop.enter_shop(customer)
        time.sleep(random.randint(customer_interval_min, customer_interval_max))


if __name__ == "__main__":
    barber = Barber()
    barber_shop = BarberShop(barber, num_seats=3)

    # Start barber thread
    barber_thread = Thread(target=barber_shop.barber_go_to_work, daemon=True)
    barber_thread.start()

    # Start customer generation thread
    customer_thread = Thread(target=generate_customers, args=(barber_shop,), daemon=True)
    customer_thread.start()

    # Start Flask server
    app.run(debug=True, port=5000)
