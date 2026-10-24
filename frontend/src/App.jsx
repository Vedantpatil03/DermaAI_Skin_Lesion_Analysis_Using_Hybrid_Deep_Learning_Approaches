import { useEffect, useState } from "react";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Analyze from "./pages/Analyze";
import History from "./pages/History";
import Results from "./pages/Results";
import {
    getAnalysisDetail,
    getAnalysisHistory,
    deleteAnalysisHistory,
    clearAnalysisHistory,
    getCurrentUser,
    getStoredUser,
    logoutUser
} from "./services/api";


function mapHistoryRecord(record) {
    const caseInformation = {
        caseId: record.case_id || "",
        patientName: record.patient_name || "",
        age: record.age == null ? "" : String(record.age),
        sex: record.sex || "",
        lesionSite: record.lesion_site || ""
    };

    return {
        historyId: record.history_id,
        caseId: caseInformation.caseId,
        patientName: caseInformation.patientName,
        age: caseInformation.age,
        sex: caseInformation.sex,
        lesionSite: caseInformation.lesionSite,
        predictedClass: record.classification?.predicted_class || "Not available",
        confidence: Number(record.classification?.confidence) || 0,
        analysisDate: record.created_at,
        result: {
            success: true,
            status: record.status || "analysis_complete",
            original_image: record.original_image || "",
            classification: record.classification || {},
            segmentation: record.segmentation || {},
            segmentation_safety: record.segmentation_safety || {},
            ood: record.ood || {},
            input_assessment: record.input_assessment || {}
        },
        caseInformation
    };
}

function App() {
    const [currentUser, setCurrentUser] = useState(getStoredUser);
    const [isCheckingSession, setIsCheckingSession] = useState(
        Boolean(sessionStorage.getItem("access_token"))
    );
    const [currentPage, setCurrentPage] = useState("dashboard");
    const [analysisResult, setAnalysisResult] = useState(null);
    const [caseInformation, setCaseInformation] = useState(null);
    const [analysisHistory, setAnalysisHistory] = useState([]);
    const [historyError, setHistoryError] = useState(null);

    useEffect(() => {
        const accessToken = sessionStorage.getItem("access_token");

        if (!accessToken) {
            setCurrentUser(null);
            sessionStorage.removeItem("current_user");
            setIsCheckingSession(false);
            return;
        }

        getCurrentUser()
            .then((user) => {
                setCurrentUser(user);

                if (!user) {
                    sessionStorage.removeItem("current_user");
                }
            })
            .catch(() => {
                setCurrentUser(null);
                sessionStorage.removeItem("current_user");
            })
            .finally(() => setIsCheckingSession(false));
    }, []);

    useEffect(() => {
        if (currentPage !== "history") {
            return;
        }

        let isCurrent = true;

        getAnalysisHistory()
            .then((response) => {
                if (!isCurrent) {
                    return;
                }

                setAnalysisHistory(
                    (response.history || []).map(mapHistoryRecord)
                );
                setHistoryError(null);
            })
            .catch((error) => {
                if (isCurrent) {
                    setAnalysisHistory([]);
                    setHistoryError(
                        error?.message ||
                        "Could not load analysis history."
                    );
                }
            });

        return () => {
            isCurrent = false;
        };
    }, [currentPage]);

    const handleAnalysisComplete = (result, information, historySaveError) => {
        const completedCaseInformation = {
            caseId: information?.caseId?.trim() || "Unknown case",
            patientName: information?.patientName?.trim() || "",
            age: information?.age?.trim() || "",
            sex: information?.sex || "",
            lesionSite: information?.lesionSite?.trim() || ""
        };

        setAnalysisResult(result);
        setCaseInformation(completedCaseInformation);
        setHistoryError(historySaveError || null);
        setAnalysisHistory((currentHistory) => {
            const historyRecord = {
                caseId: completedCaseInformation.caseId,
                patientName: completedCaseInformation.patientName,
                age: completedCaseInformation.age,
                sex: completedCaseInformation.sex,
                lesionSite: completedCaseInformation.lesionSite,
                predictedClass: result?.classification?.predicted_class || "Not available",
                confidence: Number(result?.classification?.confidence) || 0,
                analysisDate: new Date().toISOString(),
                result,
                caseInformation: completedCaseInformation
            };

            const existingRecordIndex = currentHistory.findIndex(
                (record) => record.caseId === completedCaseInformation.caseId
            );

            if (existingRecordIndex === -1) {
                return [historyRecord, ...currentHistory];
            }

            return currentHistory.map((record, index) =>
                index === existingRecordIndex
                    ? historyRecord
                    : record
            );
        });
        setCurrentPage("results");
    };

    const handleNavigate = (page) => {
        if (page === "analyze") {
            setAnalysisResult(null);
            setCaseInformation(null);
        }

        if (page === "history") {
            setHistoryError(null);
        }

        setCurrentPage(page);
    };

    const handleLogout = () => {
        logoutUser();
        setCurrentUser(null);
        setAnalysisResult(null);
        setCaseInformation(null);
        setAnalysisHistory([]);
        setCurrentPage("dashboard");
    };

    const handleHistorySelect = async (historyRecord) => {
        try {
            const response = historyRecord.historyId
                ? await getAnalysisDetail(historyRecord.historyId)
                : { analysis: historyRecord };
            const record = response.analysis;
            const mappedRecord = record.history_id
                ? mapHistoryRecord(record)
                : record;

            setAnalysisResult(mappedRecord.result);
            setCaseInformation(mappedRecord.caseInformation);
            setHistoryError(null);
            setCurrentPage("results");
        } catch (error) {
            setHistoryError(
                error?.message ||
                "Could not retrieve the selected analysis."
            );
        }
    };

    const handleHistoryDelete = async (historyRecord) => {
        if (!historyRecord.historyId) {
            setHistoryError(
                "This analysis does not have a stored history ID. Refresh the history page and try again."
            );
            return;
        }

        try {
            await deleteAnalysisHistory(historyRecord.historyId);
            setAnalysisHistory((currentHistory) =>
                currentHistory.filter(
                    (record) => record.historyId !== historyRecord.historyId
                )
            );
            setHistoryError(null);
        } catch (error) {
            setHistoryError(
                error?.message ||
                "Could not delete the selected analysis."
            );
        }
    };

    const handleHistoryClear = async () => {
        try {
            await clearAnalysisHistory();
            setAnalysisHistory([]);
            setHistoryError(null);
        } catch (error) {
            setHistoryError(
                error?.message ||
                "Could not clear analysis history."
            );
        }
    };

    const renderPage = () => {
        if (currentPage === "analyze") {
            return (
                <Analyze
                    onAnalysisComplete={handleAnalysisComplete}
                    onNavigate={handleNavigate}
                    currentUser={currentUser}
                    onLogout={handleLogout}
                />
            );
        }

        if (currentPage === "results") {
            return (
                <Results
                    result={analysisResult}
                    caseInformation={caseInformation}
                    historySaveError={historyError}
                    onNavigate={handleNavigate}
                    currentUser={currentUser}
                    onLogout={handleLogout}
                />
            );
        }

        if (currentPage === "history") {
            return (
                <History
                    history={analysisHistory}
                    error={historyError}
                    onNavigate={handleNavigate}
                    onSelectHistory={handleHistorySelect}
                    onDeleteHistory={handleHistoryDelete}
                    onClearHistory={handleHistoryClear}
                    currentUser={currentUser}
                    onLogout={handleLogout}
                />
            );
        }

        return (
            <Dashboard
                onNavigate={handleNavigate}
                currentUser={currentUser}
                onLogout={handleLogout}
            />
        );
    };

    if (isCheckingSession) {
        return (
            <main className="session-loading">
                <p>Checking your login session...</p>
            </main>
        );
    }

    if (!currentUser) {
        return <Login onLogin={setCurrentUser} />;
    }

    return (
        <div className="app">
            {renderPage()}
        </div>
    );
}

export default App;