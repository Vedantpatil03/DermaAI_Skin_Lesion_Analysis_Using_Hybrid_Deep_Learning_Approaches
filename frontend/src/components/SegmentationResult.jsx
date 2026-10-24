import { useEffect, useRef, useState } from "react";

function SegmentationResult({
    originalImage,
    maskBase64,
    lesionArea
}) {
    const canvasRef = useRef(null);

    const [isRendering, setIsRendering] =
        useState(false);

    const [renderError, setRenderError] =
        useState("");


    useEffect(() => {

        if (!originalImage || !maskBase64) {
            return;
        }

        const canvas = canvasRef.current;

        if (!canvas) {
            return;
        }

        const context = canvas.getContext("2d");

        if (!context) {
            setRenderError(
                "Lesion visualization is not supported by this browser."
            );
            return;
        }

        setIsRendering(true);
        setRenderError("");


        const original = new Image();
        const mask = new Image();


        // ========================================
        // LOAD ORIGINAL IMAGE
        // ========================================

        original.onload = () => {

            const width = original.naturalWidth;
            const height = original.naturalHeight;

            canvas.width = width;
            canvas.height = height;

            context.clearRect(
                0,
                0,
                width,
                height
            );

            context.drawImage(
                original,
                0,
                0,
                width,
                height
            );


            // ========================================
            // LOAD MASK
            // ========================================

            mask.onload = () => {

                const maskCanvas =
                    document.createElement("canvas");

                maskCanvas.width = width;
                maskCanvas.height = height;

                const maskContext =
                    maskCanvas.getContext("2d");

                if (!maskContext) {
                    setRenderError(
                        "Unable to process the segmentation mask."
                    );
                    setIsRendering(false);
                    return;
                }

                maskContext.drawImage(
                    mask,
                    0,
                    0,
                    width,
                    height
                );

                const maskData =
                    maskContext.getImageData(
                        0,
                        0,
                        width,
                        height
                    );


                // ========================================
                // MASK CHECK
                // ========================================

                const isLesionPixel = (
                    x,
                    y
                ) => {

                    if (
                        x < 0 ||
                        y < 0 ||
                        x >= width ||
                        y >= height
                    ) {
                        return false;
                    }

                    const index =
                        (y * width + x) * 4;

                    return (
                        maskData.data[index] > 128
                    );
                };


                // ========================================
                // FIND BOUNDING BOX
                // ========================================

                let minX = width;
                let minY = height;
                let maxX = -1;
                let maxY = -1;


                for (
                    let y = 0;
                    y < height;
                    y++
                ) {

                    for (
                        let x = 0;
                        x < width;
                        x++
                    ) {

                        if (
                            isLesionPixel(
                                x,
                                y
                            )
                        ) {

                            minX =
                                Math.min(
                                    minX,
                                    x
                                );

                            minY =
                                Math.min(
                                    minY,
                                    y
                                );

                            maxX =
                                Math.max(
                                    maxX,
                                    x
                                );

                            maxY =
                                Math.max(
                                    maxY,
                                    y
                                );
                        }
                    }
                }


                // ========================================
                // CREATE OVERLAY
                // ========================================

                const overlayCanvas =
                    document.createElement("canvas");

                overlayCanvas.width = width;
                overlayCanvas.height = height;

                const overlayContext =
                    overlayCanvas.getContext("2d");

                if (!overlayContext) {
                    setRenderError(
                        "Unable to create lesion overlay."
                    );
                    setIsRendering(false);
                    return;
                }


                const overlay =
                    overlayContext.createImageData(
                        width,
                        height
                    );


                // ========================================
                // LESION FILL + CONTOUR
                // ========================================

                for (
                    let y = 0;
                    y < height;
                    y++
                ) {

                    for (
                        let x = 0;
                        x < width;
                        x++
                    ) {

                        if (
                            !isLesionPixel(
                                x,
                                y
                            )
                        ) {
                            continue;
                        }


                        const index =
                            (y * width + x) * 4;


                        const boundary =
                            !isLesionPixel(x - 1, y) ||
                            !isLesionPixel(x + 1, y) ||
                            !isLesionPixel(x, y - 1) ||
                            !isLesionPixel(x, y + 1);


                        if (boundary) {

                            // Cyan contour

                            overlay.data[index] =
                                14;

                            overlay.data[index + 1] =
                                165;

                            overlay.data[index + 2] =
                                233;

                            overlay.data[index + 3] =
                                255;

                        } else {

                            // Transparent cyan fill

                            overlay.data[index] =
                                14;

                            overlay.data[index + 1] =
                                165;

                            overlay.data[index + 2] =
                                233;

                            overlay.data[index + 3] =
                                70;
                        }
                    }
                }


                overlayContext.putImageData(
                    overlay,
                    0,
                    0
                );


                // ========================================
                // DRAW OVER ORIGINAL
                // ========================================

                context.drawImage(
                    overlayCanvas,
                    0,
                    0
                );


                // ========================================
                // BOUNDING BOX
                // ========================================

                if (maxX >= 0) {

                    const padding =
                        Math.max(
                            8,
                            Math.round(
                                width * 0.01
                            )
                        );


                    const boxX =
                        Math.max(
                            0,
                            minX - padding
                        );

                    const boxY =
                        Math.max(
                            0,
                            minY - padding
                        );

                    const boxRight =
                        Math.min(
                            width,
                            maxX + padding
                        );

                    const boxBottom =
                        Math.min(
                            height,
                            maxY + padding
                        );


                    const boxWidth =
                        boxRight - boxX;

                    const boxHeight =
                        boxBottom - boxY;


                    context.save();


                    // White outline

                    context.strokeStyle =
                        "rgba(255,255,255,0.95)";

                    context.lineWidth = 5;

                    context.setLineDash([
                        14,
                        8
                    ]);

                    context.strokeRect(
                        boxX,
                        boxY,
                        boxWidth,
                        boxHeight
                    );


                    // Cyan outline

                    context.strokeStyle =
                        "#0ea5e9";

                    context.lineWidth = 2;

                    context.setLineDash([
                        14,
                        8
                    ]);

                    context.strokeRect(
                        boxX,
                        boxY,
                        boxWidth,
                        boxHeight
                    );


                    // ========================================
                    // LABEL
                    // ========================================

                    const label =
                        "AI-Detected Lesion Region";

                    const labelFontSize =
                        Math.max(
                            14,
                            Math.min(
                                22,
                                width * 0.018
                            )
                        );


                    context.font =
                        `600 ${labelFontSize}px Arial`;


                    const textWidth =
                        context.measureText(
                            label
                        ).width;


                    const labelPadding = 10;

                    const labelWidth =
                        textWidth +
                        labelPadding * 2;

                    const labelHeight =
                        labelFontSize +
                        labelPadding * 2;


                    let labelX = boxX;

                    let labelY =
                        boxY -
                        labelHeight -
                        6;


                    // Keep label inside canvas

                    if (labelY < 0) {
                        labelY =
                            boxY + 6;
                    }


                    if (
                        labelX +
                            labelWidth >
                        width
                    ) {

                        labelX =
                            width -
                            labelWidth -
                            6;
                    }


                    context.fillStyle =
                        "rgba(15,23,42,0.92)";


                    context.fillRect(
                        labelX,
                        labelY,
                        labelWidth,
                        labelHeight
                    );


                    context.fillStyle =
                        "#ffffff";


                    context.fillText(
                        label,
                        labelX +
                            labelPadding,
                        labelY +
                            labelFontSize +
                            4
                    );


                    context.restore();
                }


                setIsRendering(false);
            };


            mask.onerror = () => {

                setRenderError(
                    "The segmentation mask could not be displayed."
                );

                setIsRendering(false);
            };


            mask.src =
                `data:image/png;base64,${maskBase64}`;
        };


        original.onerror = () => {

            setRenderError(
                "The uploaded image could not be displayed."
            );

            setIsRendering(false);
        };


        original.src = originalImage;


    }, [
        originalImage,
        maskBase64
    ]);


    // ========================================
    // LESION AREA
    // ========================================

    const formattedArea =
        lesionArea !== undefined &&
        lesionArea !== null
            ? `${Number(
                lesionArea
            ).toFixed(2)}%`
            : "N/A";


    // ========================================
    // EMPTY STATE
    // ========================================

    if (
        !originalImage ||
        !maskBase64
    ) {

        return (
            <div className="segmentation-result">

                <div className="segmentation-empty">

                    <strong>
                        Lesion visualization unavailable
                    </strong>

                    <p>
                        Segmentation data is not available
                        for this analysis.
                    </p>

                </div>

            </div>
        );
    }


    return (

        <div className="segmentation-result">

            {/* ========================================
                VISUALIZATION
            ======================================== */}

            <div className="segmentation-image-wrapper">

                {isRendering && (

                    <div className="segmentation-loading">

                        <div className="loading-spinner"></div>

                        <span>
                            Rendering lesion region...
                        </span>

                    </div>
                )}


                {renderError && (

                    <div className="segmentation-empty">

                        <strong>
                            Visualization unavailable
                        </strong>

                        <p>
                            {renderError}
                        </p>

                    </div>
                )}


                {!renderError && (

                    <canvas
                        ref={canvasRef}
                        className="segmentation-canvas"
                    />

                )}

            </div>


            {/* ========================================
                LEGEND
            ======================================== */}

            {!renderError && (

                <div className="segmentation-legend">

                    <div className="legend-item">

                        <span className="legend-marker lesion-marker"></span>

                        <span>
                            AI-detected lesion region
                        </span>

                    </div>


                    <div className="legend-item">

                        <span className="legend-box-marker"></span>

                        <span>
                            Detected region boundary
                        </span>

                    </div>

                </div>
            )}


            {/* ========================================
                METRIC
            ======================================== */}

            <div className="segmentation-info">

                <div className="segmentation-metric">

                    <span>
                        Estimated Lesion Area
                    </span>

                    <strong>
                        {formattedArea}
                    </strong>

                </div>

            </div>

        </div>
    );
}


export default SegmentationResult;