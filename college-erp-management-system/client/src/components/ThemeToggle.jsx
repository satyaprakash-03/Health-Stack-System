import { useAuth } from "../context/AuthContext.jsx";

const ThemeToggle = () => {
  const { theme, toggleTheme } = useAuth();

  return (
    <button className="btn btn-icon" onClick={toggleTheme} aria-label="Toggle color theme">
      <i className={`bi ${theme === "light" ? "bi-moon-stars" : "bi-brightness-high"}`} />
    </button>
  );
};

export default ThemeToggle;
