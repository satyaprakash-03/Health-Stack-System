import { createContext, useContext, useMemo, useState } from "react";
import api from "../services/api.js";

const AuthContext = createContext(null);

const readStoredUser = () => {
  try {
    const saved = localStorage.getItem("erpUser");
    return saved ? JSON.parse(saved) : null;
  } catch {
    localStorage.removeItem("erpUser");
    localStorage.removeItem("erpToken");
    return null;
  }
};

const readStoredTheme = () => {
  try {
    return localStorage.getItem("erpTheme") || "light";
  } catch {
    return "light";
  }
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(readStoredUser);
  const [theme, setTheme] = useState(readStoredTheme);

  const login = async (email, password) => {
    const { data } = await api.post("/auth/login", { email, password });
    try {
      localStorage.setItem("erpToken", data.token);
      localStorage.setItem("erpUser", JSON.stringify(data.user));
    } catch {
      // Some embedded browsers can reject storage writes; keep session in memory.
    }
    setUser(data.user);
    return data.user;
  };

  const logout = () => {
    try {
      localStorage.removeItem("erpToken");
      localStorage.removeItem("erpUser");
    } catch {
      // Ignore storage cleanup failures in restricted browser contexts.
    }
    setUser(null);
  };

  const toggleTheme = () => {
    setTheme((current) => {
      const next = current === "light" ? "dark" : "light";
      try {
        localStorage.setItem("erpTheme", next);
      } catch {
        // Theme still changes for the current session.
      }
      return next;
    });
  };

  const value = useMemo(() => ({ user, login, logout, theme, toggleTheme }), [user, theme]);

  return (
    <AuthContext.Provider value={value}>
      <div data-theme={theme}>{children}</div>
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
