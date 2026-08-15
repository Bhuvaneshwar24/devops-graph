import { useEffect, useState } from "react";
import { Rocket, RefreshCw, AlertTriangle } from "lucide-react";
import { getDeploymentImpact } from "../services/api";

export default function Deployments() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const deploymentId = "DEP-004";

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const result = await getDeploymentImpact(deploymentId);
      setData(result || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load deployment impact.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const deployment = data[0];

  const incidents = deployment?.related_incidents || [];

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">
            {deployment?.deployment_id || deploymentId}
          </span>

          <h1>
            {deployment?.version || "payment-2.8.1"}
          </h1>

          <span className="severity">
            {deployment?.deployment_status || "DEPLOYMENT"}
          </span>
        </div>

        <div className="impact-count">
          <span>Related Incidents</span>
          <strong>{incidents.length}</strong>
        </div>
      </div>

      <div className="incident-card">
        <div className="incident-card-header">
          <div>
            <h2>Deployment Impact</h2>
            <p>
              Services and incidents associated with this deployment.
            </p>
          </div>

          <button onClick={loadData}>
            <RefreshCw size={15} /> Refresh
          </button>
        </div>

        {loading && (
          <div className="placeholder-page">
            <p>Loading deployment impact...</p>
          </div>
        )}

        {error && (
          <div className="placeholder-page">
            <h2>{error}</h2>
            <button onClick={loadData}>Retry</button>
          </div>
        )}

        {!loading && !error && deployment && (
          <>
            <div className="impact-row">
              <div className="service-side">
                <div className="service-icon source-icon">
                  <Rocket size={22} />
                </div>

                <div>
                  <span>Deployment</span>
                  <strong>{deployment.deployment_id}</strong>
                </div>
              </div>

              <div className="impact-arrow">
                <span>DEPLOYED</span>
                <strong>→</strong>
              </div>

              <div className="service-side">
                <div className="service-icon impacted-icon">
                  <Rocket size={22} />
                </div>

                <div>
                  <span>Service</span>
                  <strong>{deployment.deployed_service}</strong>
                </div>
              </div>
            </div>

            <div className="impact-row">
              <div className="service-side">
                <div className="service-icon source-icon">
                  <Rocket size={22} />
                </div>

                <div>
                  <span>Version</span>
                  <strong>{deployment.version}</strong>
                </div>
              </div>

              <div className="impact-arrow">
                <span>IMPACTS</span>
                <strong>→</strong>
              </div>

              <div className="service-side">
                <div className="service-icon impacted-icon">
                  <AlertTriangle size={22} />
                </div>

                <div>
                  <span>Dependent Service</span>
                  <strong>
                    {deployment.dependent_service || "None"}
                  </strong>
                </div>
              </div>
            </div>

            <div className="impact-row">
              <div className="service-side">
                <div className="service-icon source-icon">
                  <AlertTriangle size={22} />
                </div>

                <div>
                  <span>Deployment Status</span>
                  <strong>
                    {deployment.deployment_status || "Unknown"}
                  </strong>
                </div>
              </div>

              <div className="impact-arrow">
                <span>RELATED</span>
                <strong>→</strong>
              </div>

              <div className="service-side">
                <div className="service-icon impacted-icon">
                  <AlertTriangle size={22} />
                </div>

                <div>
                  <span>Incidents</span>
                  <strong>
                    {incidents.length
                      ? incidents.join(", ")
                      : "None"}
                  </strong>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}