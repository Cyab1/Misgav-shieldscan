import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
          <rect width="28" height="28" rx="4" fill="#1C1C1C" />
          <text
            x="14"
            y="20"
            fontFamily="Arial"
            fontSize="14"
            fontWeight="bold"
            fill="white"
            textAnchor="middle"
          >
            M
          </text>
        </svg>
        <span className="navbar-name">misgav</span>
        <span className="navbar-divider">|</span>
        <span className="navbar-product">ShieldScan</span>
      </Link>
      <span className="navbar-tagline">Website Security Audit</span>
    </nav>
  );
}
