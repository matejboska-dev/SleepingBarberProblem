from flask import Flask, render_template, request, jsonify
import threading
import time
import random

# Inicializace aplikace Flask
app = Flask(__name__)

# Globální proměnné pro konfiguraci
NUM_CHAIRS = 3
MAX_CUSTOMERS = 5

# Seznam čekajících zákazníků
waiting_customers = []

# Semafory pro synchronizaci vláken
barber_semaphore = threading.Semaphore(0)
customer_semaphore = threading.Semaphore(0)
mutex = threading.Semaphore(1)

# Funkce pro barbera
def barber():
    while True:
        print("The barber is sleeping...")
        barber_semaphore.acquire()
        mutex.acquire()
        if len(waiting_customers) > 0:
            customer = waiting_customers.pop(0)
            print(f"The barber is cutting hair for customer {customer}")
            mutex.release()
            time.sleep(random.randint(1, 5))
            print(f"The barber has finished cutting hair for customer {customer}")
            customer_semaphore.release()
        else:
            mutex.release()

# Funkce pro zákazníky
def customer(index):
    global waiting_customers
    time.sleep(random.randint(1, 5))
    mutex.acquire()
    if len(waiting_customers) < NUM_CHAIRS:
        waiting_customers.append(index)
        print(f"Customer {index} is waiting in the waiting room")
        mutex.release()
        barber_semaphore.release()
        customer_semaphore.acquire()
        print(f"Customer {index} has finished getting a haircut")
    else:
        print(f"Customer {index} is leaving because the waiting room is full")
        mutex.release()

# Spuštění vlákna pro barbera
barber_thread = threading.Thread(target=barber)

# Spuštění vláken pro zákazníky
customer_threads = []

# Inicializace webové aplikace
@app.route('/')
def index():
    return render_template('index.html', num_chairs=NUM_CHAIRS, max_customers=MAX_CUSTOMERS, waiting_customers=waiting_customers)

# Endpoint pro uložení konfigurace
@app.route('/save_config', methods=['POST'])
def save_config():
    data = request.get_json()
    global NUM_CHAIRS, MAX_CUSTOMERS
    NUM_CHAIRS = int(data['num_chairs'])
    MAX_CUSTOMERS = int(data['max_customers'])
    return jsonify({"status": "success", "message": "Nastavení byla uložena"})

# Endpoint pro získání seznamu čekajících zákazníků
@app.route('/get_customers', methods=['GET'])
def get_customers():
    return jsonify({"customers": waiting_customers})

# Endpoint pro přidání nového zákazníka
@app.route('/add_customer', methods=['POST'])
def add_customer():
    global customer_threads
    data = request.get_json()
    num_chairs = int(data['num_chairs'])
    max_customers = int(data['max_customers'])
    
    # Zkontroluj, jestli je stále místo pro zákazníka
    if len(waiting_customers) < num_chairs and len(waiting_customers) < max_customers:
        new_customer_index = len(waiting_customers) + 1
        customer_threads.append(threading.Thread(target=customer, args=(new_customer_index,)))
        customer_threads[-1].start()
        return jsonify({"status": "success", "message": f"Zákazník {new_customer_index} přidán do čekárny"})
    else:
        return jsonify({"status": "error", "message": "Čekárna je plná, zákazník nemůže být přidán"})

# Spuštění Flask aplikace
if __name__ == '__main__':
    # Spuštění barbera vlákna
    barber_thread.start()

    # Spuštění aplikace Flask
    app.run(debug=True)
