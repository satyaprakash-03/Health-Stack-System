const getBadgeTone = (value) => {
  const normalized = String(value).toLowerCase();
  if (["active", "paid", "present", "approved", "verified", "published", "completed", "open", "low", "yes"].includes(normalized)) return "success";
  if (["pending", "partial", "scheduled", "in review", "medium", "draft"].includes(normalized)) return "warning";
  if (["absent", "overdue", "rejected", "cancelled", "suspended", "high", "no"].includes(normalized)) return "danger";
  return "info";
};

const formatValue = (field, value) => {
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (!value) return "-";
  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}/.test(value)) return new Date(value).toLocaleDateString();
  if (/status|priority|risk|published|read/i.test(field)) {
    return (
      <span className={`status-badge ${getBadgeTone(value)}`}>
        <i className="bi bi-circle-fill" />
        {String(value)}
      </span>
    );
  }
  return value;
};

const DataTable = ({ fields, rows, onEdit, onDelete, canManage }) => (
  <div className="table-responsive erp-table-wrap">
    <table className="table align-middle">
      <thead>
        <tr>
          {fields.map((field) => (
            <th key={field}>{field.replace(/([A-Z])/g, " $1")}</th>
          ))}
          {canManage && <th className="text-end">Actions</th>}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row._id}>
            {fields.map((field) => (
              <td key={field}>{formatValue(field, row[field])}</td>
            ))}
            {canManage && (
              <td className="text-end">
                <button className="btn btn-sm btn-light me-2" onClick={() => onEdit(row)} aria-label="Edit record">
                  <i className="bi bi-pencil" />
                </button>
                <button className="btn btn-sm btn-outline-danger" onClick={() => onDelete(row._id)} aria-label="Delete record">
                  <i className="bi bi-trash" />
                </button>
              </td>
            )}
          </tr>
        ))}
        {!rows.length && (
          <tr>
            <td colSpan={fields.length + 1} className="text-center py-5 text-muted">
              No records found.
            </td>
          </tr>
        )}
      </tbody>
    </table>
  </div>
);

export default DataTable;
