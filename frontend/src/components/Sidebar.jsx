function Sidebar({ currentPage, onNavigate }) {
    return (
        <aside className="sidebar">
            <div className="sidebar-section">
                <p className="sidebar-title">
                    CLINICAL WORKSPACE
                </p>

                <button
                    type="button"
                    aria-label="Clinical Overview"
                    title="Clinical Overview"
                    className={
                        currentPage === "dashboard"
                            ? "sidebar-item active"
                            : "sidebar-item"
                    }
                    onClick={() => onNavigate("dashboard")}
                >
                    <span className="sidebar-icon">
                        ⌂
                    </span>

                    <span>
                        Clinical Overview
                    </span>
                </button>

                <button
                    type="button"
                    aria-label="History"
                    title="History"
                    className={
                        currentPage === "history"
                            ? "sidebar-item active"
                            : "sidebar-item"
                    }
                    onClick={() => onNavigate("history")}
                >
                    <span className="sidebar-icon">
                        =
                    </span>

                    <span>
                        History
                    </span>
                </button>

                <button
                    type="button"
                    aria-label="New Analysis"
                    title="New Analysis"
                    className={
                        currentPage === "analyze"
                            ? "sidebar-item active"
                            : "sidebar-item"
                    }
                    onClick={() => onNavigate("analyze")}
                >
                    <span className="sidebar-icon">
                        +
                    </span>

                    <span>
                        New Analysis
                    </span>
                </button>
            </div>

           
               
               
                    
            <div className="sidebar-footer">
                <p className="quick-guide-title">
                    QUICK GUIDE
                </p>

                <div className="quick-guide-steps">
                    <span className="quick-guide-step">
                        <strong>1</strong>
                        <span>Create a case</span>
                    </span>

                    <span className="quick-guide-step">
                        <strong>2</strong>
                        <span>Upload Skin Image</span>
                    </span>

                    <span className="quick-guide-step">
                        <strong>3</strong>
                        <span>Review results</span>
                    </span>

                    <span className="quick-guide-step">
                        <strong>4</strong>
                        <span>Download report</span>
                    </span>
                </div>
            </div>
        </aside>
    );
}

export default Sidebar;