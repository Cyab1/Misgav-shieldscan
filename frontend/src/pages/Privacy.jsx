import { Link } from "react-router-dom";
import "./Privacy.css";

export default function Privacy() {
  return (
    <main className="privacy">
      <div className="privacy-content">
        <div className="privacy-header">
          <Link to="/" className="back-link">
            ← Back to ShieldScan
          </Link>
          <h1>Privacy Policy</h1>
          <p className="privacy-date">misgav · Last updated: October 2026</p>
        </div>
        <section>
          <h2>Who we are</h2>
          <p>
            misgav ShieldScan is operated by <strong>misgav</strong>. Contact us
            at <a href="mailto:hello@misgav.co.za">hello@misgav.co.za</a>.
          </p>
        </section>
        <section>
          <h2>What information we collect</h2>
          <ul>
            <li>
              <strong>URLs you submit</strong> — the website address you scan
            </li>
            <li>
              <strong>Scan results</strong> — the security findings for that URL
            </li>
            <li>
              <strong>IP addresses</strong> — used to enforce our daily scan
              limit
            </li>
            <li>
              <strong>Timestamps</strong> — date and time of each scan
            </li>
          </ul>
        </section>
        <section>
          <h2>How we use your information</h2>
          <ul>
            <li>To perform the security scan you requested</li>
            <li>
              To generate and store your scan report with a shareable link
            </li>
            <li>To enforce the daily scan limit and prevent abuse</li>
          </ul>
        </section>
        <section>
          <h2>POPIA compliance</h2>
          <p>
            misgav is committed to complying with the Protection of Personal
            Information Act (POPIA), Act 4 of 2013. To request access,
            correction, or deletion of your information, contact{" "}
            <a href="mailto:hello@misgav.co.za">hello@misgav.co.za</a>.
          </p>
        </section>
        <section>
          <h2>How long we keep your data</h2>
          <p>
            Scan results are kept for 12 months. IP addresses are kept for 24
            hours. To request deletion contact{" "}
            <a href="mailto:hello@misgav.co.za">hello@misgav.co.za</a>.
          </p>
        </section>
        <section>
          <h2>Contact</h2>
          <p>
            For privacy questions contact misgav at{" "}
            <a href="mailto:hello@misgav.co.za">hello@misgav.co.za</a>.
          </p>
        </section>
      </div>
    </main>
  );
}
