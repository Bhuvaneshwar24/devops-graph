import { useEffect, useState } from "react";
import { getIncidentImpact } from "../services/api";

export default function IncidentPanel() {
  const [impact, setImpact] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const incidentId = "INC-102";

  const loadImpact = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getIncidentImpact(incidentId);
      setImpact(data);
    } catch (err) {
      console.error("Failed to load incident impact:", err);
      setError("Unable to load incident impact.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadImpact();
  }, []);

  if (loading) {
    return (
      <div className="placeholder-page">
        <h1>Incident Impact</h1>
        <p>Loading incident data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="placeholder-page">
        <h1>Incident Impact</h1>
        <p>{error}</p>
        <button onClick={loadImpact}>Retry</button>
      </div>
    );
  }

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">{incidentId}</span>
          <h1>Checkout API Incident</h1>
          <span className="severity">HIGH</span>
        </div>

        <div className="impact-count">
          <span>Impacted Services</span>
          <strong>{impact.length}</strong>
        </div>
      </div>

      <div className="incident-card">
        <div className="incident-card-header">
          <div>
            <h2>Incident Impact</h2>
            <p>Services affected by {incidentId}</p>
          </div>

          <button onClick={loadImpact}>
            ↻ Refresh
          </button>
        </div>

        <div className="impact-list">
          {impact.map((item, index) => (
            <div className="impact-row" key={index}>
              <div className="service-side">
                <div className="service-icon source-icon">▤</div>
                <div>
                  <span>Source Service</span>
                  <strong>
                    {item.affected_service || "Unknown Service"}
                  </strong>
                </div>
              </div>

              <div className="impact-arrow">
                <span>IMPACTS</span>
                <strong>→</strong>
              </div>

              <div className="service-side">
                <div className="service-icon impacted-icon">〽</div>
                <div>
                  <span>Impacted Service</span>
                  <strong>
                    {item.downstream_service || "Unknown Service"}
                  </strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}