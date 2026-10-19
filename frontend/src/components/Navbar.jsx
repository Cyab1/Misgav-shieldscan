import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <svg
          width="28"
          height="28"
          viewBox="0 0 32 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect width="32" height="32" rx="4" fill="#1C1C1C" />
          {/* Castle battlements */}
          <rect x="7" y="7" width="4" height="4" fill="white" />
          <rect x="14" y="7" width="4" height="4" fill="white" />
          <rect x="21" y="7" width="4" height="4" fill="white" />
          {/* M shape */}
          <path
            d="M7 11 L7 24 L11 24 L11 16 L16 22 L21 16 L21 24 L25 24 L25 11 L21 11 L16 18 L11 11 Z"
            fill="white"
          />
        </svg>
        <span className="navbar-name">misgav</span>
        <span className="navbar-divider">|</span>
        <span className="navbar-product">ShieldScan</span>
      </Link>
      <span className="navbar-tagline">Website Security Audit</span>
    </nav>
  );
}
