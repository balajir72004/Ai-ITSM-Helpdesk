import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState("employee");
  const [message, setMessage] = useState("");
  const [software, setSoftware] = useState("Visual Studio Code");
  const [analysis, setAnalysis] = useState(null);
  const [chatResult, setChatResult] = useState(null);
  const [ticketResult, setTicketResult] = useState(null);
  const [softwareResult, setSoftwareResult] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [tickets, setTickets] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // --------------------------------------------------
  // API REQUEST
  // --------------------------------------------------

  async function apiRequest(endpoint, method = "GET", body = null) {
    const options = {
      method,
      headers: {},
    };

    if (body) {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API}${endpoint}`, options);

    if (!response.ok) {
      throw new Error(`Request failed: HTTP ${response.status}`);
    }

    return response.json();
  }

  // --------------------------------------------------
  // ANALYZE ISSUE / CHAT / CREATE TICKET
  // --------------------------------------------------

  async function handleAction(action) {
    if (!message.trim()) {
      setError("Please enter your IT issue or question.");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);
    setChatResult(null);
    setTicketResult(null);

    try {
      if (action === "analyze") {
        const result = await apiRequest("/analyze", "POST", {
          message,
        });

        setAnalysis(result.analysis);
      } else if (action === "chat") {
        const result = await apiRequest("/chat", "POST", {
          message,
        });

        setChatResult(result);
      } else if (action === "ticket") {
        const result = await apiRequest("/tickets", "POST", {
          message,
        });

        setTicketResult(result.ticket);
      }
    } catch (err) {
      setError(
        `${err.message}. Make sure the backend is running at ${API}.`
      );
    } finally {
      setLoading(false);
    }
  }

  // --------------------------------------------------
  // LOAD DASHBOARD
  // --------------------------------------------------

  async function loadDashboard() {
    setLoading(true);
    setError("");

    try {
      const [stats, ticketData, logsData] = await Promise.all([
        apiRequest("/dashboard"),
        apiRequest("/tickets"),
        apiRequest("/audit-logs"),
      ]);

      setDashboard(stats);
      setTickets(ticketData.tickets || []);
      setAuditLogs(logsData.logs || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // --------------------------------------------------
  // SOFTWARE REQUEST
  // --------------------------------------------------

  async function requestSoftware() {
    setLoading(true);
    setError("");
    setSoftwareResult(null);

    try {
      const result = await apiRequest("/software-requests", "POST", {
        software,
      });

      setSoftwareResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // --------------------------------------------------
  // NAVIGATION
  // --------------------------------------------------

  function changeTab(tab) {
    setActiveTab(tab);
    setError("");
    setAnalysis(null);
    setChatResult(null);
    setTicketResult(null);
    setSoftwareResult(null);

    if (tab === "dashboard") {
      loadDashboard();
    }
  }

  // --------------------------------------------------
  // USER INTERFACE
  // --------------------------------------------------

  return (
    <div className="app-shell">
      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <h2>ITSM Assist</h2>
            <p>Intelligent Helpdesk</p>
          </div>
        </div>

        <p className="nav-label">WORKSPACE</p>

        <button
          className={
            activeTab === "employee" ? "nav-item active" : "nav-item"
          }
          onClick={() => changeTab("employee")}
        >
          <span>⌂</span> Employee Portal
        </button>

        <button
          className={
            activeTab === "knowledge" ? "nav-item active" : "nav-item"
          }
          onClick={() => changeTab("knowledge")}
        >
          <span>✦</span> AI Knowledge Assistant
        </button>

        <button
          className={
            activeTab === "software" ? "nav-item active" : "nav-item"
          }
          onClick={() => changeTab("software")}
        >
          <span>▣</span> Software Requests
        </button>

        <button
          className={
            activeTab === "dashboard" ? "nav-item active" : "nav-item"
          }
          onClick={() => changeTab("dashboard")}
        >
          <span>▥</span> ITSM Dashboard
        </button>

        <div className="sidebar-footer">
          <div className="status-dot" />

          <div>
            <strong>Development Mode</strong>
            <p>Mock ServiceNow integration</p>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}

      <main className="main-area">
        <header className="topbar">
          <div>
            <p className="breadcrumb">Workspace / Helpdesk</p>

            <h1>
              {activeTab === "employee" && "Employee Helpdesk"}
              {activeTab === "knowledge" && "AI Knowledge Assistant"}
              {activeTab === "software" && "Software Provisioning"}
              {activeTab === "dashboard" && "ITSM Dashboard"}
            </h1>
          </div>

          <div className="user-profile">
            <div className="avatar">E</div>

            <div>
              <strong>Employee</strong>
              <p>Standard User</p>
            </div>
          </div>
        </header>

        {error && <div className="alert error">{error}</div>}

        {loading && (
          <div className="loading-bar">
            Processing request...
          </div>
        )}

        {/* EMPLOYEE PORTAL */}

        {activeTab === "employee" && (
          <section>
            <div className="welcome-banner">
              <div>
                <span className="eyebrow">
                  AI-POWERED IT SUPPORT
                </span>

                <h2>How can we help you today?</h2>

                <p>
                  Describe your IT issue. The assistant will analyze
                  your request and help you find the next step.
                </p>
              </div>

              <div className="welcome-symbol">✦</div>
            </div>

            <div className="section-heading">
              <div>
                <h2>Submit an IT request</h2>
                <p>
                  Analyze your issue or create a support ticket.
                </p>
              </div>
            </div>

            <div className="panel request-panel">
              <label htmlFor="issue">
                Describe your issue
              </label>

              <textarea
                id="issue"
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Example: I cannot connect to the company VPN..."
                rows={5}
              />

              <div className="example-prompts">
                <button
                  type="button"
                  onClick={() =>
                    setMessage("I cannot connect to the company VPN")
                  }
                >
                  VPN connection
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setMessage("I need to reset my password")
                  }
                >
                  Password reset
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setMessage(
                      "Outlook email synchronization is not working"
                    )
                  }
                >
                  Outlook issue
                </button>
              </div>

              <div className="action-row">
                <button
                  className="button secondary"
                  disabled={loading}
                  onClick={() => handleAction("analyze")}
                >
                  Analyze with AI
                </button>

                <button
                  className="button primary"
                  disabled={loading}
                  onClick={() => handleAction("ticket")}
                >
                  Create Support Ticket
                </button>
              </div>
            </div>

            {/* TICKET ANALYSIS */}

            {analysis && (
              <div className="panel result-panel">
                <div className="result-header">
                  <h3>Ticket Analysis</h3>

                  <span className="badge blue">
                    {analysis.intent}
                  </span>
                </div>

                <div className="detail-grid">
                  <Detail
                    label="Category"
                    value={analysis.category}
                  />

                  <Detail
                    label="Subcategory"
                    value={analysis.subcategory}
                  />

                  <Detail
                    label="Priority"
                    value={analysis.priority}
                  />

                  <Detail
                    label="Assignment Group"
                    value={analysis.assignment_group}
                  />
                </div>

                <h4>Suggested next step</h4>

                <p>{analysis.resolution}</p>
              </div>
            )}

            {/* TICKET CREATION RESULT */}

            {ticketResult && (
              <div className="panel result-panel">
                <div className="result-header">
                  <h3>Ticket Created Successfully</h3>

                  <span className="badge green">
                    {ticketResult.status}
                  </span>
                </div>

                <p>
                  Ticket ID:{" "}
                  <strong>{ticketResult.ticket_id}</strong>
                </p>

                <p>{ticketResult.summary}</p>

                <p className="muted">
                  Integration: {ticketResult.integration}
                </p>
              </div>
            )}

            <div className="info-grid">
              <InfoCard
                icon="✦"
                title="Knowledge Assistant"
                text="Find troubleshooting guidance from the approved knowledge base."
                onClick={() => changeTab("knowledge")}
              />

              <InfoCard
                icon="▣"
                title="Software Requests"
                text="Request software from the available catalogue."
                onClick={() => changeTab("software")}
              />
            </div>
          </section>
        )}

        {/* AI KNOWLEDGE ASSISTANT */}

        {activeTab === "knowledge" && (
          <section>
            <div className="welcome-banner compact">
              <div>
                <span className="eyebrow">
                  KNOWLEDGE RETRIEVAL
                </span>

                <h2>Ask the IT Knowledge Assistant</h2>

                <p>
                  Search troubleshooting information and view the
                  source documents used to answer your question.
                </p>
              </div>

              <div className="welcome-symbol">✦</div>
            </div>

            <div className="panel">
              <label htmlFor="question">
                Your question
              </label>

              <textarea
                id="question"
                rows={4}
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Example: How do I fix Outlook email synchronization?"
              />

              <div className="example-prompts">
                <button
                  type="button"
                  onClick={() =>
                    setMessage(
                      "How do I troubleshoot a VPN connection?"
                    )
                  }
                >
                  VPN troubleshooting
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setMessage("How do I reset my password?")
                  }
                >
                  Password reset
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setMessage(
                      "How do I fix Outlook email synchronization?"
                    )
                  }
                >
                  Outlook synchronization
                </button>
              </div>

              <button
                className="button primary"
                disabled={loading}
                onClick={() => handleAction("chat")}
              >
                {loading
                  ? "Searching..."
                  : "Search Knowledge Base"}
              </button>
            </div>

            {/* CHAT ANSWER */}

            {chatResult && (
              <div className="panel result-panel">
                <div className="result-header">
                  <h3>Knowledge Assistant Response</h3>

                  <span
                    className={
                      chatResult.status === "answered"
                        ? "badge green"
                        : "badge orange"
                    }
                  >
                    {chatResult.status}
                  </span>
                </div>

                <p className="answer-text">
                  {chatResult.answer}
                </p>

                {/* SOURCE DOCUMENTS */}

                {chatResult.sources?.length > 0 && (
                  <>
                    <h4>Knowledge Sources</h4>

                    <div className="source-list">
                      {chatResult.sources.map((source, index) => (
                        <div
                          className="source-item"
                          key={`${source.source}-${index}`}
                        >
                          <div>
                            <strong>{source.title}</strong>
                            <p>{source.source}</p>
                          </div>

                          <span className="similarity">
                            Similarity: {source.similarity}
                          </span>
                        </div>
                      ))}
                    </div>
                  </>
                )}

                <p className="muted">
                  Method:{" "}
                  {chatResult.method ||
                    "Sentence Transformers + FAISS"}
                </p>

                {chatResult.status === "escalated" && (
                  <p className="muted">
                    Please contact IT Support for further investigation.
                  </p>
                )}
              </div>
            )}
          </section>
        )}

        {/* SOFTWARE REQUESTS */}

        {activeTab === "software" && (
          <section>
            <div className="welcome-banner compact">
              <div>
                <span className="eyebrow">
                  SOFTWARE CATALOGUE
                </span>

                <h2>Request approved software</h2>

                <p>
                  Submit a software request through the current
                  simulated provisioning workflow.
                </p>
              </div>

              <div className="welcome-symbol">▣</div>
            </div>

            <div className="panel request-panel">
              <label htmlFor="software">
                Select software
              </label>

              <select
                id="software"
                value={software}
                onChange={(event) =>
                  setSoftware(event.target.value)
                }
              >
                <option>Visual Studio Code</option>
                <option>Python</option>
                <option>Google Chrome</option>
                <option>Notepad++</option>
              </select>

              <button
                className="button primary"
                disabled={loading}
                onClick={requestSoftware}
              >
                Submit Software Request
              </button>
            </div>

            {softwareResult && (
              <div className="panel result-panel">
                <h3>{softwareResult.message}</h3>

                <pre>
                  {JSON.stringify(
                    softwareResult.request || softwareResult,
                    null,
                    2
                  )}
                </pre>

                <p className="muted">
                  Requests use a mock integration. No software is
                  installed automatically on the device.
                </p>
              </div>
            )}
          </section>
        )}

        {/* ITSM DASHBOARD */}

        {activeTab === "dashboard" && (
          <section>
            <div className="section-heading">
              <div>
                <h2>Helpdesk Overview</h2>

                <p>
                  Current helpdesk statistics from the backend.
                </p>
              </div>

              <button
                className="button secondary"
                onClick={loadDashboard}
                disabled={loading}
              >
                Refresh
              </button>
            </div>

            {dashboard && (
              <>
                <div className="stats-grid">
                  <StatCard
                    label="Total Tickets"
                    value={dashboard.total_tickets}
                    icon="▤"
                  />

                  <StatCard
                    label="Open Tickets"
                    value={dashboard.open_tickets}
                    icon="◷"
                  />

                  <StatCard
                    label="Software Requests"
                    value={dashboard.software_requests}
                    icon="▣"
                  />

                  <StatCard
                    label="Successful Automations"
                    value={dashboard.successful_automations}
                    icon="✓"
                  />

                  <StatCard
                    label="Escalated Requests"
                    value={dashboard.escalated_requests}
                    icon="↗"
                  />
                </div>

                {/* TICKET TABLE */}

                <div className="panel table-panel">
                  <h3>Recent Tickets</h3>

                  {tickets.length === 0 ? (
                    <p className="muted">
                      No tickets have been created yet.
                    </p>
                  ) : (
                    <div className="table-scroll">
                      <table>
                        <thead>
                          <tr>
                            <th>Ticket ID</th>
                            <th>Summary</th>
                            <th>Category</th>
                            <th>Priority</th>
                            <th>Status</th>
                          </tr>
                        </thead>

                        <tbody>
                          {tickets.map((ticket) => (
                            <tr key={ticket.ticket_id}>
                              <td>{ticket.ticket_id}</td>
                              <td>{ticket.summary}</td>
                              <td>{ticket.category}</td>
                              <td>{ticket.priority}</td>
                              <td>{ticket.status}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>

                {/* AUDIT LOG TABLE */}

                <div className="panel table-panel">
                  <h3>Audit Logs</h3>

                  {auditLogs.length === 0 ? (
                    <p className="muted">
                      No audit events recorded yet.
                    </p>
                  ) : (
                    <div className="table-scroll">
                      <table>
                        <thead>
                          <tr>
                            <th>Action</th>
                            <th>Status</th>
                            <th>Timestamp</th>
                          </tr>
                        </thead>

                        <tbody>
                          {auditLogs.map((log, index) => (
                            <tr key={log.audit_id || index}>
                              <td>
                                {log.action}
                                {log.software
                                  ? ` — ${log.software}`
                                  : ""}
                              </td>

                              <td>{log.status}</td>
                              <td>{log.timestamp}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </>
            )}
          </section>
        )}

        <footer className="page-footer">
          AI-Powered ITSM Helpdesk · Prototype · Mock ServiceNow integration
        </footer>
      </main>
    </div>
  );
}

// --------------------------------------------------
// REUSABLE COMPONENTS
// --------------------------------------------------

function Detail({ label, value }) {
  return (
    <div className="detail-item">
      <span>{label}</span>
      <strong>{value || "—"}</strong>
    </div>
  );
}

function InfoCard({ icon, title, text, onClick }) {
  return (
    <button className="info-card" onClick={onClick}>
      <span className="info-icon">{icon}</span>

      <span>
        <strong>{title}</strong>
        <p>{text}</p>
      </span>

      <span className="arrow">→</span>
    </button>
  );
}

function StatCard({ label, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{label}</span>
        <span className="stat-icon">{icon}</span>
      </div>

      <strong>{value ?? 0}</strong>
    </div>
  );
}

export default App;