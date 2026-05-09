import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div className="app-error-screen">
          <div className="app-error-card">
            <span className="brand-icon">E</span>
            <h1>EduSphere could not load</h1>
            <p>{this.state.error.message || "A browser runtime error stopped the app from rendering."}</p>
            <button className="btn btn-primary" onClick={() => window.location.reload()}>
              Reload Portal
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
