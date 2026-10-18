import { Link } from "react-router-dom";
import "./Privacy.css";

export default function Terms() {
  return (
    <main className="privacy">
      <div className="privacy-content">
        <div className="privacy-header">
          <Link to="/" className="back-link">
            ← Back to ShieldScan
          </Link>
          <h1>Terms of Use</h1>
          <p className="privacy-date">misgav · Last updated: October 2026</p>
        </div>
        <section>
          <h2>1. About misgav ShieldScan</h2>
          <p>
            misgav ShieldScan is a free website security audit tool operated by
            misgav. By using ShieldScan, you agree to these Terms of Use.
          </p>
        </section>
        <section>
          <h2>2. Acceptable use</h2>
          <ul>
            <li>
              You may only scan websites you own or have explicit permission to
              scan
            </li>
            <li>
              You will not use ShieldScan for any unlawful or malicious purpose
            </li>
            <li>
              You will not attempt to circumvent the daily scan limit or abuse
              the service
            </li>
          </ul>
        </section>
        <section>
          <h2>3. Nature of the service</h2>
          <p>
            ShieldScan performs automated, non-intrusive checks on publicly
            accessible website information. It does not perform penetration
            testing or access any restricted systems. Scans may appear in the
            access logs of the scanned website.
          </p>
        </section>
        <section>
          <h2>4. No warranty</h2>
          <p>
            ShieldScan is provided "as is" without any warranty. A passing grade
            does not mean your website is fully secure. Results are a starting
            point for security awareness, not a substitute for a professional
            security audit.
          </p>
        </section>
        <section>
          <h2>5. Limitation of liability</h2>
          <p>
            misgav shall not be liable for any damages arising from your use of
            ShieldScan, including decisions made based on scan results.
          </p>
        </section>
        <section>
          <h2>6. Rate limiting</h2>
          <p>
            ShieldScan is free and limited to 5 scans per IP address per day.
            Contact <a href="mailto:hello@misgav.co.za">hello@misgav.co.za</a>{" "}
            for unlimited access.
          </p>
        </section>
        <section>
          <h2>7. Governing law</h2>
          <p>
            These terms are governed by the laws of the Republic of South
            Africa.
          </p>
        </section>
        <section>
          <h2>8. Contact</h2>
          <p>
            For questions contact misgav at{" "}
            <a href="mailto:hello@misgav.co.za">hello@misgav.co.za</a>.
          </p>
        </section>
      </div>
    </main>
  );
}
