import { jsPDF } from "jspdf";

const PROJECT_NAME =
    "AI-Powered Skin Lesion Analysis & Clinical Decision Support System";

const CLINICAL_NOTE =
    "This report provides AI-assisted image analysis for clinical review. Results should be interpreted together with the original image, relevant clinical information and professional medical judgment.";

function asImageSource(value, mimeType = "image/png") {
    if (!value) {
        return "";
    }

    return value.startsWith("data:")
        ? value
        : `data:${mimeType};base64,${value}`;
}

function imageFormat(source) {
    if (source.startsWith("data:image/png")) {
        return "PNG";
    }

    if (source.startsWith("data:image/webp")) {
        return "WEBP";
    }

    return "JPEG";
}

function loadImage(source) {
    return new Promise((resolve, reject) => {
        if (!source) {
            resolve(null);
            return;
        }

        const image = new Image();
        image.onload = () => resolve(image);
        image.onerror = () => reject(new Error("Unable to prepare report image."));
        image.src = source;
    });
}

async function createLesionVisualization(originalSource, maskSource) {
    const original = await loadImage(originalSource);
    const mask = await loadImage(maskSource);

    if (!original || !mask) {
        return "";
    }

    const canvas = document.createElement("canvas");
    const width = original.naturalWidth || original.width;
    const height = original.naturalHeight || original.height;
    canvas.width = width;
    canvas.height = height;

    const context = canvas.getContext("2d");
    if (!context) {
        return "";
    }

    context.drawImage(original, 0, 0, width, height);

    const maskCanvas = document.createElement("canvas");
    maskCanvas.width = width;
    maskCanvas.height = height;
    const maskContext = maskCanvas.getContext("2d");

    if (!maskContext) {
        return canvas.toDataURL("image/jpeg", 0.9);
    }

    maskContext.drawImage(mask, 0, 0, width, height);
    const maskData = maskContext.getImageData(0, 0, width, height).data;
    const overlay = maskContext.createImageData(width, height);

    for (let index = 0; index < maskData.length; index += 4) {
        if (maskData[index] <= 128) {
            continue;
        }

        overlay.data[index] = 17;
        overlay.data[index + 1] = 135;
        overlay.data[index + 2] = 119;
        overlay.data[index + 3] = 105;
    }

    maskContext.putImageData(overlay, 0, 0);
    context.drawImage(maskCanvas, 0, 0, width, height);
    return canvas.toDataURL("image/jpeg", 0.9);
}

function addPageNumber(pdf, pageNumber) {
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    pdf.setFontSize(8);
    pdf.setTextColor(120, 132, 145);
    pdf.text(`Page ${pageNumber}`, pageWidth - 25, pageHeight - 12);
}

function addSectionTitle(pdf, title, y) {
    pdf.setFillColor(232, 243, 250);
    pdf.roundedRect(18, y - 6, 174, 10, 2, 2, "F");
    pdf.setFontSize(10);
    pdf.setTextColor(32, 71, 95);
    pdf.setFont(undefined, "bold");
    pdf.text(title, 23, y + 1);
    pdf.setFont(undefined, "normal");
}

function addLabelValue(pdf, label, value, x, y) {
    pdf.setFontSize(9);
    pdf.setTextColor(105, 117, 130);
    pdf.text(label, x, y);
    pdf.setFont(undefined, "bold");
    pdf.setTextColor(30, 43, 58);
    pdf.text(value, x, y + 6);
    pdf.setFont(undefined, "normal");
}

export async function downloadAnalysisReport(result) {
    if (!result) {
        return;
    }

    const classification = result.classification || {};
    const segmentation = result.segmentation || {};
    const probabilities = classification.probabilities || {};
    const predictedClass = classification.predicted_class || "Not available";
    const confidence = Number(classification.confidence || 0) * 100;
    const lesionArea = segmentation.lesion_area_percentage;
    const caseInformation = result.case_information || {};
    const originalSource = asImageSource(result.original_image, "image/jpeg");
    const maskSource = asImageSource(segmentation.mask_base64);
    const visualization = await createLesionVisualization(
        originalSource,
        maskSource
    ).catch(() => "");

    const pdf = new jsPDF({
        unit: "mm",
        format: "a4"
    });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    let pageNumber = 1;
    let y = 22;

    pdf.setFillColor(28, 76, 102);
    pdf.rect(0, 0, pageWidth, 36, "F");
    pdf.setTextColor(255, 255, 255);
    pdf.setFontSize(22);
    pdf.setFont(undefined, "bold");
    pdf.text("DermaAI", 18, 16);
    pdf.setFontSize(9);
    pdf.setFont(undefined, "normal");
    pdf.text(PROJECT_NAME, 18, 25);
    pdf.setFont(undefined, "normal");

    y = 50;
    pdf.setTextColor(30, 43, 58);
    pdf.setFontSize(18);
    pdf.setFont(undefined, "bold");
    pdf.text("Skin Lesion Analysis Report", 18, y);
    pdf.setFont(undefined, "normal");
    y += 13;

    addSectionTitle(pdf, "Case Information", y);
    y += 15;
    addLabelValue(pdf, "Patient / Case ID", String(caseInformation.caseId || "Not available"), 23, y);
    if (caseInformation.patientName) {
        addLabelValue(pdf, "Patient", String(caseInformation.patientName), 105, y);
    }
    y += 20;

    const optionalCaseFields = [
        ["Age", caseInformation.age],
        ["Sex", caseInformation.sex],
        ["Lesion Site", caseInformation.lesionSite]
    ].filter(([, value]) => value);

    optionalCaseFields.forEach(([label, value], index) => {
        addLabelValue(pdf, label, String(value), index % 2 === 0 ? 23 : 105, y);

        if (index % 2 === 1 || index === optionalCaseFields.length - 1) {
            y += 20;
        }
    });

    addLabelValue(
        pdf,
        "Analysis Date / Time",
        new Date().toLocaleString(),
        23,
        y
    );
    y += 25;

    addSectionTitle(pdf, "AI Classification", y);
    y += 15;
    addLabelValue(pdf, "Predicted Disease", String(predictedClass), 23, y);
    addLabelValue(pdf, "Prediction Confidence", `${confidence.toFixed(2)}%`, 105, y);
    y += 28;

    addSectionTitle(pdf, "Lesion Assessment", y);
    y += 15;
    addLabelValue(
        pdf,
        "Estimated Lesion Area",
        lesionArea !== undefined ? `${Number(lesionArea).toFixed(2)}%` : "Not available",
        23,
        y
    );
    y += 22;

    if (originalSource || visualization) {
        const imageWidth = 78;
        const imageHeight = 58;
        pdf.setFontSize(9);
        pdf.setTextColor(105, 117, 130);
        pdf.text("Original Uploaded Image", 23, y);
        pdf.text("AI-Detected Lesion Region", 109, y);
        y += 4;

        if (originalSource) {
            pdf.addImage(
                originalSource,
                imageFormat(originalSource),
                23,
                y,
                imageWidth,
                imageHeight
            );
        }

        if (visualization) {
            pdf.addImage(visualization, "JPEG", 109, y, imageWidth, imageHeight);
        }

        y += imageHeight + 14;
    }

    if (y > pageHeight - 55) {
        addPageNumber(pdf, pageNumber);
        pdf.addPage();
        pageNumber += 1;
        y = 22;
    }

    addSectionTitle(pdf, "Prediction Results", y);
    y += 15;

    Object.entries(probabilities)
        .sort(([, first], [, second]) => Number(second) - Number(first))
        .forEach(([className, probability]) => {
            const percentage = Number(probability) * 100;
            pdf.setFontSize(9);
            pdf.setTextColor(45, 58, 73);
            pdf.text(String(className), 23, y);
            pdf.text(`${percentage.toFixed(2)}%`, 168, y);
            pdf.setDrawColor(221, 230, 236);
            pdf.line(23, y + 3, 192, y + 3);
            pdf.setFillColor(32, 128, 151);
            pdf.roundedRect(23, y + 5, Math.min(169, Math.max(0, percentage * 1.69)), 2, 1, 1, "F");
            y += 13;
        });

    y += 10;
    if (y > pageHeight - 55) {
        addPageNumber(pdf, pageNumber);
        pdf.addPage();
        pageNumber += 1;
        y = 22;
    }

    addSectionTitle(pdf, "Clinical Decision Support", y);
    y += 15;
    pdf.setFontSize(9);
    pdf.setTextColor(70, 82, 96);
    const noteLines = pdf.splitTextToSize(CLINICAL_NOTE, 164);
    pdf.text(noteLines, 23, y);

    addPageNumber(pdf, pageNumber);
    pdf.save("skin-lesion-analysis-report.pdf");
}
