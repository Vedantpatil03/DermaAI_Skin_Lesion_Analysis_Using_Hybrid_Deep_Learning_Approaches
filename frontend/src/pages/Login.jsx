import { useState } from "react";

import { loginUser, registerUser } from "../services/api";

function PasswordEyeIcon() {
    return (
        <svg
            viewBox="0 0 24 24"
            width="18"
            height="18"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
        >
            <path d="M2.5 12s3.5-5 9.5-5 9.5 5 9.5 5-3.5 5-9.5 5-9.5-5-9.5-5Z" />
            <circle cx="12" cy="12" r="2.5" />
        </svg>
    );
}

function Login({ onLogin }) {
    const [isRegistering, setIsRegistering] = useState(false);
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [isPasswordVisible, setIsPasswordVisible] = useState(false);
    const [isConfirmPasswordVisible, setIsConfirmPasswordVisible] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError("");
        setSuccess("");

        if (isRegistering && password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setIsSubmitting(true);

        try {
            if (isRegistering) {
                await registerUser(name.trim(), email.trim(), password);
                setIsRegistering(false);
                setPassword("");
                setConfirmPassword("");
                setSuccess("Account created successfully. You can now sign in.");
            } else {
                const user = await loginUser(email.trim(), password);
                onLogin(user);
            }
        } catch (loginError) {
            setError(
                loginError?.message ||
                (
                    isRegistering
                        ? "Could not create your account. Please try again."
                        : "Could not sign in. Please check your details and try again."
                )
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const toggleMode = () => {
        setIsRegistering((currentMode) => !currentMode);
        setError("");
        setSuccess("");
    };

    return (
        <main className="login-page">
            <section className="login-card" aria-labelledby="login-title">
                <div className="login-brand">
                    <img
                        src="/dermaailogo.png"
                        alt="DermaAI logo"
                        className="login-logo"
                    />
                    <p className="section-label">DERMAAI CLINICAL WORKSPACE</p>
                
                </div>

                <h1 id="login-title">
                    {isRegistering ? "Create your account" : "Welcome back"}
                </h1>
                <p className="login-subtitle">
                    {isRegistering
                        ? "Register as a doctor to securely save and access your analysis history."
                        : "Sign in to access your skin lesion analyses and saved history."}
                </p>

                {error && (
                    <div className="error-message login-error" role="alert">
                        {error}
                    </div>
                )}

                {success && (
                    <div className="success-message login-success" role="status">
                        {success}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="login-form">
                    {isRegistering && (
                        <>
                            <label htmlFor="login-name">Full name</label>
                            <input
                                id="login-name"
                                type="text"
                                value={name}
                                onChange={(event) => setName(event.target.value)}
                                autoComplete="name"
                                minLength="2"
                                required
                            />
                        </>
                    )}

                    <label htmlFor="login-email">Email address</label>
                    <input
                        id="login-email"
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        autoComplete="email"
                        required
                    />

                    <label htmlFor="login-password">Password</label>
                    <div className="password-input-wrapper">
                        <input
                            id="login-password"
                            type={isPasswordVisible ? "text" : "password"}
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            autoComplete="current-password"
                            required
                        />
                        <button
                            type="button"
                            className="password-visibility-button"
                            aria-label={isPasswordVisible ? "Hide password" : "Show password"}
                            onClick={() => setIsPasswordVisible((isVisible) => !isVisible)}
                        >
                            <PasswordEyeIcon />
                        </button>
                    </div>

                    {isRegistering && (
                        <>
                            <label htmlFor="login-confirm-password">
                                Confirm Password
                            </label>
                            <div className="password-input-wrapper">
                                <input
                                    id="login-confirm-password"
                                    type={isConfirmPasswordVisible ? "text" : "password"}
                                    value={confirmPassword}
                                    onChange={(event) => setConfirmPassword(event.target.value)}
                                    autoComplete="new-password"
                                    required
                                />
                                <button
                                    type="button"
                                    className="password-visibility-button"
                                    aria-label={
                                        isConfirmPasswordVisible
                                            ? "Hide confirm password"
                                            : "Show confirm password"
                                    }
                                    onClick={() => setIsConfirmPasswordVisible((isVisible) => !isVisible)}
                                >
                                    <PasswordEyeIcon />
                                </button>
                            </div>
                        </>
                    )}

                    <button
                        type="submit"
                        className="primary-button login-submit"
                        disabled={isSubmitting}
                    >
                        {isSubmitting
                            ? (isRegistering ? "Creating account..." : "Signing in...")
                            : (isRegistering ? "Create account" : "Sign in")}
                    </button>
                </form>

                <p className="login-mode-switch">
                    {isRegistering
                        ? "Already have an account?"
                        : "New to DermaAI?"}
                    <button
                        type="button"
                        className="login-mode-button"
                        onClick={toggleMode}
                    >
                        {isRegistering ? "Sign in" : "Sign up"}
                    </button>
                </p>
            </section>
        </main>
    );
}

export default Login;
