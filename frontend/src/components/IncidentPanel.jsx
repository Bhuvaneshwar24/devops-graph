import { useEffect, useState } from "react";
import { getIncidentImpact, getIncidents } from "../services/api";

export default function IncidentPanel() {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncidentId, setSelectedIncidentId] = useState("");
  const [impact, setImpact] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadIncidents = async () => {
    try {
      const data = await getIncidents();
      setIncidents(data || []);

      if (data && data.length > 0) {
        setSelectedIncidentId((current) => current || data[0].id);
      }
    } catch (err) {
      console.error("Failed to load incidents:", err);
      setIncidents([]);
      setSelectedIncidentId("");
    }
  };

  const loadImpact = async (incidentId) => {
    if (!incidentId) {
      setImpact([]);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await getIncidentImpact(incidentId);
      setImpact(data || []);
    } catch (err) {
      console.error("Failed to load incident impact:", err);
      setError("Unable to load incident impact.");
      setImpact([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIncidents();
  }, []);

  useEffect(() => {
    if (selectedIncidentId) {
      loadImpact(selectedIncidentId);
    }
  }, [selectedIncidentId]);

  const selectedIncident = incidents.find(
    (incident) => incident.id === selectedIncidentId
  );

  if (loading && !selectedIncidentId) {
    return (
      <div className="placeholder-page">
        <h1>Incident Impact</h1>
        <p>Loading incident data...</p>
      </div>
    );
  }

  if (error && !selectedIncidentId) {
    return (
      <div className="placeholder-page">
        <h1>Incident Impact</h1>
        <p>{error}</p>
        <button onClick={() => loadImpact(selectedIncidentId)}>Retry</button>
      </div>
    );
  }

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">
            {selectedIncident?.id || "INCIDENT"}
          </span>
          <h1>{selectedIncident?.title || "Incident Impact"}</h1>
          <span className="severity">
            {selectedIncident?.severity || "UNKNOWN"}
          </span>
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
            <p>
              {selectedIncidentId
                ? `Services affected by ${selectedIncidentId}`
                : "Select an incident to view impact."}
            </p>
          </div>

          <button onClick={() => loadImpact(selectedIncidentId)}>
            ↻ Refresh
          </button>
        </div>

        <div
          style={{
            padding: "18px 24px 0",
            borderBottom: "1px solid #243044",
          }}
        >
          <label
            style={{
              display: "block",
              color: "#cbd5e1",
              fontSize: "12px",
              marginBottom: "8px",
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: "0.06em",
            }}
          >
            Incident
          </label>
          <select
            value={selectedIncidentId}
            onChange={(event) => setSelectedIncidentId(event.target.value)}
            style={{
              width: "100%",
              background: "#0f172a",
              color: "#f8fafc",
              border: "1px solid #334155",
              borderRadius: "8px",
              padding: "10px 12px",
            }}
          >
            <option value="">Select an incident</option>
            {incidents.map((incident) => (
              <option key={incident.id} value={incident.id}>
                {incident.title} ({incident.id})
              </option>
            ))}
          </select>
        </div>

        {loading && (
          <div className="placeholder-page">
            <p>Loading incident impact...</p>
          </div>
        )}

        {!loading && !error && impact.length === 0 && selectedIncidentId && (
          <div className="placeholder-page">
            <h2>No impacted services found</h2>
          </div>
        )}

        {!loading && error && (
          <div className="placeholder-page">
            <h2>{error}</h2>
            <button onClick={() => loadImpact(selectedIncidentId)}>Retry</button>
          </div>
        )}

        {!loading && !error && impact.length > 0 && (
          <div className="impact-list">
            {impact.map((item, index) => (
              <div className="impact-row" key={`${item.incident_id}-${item.affected_service}-${item.downstream_service}-${index}`}>
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
        )}
      </div>
    </div>
  );
}