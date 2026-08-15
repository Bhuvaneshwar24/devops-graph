import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import { getServices } from "./services/api";
import "./App.css";
import GraphView from "./components/GraphView";
import IncidentPanel from "./components/IncidentPanel";
import DatabaseImpact from "./components/DatabaseImpact";
import Deployments from "./components/Deployments";
import Search from "./components/Search";

function App() {
  const [services, setServices] = useState([]);
  const [activeView, setActiveView] = useState("dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadServices() {
      try {
        setLoading(true);
        const data = await getServices();
        setServices(data);
        setError("");
      } catch (err) {
        console.error("Failed to load services:", err);
        setError("Unable to connect to the DevOps API.");
      } finally {
        setLoading(false);
      }
    }

    loadServices();
  }, []);

  function renderContent() {
    if (loading) {
      return (
        <div className="loading-screen">
          <div className="loading-spinner" />
          <p>Loading infrastructure graph...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="error-screen">
          <h2>Backend Connection Failed</h2>
          <p>{error}</p>
          <p>
            Make sure FastAPI is running on port 8000.
          </p>
        </div>
      );
    }

    switch (activeView) {
      case "dashboard":
        return <Dashboard services={services} />;

      case "graph":
  return <GraphView services={services} />;

      case "incidents":
  return <IncidentPanel />;

     case "database":
  return <DatabaseImpact />;

      case "deployments":
  return <Deployments />;

      case "search":
  return <Search />;

      default:
        return <Dashboard services={services} />;
    }
  }

  return (
    <div className="app">
      <Sidebar
        activeView={activeView}
        setActiveView={setActiveView}
      />

      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;