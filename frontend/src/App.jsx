import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  BarChart3,
  FileText,
  LayoutDashboard,
  MessageSquare,
  Upload,
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  getCompanyProfile,
  getCompanyReport,
  getCompanyTrends,
  getTransactions,
  uploadTransactions,
  askCompanyAssistant,
} from "./services/api";

import "./index.css";

function App() {
  const [profile, setProfile] = useState(null);
  const [trends, setTrends] = useState([]);
  const [report, setReport] = useState(null);
  const [transactions, setTransactions] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activePage, setActivePage] = useState("dashboard");
  const [chatMessages, setChatMessages] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [companies, setCompanies] = useState([]);

  useEffect(() => {
    async function loadCompanies() {
      try {
        const response = await getTransactions("");

        const transactions = response.transactions || [];

        const uniqueCompanies = [
          ...new Set(
            transactions
              .map((transaction) => transaction.company_id)
              .filter(Boolean),
          ),
        ];

        setCompanies(uniqueCompanies);

        if (uniqueCompanies.length > 0) {
          setCompanyId((current) =>
            current && uniqueCompanies.includes(current)
              ? current
              : uniqueCompanies[0],
          );
        }
      } catch (error) {
        console.error("Failed to load companies:", error);
      }
    }

    loadCompanies();
  }, []);

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [profileData, trendsData, reportData, transactionsData] =
        await Promise.all([
          getCompanyProfile(companyId),
          getCompanyTrends(companyId),
          getCompanyReport(companyId),
          getTransactions(companyId),
        ]);

      setProfile(profileData);
      setTrends(trendsData);
      setReport(reportData);
      setTransactions(transactionsData.transactions || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!companyId) {
      setLoading(false);
      return;
    }
    loadDashboard();
  }, [companyId]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">G</div>

          <div>
            <h1>GreenLedger</h1>
            <span>ESG Intelligence</span>
          </div>
        </div>

        <nav className="navigation">
          <button
            className={`nav-item ${activePage === "dashboard" ? "active" : ""}`}
            onClick={() => setActivePage("dashboard")}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </button>

          <button
            className={`nav-item ${activePage === "analytics" ? "active" : ""}`}
            onClick={() => setActivePage("analytics")}
          >
            <BarChart3 size={18} />
            Analytics
          </button>

          <button
            className={`nav-item ${activePage === "reports" ? "active" : ""}`}
            onClick={() => setActivePage("reports")}
          >
            <FileText size={18} />
            Reports
          </button>

          <button
            className={`nav-item ${activePage === "assistant" ? "active" : ""}`}
            onClick={() => setActivePage("assistant")}
          >
            <MessageSquare size={18} />
            ESG Assistant
          </button>

          <button
            className={`nav-item ${activePage === "upload" ? "active" : ""}`}
            onClick={() => setActivePage("upload")}
          >
            <Upload size={18} />
            Upload Data
          </button>
        </nav>

        <div className="sidebar-footer">
          <span>Prototype</span>
          <small>ESG Intelligence Platform</small>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">
              {activePage === "upload"
                ? "DATA INGESTION"
                : activePage === "assistant"
                  ? "AI INTELLIGENCE"
                  : activePage === "analytics"
                    ? "PERFORMANCE INTELLIGENCE"
                    : activePage === "reports"
                      ? "ESG REPORTING"
                      : "COMPANY OVERVIEW"}
            </p>
            <h2>
              {activePage === "upload"
                ? "Upload Transaction Data"
                : activePage === "assistant"
                  ? "ESG Assistant"
                  : activePage === "analytics"
                    ? "ESG Analytics"
                    : activePage === "reports"
                      ? "ESG Reports"
                      : "ESG Dashboard"}
            </h2>
          </div>

          <div className="company-selector">
            <span>Company</span>

            {companies.length > 0 ? (
              <select
                value={companyId}
                onChange={(event) => {
                  setCompanyId(event.target.value);
                  setChatMessages([]);
                }}
              >
                {companies.map((company) => (
                  <option key={company} value={company}>
                    {company}
                  </option>
                ))}
              </select>
            ) : (
              <strong>No company data</strong>
            )}
          </div>
        </header>

        {loading && activePage !== "upload" && (
          <div className="state-card">Loading ESG intelligence...</div>
        )}

        {error && (
          <div className="state-card error-state">
            <strong>Unable to load dashboard</strong>
            <p>{error}</p>
          </div>
        )}

        {!error &&
          (activePage === "upload" ? (
            <UploadPage
              onUploadSuccess={(uploadResult) => {
                const uploadedCompanies = Object.keys(
                  uploadResult?.indexed_companies || {},
                );

                if (uploadedCompanies.length > 0) {
                  setCompanies((current) => [
                    ...new Set([...current, ...uploadedCompanies]),
                  ]);

                  setCompanyId(uploadedCompanies[0]);
                }

                setChatMessages([]);
                setActivePage("dashboard");
              }}
            />
          ) : !loading && profile && activePage === "assistant" ? (
            <AssistantPage
              companyId={companyId}
              messages={chatMessages}
              setMessages={setChatMessages}
            />
          ) : !loading && profile && activePage === "analytics" ? (
            <AnalyticsPage
              companyId={companyId}
              profile={profile}
              trends={trends}
              report={report}
              transactions={transactions}
            />
          ) : !loading && profile && activePage === "reports" ? (
            <ReportsPage companyId={companyId} report={report} />
          ) : !loading && profile ? (
            <>
              <section className="score-grid">
                <ScoreCard
                  title="Overall ESG"
                  score={profile.overall_score}
                  primary
                />

                <ScoreCard
                  title="Environmental"
                  score={profile.environmental_score}
                />

                <ScoreCard title="Social" score={profile.social_score} />

                <ScoreCard
                  title="Governance"
                  score={profile.governance_score}
                />
              </section>

              <section className="metric-grid">
                <MetricCard
                  label="Transactions"
                  value={profile.transaction_count}
                />

                <MetricCard
                  label="Transaction Volume"
                  value={`₹${Number(profile.total_volume).toLocaleString(
                    "en-IN",
                  )}`}
                />

                <MetricCard label="Anomalies" value={profile.anomaly_count} />

                <MetricCard
                  label="High Risk"
                  value={profile.high_risk_anomalies}
                />
              </section>

              <section className="content-grid">
                <div className="panel">
                  <div className="panel-header">
                    <div>
                      <p className="eyebrow">ESG IMPACT</p>
                      <h3>Transaction Impact</h3>
                    </div>
                  </div>

                  <div className="impact-list">
                    <ImpactRow
                      label="Positive"
                      value={profile.impact_counts.POSITIVE}
                    />

                    <ImpactRow
                      label="Negative"
                      value={profile.impact_counts.NEGATIVE}
                    />

                    <ImpactRow
                      label="Neutral"
                      value={profile.impact_counts.NEUTRAL}
                    />
                  </div>
                </div>

                <div className="panel">
                  <div className="panel-header">
                    <div>
                      <p className="eyebrow">DATASET</p>
                      <h3>Recent Transactions</h3>
                    </div>
                  </div>

                  <div className="transaction-preview">
                    {transactions.slice(0, 5).map((transaction) => (
                      <div
                        className="transaction-row"
                        key={transaction.transaction_id}
                      >
                        <div>
                          <strong>{transaction.transaction_id}</strong>
                          <span>{transaction.description}</span>
                        </div>

                        <strong>
                          ₹{Number(transaction.amount).toLocaleString("en-IN")}
                        </strong>
                      </div>
                    ))}
                  </div>
                </div>
              </section>

              <section className="dashboard-grid">
                <div className="panel trend-panel">
                  <div className="panel-header">
                    <div>
                      <p className="eyebrow">PERFORMANCE</p>
                      <h3>ESG Trend</h3>
                    </div>
                  </div>

                  <div className="chart-container">
                    {trends.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={trends}>
                          <CartesianGrid strokeDasharray="3 3" />

                          <XAxis dataKey="period" tick={{ fontSize: 11 }} />

                          <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />

                          <Tooltip />

                          <Line
                            type="monotone"
                            dataKey="environmental_score"
                            name="Environmental"
                            strokeWidth={2}
                            dot={{ r: 3 }}
                          />

                          <Line
                            type="monotone"
                            dataKey="social_score"
                            name="Social"
                            strokeWidth={2}
                            dot={{ r: 3 }}
                          />

                          <Line
                            type="monotone"
                            dataKey="governance_score"
                            name="Governance"
                            strokeWidth={2}
                            dot={{ r: 3 }}
                          />

                          <Line
                            type="monotone"
                            dataKey="overall_score"
                            name="Overall"
                            strokeWidth={3}
                            dot={{ r: 4 }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="empty-state">
                        No trend data available.
                      </div>
                    )}
                  </div>
                </div>

                <div className="panel anomaly-panel">
                  <div className="panel-header">
                    <div>
                      <p className="eyebrow">RISK MONITORING</p>
                      <h3>Anomalies</h3>
                    </div>

                    <span className="panel-count">
                      {report?.anomalies?.length || 0}
                    </span>
                  </div>

                  <div className="anomaly-list">
                    {report?.anomalies?.length > 0 ? (
                      report.anomalies.map((anomaly) => (
                        <div
                          className="anomaly-item"
                          key={anomaly.transaction_id}
                        >
                          <div>
                            <strong>{anomaly.transaction_id}</strong>

                            {anomaly.reasons.map((reason) => (
                              <p key={reason}>{reason}</p>
                            ))}
                          </div>

                          <span className="risk-badge">{anomaly.severity}</span>
                        </div>
                      ))
                    ) : (
                      <div className="empty-state">No anomalies detected.</div>
                    )}
                  </div>
                </div>
              </section>

              <section className="panel report-panel">
                <div className="panel-header">
                  <div>
                    <p className="eyebrow">INTELLIGENCE</p>
                    <h3>Key ESG Signals</h3>
                  </div>

                  <span className="panel-count">
                    {report?.key_signals?.length || 0}
                  </span>
                </div>

                <div className="signal-list">
                  {report?.key_signals?.map((signal) => (
                    <div className="signal-item" key={signal.transaction_id}>
                      <div>
                        <strong>{signal.signal}</strong>
                        <p>{signal.reason}</p>
                      </div>

                      <span>{signal.impact}</span>
                    </div>
                  ))}
                </div>
              </section>
            </>
          ) : activePage === "dashboard" ? (
            <EmptyDashboard onUpload={() => setActivePage("upload")} />
          ) : null)}
      </main>
    </div>
  );
}

function EmptyDashboard({ onUpload }) {
  return (
    <div className="empty-dashboard">
      <div className="empty-dashboard-card">
        <div className="empty-dashboard-icon">G</div>

        <p className="eyebrow">GET STARTED</p>

        <h3>No transaction data yet</h3>

        <p className="empty-dashboard-description">
          Upload a transaction dataset to generate ESG intelligence for your
          company, including environmental, social, and governance scores,
          anomaly detection, trends, and evidence-backed insights.
        </p>

        <div className="empty-dashboard-features">
          <div>
            <strong>ESG Scoring</strong>
            <span>Environmental, social, and governance analysis</span>
          </div>

          <div>
            <strong>Risk Detection</strong>
            <span>Identify high-risk ESG transaction signals</span>
          </div>

          <div>
            <strong>AI Assistant</strong>
            <span>Ask questions using your transaction evidence</span>
          </div>
        </div>

        <button className="primary-button" onClick={onUpload}>
          Upload Transaction Data
        </button>

        <span className="empty-dashboard-hint">CSV files only</span>
      </div>
    </div>
  );
}

function AnalyticsPage({ companyId, profile, trends, report, transactions }) {
  const monthlyVolume = {};

  transactions.forEach((transaction) => {
    const month = transaction.timestamp?.slice(0, 7);

    if (!month) {
      return;
    }

    monthlyVolume[month] =
      (monthlyVolume[month] || 0) + Number(transaction.amount || 0);
  });

  const volumeData = Object.entries(monthlyVolume)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([period, volume]) => ({
      period,
      volume,
    }));

  const latestTrend = trends.length > 0 ? trends[trends.length - 1] : null;

  return (
    <div className="analytics-page">
      <div className="analytics-intro">
        <p>
          Explore ESG performance, transaction activity, and risk patterns for{" "}
          {companyId}.
        </p>
      </div>
      <section className="analytics-metric-grid">
        <MetricCard
          label="Overall ESG"
          value={Number(profile.overall_score).toFixed(1)}
        />

        <MetricCard
          label="Environmental"
          value={Number(profile.environmental_score).toFixed(1)}
        />

        <MetricCard
          label="Social"
          value={Number(profile.social_score).toFixed(1)}
        />

        <MetricCard
          label="Governance"
          value={Number(profile.governance_score).toFixed(1)}
        />
      </section>

      <section className="analytics-grid">
        <div className="panel analytics-chart-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">ESG PERFORMANCE</p>
              <h3>Score Trend</h3>
            </div>
          </div>

          <div className="analytics-chart-container">
            {trends.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trends}>
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis dataKey="period" tick={{ fontSize: 11 }} />

                  <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="environmental_score"
                    name="Environmental"
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />

                  <Line
                    type="monotone"
                    dataKey="social_score"
                    name="Social"
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />

                  <Line
                    type="monotone"
                    dataKey="governance_score"
                    name="Governance"
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />

                  <Line
                    type="monotone"
                    dataKey="overall_score"
                    name="Overall"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">No ESG trend data available.</div>
            )}
          </div>
        </div>

        <div className="panel analytics-chart-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">TRANSACTION ACTIVITY</p>
              <h3>Monthly Transaction Volume</h3>
            </div>
          </div>

          <div className="analytics-chart-container">
            {volumeData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={volumeData}>
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis dataKey="period" tick={{ fontSize: 11 }} />

                  <YAxis
                    tick={{ fontSize: 11 }}
                    tickFormatter={(value) =>
                      `₹${Number(value).toLocaleString("en-IN")}`
                    }
                  />

                  <Tooltip
                    formatter={(value) =>
                      `₹${Number(value).toLocaleString("en-IN")}`
                    }
                  />

                  <Line
                    type="monotone"
                    dataKey="volume"
                    name="Transaction Volume"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">
                No transaction activity available.
              </div>
            )}
          </div>
        </div>
      </section>

      <section className="analytics-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">IMPACT DISTRIBUTION</p>
              <h3>Transaction Impact</h3>
            </div>
          </div>

          <div className="analytics-breakdown">
            <div className="analytics-breakdown-row">
              <span>Positive</span>
              <strong>{profile.impact_counts.POSITIVE}</strong>
            </div>

            <div className="analytics-breakdown-row">
              <span>Negative</span>
              <strong>{profile.impact_counts.NEGATIVE}</strong>
            </div>

            <div className="analytics-breakdown-row">
              <span>Neutral</span>
              <strong>{profile.impact_counts.NEUTRAL}</strong>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">RISK MONITORING</p>
              <h3>Anomaly Overview</h3>
            </div>
          </div>

          <div className="analytics-breakdown">
            <div className="analytics-breakdown-row">
              <span>Total anomalies</span>
              <strong>{profile.anomaly_count}</strong>
            </div>

            <div className="analytics-breakdown-row">
              <span>High-risk anomalies</span>
              <strong>{profile.high_risk_anomalies}</strong>
            </div>

            <div className="analytics-breakdown-row">
              <span>Transactions analyzed</span>
              <strong>{profile.transaction_count}</strong>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">LATEST PERIOD</p>
              <h3>Current ESG Position</h3>
            </div>
          </div>

          {latestTrend ? (
            <div className="analytics-breakdown">
              <div className="analytics-breakdown-row">
                <span>Period</span>
                <strong>{latestTrend.period}</strong>
              </div>

              <div className="analytics-breakdown-row">
                <span>Overall ESG</span>
                <strong>{Number(latestTrend.overall_score).toFixed(1)}</strong>
              </div>

              <div className="analytics-breakdown-row">
                <span>Transactions</span>
                <strong>{latestTrend.transaction_count}</strong>
              </div>
            </div>
          ) : (
            <div className="empty-state">No recent period available.</div>
          )}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">ESG SIGNALS</p>
            <h3>Signals Detected</h3>
          </div>

          <span className="panel-count">
            {report?.key_signals?.length || 0}
          </span>
        </div>

        <div className="signal-list">
          {report?.key_signals?.length > 0 ? (
            report.key_signals.map((signal, index) => (
              <div
                className="signal-item"
                key={`${signal.transaction_id}-${signal.signal}-${index}`}
              >
                <div>
                  <strong>{signal.signal}</strong>
                  <p>
                    {signal.transaction_id} — {signal.reason}
                  </p>
                </div>

                <span>{signal.impact}</span>
              </div>
            ))
          ) : (
            <div className="empty-state">No ESG signals detected.</div>
          )}
        </div>
      </section>
    </div>
  );
}

function ReportsPage({ companyId, report }) {
  if (!report) {
    return (
      <div className="state-card">
        No ESG report is available for {companyId}.
      </div>
    );
  }

  const summary = report.summary || {};
  const scores = report.scores || {};
  const impactCounts = report.impact_counts || {};
  const signals = report.key_signals || [];
  const anomalies = report.anomalies || [];
  const recommendations = report.recommendations || [];
  const trends = report.trends || [];

  return (
    <div className="reports-page">
      <div className="report-header">
        <div>
          <p className="eyebrow">ESG REPORTING</p>

          <h2>ESG Report</h2>

          <p>
            Executive ESG intelligence report for {companyId}, generated from
            transaction-level analysis.
          </p>
        </div>

        <div className="report-company">
          <span>Company</span>
          <strong>{companyId}</strong>
        </div>
      </div>

      <section className="report-summary-grid">
        <div className="report-score-card primary-report-score">
          <span>Overall ESG</span>
          <strong>{Number(summary.overall_score ?? 0).toFixed(1)}</strong>
          <small>out of 100</small>
        </div>

        <div className="report-stat-card">
          <span>Transactions</span>
          <strong>{summary.transaction_count ?? 0}</strong>
        </div>

        <div className="report-stat-card">
          <span>Transaction Volume</span>
          <strong>
            ₹{Number(summary.total_volume ?? 0).toLocaleString("en-IN")}
          </strong>
        </div>

        <div className="report-stat-card">
          <span>Anomalies</span>
          <strong>{anomalies.length}</strong>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">ESG PERFORMANCE</p>
            <h3>Environmental, Social & Governance Scores</h3>
          </div>
        </div>

        <div className="report-score-grid">
          <div className="report-dimension">
            <span>Environmental</span>
            <strong>{Number(scores.environmental ?? 0).toFixed(1)}</strong>
            <div className="score-bar">
              <div
                className="score-bar-fill"
                style={{
                  width: `${Math.min(
                    100,
                    Math.max(0, Number(scores.environmental ?? 0)),
                  )}%`,
                }}
              />
            </div>
          </div>

          <div className="report-dimension">
            <span>Social</span>
            <strong>{Number(scores.social ?? 0).toFixed(1)}</strong>
            <div className="score-bar">
              <div
                className="score-bar-fill"
                style={{
                  width: `${Math.min(
                    100,
                    Math.max(0, Number(scores.social ?? 0)),
                  )}%`,
                }}
              />
            </div>
          </div>

          <div className="report-dimension">
            <span>Governance</span>
            <strong>{Number(scores.governance ?? 0).toFixed(1)}</strong>
            <div className="score-bar">
              <div
                className="score-bar-fill"
                style={{
                  width: `${Math.min(
                    100,
                    Math.max(0, Number(scores.governance ?? 0)),
                  )}%`,
                }}
              />
            </div>
          </div>
        </div>
      </section>

      <section className="report-two-column">
        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">TRANSACTION IMPACT</p>
              <h3>Impact Distribution</h3>
            </div>
          </div>

          <div className="report-list">
            <div className="report-list-row">
              <span>Positive</span>
              <strong>{impactCounts.POSITIVE ?? 0}</strong>
            </div>

            <div className="report-list-row">
              <span>Negative</span>
              <strong>{impactCounts.NEGATIVE ?? 0}</strong>
            </div>

            <div className="report-list-row">
              <span>Neutral</span>
              <strong>{impactCounts.NEUTRAL ?? 0}</strong>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">ESG TREND</p>
              <h3>Recent Performance</h3>
            </div>
          </div>

          <div className="report-list">
            {trends.length > 0 ? (
              trends.slice(-5).map((trend) => (
                <div className="report-list-row" key={trend.period}>
                  <span>{trend.period}</span>

                  <strong>{Number(trend.overall_score).toFixed(1)}</strong>
                </div>
              ))
            ) : (
              <div className="empty-state">No trend data available.</div>
            )}
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">KEY SIGNALS</p>
            <h3>ESG Signals Identified</h3>
          </div>

          <span className="panel-count">{signals.length}</span>
        </div>

        {signals.length > 0 ? (
          <div className="report-signal-list">
            {signals.map((signal, index) => (
              <div
                className="report-signal"
                key={`${signal.transaction_id}-${signal.signal}-${index}`}
              >
                <div>
                  <strong>{signal.signal}</strong>

                  <p>
                    {signal.transaction_id} — {signal.reason}
                  </p>
                </div>

                <span
                  className={`report-impact ${
                    signal.impact === "NEGATIVE"
                      ? "negative"
                      : signal.impact === "POSITIVE"
                        ? "positive"
                        : ""
                  }`}
                >
                  {signal.impact}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">No ESG signals were identified.</div>
        )}
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">ANOMALIES</p>
            <h3>Transactions Requiring Attention</h3>
          </div>

          <span className="panel-count">{anomalies.length}</span>
        </div>

        {anomalies.length > 0 ? (
          <div className="report-anomaly-list">
            {anomalies.map((anomaly) => (
              <div className="report-anomaly" key={anomaly.transaction_id}>
                <div>
                  <strong>{anomaly.transaction_id}</strong>

                  <p>{anomaly.reasons?.join(" ") || "ESG anomaly detected."}</p>
                </div>

                <span className="anomaly-severity">{anomaly.severity}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">No anomalies detected.</div>
        )}
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">RECOMMENDATIONS</p>
            <h3>Suggested Actions</h3>
          </div>

          <span className="panel-count">{recommendations.length}</span>
        </div>

        {recommendations.length > 0 ? (
          <div className="recommendation-list">
            {recommendations.map((recommendation, index) => (
              <div
                className="recommendation-item"
                key={`${recommendation}-${index}`}
              >
                <span>{index + 1}</span>
                <p>{recommendation}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">No recommendations are available.</div>
        )}
      </section>

      <div className="report-disclaimer">
        <strong>Prototype analysis</strong>
        <p>
          GreenLedger's ESG scores and transaction signals are prototype
          analytics derived from the uploaded transaction data. They are not
          regulatory, investment, accounting, or professional ESG ratings.
        </p>
      </div>
    </div>
  );
}

function ScoreCard({ title, score, primary = false }) {
  return (
    <div className={`score-card ${primary ? "score-card-primary" : ""}`}>
      <span>{title}</span>

      <strong>{Number(score).toFixed(1)}</strong>

      <small>out of 100</small>
    </div>
  );
}

function MetricCard({ label, value }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ImpactRow({ label, value }) {
  return (
    <div className="impact-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function UploadPage({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setError("");
    setResult(null);

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setFile(null);
      setError("Please select a CSV file.");
      return;
    }

    setFile(selectedFile);
  }

  async function handleUpload() {
    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    try {
      setUploading(true);
      setError("");
      setResult(null);

      const response = await uploadTransactions(file);

      setResult(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="upload-page">
      <div className="upload-intro">
        <p className="eyebrow">DATA INGESTION</p>

        <h2>Upload Transaction Data</h2>

        <p>
          Upload a CSV dataset to generate ESG intelligence, detect anomalies,
          and update the company report.
        </p>
      </div>

      <label className="upload-zone">
        <input type="file" accept=".csv,text/csv" onChange={handleFileChange} />

        <Upload size={30} />

        <strong>{file ? file.name : "Choose a CSV file"}</strong>

        <span>
          {file
            ? `${(file.size / 1024).toFixed(1)} KB selected`
            : "CSV files only"}
        </span>
      </label>

      {error && <div className="upload-message upload-error">{error}</div>}

      {result && (
        <div className="upload-success">
          <div>
            <strong>Upload successful</strong>

            <p>
              {result.transaction_count} transactions processed successfully.
            </p>
          </div>

          <div className="upload-result-grid">
            {Object.entries(result.indexed_companies || {}).map(
              ([companyId, count]) => (
                <div className="upload-result-card" key={companyId}>
                  <span>{companyId}</span>
                  <strong>{count}</strong>
                  <small>indexed chunks</small>
                </div>
              ),
            )}
          </div>

          <button
            className="primary-button"
            onClick={() => onUploadSuccess(result)}
          >
            View Updated Dashboard
          </button>
        </div>
      )}

      {!result && (
        <button
          className="primary-button upload-button"
          onClick={handleUpload}
          disabled={!file || uploading}
        >
          {uploading ? "Processing..." : "Upload & Analyze"}
        </button>
      )}
    </div>
  );
}

function AssistantPage({ companyId, messages, setMessages }) {
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");
  const chatEndRef = useRef(null);
  const [expandedEvidence, setExpandedEvidence] = useState({});

  async function handleAsk(event) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || asking) {
      return;
    }

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((current) => [...current, userMessage]);

    setQuestion("");
    setError("");
    setAsking(true);

    try {
      const response = await askCompanyAssistant(companyId, trimmedQuestion);

      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.answer,
        evidence: response.evidence || [],
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch (err) {
      setError(err.message);
    } finally {
      setAsking(false);
    }
  }

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages]);

  return (
    <div className="assistant-page">
      <div className="assistant-intro">
        <div>
          <p className="eyebrow">AI INTELLIGENCE</p>

          <h2>ESG Assistant</h2>

          <p>
            Ask questions about {companyId}'s ESG performance using evidence
            from its transaction data.
          </p>
        </div>

        <div className="assistant-status">
          <span className="status-dot" />
          Evidence-backed
        </div>
      </div>

      <div className="suggestion-row">
        <button
          onClick={() => setQuestion("What are the main environmental risks?")}
        >
          Environmental risks
        </button>

        <button
          onClick={() => setQuestion("What ESG signals should I investigate?")}
        >
          Signals to investigate
        </button>

        <button
          onClick={() => setQuestion("What recommendations are available?")}
        >
          Recommendations
        </button>
      </div>

      <div className="chat-panel">
        <div className="chat-history">
          {messages.length === 0 && (
            <div className="chat-empty">
              <MessageSquare size={28} />

              <strong>Ask GreenLedger</strong>

              <p>
                Ask a question about the company's ESG data, risks, trends, or
                signals.
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              className={`chat-message ${
                message.role === "user" ? "chat-user" : "chat-assistant"
              }`}
              key={message.id}
            >
              <div className="message-label">
                {message.role === "user" ? "YOU" : "GREENLEDGER"}
              </div>

              <div className="assistant-message">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              </div>

              {message.role === "assistant" && message.evidence?.length > 0 && (
                <div className="evidence-section">
                  <button
                    type="button"
                    className="evidence-heading evidence-toggle"
                    onClick={() =>
                      setExpandedEvidence((current) => ({
                        ...current,
                        [message.evidence[0]?.id]:
                          !current[message.evidence[0]?.id],
                      }))
                    }
                  >
                    <span className="evidence-heading-content">
                      <FileText size={14} />
                      Evidence used
                    </span>

                    <span className="evidence-toggle-icon">
                      {expandedEvidence[message.evidence[0]?.id] ? "−" : "+"}
                    </span>
                  </button>

                  {expandedEvidence[message.evidence[0]?.id] && (
                    <div className="evidence-list">
                      {message.evidence.map((evidence) => (
                        <div className="evidence-card" key={evidence.id}>
                          <div className="evidence-meta">
                            <span>
                              {evidence.metadata?.section
                                ?.replace("_", " ")
                                ?.toUpperCase() || "ESG EVIDENCE"}
                            </span>

                            {evidence.metadata?.transaction_id && (
                              <span>{evidence.metadata.transaction_id}</span>
                            )}
                          </div>

                          <p>{evidence.document}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
          <div ref={chatEndRef} />

          {asking && (
            <div className="chat-message chat-assistant">
              <div className="message-label">GREENLEDGER</div>

              <div className="typing-indicator">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {error && <div className="chat-error">{error}</div>}

        <form className="chat-input-area" onSubmit={handleAsk}>
          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask about ESG performance..."
            disabled={asking}
          />

          <button type="submit" disabled={!question.trim() || asking}>
            {asking ? "..." : "Ask"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
