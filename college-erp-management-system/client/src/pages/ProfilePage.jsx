import { useState } from "react";
import api from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

const ProfilePage = () => {
  const { user } = useAuth();
  const [form, setForm] = useState(user || {});
  const [message, setMessage] = useState("");

  const save = async (event) => {
    event.preventDefault();
    const { data } = await api.patch("/auth/profile", form);
    try {
      localStorage.setItem("erpUser", JSON.stringify(data.user));
    } catch {
      // Keep the saved profile in the API even if local storage is unavailable.
    }
    setMessage("Profile updated successfully. Refresh to sync the topbar.");
  };

  return (
    <div className="panel profile-panel">
      <div className="panel-heading">
        <h3>Profile Management</h3>
        <span>Keep account and contact details current</span>
      </div>
      {message && <div className="alert alert-success">{message}</div>}
      <form onSubmit={save} className="row g-3">
        {["name", "email", "phone", "department"].map((field) => (
          <div className="col-md-6" key={field}>
            <label className="form-label text-capitalize">{field}</label>
            <input
              className="form-control"
              disabled={field === "email"}
              value={form[field] || ""}
              onChange={(event) => setForm({ ...form, [field]: event.target.value })}
            />
          </div>
        ))}
        <div className="col-12">
          <button className="btn btn-primary">Save Profile</button>
        </div>
      </form>
    </div>
  );
};

export default ProfilePage;
