import ThemeToggle from "./ThemeToggle.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { roleLabels } from "../data/moduleConfig.js";

const Topbar = ({ onMenu }) => {
  const { user, logout } = useAuth();
  const today = new Date().toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" });

  return (
    <header className="erp-topbar">
      <button className="btn btn-icon d-lg-none" onClick={onMenu} aria-label="Open navigation">
        <i className="bi bi-list" />
      </button>
      <div>
        <h1>College ERP Portal</h1>
        <p>{roleLabels[user?.role]} workspace for academic operations</p>
      </div>
      <div className="topbar-actions">
        <div className="search-pill d-none d-md-flex">
          <i className="bi bi-search" />
          <span>Search modules, reports, people</span>
        </div>
        <div className="date-chip d-none d-xl-flex">
          <i className="bi bi-calendar2-week" />
          <span>{today}</span>
        </div>
        <button className="btn btn-icon d-none d-sm-inline-grid" aria-label="Notifications">
          <i className="bi bi-bell" />
        </button>
        <ThemeToggle />
        <div className="user-chip">
          <span>{user?.name?.charAt(0) || "U"}</span>
          <div className="d-none d-sm-block">
            <strong>{user?.name}</strong>
            <small>{roleLabels[user?.role]}</small>
          </div>
        </div>
        <button className="btn btn-outline-danger btn-sm" onClick={logout}>
          <i className="bi bi-box-arrow-right me-1" />
          Logout
        </button>
      </div>
    </header>
  );
};

export default Topbar;
