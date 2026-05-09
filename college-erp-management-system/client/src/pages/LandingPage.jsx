import { Link } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle.jsx";

const featureCards = [
  ["bi-shield-lock", "Secure role portals", "Separate dashboards for admin, faculty, and students with JWT-backed access."],
  ["bi-kanban", "Academic operations", "Manage admissions, faculty, departments, courses, subjects, results, and attendance."],
  ["bi-graph-up", "Analytics ready", "Leadership charts, fee reports, attendance trends, and student performance insights."],
  ["bi-chat-dots", "Connected campus", "Notices, internal messages, grievances, events, placements, library, and hostel tools."]
];

const LandingPage = () => (
  <div className="landing-page">
    <nav className="landing-nav">
      <Link className="brand-mark text-decoration-none" to="/">
        <span className="brand-icon">E</span>
        <div>
          <strong>EduSphere ERP</strong>
          <small>Modern University Operations</small>
        </div>
      </Link>
      <div className="d-flex align-items-center gap-2">
        <ThemeToggle />
        <Link className="btn btn-outline-light" to="/login">
          Login
        </Link>
      </div>
    </nav>

    <section className="hero-section">
      <div className="hero-overlay" />
      <div className="hero-content">
        <span className="eyebrow">College ERP Management System</span>
        <h1>EduSphere ERP</h1>
        <p>
          A professional MERN portal for admissions, academics, finance, examinations, communication,
          student services, and institutional analytics.
        </p>
        <div className="d-flex flex-wrap gap-3">
          <Link className="btn btn-primary btn-lg" to="/login">
            Open Dashboard
          </Link>
          <a className="btn btn-light btn-lg" href="#features">
            Explore Features
          </a>
        </div>
        <div className="hero-metrics">
          <div className="hero-metric">
            <strong>22+</strong>
            <span>ERP modules</span>
          </div>
          <div className="hero-metric">
            <strong>3</strong>
            <span>secure role portals</span>
          </div>
          <div className="hero-metric">
            <strong>100%</strong>
            <span>responsive UI</span>
          </div>
          <div className="hero-metric">
            <strong>JWT</strong>
            <span>protected APIs</span>
          </div>
        </div>
      </div>
    </section>

    <section id="features" className="page-band">
      <div className="container">
        <div className="section-heading">
          <span>Full campus suite</span>
          <h2>Built for real university workflows</h2>
        </div>
        <div className="row g-4">
          {featureCards.map(([icon, title, body]) => (
            <div className="col-md-6 col-xl-3" key={title}>
              <div className="feature-card">
                <i className={`bi ${icon}`} />
                <h3>{title}</h3>
                <p>{body}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>

    <section className="page-band muted-band">
      <div className="container">
        <div className="row g-4 align-items-stretch">
          <div className="col-lg-4">
            <div className="testimonial">
              <p>"The ERP gives us one reliable view of academics, fees, and student services."</p>
              <strong>Registrar Office</strong>
            </div>
          </div>
          <div className="col-lg-4">
            <div className="testimonial">
              <p>"Faculty can manage attendance, assignments, notices, and performance from one place."</p>
              <strong>Dean of Academics</strong>
            </div>
          </div>
          <div className="col-lg-4">
            <div className="testimonial">
              <p>"Students get clarity on schedules, results, documents, leaves, and campus updates."</p>
              <strong>Student Council</strong>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section className="page-band contact-band">
      <div className="container">
        <div className="row g-4">
          <div className="col-lg-5">
            <div className="section-heading text-start">
              <span>Contact admissions</span>
              <h2>Request an ERP walkthrough</h2>
              <p>Send a note to the campus technology team for onboarding, integrations, or deployment planning.</p>
            </div>
          </div>
          <div className="col-lg-7">
            <form className="contact-form">
              <div className="row g-3">
                <div className="col-md-6">
                  <input className="form-control" placeholder="Name" />
                </div>
                <div className="col-md-6">
                  <input className="form-control" placeholder="Email" type="email" />
                </div>
                <div className="col-12">
                  <textarea className="form-control" rows="4" placeholder="Message" />
                </div>
                <div className="col-12">
                  <button className="btn btn-primary" type="button">
                    Submit Enquiry
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
);

export default LandingPage;
