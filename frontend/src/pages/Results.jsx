import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import SegmentationResult from "../components/SegmentationResult";
import { downloadAnalysisReport } from "../services/report";


function Results({
    result,
    caseInformation,
    historySaveError,
    onNavigate,
    currentUser,
    onLogout
}) {

    const handleDownloadReport = async () => {
        await downloadAnalysisReport({
            ...result,
            case_information: caseInformation
        });
    };

    // ========================================
    // NO RESULT STATE
    // ========================================

    if (!result) {

        return (
            <div className="dashboard-layout">

                <Navbar
                    currentPage="results"
                    onNavigate={onNavigate}
                    currentUser={currentUser}
                    onLogout={onLogout}
                />

                <div className="dashboard-body">

                    <Sidebar
                        currentPage="results"
                        onNavigate={onNavigate}
                    />

                    <main className="dashboard-content">

                        <section className="empty-results">

                            <p className="section-label">
                                ANALYSIS RESULTS
                            </p>

                            <h2>
                                No Analysis Available
                            </h2>

                            <p className="welcome-text">
                                Start a new analysis to view
                                AI-assisted skin lesion
                                analysis results.
                            </p>

                            <button
                                type="button"
                                className="primary-button"
                                onClick={() =>
                                    onNavigate("analyze")
                                }
                            >
                                Start New Analysis
                            </button>

                        </section>

                    </main>

                </div>

            </div>
        );
    }


    // ========================================
    // RESULT DATA
    // ========================================

    const classification =
        result.classification || {};

    const segmentation =
        result.segmentation || {};

    const segmentationSafety =
        result.segmentation_safety || {};


    const predictedClass =
        classification.predicted_class ||
        "Not available";


    const confidence =
        classification.confidence || 0;


    const confidencePercentage =
        (confidence * 100).toFixed(2);


    const lesionArea =
        segmentation.lesion_area_percentage;


    // ========================================
    // PROBABILITIES
    // ========================================

    const probabilities =
        classification.probabilities || {};


    const probabilityEntries =
        Object.entries(probabilities)
            .sort(
                ([, first], [, second]) =>
                    second - first
            );


    // ========================================
    // MAIN UI
    // ========================================

    return (

        <div className="dashboard-layout">

            <Navbar
                currentPage="results"
                onNavigate={onNavigate}
                currentUser={currentUser}
                onLogout={onLogout}
            />


            <div className="dashboard-body">

                <Sidebar
                    currentPage="results"
                    onNavigate={onNavigate}
                />


                <main className="dashboard-content results-content">


                    {/* ========================================
                        PAGE HEADER
                    ======================================== */}

                    <section className="results-header">

                        <div>

                            <p className="section-label">
                                ANALYSIS RESULTS
                            </p>

                                <h2>
                                Analysis Results
                            </h2>

                            <p className="welcome-text">
                                AI-assisted analysis summary
                                for clinical review.
                            </p>

                        </div>


                        <div className="results-header-actions">
                            <button
                                type="button"
                                className="secondary-button report-button"
                                onClick={handleDownloadReport}
                            >
                                Download Clinical Report
                            </button>

                            <button
                                type="button"
                                className="secondary-button"
                                onClick={() =>
                                    onNavigate("analyze")
                                }
                            >
                                New Analysis
                            </button>
                        </div>

                    </section>

                    {historySaveError && (
                        <div className="error-message" role="alert">
                            <div className="error-message-header">
                                <span className="error-warning-icon">!</span>
                                <strong>History Save Unavailable</strong>
                            </div>
                            <p>
                                The analysis completed successfully, but it
                                could not be saved to history:{" "}
                                {historySaveError}
                            </p>
                        </div>
                    )}


                    <section className="case-information-card">

                        <div className="result-card-header">
                            <div>
                                <p className="section-label">
                                    CASE/PATIENT INFORMATION
                                </p>

                            
                            </div>
                        </div>

                        <div className="case-information-grid">
                            {[
                                ["Case ID", caseInformation?.caseId],
                                ["Patient", caseInformation?.patientName],
                                ["Age", caseInformation?.age],
                                ["Sex", caseInformation?.sex],
                                ["Lesion Site", caseInformation?.lesionSite]
                            ].map(([label, value]) => value ? (
                                <div className="case-information-item" key={label}>
                                    <span>{label}</span>
                                    <strong>{value}</strong>
                                </div>
                            ) : null)}
                        </div>
                    </section>


                    {/* ========================================
                        ANALYSIS STATUS
                    ======================================== */}

                    <section className="analysis-status-card">

                        <div className="status-indicator">
                            <span></span>
                        </div>

                        <div>

                            <strong>
                                Analysis Completed
                            </strong>

                            <p>
                                The uploaded image was processed
                                successfully by the available
                                AI analysis pipeline.
                            </p>

                        </div>

                    </section>


                    {/* ========================================
                        CLASSIFICATION SUMMARY
                    ======================================== */}

                    <section className="prediction-summary">

                        <div className="prediction-main">

                            <div className="result-icon">
                                AI
                            </div>


                            <div>

                                <p className="result-label">
                                    AI CLASSIFICATION
                                </p>

                                <h3>
                                    {predictedClass}
                                </h3>

                                <p>
                                    AI-assisted classification result
                                    for clinical review.
                                </p>

                            </div>

                        </div>


                        <div className="confidence-box">

                            <span>
                                Prediction Confidence
                            </span>

                            <strong>
                                {confidencePercentage}%
                            </strong>

                        </div>

                    </section>


                    {/* ========================================
                        IMAGE ANALYSIS
                    ======================================== */}

                    <section className="result-grid">


                        {/* ----------------------------------------
                            ORIGINAL IMAGE
                        ---------------------------------------- */}

                        <div className="result-card image-result-card">

                            <div className="result-card-header">

                                <div>

                                    <p className="section-label">
                                        INPUT IMAGE
                                    </p>

                                    <h3>
                                        Original Image
                                    </h3>

                                </div>

                            </div>


                            <div className="original-image-container">

                                {result.original_image ? (

                                    <img
                                        src={result.original_image}
                                        alt="Uploaded skin lesion"
                                        className="original-result-image"
                                    />

                                ) : (

                                    <div className="image-unavailable">

                                        Original image unavailable.

                                    </div>

                                )}

                            </div>


                            <p className="result-description">
                                Original image submitted for
                                AI-assisted analysis.
                            </p>

                        </div>


                        {/* ----------------------------------------
                            SEGMENTATION
                        ---------------------------------------- */}

                        <div className="result-card">

                            <div className="result-card-header">

                                <div>

                                    <p className="section-label">
                                        LESION SEGMENTATION
                                    </p>

                                    <h3>
                                        AI-Detected Lesion Region
                                    </h3>

                                </div>


                                <span className="metric-value">

                                    {lesionArea !== undefined
                                        ? `${Number(
                                            lesionArea
                                        ).toFixed(2)}%`
                                        : "N/A"
                                    }

                                </span>

                            </div>


                            <SegmentationResult
                                originalImage={
                                    result.original_image
                                }

                                maskBase64={
                                    segmentation.mask_base64
                                }

                                lesionArea={
                                    lesionArea
                                }
                            />


                            <p className="result-description">
                                The highlighted region represents
                                the visible lesion region identified
                                for clinical review.
                            </p>

                        </div>

                    </section>


                    {/* ========================================
                        LESION METRICS
                    ======================================== */}

                    <section className="metrics-grid">


                        <div className="metric-card">

                            <span className="metric-label">
                                Lesion Area
                            </span>

                            <strong>

                                {lesionArea !== undefined
                                    ? `${Number(
                                        lesionArea
                                    ).toFixed(2)}%`
                                    : "N/A"
                                }

                            </strong>

                            <p>
                                Estimated segmented
                                image area.
                            </p>

                        </div>


                        <div className="metric-card">

                            <span className="metric-label">
                                Segmentation Status
                            </span>

                            <strong>

                                {segmentationSafety.safe
                                    ? "Valid"
                                    : "Review"
                                }

                            </strong>

                            <p>
                                AI-assisted lesion region
                                assessment.
                            </p>

                        </div>


                        <div className="metric-card">

                            <span className="metric-label">
                                Classification
                            </span>

                            <strong>
                                Complete
                            </strong>

                            <p>
                                AI-assisted classification result.
                            </p>

                        </div>


                    </section>


                    {/* ========================================
                        CLASS PROBABILITIES
                    ======================================== */}

                    <section className="result-card probability-card">

                        <div className="result-card-header">

                            <div>

                                <p className="section-label">
                                    CLASSIFICATION
                                </p>

                                <h3>
                                    Class Probability Distribution
                                </h3>

                                <p className="result-description">
                                    Available probability estimates
                                    across the lesion classes.
                                </p>

                            </div>

                        </div>


                        <div className="probability-list">

                            {probabilityEntries.map(
                                ([className, probability]) => {

                                    const percentage =
                                        Number(
                                            probability
                                        ) * 100;


                                    return (

                                        <div
                                            className="probability-row"
                                            key={className}
                                        >

                                            <div className="probability-label">

                                                <span>
                                                    {className}
                                                </span>

                                                <strong>
                                                    {percentage.toFixed(2)}%
                                                </strong>

                                            </div>


                                            <div className="probability-bar">

                                                <div
                                                    className={
                                                        className ===
                                                        predictedClass
                                                            ? "probability-fill primary"
                                                            : "probability-fill"
                                                    }

                                                    style={{
                                                        width:
                                                            `${Math.min(
                                                                percentage,
                                                                100
                                                            )}%`
                                                    }}
                                                />

                                            </div>

                                        </div>

                                    );

                                }
                            )}

                        </div>

                    </section>


                    {/* ========================================
                        CLINICAL DECISION SUPPORT
                    ======================================== */}

                    <section className="clinical-note">

                        <strong>
                            Clinical Decision Support
                        </strong>

                        <p>
                            This system provides AI-assisted
                            image analysis for clinical review.
                            Classification results and
                            segmentation outputs should be
                            considered together with the
                            original image, relevant clinical
                            information and professional
                            medical judgment.
                        </p>

                    </section>


                </main>

            </div>

        </div>
    );
}


export default Results;