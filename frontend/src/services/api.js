import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function getServices() {
  const response = await api.get("/api/services");
  return response.data.data;
}

export async function getService(serviceId) {
  const response = await api.get(`/api/services/${serviceId}`);
  return response.data.data;
}

export async function getServiceDependencies(serviceId) {
  const response = await api.get(
    `/api/services/${serviceId}/dependencies`
  );

  return response.data.data;
}

export async function getIncidentImpact(incidentId) {
  const response = await api.get(
    `/api/incidents/${incidentId}/impact`
  );

  return response.data.data;
}

export async function getDatabaseBlastRadius(databaseId) {
  const response = await api.get(
    `/api/databases/${databaseId}/blast-radius`
  );

  return response.data.data;
}

export async function getDeploymentImpact(deploymentId) {
  const response = await api.get(
    `/api/deployments/${deploymentId}/impact`
  );

  return response.data.data;
}

export async function searchGraph(query) {
  const response = await api.get("/api/search", {
    params: {
      q: query,
    },
  });

  return response.data.data;
}

export default api;