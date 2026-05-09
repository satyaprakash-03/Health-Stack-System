import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api.js";

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    const { data } = await api.post("/auth/forgot-password", { email });
    setMessage(data.message);
  };

  return (
    <div className="auth-page compact-auth">
      <div className="auth-card">
        <h2>Reset password</h2>
        <p className="text-muted">Enter your ERP account email to receive a reset link.</p>
        {message && <div className="alert alert-info">{message}</div>}
        <form onSubmit={submit} className="vstack gap-3">
          <input className="form-control" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@college.edu" />
          <button className="btn btn-primary">Send Reset Link</button>
          <Link to="/login">Back to login</Link>
        </form>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
