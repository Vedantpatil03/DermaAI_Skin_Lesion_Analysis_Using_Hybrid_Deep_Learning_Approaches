import { useEffect, useRef, useState } from "react";

function ImageUpload({ onFileSelect, resetSignal = 0 }) {
    const fileInputRef = useRef(null);

    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);

    useEffect(() => {
        setSelectedFile(null);
        setPreviewUrl(null);

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    }, [resetSignal]);

    const handleFile = (file) => {
        if (!file) {
            return;
        }

        if (!file.type.startsWith("image/")) {
            return;
        }

        setSelectedFile(file);

        const url = URL.createObjectURL(file);
        setPreviewUrl(url);

        onFileSelect(file);
    };

    const handleInputChange = (event) => {
        const file = event.target.files?.[0];

        handleFile(file);
    };

    const handleDrop = (event) => {
        event.preventDefault();

        setIsDragging(false);

        const file = event.dataTransfer.files?.[0];

        handleFile(file);
    };

    const handleDragOver = (event) => {
        event.preventDefault();

        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleBrowse = () => {
        fileInputRef.current?.click();
    };

    const handleRemove = () => {
        setSelectedFile(null);
        setPreviewUrl(null);

        onFileSelect(null);

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    return (
        <div className="image-upload">
            {!selectedFile && (
                <div
                    className={
                        isDragging
                            ? "upload-zone dragging"
                            : "upload-zone"
                    }
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                >
                    <div className="upload-icon">
                        ↑
                    </div>

                    <h3>
                        Upload Skin Lesion Image
                    </h3>

                    <p>
                        Drag and drop an image here,
                        or browse from your device.
                    </p>

                    <button
                        type="button"
                        className="secondary-button"
                        onClick={handleBrowse}
                    >
                        Browse Image
                    </button>

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        onChange={handleInputChange}
                        hidden
                    />

                    <span className="upload-note">
                        Supported formats: JPG, PNG, WEBP
                    </span>
                </div>
            )}

            {selectedFile && previewUrl && (
                <div className="preview-container">
                    <div className="preview-header">
                        <div>
                            <p className="section-label">
                                SELECTED IMAGE
                            </p>

                            <h3>
                                Ready for analysis
                            </h3>
                        </div>

                        <button
                            type="button"
                            className="remove-button"
                            onClick={handleRemove}
                        >
                            Remove
                        </button>
                    </div>

                    <div className="image-preview">
                        <img
                            src={previewUrl}
                            alt="Selected skin lesion"
                        />
                    </div>

                    <div className="file-information">
                        <strong>
                            {selectedFile.name}
                        </strong>

                        <span>
                            {(
                                selectedFile.size /
                                1024
                            ).toFixed(1)}{" "}
                            KB
                        </span>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ImageUpload;