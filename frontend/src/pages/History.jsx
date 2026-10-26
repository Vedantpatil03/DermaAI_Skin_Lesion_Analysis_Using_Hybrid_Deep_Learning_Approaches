import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";


function formatAnalysisDate(dateValue) {
    const normalizedDateValue =
        typeof dateValue === "string" &&
        !/(Z|[+-]\d{2}:?\d{2})$/i.test(dateValue)
            ? `${dateValue}Z`
            : dateValue;

    return new Date(normalizedDateValue).toLocaleString([], {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Kolkata"
    });
}


function History({
    history,
    error,
    onNavigate,
    onSelectHistory,
    onDeleteHistory,
    onClearHistory,
    currentUser,
    onLogout
}) {
    return (
        <div className="dashboard-layout">
            <Navbar
                currentPage="history"
                onNavigate={onNavigate}
                currentUser={currentUser}
                onLogout={onLogout}
            />

            <div className="dashboard-body">
                <Sidebar
                    currentPage="history"
                    onNavigate={onNavigate}
                />

                <main className="dashboard-content history-content">
                    <section className="history-header">
                        <div className="history-header-content">
                            <div>
                                <p className="section-label">
                                    HISTORY
                                </p>

                                <h1>
                             Analysis History
                        </h1>

                                <p className="welcome-text">
                                    Review previously completed analysis cases.
                                </p>
                            </div>

                            {history.length > 0 && (
                                <button
                                    type="button"
                                    className="secondary-button history-clear-button"
                                    onClick={() => {
                                        if (
                                            window.confirm(
                                                "Delete all analysis history? This action cannot be undone."
                                            )
                                        ) {
                                            onClearHistory();
                                        }
                                    }}
                                >
                                    Clear History
                                </button>
                            )}
                        </div>
                    </section>

                    {error && (
                        <div className="error-message" role="alert">
                            <div className="error-message-header">
                                <span className="error-warning-icon">!</span>
                                <strong>History Unavailable</strong>
                            </div>
                            <p>{error}</p>
                        </div>
                    )}

                    {history.length === 0 ? (
                        <section className="history-empty-state">
                            <p className="section-label">
                               NO ANALYSIS HISTORY
                            </p>

                            

                            <p>
                                Completed analysis cases will appear here.
                            </p>

                            <button
                                type="button"
                                className="primary-button"
                                onClick={() => onNavigate("analyze")}
                            >
                                New Analysis
                            </button>
                        </section>
                    ) : (
                        <section className="history-card">
                            <div className="history-table-wrapper">
                                <table className="history-table">
                                    <thead>
                                        <tr>
                                            <th>Case ID</th>
                                            <th>Patient</th>
                                            <th>Analysis Date</th>
                                            <th>Classification</th>
                                            <th>Confidence</th>
                                            <th>Status</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {history.map((record) => (
                                            <tr key={record.historyId || `${record.caseId}-${record.analysisDate}`}>
                                                <td data-label="Case ID">{record.caseId}</td>
                                                <td data-label="Patient">{record.patientName || "Not provided"}</td>
                                                <td data-label="Analysis Date">{formatAnalysisDate(record.analysisDate)}</td>
                                                <td data-label="Classification">{record.predictedClass}</td>
                                                <td data-label="Confidence">{(record.confidence * 100).toFixed(2)}%</td>
                                                <td data-label="Status">
                                                    <span className="history-status">Completed</span>
                                                </td>
                                                <td data-label="Action">
                                                    <div className="history-actions">
                                                        <button
                                                            type="button"
                                                            className="history-action"
                                                            onClick={() => onSelectHistory(record)}
                                                        >
                                                            View Results
                                                        </button>
                                                        <button
                                                            type="button"
                                                            className="history-delete-action"
                                                            aria-label={`Delete analysis ${record.caseId}`}
                                                            title="Delete analysis"
                                                            onClick={() => {
                                                   if (
                                                        window.confirm(
                                                            "Are you sure you want to delete this analysis?"
                                              )
                                            ) {
                                                        onDeleteHistory(record);
                                               }
                                                          }}
                                                        >
                                                            <svg
                                                                aria-hidden="true"
                                                                viewBox="0 0 24 24"
                                                                focusable="false"
                                                            >
                                                                <path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3" />
                                                            </svg>
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </section>
                    )}
                </main>
            </div>
        </div>
    );
}


export default History;