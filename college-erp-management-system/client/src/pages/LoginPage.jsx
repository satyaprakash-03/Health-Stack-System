import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

const demoAccounts = [
  ["Admin", "admin@collegeerp.com", "Admin@12345"],
  ["Faculty", "faculty@collegeerp.com", "Faculty@12345"],
  ["Student", "student@collegeerp.com", "Student@12345"]
];

const LoginPage = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "admin@collegeerp.com", password: "Admin@12345" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/dashboard" replace />;

  const submit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(form.email, form.password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.message || "Login failed. Check API and credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-visual">
        <Link className="brand-mark text-decoration-none" to="/">
          <span className="brand-icon">E</span>
          <div>
            <strong>EduSphere ERP</strong>
            <small>Campus command center</small>
          </div>
        </Link>
        <h1>One secure portal for the whole institution.</h1>
        <p>Role-based dashboards for administrators, faculty, and students with production-oriented MERN architecture.</p>
      </div>
      <div className="auth-card">
        <h2>Sign in</h2>
        <p className="text-muted">Use one of the seeded demo accounts after running the seed script.</p>
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={submit} className="vstack gap-3">
          <div>
            <label className="form-label">Email</label>
            <input className="form-control" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
          </div>
          <div>
            <label className="form-label">Password</label>
            <input className="form-control" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
          </div>
          <button className="btn btn-primary btn-lg" disabled={loading}>
            {loading ? "Signing in..." : "Login Securely"}
          </button>
          <Link to="/forgot-password">Forgot password?</Link>
        </form>
        <div className="demo-grid">
          {demoAccounts.map(([role, email, password]) => (
            <button key={role} className="demo-account" onClick={() => setForm({ email, password })}>
              <strong>{role}</strong>
              <small>{email}</small>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
