"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView() {
  const [carsData, setCarsData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/cars")
      .then((response) => response.json())
      .then((data) => setCarsData(data));
  }, []);

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
        />
      )}
    </MapContainer>
  );
}