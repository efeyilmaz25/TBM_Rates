from fastapi import FastAPI
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

@app.get("/api/tcmb")
def get_tcmb_rates():
    url = "https://www.tcmb.gov.tr/kurlar/today.xml"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    tree = ET.fromstring(response.content)
    rates = {}
    for currency in tree.findall("Currency"):
        code = currency.get("CurrencyCode")
        name = currency.find("Isim").text
        forex_selling = currency.find("ForexSelling").text
        rates[code] = {"name": name, "forex_selling": forex_selling}

    return {"date": tree.attrib.get("Tarih"), "rates": rates}
