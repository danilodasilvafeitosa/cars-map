"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import FitBoundsToTalhoes from "./FitBoundsToTalhoes";
import TalhoesSidebar from "./TalhoesSidebar";

export default function MapView() {
  const [carsData, setCarsData] = useState(null);
  const [selectedCodImovel, setSelectedCodImovel] = useState(null);
  const [talhoesData, setTalhoesData] = useState(null);
  const [selectedTalhaoIds, setSelectedTalhaoIds] = useState<string[]>([]);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [selectedCarInfo, setSelectedCarInfo] = useState<any>(null);

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
          setSelectedCarInfo(feature.properties);
          setTalhoesData(data);
          const allIds = data.features.map((f: any) => f.properties.talhao_id);
          setSelectedTalhaoIds(allIds);
        })
    });
  }

  function toggleTalhaoSelection(talhaoId: string) {
    setSelectedTalhaoIds((prev) =>
      prev.includes(talhaoId)
        ? prev.filter((id) => id !== talhaoId)
        : [...prev, talhaoId]
    );
  }

  function getTalhaoStyle(feature: any) {
    const isSelected = selectedTalhaoIds.includes(feature.properties.talhao_id);
    return {
      color: isSelected ? "orange" : "green",
      weight: 1,
      fillOpacity: isSelected ? 0.4 : 0.1,
    };
  }

  function handleTalhaoClick(feature: any, layer: any) {
    layer.on("click", (e: any) => {
      L.DomEvent.stopPropagation(e);
      toggleTalhaoSelection(feature.properties.talhao_id);
    });
  }

  async function handleGenerateReport() {
    if (!selectedCodImovel) return;

    setIsGeneratingReport(true);

    try {
      const response = await fetch(
        `http://localhost:8000/cars/${selectedCodImovel}/report`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ talhao_ids: selectedTalhaoIds }),
        }
      );

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `relatorio_${selectedCodImovel}.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Erro ao gerar relatório:", error);
    } finally {
      setIsGeneratingReport(false);
    }
  }

  return (
    <div style={{ position: "relative" }}>
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
            style={getTalhaoStyle}
            onEachFeature={handleTalhaoClick}
          />
        )}
        {talhoesData && <FitBoundsToTalhoes data={talhoesData} />}
      </MapContainer>
      <TalhoesSidebar
        talhoesData={talhoesData}
        selectedCarInfo={selectedCarInfo}
        selectedTalhaoIds={selectedTalhaoIds}
        onToggle={toggleTalhaoSelection}
        onGenerateReport={handleGenerateReport}
        isGeneratingReport={isGeneratingReport}
      />
    </div>
  );
}