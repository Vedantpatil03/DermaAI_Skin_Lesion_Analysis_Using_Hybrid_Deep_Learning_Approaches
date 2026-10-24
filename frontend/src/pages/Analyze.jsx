import { useRef, useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ImageUpload from "../components/ImageUpload";

import {
    analyzeImage,
    saveAnalysisHistory
} from "../services/api";


const getDoctorFriendlyError = (rawMessage = "") => {
    const normalized = String(rawMessage).toLowerCase();

    const mappings = [
        {
            test: /(resolution is too low|too low for reliable analysis|image resolution is too low)/,
            heading: "Image Quality Issue",
            description: "The uploaded image resolution is too low for reliable analysis. Please upload a clearer, higher-resolution image of the lesion."
        },
        {
            test: /(does not contain enough visual information|not enough visible detail|insufficient.*detail)/,
            heading: "Image Quality Issue",
            description: "The uploaded image does not contain enough visible detail for analysis. Please upload a clear image showing the skin lesion."
        },
        {
            test: /(no meaningful lesion region|fragmented for reliable analysis|clear lesion region could not be identified|could not be identified as a skin lesion)/,
            heading: "Lesion Not Clearly Identified",
            description: "A clear lesion region could not be identified in the uploaded image. Please upload a closer image with the lesion clearly visible."
        },
        {
            test: /(outside the supported.*distribution|not a suitable.*image|could not be reliably validated as a suitable skin-lesion image|unsuitable.*image|outside.*supported.*feature)/,
            heading: "Image Not Suitable",
            description: "The uploaded image does not appear suitable for skin-lesion analysis. Please upload a clear photograph of the skin lesion."
        },
        {
            test: /(unusually large portion of the image|image-spanning shape|framing is unsuitable|could not be reliably assessed because the image framing is unsuitable|segment.*large portion)/,
            heading: "Image Framing Issue",
            description: "The lesion could not be reliably assessed because the image framing is unsuitable. Please upload an image where the lesion is clearly visible with some surrounding skin."
        }
    ];

    const matched = mappings.find(({ test }) => test.test(normalized));

    if (matched) {
        return {
            heading: matched.heading,
            description: matched.description
        };
    }

    return {
        heading: "Analysis Could Not Be Completed",
        description: "The image could not be processed at this time. Please try again with a clear skin lesion image."
    };
};


function Analyze({ onAnalysisComplete, onNavigate, currentUser, onLogout }) {

    const [selectedFile, setSelectedFile] =
        useState(null);

    const [caseInformation, setCaseInformation] = useState({
        caseId: "",
        patientName: "",
        age: "",
        sex: "",
        lesionSite: ""
    });

    const [isAnalyzing, setIsAnalyzing] =
        useState(false);

    const [errorInfo, setErrorInfo] = useState(null);
    const [, setHistorySaveError] = useState(null);
    const [uploadResetKey, setUploadResetKey] = useState(0);
    const historySaveKeys = useRef(new Set());


    const handleFileSelect = (file) => {

        setSelectedFile(file);

        setErrorInfo(null);
        setHistorySaveError(null);
    };

    const resetToUploadState = () => {
        setSelectedFile(null);
        setErrorInfo(null);
        setHistorySaveError(null);
        setUploadResetKey((currentValue) => currentValue + 1);
    };

    const handleCaseInformationChange = (event) => {
        const { name, value } = event.target;

        setCaseInformation((currentInformation) => ({
            ...currentInformation,
            [name]: value
        }));

        setErrorMessage("");
    };


    const fileToDataUrl = (file) => {

        return new Promise(
            (resolve, reject) => {

                const reader =
                    new FileReader();

                reader.onload = () => {
                    resolve(reader.result);
                };

                reader.onerror = () => {
                    reject(
                        new Error(
                            "Could not prepare the uploaded image."
                        )
                    );
                };

                reader.readAsDataURL(file);
            }
        );
    };


    const handleAnalyze = async () => {

        if (!caseInformation.caseId.trim()) {

            setErrorInfo({
                heading: "Analysis Could Not Be Completed",
                description: "Please enter a Patient / Case ID before starting analysis."
            });

            return;
        }

        if (!selectedFile) {

            setErrorInfo({
                heading: "Analysis Could Not Be Completed",
                description: "Please upload a clear skin lesion image before starting analysis."
            });

            return;
        }


        setIsAnalyzing(true);

        setErrorInfo(null);
        setHistorySaveError(null);


        try {

            const result =
                await analyzeImage(
                    selectedFile
                );


            if (!result?.success) {

                throw new Error(
                    result?.message ||
                    "The image analysis could not be completed."
                );
            }


            const originalImage =
                await fileToDataUrl(
                    selectedFile
                );


            const resultWithImage = {
                ...result,

                original_image:
                    originalImage
            };

            const normalizedCaseInformation = {
                caseId: caseInformation.caseId.trim(),
                patientName: caseInformation.patientName.trim(),
                age: caseInformation.age.trim(),
                sex: caseInformation.sex,
                lesionSite: caseInformation.lesionSite.trim()
            };

            const historySaveKey = normalizedCaseInformation.caseId;
            let currentHistorySaveError = null;

            if (!historySaveKeys.current.has(historySaveKey)) {
                historySaveKeys.current.add(historySaveKey);

                try {
                    await saveAnalysisHistory({
                        ...resultWithImage,
                        segmentation: Object.fromEntries(
                            Object.entries(resultWithImage.segmentation || {})
                        ),
                        case_id: normalizedCaseInformation.caseId,
                        case_information: {
                            patient_name: normalizedCaseInformation.patientName,
                            age: normalizedCaseInformation.age,
                            sex: normalizedCaseInformation.sex,
                            lesion_site: normalizedCaseInformation.lesionSite
                        }
                    });
                } catch (historyError) {
                    historySaveKeys.current.delete(historySaveKey);
                    currentHistorySaveError =
                        historyError?.message ||
                        "The analysis completed, but it could not be saved to history."
                    setHistorySaveError(currentHistorySaveError);
                }
            }


            onAnalysisComplete(
                resultWithImage,
                normalizedCaseInformation,
                currentHistorySaveError
            );


        } catch (error) {

            setErrorInfo(
                getDoctorFriendlyError(
                    error?.message ||
                    "The image could not be processed at this time."
                )
            );


        } finally {

            setIsAnalyzing(false);
        }
    };


    return (

        <div className="dashboard-layout">

            <Navbar
                currentPage="analyze"
                onNavigate={onNavigate}
                currentUser={currentUser}
                onLogout={onLogout}
            />


            <div className="dashboard-body">

                <Sidebar
                    currentPage="analyze"
                    onNavigate={onNavigate}
                />


                <main className="dashboard-content">

                    <section className="analysis-header">

                    <p className="section-label">
                                Analysis
                            </p>    

                        <h1>
                             Skin Lesion Image Analysis
                        </h1>


                        <p className="welcome-text">
                            Upload a clear skin lesion image for
                            AI-assisted clinical review.
                        </p>

                    </section>


                    <section className="analysis-container">

                        <div className="case-information-form">

                            <div className="form-section-heading">
                                <p className="section-label">
                                    CASE INFORMATION
                                </p>

                                <h3>
                                    Patient / Case Information
                                </h3>

                                <p>
                                    Enter the details needed to identify this
                                    analysis.
                                </p>
                            </div>

                            <div className="form-grid">
                                <label className="form-field form-field-wide">
                                    <span>
                                        Patient / Case ID <strong>*</strong>
                                    </span>

                                    <input
                                        name="caseId"
                                        type="text"
                                        value={caseInformation.caseId}
                                        onChange={handleCaseInformationChange}
                                        placeholder="e.g. P-2026-00125"
                                        autoComplete="off"
                                    />
                                </label>

                                <label className="form-field">
                                    <span>Patient Name</span>

                                    <input
                                        name="patientName"
                                        type="text"
                                        value={caseInformation.patientName}
                                        onChange={handleCaseInformationChange}
                                        autoComplete="off"
                                    />
                                </label>

                                <label className="form-field">
                                    <span>Age</span>

                                    <input
                                        name="age"
                                        type="number"
                                        min="0"
                                        max="130"
                                        value={caseInformation.age}
                                        onChange={handleCaseInformationChange}
                                        inputMode="numeric"
                                    />
                                </label>

                                <label className="form-field">
                                    <span>Sex</span>

                                    <select
                                        name="sex"
                                        value={caseInformation.sex}
                                        onChange={handleCaseInformationChange}
                                    >
                                        <option value="">Select</option>
                                        <option value="Female">Female</option>
                                        <option value="Male">Male</option>
                                        <option value="Intersex">Intersex</option>
                                        <option value="Prefer not to say">
                                            Prefer not to say
                                        </option>
                                    </select>
                                </label>

                                <label className="form-field">
                                    <span>Lesion Site (Optional)</span>

                                    <input
                                        name="lesionSite"
                                        type="text"
                                        value={caseInformation.lesionSite}
                                        onChange={handleCaseInformationChange}
                                        placeholder="e.g. Left forearm"
                                        autoComplete="off"
                                    />
                                </label>
                            </div>
                        </div>

                        <div className="image-section-heading">
                            <p className="section-label">
                                IMAGE
                            </p>

                            <h3>
                                Upload Skin Lesion Image
                            </h3>
                        </div>

                        <ImageUpload
                            onFileSelect={
                                handleFileSelect
                            }
                            resetSignal={uploadResetKey}
                        />


                        {errorInfo && (

                            <div className="error-message" role="alert">
                                <div className="error-message-header">
                                    <span className="error-warning-icon">
                                        ⚠
                                    </span>

                                    <strong>
                                        {errorInfo.heading}
                                    </strong>
                                </div>

                                <p>
                                    {errorInfo.description}
                                </p>

                                <button
                                    type="button"
                                    className="secondary-button upload-another-button"
                                    onClick={resetToUploadState}
                                >
                                    Upload Another Image
                                </button>
                            </div>

                        )}


                        <div className="analysis-actions">

                            <button
                                type="button"
                                className="primary-button"
                                disabled={
                                    !selectedFile ||
                                    isAnalyzing
                                }
                                onClick={
                                    handleAnalyze
                                }
                            >

                                {isAnalyzing
                                    ? "Preparing Analysis..."
                                    : "Start Analysis"}

                            </button>


                            {isAnalyzing && (

                                <div className="analysis-status">

                                    <span className="loading-dot"></span>


                                    <span>
                                        AI analysis is processing the image.
                                        This may take some time.
                                    </span>

                                </div>

                            )}

                        </div>

                    </section>


                    <section className="analysis-note">

                        <strong>
                            Clinical Decision Support
                        </strong>


                        <p>
                            This system provides AI-assisted
                            analysis for clinical review.
                            Results should be interpreted
                            together with clinical assessment
                            and professional medical judgment.
                        </p>

                    </section>

                </main>

            </div>

        </div>
    );
}


export default Analyze;