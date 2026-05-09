import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5050/api"
});

api.interceptors.request.use((config) => {
  let token = null;
  try {
    token = localStorage.getItem("erpToken");
  } catch {
    token = null;
  }
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      try {
        localStorage.removeItem("erpToken");
        localStorage.removeItem("erpUser");
      } catch {
        // Ignore storage cleanup failures in restricted browser contexts.
      }
    }
    return Promise.reject(error);
  }
);

export default api;
