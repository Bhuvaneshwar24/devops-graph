import { useEffect, useMemo, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";

const API_URL = "http://127.0.0.1:8000";

function GraphView({ services = [] }) {
  const [selectedService, setSelectedService] = useState(
    services[0]?.id || ""
  );
  const [dependencies, setDependencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (services.length > 0 && !selectedService) {
      setSelectedService(services[0].id);
    }
  }, [services, selectedService]);

  useEffect(() => {
    if (!selectedService) return;

    const loadDependencies = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `${API_URL}/api/services/${selectedService}/dependencies`
        );

        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }

        const result = await response.json();
        setDependencies(result.data || []);
      } catch (err) {
        console.error(err);
        setError(err.message);
        setDependencies([]);
      } finally {
        setLoading(false);
      }
    };

    loadDependencies();
  }, [selectedService]);

  const { nodes, edges } = useMemo(() => {
    if (!dependencies.length) {
      return { nodes: [], edges: [] };
    }

    const current = dependencies[0].service;

    const nodeMap = new Map();

    nodeMap.set(current, {
      id: current,
      position: { x: 400, y: 250 },
      data: { label: current },
      style: {
        background: "#2563eb",
        color: "#ffffff",
        border: "1px solid #60a5fa",
        borderRadius: "10px",
        padding: "12px 20px",
        fontWeight: "600",
        width: 180,
        textAlign: "center",
      },
    });

    dependencies.forEach((item, index) => {
      nodeMap.set(item.dependency, {
        id: item.dependency,
        position: {
          x: 120 + index * 300,
          y: 500,
        },
        data: {
          label: item.dependency,
        },
        style: {
          background: "#111827",
          color: "#ffffff",
          border: "1px solid #475569",
          borderRadius: "10px",
          padding: "12px 20px",
          fontWeight: "500",
          width: 180,
          textAlign: "center",
        },
      });
    });

    const generatedEdges = dependencies.map((item, index) => ({
      id: `edge-${index}`,
      source: current,
      target: item.dependency,
      label: item.dependency_criticality,
      markerEnd: {
        type: MarkerType.ArrowClosed,
      },
      style: {
        stroke: "#60a5fa",
        strokeWidth: 2,
      },
      labelStyle: {
        fill: "#94a3b8",
        fontWeight: 600,
      },
    }));

    return {
      nodes: Array.from(nodeMap.values()),
      edges: generatedEdges,
    };
  }, [dependencies]);

  return (
    <div
      style={{
        width: "100%",
        height: "calc(100vh - 120px)",
        minHeight: "600px",
        position: "relative",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 0,
          right: 0,
          zIndex: 10,
        }}
      >
        <select
          value={selectedService}
          onChange={(e) => setSelectedService(e.target.value)}
          style={{
            background: "#111827",
            color: "#ffffff",
            border: "1px solid #334155",
            borderRadius: "6px",
            padding: "8px 12px",
          }}
        >
          {services.map((service) => (
            <option key={service.id} value={service.id}>
              {service.name}
            </option>
          ))}
        </select>
      </div>

      {loading && (
        <div
          style={{
            position: "absolute",
            top: 70,
            left: 20,
            zIndex: 10,
            color: "#94a3b8",
          }}
        >
          Loading dependency graph...
        </div>
      )}

      {error && (
        <div
          style={{
            position: "absolute",
            top: 70,
            left: 20,
            zIndex: 10,
            color: "#f87171",
          }}
        >
          Graph error: {error}
        </div>
      )}

      {!loading && !error && nodes.length === 0 && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            color: "#94a3b8",
          }}
        >
          No dependencies found.
        </div>
      )}

      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        attributionPosition="bottom-left"
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}

export default GraphView;