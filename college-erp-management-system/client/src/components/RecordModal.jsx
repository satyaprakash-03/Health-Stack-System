import { useEffect, useState } from "react";

const RecordModal = ({ show, fields, record, title, onClose, onSubmit }) => {
  const [form, setForm] = useState({});

  useEffect(() => {
    setForm(record || {});
  }, [record, show]);

  if (!show) return null;

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(form);
  };

  return (
    <div className="modal-backdrop-custom">
      <div className="record-modal">
        <div className="modal-titlebar">
          <div>
            <span className="eyebrow">Record Editor</span>
            <h2>{record?._id ? `Edit ${title}` : `Add ${title}`}</h2>
          </div>
          <button className="btn btn-icon" onClick={onClose} aria-label="Close modal">
            <i className="bi bi-x-lg" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="row g-3">
          {fields.map((field) => (
            <div className="col-md-6" key={field}>
              <label className="form-label text-capitalize">{field.replace(/([A-Z])/g, " $1")}</label>
              <input
                className="form-control"
                value={form[field] ?? ""}
                onChange={(event) => setForm({ ...form, [field]: event.target.value })}
                placeholder={`Enter ${field}`}
              />
            </div>
          ))}
          <div className="col-12 d-flex justify-content-end gap-2">
            <button type="button" className="btn btn-light" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Save Record
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RecordModal;
