const StatCard = ({ icon, label, value, helper, tone = "primary" }) => (
  <div className={`stat-card tone-${tone}`}>
    <div className="stat-icon">
      <i className={`bi ${icon}`} />
    </div>
    <div>
      <p>{label}</p>
      <h3>{value}</h3>
      <small>{helper}</small>
    </div>
  </div>
);

export default StatCard;
