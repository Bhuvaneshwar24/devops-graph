import {
  Activity,
  AlertTriangle,
  CheckCircle,
  Server,
} from "lucide-react";

function Dashboard({ services }) {
  const healthy = services.filter(
    (service) => service.status === "healthy"
  ).length;

  const degraded = services.filter(
    (service) => service.status === "degraded"
  ).length;

  const critical = services.filter(
    (service) => service.criticality === "critical"
  ).length;

  return (
    <div className="dashboard">
      <div className="page-header">
        <div>
          <h1>Operations Dashboard</h1>
          <p>
            Real-time overview of services and infrastructure
            dependencies.
          </p>
        </div>

        <div className="connection-status">
          <span className="status-dot" />
          Connected to CognoDB
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Server size={22} />
          </div>

          <div>
            <div className="stat-label">Total Services</div>
            <div className="stat-value">{services.length}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon healthy">
            <CheckCircle size={22} />
          </div>

          <div>
            <div className="stat-label">Healthy</div>
            <div className="stat-value">{healthy}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon warning">
            <AlertTriangle size={22} />
          </div>

          <div>
            <div className="stat-label">Degraded</div>
            <div className="stat-value">{degraded}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon critical">
            <Activity size={22} />
          </div>

          <div>
            <div className="stat-label">Critical Services</div>
            <div className="stat-value">{critical}</div>
          </div>
        </div>
      </div>

      <div className="content-card">
        <div className="card-header">
          <div>
            <h2>Service Health</h2>
            <p>Current status of monitored services</p>
          </div>
        </div>

        <div className="service-table">
          <div className="table-header">
            <span>Service</span>
            <span>Criticality</span>
            <span>Status</span>
          </div>

          {services.map((service) => (
            <div className="table-row" key={service.id}>
              <div>
                <strong>{service.name}</strong>
                <small>{service.description}</small>
              </div>

              <span
                className={`badge ${service.criticality}`}
              >
                {service.criticality}
              </span>

              <span
                className={`status-badge ${service.status}`}
              >
                <span className="status-dot" />
                {service.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;