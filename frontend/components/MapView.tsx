"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

function FitBoundsToTalhoes({ data }: { data: any }) {
  const map = useMap();

  useEffect(() => {
    if (data) {
      const geoJsonLayer = L.geoJSON(data);
      map.fitBounds(geoJsonLayer.getBounds());
    }
  }, [data, map]);

  return null;
}

export default function MapView() {
  const [carsData, setCarsData] = useState(null);
  const [selectedCodImovel, setSelectedCodImovel] = useState(null);
  const [talhoesData, setTalhoesData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/cars")
      .then((response) => response.json())
      .then((data) => setCarsData(data));
  }, []);

  function handleCarClick(feature: any, layer: any) {
    layer.on("click", () => {
      const codImovel = feature.properties.cod_imovel;

      fetch(`http://localhost:8000/cars/${codImovel}/talhoes`)
        .then((response) => response.json())
        .then((data) => {
          setSelectedCodImovel(codImovel);
          setTalhoesData(data);
        })
        .catch((error) => console.error("Erro ao buscar talhões:", error));
    });
  }

  return (
    <MapContainer
      center={[-17.88, -51.71]}
      zoom={11}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {carsData && (
        <GeoJSON
          data={carsData}
          style={{ color: "blue", weight: 1, fillOpacity: 0.1 }}
          onEachFeature={handleCarClick}
        />
      )}
      {talhoesData && (
        <GeoJSON
          key={selectedCodImovel}
          data={talhoesData}
          style={{ color: "green", weight: 1, fillOpacity: 0.1 }}
        />
      )}
      {talhoesData && <FitBoundsToTalhoes data={talhoesData} />}
    </MapContainer>
  );
}