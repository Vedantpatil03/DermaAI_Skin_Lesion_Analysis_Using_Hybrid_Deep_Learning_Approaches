import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Dashboard({ onNavigate, currentUser, onLogout }) {
    return (
        <div className="dashboard-layout">
            <Navbar
                currentPage="dashboard"
                onNavigate={onNavigate}
                currentUser={currentUser}
                onLogout={onLogout}
            />

            <div className="dashboard-body">
                <Sidebar
                    currentPage="dashboard"
                    onNavigate={onNavigate}
                />

                <main className="dashboard-content">
                    <section className="welcome-section dashboard-hero">
                        <div className="dashboard-hero-copy">
                            

                            

                            <p className="section-label">
                                CLINICAL DASHBOARD
                            </p>

                            <h2>
                                Dermatology Skin Image Analysis
                            </h2>

                            <p className="welcome-text">
                                AI-assisted skin lesion assessment to support
                                clinical review.
                            </p>

                            <button
                                type="button"
                                className="primary-button"
                                onClick={() =>
                                    onNavigate("analyze")
                                }
                            >
                                New Analysis
                                <span aria-hidden="true">-&gt;</span>
                            </button>
                        </div>

                        
                    </section>

                    <section className="dashboard-cards" aria-label="Analysis capabilities">
                        <div className="info-card">
                            <div className="card-icon">
                                AI
                            </div>

                            <div>
                                <h3>
                                    Lesion Classification
                                </h3>

                                <p>
                                    Classifies the lesion image and provides
                                    confidence and probability results.
                                </p>
                            </div>
                        </div>

                        <div className="info-card">
                            <div className="card-icon">
                                ◉
                            </div>

                            <div>
                                <h3>
                                    Lesion Analysis
                                </h3>

                                <p>
                                    Identifies the lesion region and estimates
                                    the affected image area.
                                </p>
                            </div>
                        </div>

                        <div className="info-card">
                            <div className="card-icon">
                                ✦
                            </div>

                            <div>
                                <h3>
                                    Clinical Review
                                </h3>

                                <p>
                                    Combines the image, classification,
                                    confidence, and prediction results.
                                </p>
                            </div>
                        </div>
                    </section>

                    <section className="workflow-card">
                        <div className="workflow-heading">
                            <p className="section-label">
                                ANALYSIS WORKFLOW
                            </p>

                            

                            <p>
                                A clear process from case creation to
                                AI-assisted review.
                            </p>
                        </div>

                        <div className="workflow-steps">
                            <div className="workflow-step">
                                <span>01</span>

                                <div>
                                    <strong>
                                        New Analysis
                                    </strong>

                                    <p>
                                        Create a case and upload a lesion image.
                                    </p>
                                </div>
                            </div>

                            <div className="workflow-step">
                                <span>02</span>

                                <div>
                                    <strong>
                                        Analysis Results
                                    </strong>

                                    <p>
                                        Review classification, confidence,
                                        region, and probability results.
                                    </p>
                                </div>
                            </div>

                            <div className="workflow-step">
                                <span>03</span>

                                <div>
                                    <strong>
                                        Clinical Review
                                    </strong>

                                    <p>
                                        Review findings with the image and
                                        clinical details.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </section>

                </main>
            </div>
        </div>
    );
}

export default Dashboard;