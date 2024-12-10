# SleepingBarberProblem
Jak to funguje?

Frontend (HTML + JavaScript) umožňuje zadávat konfiguraci a přidávat nové zákazníky.
Backend (Python + Flask) zpracovává požadavky pro změnu konfigurace a správu zákazníků. Po přidání zákazníka se vlákno pro zákazníka spustí a provede simulaci jeho čekání a stříhání.

app.py:

/save_config: Tento endpoint umožňuje aktualizovat konfiguraci (počet židlí a maximální počet zákazníků) a uložit je na server.
/get_customers: Tento endpoint vrací seznam čekajících zákazníků ve formátu JSON.
/add_customer: Tento endpoint přidává nového zákazníka, pokud je v čekárně místo. Zkontroluje počet zákazníků a židlí, než přidá nového zákazníka a spustí pro něj vlákno.
Hlavní aplikace (app.run()): Flask aplikace je spuštěna s ladicím režimem (debug=True) pro testování.