"use client";

export default function TalhoesSidebar({
  talhoesData,
  selectedCarInfo,
  selectedTalhaoIds,
  onToggle,
  onGenerateReport,
  isGeneratingReport,
}: {
  talhoesData: any;
  selectedCarInfo: any
  selectedTalhaoIds: string[];
  onToggle: (id: string) => void;
  onGenerateReport: () => void;
  isGeneratingReport: boolean;
}) {
  if (!talhoesData) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: 10,
        right: 10,
        zIndex: 1000,
        background: "white",
        borderRadius: "8px",
        width: "320px",
        maxHeight: "80vh",
        boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
        color: "#1a1a1a",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ padding: "16px 16px 0 16px" }}>
        <h3 style={{ marginBottom: "8px", color: "#1a1a1a" }}>Talhões</h3>
      </div>

      <div style={{ padding: "16px 16px 0 16px" }}>
        {selectedCarInfo && (
          <div
            style={{
              background: "#f5f5f5",
              padding: "10px",
              borderRadius: "6px",
              marginBottom: "12px",
              fontSize: "13px",
            }}
          >
            <div>
              <strong>CAR:</strong> {selectedCarInfo.cod_imovel}
            </div>

             <div>
              <strong>Area:</strong> {selectedCarInfo.area_ha} ha
            </div>
          </div>
        )}
      </div>

      <div style={{ overflowY: "auto", padding: "0 16px", flex: 1 }}>
        {talhoesData.features.map((feature: any) => {
          const id = feature.properties.talhao_id;
          return (
            <label
              key={id}
              style={{
                display: "block",
                marginBottom: "6px",
                fontSize: "14px",
                color: "#1a1a1a",
              }}
            >
              <input
                type="checkbox"
                checked={selectedTalhaoIds.includes(id)}
                onChange={() => onToggle(id)}
              />
              {" "}
              {id.slice(0, 8)} ({feature.properties.area_ha} ha)
            </label>
          );
        })}
      </div>

      <div style={{ padding: "16px" }}>
        <button
          onClick={onGenerateReport}
          disabled={isGeneratingReport || selectedTalhaoIds.length === 0}
          style={{
            width: "100%",
            padding: "10px",
            background: isGeneratingReport ? "#ccc" : "#f97316",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: isGeneratingReport ? "not-allowed" : "pointer",
            fontSize: "14px",
            fontWeight: "bold",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
          }}
        >
        {isGeneratingReport && (
          <span
            style={{
              width: "14px",
              height: "14px",
              border: "2px solid white",
              borderTopColor: "transparent",
              borderRadius: "50%",
              display: "inline-block",
              animation: "spin 0.8s linear infinite",
            }}
          />
        )}
        {isGeneratingReport ? "Gerando relatório..." : "Gerar Relatório PDF"}
      </button>
      </div>
    </div>
  );
}