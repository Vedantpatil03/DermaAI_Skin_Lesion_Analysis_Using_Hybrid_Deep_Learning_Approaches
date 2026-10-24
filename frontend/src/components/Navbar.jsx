import { useEffect, useRef, useState } from "react";

function Navbar({ currentPage, onNavigate, currentUser, onLogout }) {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false);
    const accountMenuRef = useRef(null);

    useEffect(() => {
        const handleDocumentClick = (event) => {
            if (
                isAccountMenuOpen &&
                accountMenuRef.current &&
                !accountMenuRef.current.contains(event.target)
            ) {
                setIsAccountMenuOpen(false);
            }
        };

        document.addEventListener("mousedown", handleDocumentClick);
        return () => document.removeEventListener("mousedown", handleDocumentClick);
    }, [isAccountMenuOpen]);

    const handleNavigate = (page) => {
        setIsMobileMenuOpen(false);
        onNavigate(page);
    };

    return (
        <header className="navbar">
            <div className="navbar-left">
                <button
                    type="button"
                    className="mobile-menu-button"
                    aria-label="Open navigation menu"
                    aria-expanded={isMobileMenuOpen}
                    onClick={() => setIsMobileMenuOpen((isOpen) => !isOpen)}
                >
                    <span />
                    <span />
                    <span />
                </button>

                <img
                    src="/dermaailogo.png"
                    alt="DermaAI logo"
                    className="brand-logo"
                />

                <div className="brand-text">
                    <h1>DermaAI</h1>
                    <span>Intelligent Dermatological Image Analysis & Clinical Decision Support System</span>
                </div>
            </div>

            <nav className="navbar-menu">
                <button
                    type="button"
                    className={
                        currentPage === "dashboard"
                            ? "active"
                            : ""
                    }
                    onClick={() => handleNavigate("dashboard")}
                >
                    Clinical Dashboard
                </button>

                <button
                    type="button"
                    className={
                        currentPage === "analyze"
                            ? "active"
                            : ""
                    }
                    onClick={() => handleNavigate("analyze")}
                >
                    Analysis 
                </button>

                <button
                    type="button"
                    className={
                        currentPage === "results"
                            ? "active"
                            : ""
                    }
                    onClick={() => handleNavigate("results")}
                >
                    Results
                </button>

                <button
                    type="button"
                    className={
                        currentPage === "history"
                            ? "active"
                            : ""
                    }
                    onClick={() => handleNavigate("history")}
                >
                    History
                </button>
            </nav>

            <div className="navbar-account" ref={accountMenuRef}>
                <button
                    type="button"
                    className="navbar-profile-button"
                    aria-label="Open account menu"
                    aria-expanded={isAccountMenuOpen}
                    aria-haspopup="menu"
                    onClick={() => setIsAccountMenuOpen((isOpen) => !isOpen)}
                >
                    <span className="navbar-avatar">
                        {(currentUser?.name || currentUser?.email || "U")
                            .split(/\s+/)
                            .map((part) => part[0])
                            .join("")
                            .slice(0, 2)
                            .toUpperCase()}
                    </span>
                </button>

                {isAccountMenuOpen && (
                    <div className="account-menu" role="menu">
                        <div className="account-menu-header">
                            <strong>{currentUser?.name || "DermaAI User"}</strong>
                            <span>{currentUser?.email}</span>
                        </div>

                        
                        <button
                            type="button"
                            className="account-menu-signout"
                            role="menuitem"
                            onClick={onLogout}
                        >
                            <span className="account-menu-icon" aria-hidden="true">↪</span>
                            Sign Out
                        </button>
                    </div>
                )}
            </div>

            {isMobileMenuOpen && (
                <nav className="mobile-navbar-menu" aria-label="Mobile navigation">
                    <button
                        type="button"
                        className={currentPage === "dashboard" ? "active" : ""}
                        onClick={() => handleNavigate("dashboard")}
                    >
                        Clinical Dashboard
                    </button>
                    <button
                        type="button"
                        className={currentPage === "analyze" ? "active" : ""}
                        onClick={() => handleNavigate("analyze")}
                    >
                        Analysis
                    </button>
                    <button
                        type="button"
                        className={currentPage === "history" ? "active" : ""}
                        onClick={() => handleNavigate("history")}
                    >
                        History
                    </button>
                </nav>
            )}
        </header>
    );
}

export default Navbar;