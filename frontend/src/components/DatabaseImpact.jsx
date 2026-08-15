import { useEffect, useState } from "react";
import { Database, RefreshCw, ArrowRight } from "lucide-react";
import { getDatabaseBlastRadius, getDatabases } from "../services/api";

export default function DatabaseImpact() {
  const [databases, setDatabases] = useState([]);
  const [selectedDatabaseId, setSelectedDatabaseId] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDatabases = async () => {
    try {
      const result = await getDatabases();
      setDatabases(result || []);

      if (result && result.length > 0) {
        setSelectedDatabaseId((current) => current || result[0].id);
      }
    } catch (err) {
      console.error("Failed to load databases:", err);
      setDatabases([]);
      setSelectedDatabaseId("");
    }
  };

  const loadData = async (databaseId) => {
    if (!databaseId) {
      setData([]);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await getDatabaseBlastRadius(databaseId);
      setData(result || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load database impact.");
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDatabases();
  }, []);

  useEffect(() => {
    if (selectedDatabaseId) {
      loadData(selectedDatabaseId);
    }
  }, [selectedDatabaseId]);

  const selectedDatabase = databases.find(
    (database) => database.id === selectedDatabaseId
  );

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">DATABASE</span>
          <h1>{selectedDatabase?.name || "Database Impact"}</h1>

          <span className="severity">
            BLAST RADIUS
          </span>
        </div>

        <div className="impact-count">
          <span>Affected Relationships</span>
          <strong>{data.length}</strong>
        </div>
      </div>

      <div className="incident-card">
        <div className="incident-card-header">
          <div>
            <h2>Database Impact</h2>
            <p>
              Services directly and indirectly affected by this database.
            </p>
          </div>

          <button onClick={() => loadData(selectedDatabaseId)}>
            <RefreshCw size={15} /> Refresh
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
            Database
          </label>
          <select
            value={selectedDatabaseId}
            onChange={(event) => setSelectedDatabaseId(event.target.value)}
            style={{
              width: "100%",
              background: "#0f172a",
              color: "#f8fafc",
              border: "1px solid #334155",
              borderRadius: "8px",
              padding: "10px 12px",
            }}
          >
            <option value="">Select a database</option>
            {databases.map((database) => (
              <option key={database.id} value={database.id}>
                {database.name} ({database.id})
              </option>
            ))}
          </select>
        </div>

        {loading && (
          <div className="placeholder-page">
            <p>Loading database impact...</p>
          </div>
        )}

        {!loading && !error && selectedDatabaseId && data.length === 0 && (
          <div className="placeholder-page">
            <Database size={40} />
            <h2>No impact data found</h2>
          </div>
        )}

        {!loading && error && (
          <div className="placeholder-page">
            <h2>{error}</h2>
            <button onClick={() => loadData(selectedDatabaseId)}>Retry</button>
          </div>
        )}

        {!loading &&
          !error &&
          data.map((item, index) => (
            <div className="impact-row" key={`${item.database_id}-${item.directly_affected_service}-${item.dependent_service}-${index}`}>
              <div className="service-side">
                <div className="service-icon source-icon">
                  <Database size={22} />
                </div>

                <div>
                  <span>Database</span>
                  <strong>{item.database || selectedDatabase?.name}</strong>
                </div>
              </div>

              <div className="impact-arrow">
                <span>DIRECT</span>
                <strong>
                  <ArrowRight size={24} />
                </strong>
              </div>

              <div className="service-side">
                <div className="service-icon impacted-icon">
                  <Database size={22} />
                </div>

                <div>
                  <span>Direct Service</span>
                  <strong>
                    {item.directly_affected_service || "Unknown"}
                  </strong>

                  {item.dependent_service && (
                    <>
                      <span style={{ marginTop: "8px" }}>
                        Dependent Service
                      </span>
                      <strong>{item.dependent_service}</strong>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}