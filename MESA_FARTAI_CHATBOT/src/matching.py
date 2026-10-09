from math import radians, sin, cos, sqrt, atan2

def distancia_km(lat1, lon1, lat2, lon2):
    """Calcula distância aproximada entre dois pontos usando Haversine."""
    R = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )

    return 2 * R * atan2(sqrt(a), sqrt(1 - a))


def encontrar_ongs_proximas(lat, lon, ongs):
    resultados = []

    for ong in ongs:
        distancia = distancia_km(
            lat, lon,
            ong["latitude"], ong["longitude"]
        )

        resultados.append({
            **ong,
            "distancia_km": round(distancia, 2)
        })

    return sorted(resultados, key=lambda x: x["distancia_km"])
