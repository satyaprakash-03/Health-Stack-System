import { NavLink } from "react-router-dom";
import { modules } from "../data/moduleConfig.js";
import { useAuth } from "../context/AuthContext.jsx";

const Sidebar = ({ open, onClose }) => {
  const { user } = useAuth();
  const visibleModules = modules.filter((module) => module.roles.includes(user?.role));

  return (
    <aside className={`erp-sidebar ${open ? "show" : ""}`}>
      <div className="brand-mark">
        <span className="brand-icon">E</span>
        <div>
          <strong>EduSphere</strong>
          <small>University ERP</small>
        </div>
      </div>

      <nav className="sidebar-nav">
        <span className="sidebar-section-label">Workspace</span>
        <NavLink to="/dashboard" onClick={onClose} className={({ isActive }) => (isActive ? "active" : "")}>
          <i className="bi bi-speedometer2" />
          Dashboard
        </NavLink>
        <NavLink to="/profile" onClick={onClose} className={({ isActive }) => (isActive ? "active" : "")}>
          <i className="bi bi-person-circle" />
          Profile
        </NavLink>
        <span className="sidebar-section-label">ERP Modules</span>
        {visibleModules.map((module) => (
          <NavLink key={module.key} to={`/modules/${module.key}`} onClick={onClose} className={({ isActive }) => (isActive ? "active" : "")}>
            <i className={`bi ${module.icon}`} />
            {module.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
