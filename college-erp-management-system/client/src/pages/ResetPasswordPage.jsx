import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../services/api.js";

const ResetPasswordPage = () => {
  const { token } = useParams();
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    await api.patch(`/auth/reset-password/${token}`, { password });
    setMessage("Password reset successfully. You can now sign in.");
  };

  return (
    <div className="auth-page compact-auth">
      <div className="auth-card">
        <h2>Create new password</h2>
        {message && <div className="alert alert-success">{message}</div>}
        <form onSubmit={submit} className="vstack gap-3">
          <input className="form-control" type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="New password" />
          <button className="btn btn-primary">Reset Password</button>
          <Link to="/login">Back to login</Link>
        </form>
      </div>
    </div>
  );
};

export default ResetPasswordPage;
