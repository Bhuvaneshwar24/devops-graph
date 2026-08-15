import { useState } from "react";
import { Search as SearchIcon, Server, AlertTriangle, Rocket } from "lucide-react";
import { searchGraph } from "../services/api";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (event) => {
    event.preventDefault();

    if (!query.trim()) {
      setResults([]);
      setSearched(false);
      return;
    }

    try {
      setLoading(true);

      const data = await searchGraph(query.trim());

      setResults(data || []);
      setSearched(true);
    } catch (error) {
      console.error(error);
      setResults([]);
      setSearched(true);
    } finally {
      setLoading(false);
    }
  };

  const getIcon = (labels = []) => {
    if (labels.includes("Incident")) {
      return <AlertTriangle size={22} />;
    }

    if (labels.includes("Deployment")) {
      return <Rocket size={22} />;
    }

    if (labels.includes("Database")) {
      return <Server size={22} />;
    }

    return <Server size={22} />;
  };

  return (
    <div className="incident-page">
      <div className="incident-header">
        <div>
          <span className="incident-id">GRAPH SEARCH</span>
          <h1>Search Infrastructure</h1>

          <span className="severity">
            COGNODB
          </span>
        </div>

        <div className="impact-count">
          <span>Results</span>
          <strong>{results.length}</strong>
        </div>
      </div>

      <div className="incident-card">
        <div className="incident-card-header">
          <div>
            <h2>Search Graph</h2>
            <p>
              Search services, incidents, databases, deployments and graph entities.
            </p>
          </div>
        </div>

        <form
          onSubmit={handleSearch}
          style={{
            display: "flex",
            gap: "12px",
            padding: "30px 32px",
            borderBottom: "1px solid #243044",
          }}
        >
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name, ID, title or version..."
            style={{
              flex: 1,
              padding: "14px 16px",
              background: "#0f172a",
              border: "1px solid #334155",
              borderRadius: "8px",
              color: "#f8fafc",
              fontSize: "15px",
              outline: "none",
            }}
          />

          <button
            type="submit"
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              padding: "12px 20px",
              border: "none",
              borderRadius: "8px",
              background: "#2563eb",
              color: "#fff",
              cursor: "pointer",
              fontSize: "14px",
            }}
          >
            <SearchIcon size={17} />
            Search
          </button>
        </form>

        {loading && (
          <div className="placeholder-page">
            <p>Searching CognoDB...</p>
          </div>
        )}

        {!loading && searched && results.length === 0 && (
          <div className="placeholder-page">
            <SearchIcon size={40} />
            <h2>No results found</h2>
            <p>Try another service, incident ID, database, or deployment.</p>
          </div>
        )}

        {!loading &&
          results.map((item, index) => (
            <div className="impact-row" key={`${item.id}-${index}`}>
              <div className="service-side">
                <div className="service-icon source-icon">
                  {getIcon(item.labels)}
                </div>

                <div>
                  <span>
                    {item.labels?.[0] || "Node"}
                  </span>

                  <strong>{item.name || item.id}</strong>
                </div>
              </div>

              <div className="impact-arrow">
                <span>ID</span>
                <strong>→</strong>
              </div>

              <div className="service-side">
                <div>
                  <span>Identifier</span>
                  <strong>{item.id}</strong>
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}