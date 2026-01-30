# Kokoushuoneiden varausrajapinta

Yksinkertainen, REST-pohjainen rajapinta kokoushuoneiden varaamiseen. Toteutettu Pythonilla ja FastAPI:lla.

Sovellus hyödyntää in-memory -tietokantaa ja varmistaa tietojen eheyden samanaikaisessa käytössä.

## Ominaisuudet

* **Varausten hallinta:** Luo, listaa ja peru varauksia.
* **Validointi:** Estää varaukset menneisyyteen ja varmistaa aikojen loogisuuden.
* **Päällekkäisyyksien esto:** Estää saman huoneen varaamisen päällekkäin.
* **Säieturvallisuus:** Käsittelee samanaikaiset (concurrent) pyynnöt turvallisesti ilman race condition -riskiä.

## Teknologiat

* Python 3.14.0
* FastAPI
* Pydantic
* Uvicorn

## Asennus ja käynnistys

1. Asenna riippuvuudet:
```bash
pip install -r requirements.txt
```

2. Käynnistä palvelin:
```bash
    uvicorn main:app --reload

    Palvelin käynnistyy oletuksena osoitteeseen http://127.0.0.1:8000.
    API-dokumentaatio (Swagger UI) löytyy osoitteesta: http://127.0.0.1:8000/docs
```

## Testaus

Projektissa on automaattiset testit logiikalle ja kuormitukselle. Testit ajetaan projektin juuresta:

```bash
# API-logiikan ja validoinnin testaus
python tests/test_api.py
```

```bash
# Samanaikaisuuden (Concurrency) kuormitustesti
python tests/test_concurrency.py 
```