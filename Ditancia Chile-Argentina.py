import requests
import os
import sys
import textwrap
API_KEY = "9fc3a56e-d04f-4b56-9608-be27c36009f2"
HEADERS = {"User-Agent": "DRY7122-script/1.0"}
def geocode(ciudad):
    """Obtiene coordenadas lat/lon desde una ciudad usando GraphHopper Geocode API"""
    url = "https://graphhopper.com/api/1/geocode"
    params = {"q": ciudad, "limit": 1, "locale": "es", "key": API_KEY}
    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    hits = r.json().get("hits")
    if not hits:
        raise ValueError(f"No se encontró la ciudad: {ciudad}")
    return hits[0]["point"]["lat"], hits[0]["point"]["lng"]
def ruta(origen, destino, vehiculo="car"):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{origen[0]},{origen[1]}", f"{destino[0]},{destino[1]}"],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "points_encoded": "false",
        "key": API_KEY
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    if "message" in data:
        raise RuntimeError(data["message"])
    path = data["paths"][0]
    return {
        "dist_m": path["distance"],
        "time_ms": path["time"],
        "instrucciones": [i["text"] for i in path["instructions"]]
    }
def main():
    print("=== Ruta Chile ↔ Argentina con GraphHopper ===")
    print("(Escribe 's' en cualquier momento para salir)\n")
    while True:
        try:
            origen = input("Ciudad origen: ").strip()
            if origen.lower() == 's':
                break
            destino = input("Ciudad destino: ").strip()
            if destino.lower() == 's':
                break
            transporte = input("Transporte (car/bike/foot): ").strip().lower()
            if transporte == 's':
                break
            lat_origen = geocode(origen)
            lat_destino = geocode(destino)
            datos = ruta(lat_origen, lat_destino, transporte)
            km = datos["dist_m"] / 1000
            millas = km * 0.621371
            minutos = datos["time_ms"] / 60000
            horas = int(minutos // 60)
            minutos = int(minutos % 60)
            print(f"\nDistancia: {km:.2f} km | {millas:.2f} mi")
            print(f"Duración estimada: {horas} h {minutos:02d} min")
            print("Narrativa del viaje:")
            for paso in datos["instrucciones"]:
                print(" •", textwrap.fill(paso, width=70,
                                         subsequent_indent="   "))
            print("\n" + "-"*60 + "\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")
            continue
if __name__ == "__main__":
    main()
