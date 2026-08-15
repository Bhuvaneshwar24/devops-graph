import {
  LayoutDashboard,
  Network,
  AlertTriangle,
  Database,
  Rocket,
  Search,
} from "lucide-react";

function Sidebar({ activeView, setActiveView }) {
  const items = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      id: "graph",
      label: "Service Graph",
      icon: Network,
    },
    {
      id: "incidents",
      label: "Incidents",
      icon: AlertTriangle,
    },
    {
      id: "databases",
      label: "Database Impact",
      icon: Database,
    },
    {
      id: "deployments",
      label: "Deployments",
      icon: Rocket,
    },
    {
      id: "search",
      label: "Search",
      icon: Search,
    },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">AI</div>

        <div>
          <div className="brand-title">DevOps Graph</div>
          <div className="brand-subtitle">Incident Intelligence</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              className={`nav-item ${
                activeView === item.id ? "active" : ""
              }`}
              onClick={() => setActiveView(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="status-dot" />

        <div>
          <div className="system-status">System Connected</div>
          <div className="system-subtitle">CognoDB</div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;