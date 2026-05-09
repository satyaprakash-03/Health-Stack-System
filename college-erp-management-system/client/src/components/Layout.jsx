import { useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar.jsx";
import Topbar from "./Topbar.jsx";

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="erp-shell">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      {sidebarOpen && <button className="sidebar-backdrop d-lg-none" onClick={() => setSidebarOpen(false)} aria-label="Close navigation" />}
      <main className="erp-main">
        <Topbar onMenu={() => setSidebarOpen(true)} />
        <section className="erp-content">
          <Outlet />
        </section>
      </main>
    </div>
  );
};

export default Layout;
