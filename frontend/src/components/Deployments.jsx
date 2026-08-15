import { useEffect, useState } from "react";
import { Rocket, RefreshCw, AlertTriangle } from "lucide-react";
import { getDeploymentImpact, getDeployments } from "../services/api";

export default function Deployments() {
  const [deployments, setDeployments] = useState([]);
  const [selectedDeploymentId, setSelectedDeploymentId] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDeployments = async () => {
    try {
      const result = await getDeployments();
      setDeployments(result || []);

      if (result && result.length > 0) {
        setSelectedDeploymentId((current) => current || result[0].id);
      }
    } catch (err) {
      console.error("Failed to load deployments:", err);
      setDeployments([]);
      setSelectedDeploymentId("");
    }
  };

  const loadData = async (deploymentId) => {
    if (!deploymentId) {
      setData([]);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await getDeploymentImpact(deploymentId);
      setData(result || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load deployment impact.");
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDeployments();
  }, []);

  useEffect(() => {
    if (selectedDeploymentId) {
      loadData(selectedDeploymentId);
    }
  }, [selectedDeploymentId]);

  const selectedDeployment = deployments.find(
    (deployment) => deployment.id === selectedDeploymentId
  );
  const deployment = data[0];
  const incidents = deployment?.related_incidents || [];

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">
            {deployment?.deployment_id || selectedDeployment?.id || "DEPLOYMENT"}
          </span>

          <h1>
            {deployment?.version || selectedDeployment?.version || "Deployment Impact"}
          </h1>

          <span className="severity">
            {deployment?.deployment_status || selectedDeployment?.status || "DEPLOYMENT"}
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

          <button onClick={() => loadData(selectedDeploymentId)}>
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
            Deployment
          </label>
          <select
            value={selectedDeploymentId}
            onChange={(event) => setSelectedDeploymentId(event.target.value)}
            style={{
              width: "100%",
              background: "#0f172a",
              color: "#f8fafc",
              border: "1px solid #334155",
              borderRadius: "8px",
              padding: "10px 12px",
            }}
          >
            <option value="">Select a deployment</option>
            {deployments.map((deploymentItem) => (
              <option key={deploymentItem.id} value={deploymentItem.id}>
                {deploymentItem.version} ({deploymentItem.id})
              </option>
            ))}
          </select>
        </div>

        {loading && (
          <div className="placeholder-page">
            <p>Loading deployment impact...</p>
          </div>
        )}

        {!loading && !error && selectedDeploymentId && data.length === 0 && (
          <div className="placeholder-page">
            <h2>No deployment impact found</h2>
          </div>
        )}

        {!loading && error && (
          <div className="placeholder-page">
            <h2>{error}</h2>
            <button onClick={() => loadData(selectedDeploymentId)}>Retry</button>
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