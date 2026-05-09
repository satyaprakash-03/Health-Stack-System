import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import DataTable from "../components/DataTable.jsx";
import RecordModal from "../components/RecordModal.jsx";
import api from "../services/api.js";
import { canEdit, modules } from "../data/moduleConfig.js";
import { useAuth } from "../context/AuthContext.jsx";

const ModulePage = () => {
  const { moduleKey } = useParams();
  const { user } = useAuth();
  const config = useMemo(() => modules.find((item) => item.key === moduleKey), [moduleKey]);
  const [rows, setRows] = useState([]);
  const [pagination, setPagination] = useState({ page: 1, pages: 1, total: 0 });
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [modal, setModal] = useState({ show: false, record: null });
  const [loading, setLoading] = useState(false);

  const canManage = canEdit(user?.role);

  const fetchRows = async (page = 1) => {
    setLoading(true);
    try {
      const { data } = await api.get(`/modules/${moduleKey}`, { params: { page, search, status } });
      setRows(data.items);
      setPagination(data.pagination);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (config) fetchRows(1);
  }, [moduleKey]);

  const saveRecord = async (record) => {
    if (record._id) {
      await api.patch(`/modules/${moduleKey}/${record._id}`, record);
    } else {
      await api.post(`/modules/${moduleKey}`, record);
    }
    setModal({ show: false, record: null });
    fetchRows(pagination.page);
  };

  const deleteRecord = async (id) => {
    if (!window.confirm("Delete this record?")) return;
    await api.delete(`/modules/${moduleKey}/${id}`);
    fetchRows(pagination.page);
  };

  if (!config) {
    return <div className="alert alert-warning">Module not found.</div>;
  }

  return (
    <div className="module-page">
      <div className="module-header">
        <div>
          <span className="eyebrow">ERP Module</span>
          <h2>
            <i className={`bi ${config.icon} me-2`} />
            {config.label}
          </h2>
          <p>Search, filter, paginate, and manage records through REST API integration.</p>
        </div>
        {canManage && (
          <button className="btn btn-primary" onClick={() => setModal({ show: true, record: null })}>
            <i className="bi bi-plus-circle me-2" />
            Add Record
          </button>
        )}
      </div>

      <div className="module-insights">
        <div>
          <i className="bi bi-database-check" />
          <strong>{pagination.total}</strong>
          <span>Total records</span>
        </div>
        <div>
          <i className="bi bi-funnel" />
          <strong>{search || status ? "Filtered" : "All"}</strong>
          <span>Current view</span>
        </div>
        <div>
          <i className="bi bi-shield-check" />
          <strong>{canManage ? "Editable" : "Read only"}</strong>
          <span>Your access</span>
        </div>
      </div>

      <div className="toolbar panel">
        <div className="input-group">
          <span className="input-group-text">
            <i className="bi bi-search" />
          </span>
          <input className="form-control" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by name, title, roll no, code, or company" />
        </div>
        <select className="form-select" value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">All statuses</option>
          <option>Active</option>
          <option>Pending</option>
          <option>Published</option>
          <option>Open</option>
          <option>Completed</option>
        </select>
        <button className="btn btn-dark" onClick={() => fetchRows(1)}>
          Filter
        </button>
        <button className="btn btn-light" onClick={() => window.print()}>
          <i className="bi bi-printer me-2" />
          Print
        </button>
      </div>

      <div className="panel">
        <div className="panel-heading">
          <h3>{config.label} Records</h3>
          <span>{loading ? "Loading..." : `${pagination.total} total records`}</span>
        </div>
        <DataTable fields={config.fields} rows={rows} canManage={canManage} onEdit={(record) => setModal({ show: true, record })} onDelete={deleteRecord} />
        <div className="pagination-bar">
          <button className="btn btn-light" disabled={pagination.page <= 1} onClick={() => fetchRows(pagination.page - 1)}>
            <i className="bi bi-chevron-left" />
          </button>
          <span>
            Page {pagination.page} of {pagination.pages}
          </span>
          <button className="btn btn-light" disabled={pagination.page >= pagination.pages} onClick={() => fetchRows(pagination.page + 1)}>
            <i className="bi bi-chevron-right" />
          </button>
        </div>
      </div>

      <RecordModal
        show={modal.show}
        title={config.label}
        fields={config.fields}
        record={modal.record}
        onClose={() => setModal({ show: false, record: null })}
        onSubmit={saveRecord}
      />
    </div>
  );
};

export default ModulePage;
