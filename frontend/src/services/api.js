
const API_BASE_URL = (
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

// Get the authentication token
function getAuthToken() {
    return sessionStorage.getItem("access_token");
}

// Handle API responses
async function parseResponse(response, fallbackMessage) {
    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error("The server returned an invalid response.");
    }

    if (!response.ok) {
        throw new Error(
            data?.detail ||
            data?.message ||
            fallbackMessage
        );
    }

    return data;
}

// Register a new user
export async function registerUser(name, email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, password })
    });

    return parseResponse(response, "Could not create your account.");
}

// Log in a user
export async function loginUser(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await parseResponse(
        response,
        "Invalid email or password."
    );

    if (!data.access_token) {
        throw new Error("No access token was returned.");
    }

    sessionStorage.setItem("access_token", data.access_token);

    if (data.user) {
        sessionStorage.setItem(
            "current_user",
            JSON.stringify(data.user)
        );
    }

    return data.user;
}

// Get the currently logged-in user
export async function getCurrentUser() {
    const token = getAuthToken();

    if (!token) {
        return null;
    }

    const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        logoutUser();
        return null;
    }

    const data = await parseResponse(
        response,
        "Could not verify the login session."
    );

    if (data.user) {
        sessionStorage.setItem(
            "current_user",
            JSON.stringify(data.user)
        );
        return data.user;
    }

    return data;
}

// Get the stored user
export function getStoredUser() {
    try {
        return JSON.parse(
            sessionStorage.getItem("current_user") || "null"
        );
    } catch {
        return null;
    }
}

// Log out the user
export function logoutUser() {
    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("current_user");
}

// Analyze a skin lesion image
export async function analyzeImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/analyze/`, {
        method: "POST",
        body: formData
    });

    return parseResponse(response, "Image analysis failed.");
}

// Save a successful analysis to history
export async function saveAnalysisHistory(analysisData) {
    const token = getAuthToken();

    if (!token) {
        throw new Error("Please log in before saving analysis history.");
    }

    const response = await fetch(`${API_BASE_URL}/history/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(analysisData)
    });

    return parseResponse(response, "Could not save analysis history.");
}

// Retrieve analysis history
export async function getAnalysisHistory() {
    const token = getAuthToken();

    if (!token) {
        throw new Error("Please log in to view analysis history.");
    }

    const response = await fetch(`${API_BASE_URL}/history/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    return parseResponse(response, "Could not retrieve analysis history.");
}

// Delete all analysis history
export async function clearAnalysisHistory() {
    const token = getAuthToken();

    if (!token) {
        throw new Error("Please log in before clearing analysis history.");
    }

    const response = await fetch(`${API_BASE_URL}/history/`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    return parseResponse(response, "Could not clear analysis history.");
}

// Retrieve a single analysis record
export async function getAnalysisDetail(historyId) {
    const token = getAuthToken();

    if (!token) {
        throw new Error("Please log in to view analysis history.");
    }

    const response = await fetch(
        `${API_BASE_URL}/history/${encodeURIComponent(historyId)}`,
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    return parseResponse(response, "Could not retrieve the analysis record.");
}

// Delete a single analysis record
export async function deleteAnalysisHistory(historyId) {
    const token = getAuthToken();

    if (!token) {
        throw new Error("Please log in before deleting analysis history.");
    }

    if (!historyId) {
        throw new Error(
            "Missing history record ID. Refresh the history page and try again."
        );
    }

    const response = await fetch(
        `${API_BASE_URL}/history/${encodeURIComponent(historyId)}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    return parseResponse(
        response,
        "Could not delete the analysis record."
    );
}
