import pytest

zbiornik_wody_1 = 80.0
zbiornik_wody_2 = 80.0
zbiornik_rezerwa = 80.0

zbiornik_wegiel = 0.0
tryb_zasilania = "Odlaczony"

def test_analiza_produkcji():
    print(f"\n--- RAPORT STANU ---")
    print(f"Woda 1: {zbiornik_wody_1}%")
    print(f"Woda 2: {zbiornik_wody_2}%")
    print(f"Rezerwa: {zbiornik_rezerwa}%")
    print(f"Węgiel: {zbiornik_wegiel}%")
    print(f"Zasilanie: {tryb_zasilania}")

    czy_woda_ok = (zbiornik_wody_1 > 50) and (zbiornik_wody_2 > 50) and (zbiornik_rezerwa > 50)

    czy_wegiel_ok = (zbiornik_wegiel > 50)

    czy_zasilanie_ok = (tryb_zasilania != "Odlaczony")

    print(f"--------------------")
    print(f"Status Wody:      {'OK' if czy_woda_ok else 'BŁĄD'}")
    print(f"Status Węgla:     {'OK' if czy_wegiel_ok else 'BŁĄD'}")
    print(f"Status Zasilania: {'OK' if czy_zasilanie_ok else 'BŁĄD'}")

    mozna_rozpoczac = czy_woda_ok and czy_wegiel_ok and czy_zasilanie_ok

    assert mozna_rozpoczac is True, "ZATRZYMANIE: Nie spełniono warunków startu!"