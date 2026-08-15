import { useEffect, useState } from "react";
import { Database, RefreshCw, ArrowRight } from "lucide-react";
import { getDatabaseBlastRadius } from "../services/api";

export default function DatabaseImpact() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const databaseId = "db-orders";

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const result = await getDatabaseBlastRadius(databaseId);
      setData(result || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load database impact.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">DATABASE</span>
          <h1>Orders PostgreSQL</h1>

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

          <button onClick={loadData}>
            <RefreshCw size={15} /> Refresh
          </button>
        </div>

        {loading && (
          <div className="placeholder-page">
            <p>Loading database impact...</p>
          </div>
        )}

        {error && (
          <div className="placeholder-page">
            <h2>{error}</h2>
            <button onClick={loadData}>Retry</button>
          </div>
        )}

        {!loading && !error && data.length === 0 && (
          <div className="placeholder-page">
            <Database size={40} />
            <h2>No impact data found</h2>
          </div>
        )}

        {!loading &&
          !error &&
          data.map((item, index) => (
            <div className="impact-row" key={index}>
              <div className="service-side">
                <div className="service-icon source-icon">
                  <Database size={22} />
                </div>

                <div>
                  <span>Database</span>
                  <strong>{item.database || "Orders PostgreSQL"}</strong>
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