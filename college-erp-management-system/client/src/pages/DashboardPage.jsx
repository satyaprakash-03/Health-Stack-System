import { useEffect, useState } from "react";
import { Bar, Doughnut, Line } from "react-chartjs-2";
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  ArcElement,
  PointElement,
  Tooltip
} from "chart.js";
import StatCard from "../components/StatCard.jsx";
import api from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Tooltip, Legend);

const DashboardPage = () => {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    api.get("/dashboard/summary").then(({ data }) => setSummary(data));
  }, []);

  const counts = summary?.counts || {};
  const stats = [
    ["bi-mortarboard", "Students", counts.students || 0, "+12 admitted this month", "primary"],
    ["bi-person-workspace", "Faculty", counts.faculty || 0, "87% workload balanced", "success"],
    ["bi-cash-coin", "Fees Pending", `₹${((summary?.finance?.pending || 0) / 100000).toFixed(1)}L`, "Collections follow-up", "warning"],
    ["bi-briefcase", "Placements", counts.placements || 0, "Active company drives", "info"]
  ];

  const trendData = {
    labels: summary?.trend?.map((item) => item.month) || [],
    datasets: [
      {
        label: "Students",
        data: summary?.trend?.map((item) => item.students) || [],
        borderColor: "#2563eb",
        backgroundColor: "rgba(37, 99, 235, .15)",
        tension: 0.4
      },
      {
        label: "Attendance %",
        data: summary?.trend?.map((item) => item.attendance) || [],
        borderColor: "#10b981",
        backgroundColor: "rgba(16, 185, 129, .15)",
        tension: 0.4
      }
    ]
  };

  const performanceData = {
    labels: summary?.performance?.map((item) => item.label) || [],
    datasets: [
      {
        label: "Score",
        data: summary?.performance?.map((item) => item.value) || [],
        backgroundColor: ["#2563eb", "#10b981", "#f59e0b", "#14b8a6"]
      }
    ]
  };

  return (
    <div className="dashboard-page">
      <div className="welcome-panel">
        <div>
          <span className="eyebrow">Welcome back</span>
          <h2>{user?.name}</h2>
          <p>Monitor operations, review campus trends, and move quickly across the ERP modules.</p>
        </div>
        <div className="quick-actions">
          <button className="btn btn-light">
            <i className="bi bi-download me-2" />
            Export Report
          </button>
          <button className="btn btn-primary">
            <i className="bi bi-plus-circle me-2" />
            New Record
          </button>
        </div>
      </div>

      <div className="row g-3 mb-4">
        {stats.map(([icon, label, value, helper, tone]) => (
          <div className="col-md-6 col-xl-3" key={label}>
            <StatCard icon={icon} label={label} value={value} helper={helper} tone={tone} />
          </div>
        ))}
      </div>

      <div className="row g-4">
        <div className="col-xl-8">
          <div className="panel">
            <div className="panel-heading">
              <h3>Enrollment & Attendance Trend</h3>
              <span>Monthly campus health</span>
            </div>
            <Line data={trendData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>
        <div className="col-xl-4">
          <div className="panel">
            <div className="panel-heading">
              <h3>Performance Mix</h3>
              <span>Academic analytics</span>
            </div>
            <Doughnut data={performanceData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>
        <div className="col-xl-7">
          <div className="panel">
            <div className="panel-heading">
              <h3>Finance Snapshot</h3>
              <span>Collected vs pending</span>
            </div>
            <Bar
              data={{
                labels: ["Collected", "Pending", "Scholarship"],
                datasets: [{ label: "Amount", data: Object.values(summary?.finance || {}), backgroundColor: ["#10b981", "#f59e0b", "#2563eb"] }]
              }}
              options={{ responsive: true, maintainAspectRatio: false }}
            />
          </div>
        </div>
        <div className="col-xl-5">
          <div className="panel">
            <div className="panel-heading">
              <h3>Upcoming</h3>
              <span>Calendar highlights</span>
            </div>
            <div className="timeline-list">
              {(summary?.upcoming || []).map((item) => (
                <div className="timeline-item" key={item.title}>
                  <span>{item.type}</span>
                  <div>
                    <strong>{item.title}</strong>
                    <small>{new Date(item.date).toLocaleDateString()}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
