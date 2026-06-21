import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen, Mail, KeyRound, ArrowLeft } from "lucide-react";
import toast from "react-hot-toast";
import useAuthStore from "../../stores/authStore";
import { authAPI } from "../../services/api";

export default function Login() {
  const [mode, setMode] = useState("password"); // "password" | "otp-send" | "otp-verify"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [otpEmail, setOtpEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  // Password login
  const handlePasswordLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const user = await login(email, password);
      toast.success(`Welcome back, ${user.first_name}!`);
      navigate(user.role === "admin" ? "/admin" : user.role === "lecturer" ? "/lecturer" : "/dashboard");
    } catch {
      toast.error("Invalid email or password");
    }
    setLoading(false);
  };

  // Send OTP
  const handleSendOTP = async (e) => {
    e.preventDefault();
    if (!otpEmail) { toast.error("Enter your email"); return; }
    setLoading(true);
    try {
      await authAPI.sendOTP({ email: otpEmail });
      toast.success("OTP sent to your email!");
      setMode("otp-verify");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to send OTP");
    }
    setLoading(false);
  };

  // Verify OTP
  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    if (!otp || otp.length !== 6) { toast.error("Enter the 6-digit OTP"); return; }
    setLoading(true);
    try {
      const { data } = await authAPI.verifyOTP({ email: otpEmail, otp });
      // Store tokens and user
      localStorage.setItem("tokens", JSON.stringify(data.tokens));
      localStorage.setItem("user", JSON.stringify(data.user));
      useAuthStore.setState({ user: data.user, tokens: data.tokens });
      toast.success(`Welcome, ${data.user.first_name}!`);
      navigate(data.user.role === "admin" ? "/admin" : data.user.role === "lecturer" ? "/lecturer" : "/dashboard");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid OTP");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 to-primary-900 items-center justify-center p-12">
        <div className="text-white max-w-md">
          <BookOpen size={48} className="mb-6" />
          <h1 className="text-4xl font-bold mb-4">Podar LMS</h1>
          <p className="text-primary-100 text-lg leading-relaxed">
            A modern learning management system for students, lecturers, and administrators.
          </p>
        </div>
      </div>

      {/* Form */}
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-sm">
          <div className="lg:hidden flex items-center gap-2 mb-8">
            <BookOpen size={28} className="text-primary-600" />
            <span className="text-2xl font-bold text-gray-900">Podar LMS</span>
          </div>

          {/* ─── Password Login ─── */}
          {mode === "password" && (
            <>
              <h2 className="text-2xl font-bold text-gray-900 mb-1">Sign in</h2>
              <p className="text-gray-500 mb-6">Enter your credentials to continue</p>
              <form onSubmit={handlePasswordLogin} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" className="input" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <input type="password" className="input" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" disabled={loading} className="btn-primary w-full">
                  {loading ? "Signing in..." : "Sign in"}
                </button>
              </form>

              {/* Divider */}
              <div className="flex items-center gap-3 my-5">
                <div className="flex-1 h-px bg-gray-200"></div>
                <span className="text-xs text-gray-400 uppercase">or</span>
                <div className="flex-1 h-px bg-gray-200"></div>
              </div>

              {/* OTP Login Button */}
              <button
                onClick={() => setMode("otp-send")}
                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border-2 border-primary-200 text-primary-700 font-medium hover:bg-primary-50 transition"
              >
                <Mail size={18} />
                Sign in with Email OTP
              </button>

              <p className="text-center text-sm text-gray-500 mt-6">
                Don't have an account? <Link to="/register" className="text-primary-600 font-medium hover:underline">Sign up</Link>
              </p>
            </>
          )}

          {/* ─── OTP: Enter Email ─── */}
          {mode === "otp-send" && (
            <>
              <button onClick={() => setMode("password")} className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4">
                <ArrowLeft size={16} /> Back to password login
              </button>
              <h2 className="text-2xl font-bold text-gray-900 mb-1">Email OTP Login</h2>
              <p className="text-gray-500 mb-6">We'll send a 6-digit code to your email</p>
              <form onSubmit={handleSendOTP} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email address</label>
                  <input type="email" className="input" placeholder="you@example.com" value={otpEmail}
                    onChange={(e) => setOtpEmail(e.target.value)} required autoFocus />
                </div>
                <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2">
                  <Mail size={18} />
                  {loading ? "Sending..." : "Send OTP"}
                </button>
              </form>
            </>
          )}

          {/* ─── OTP: Enter Code ─── */}
          {mode === "otp-verify" && (
            <>
              <button onClick={() => setMode("otp-send")} className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4">
                <ArrowLeft size={16} /> Change email
              </button>
              <h2 className="text-2xl font-bold text-gray-900 mb-1">Enter OTP</h2>
              <p className="text-gray-500 mb-6">
                We sent a 6-digit code to <span className="font-medium text-gray-800">{otpEmail}</span>
              </p>
              <form onSubmit={handleVerifyOTP} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">6-digit OTP</label>
                  <input type="text" className="input text-center text-2xl tracking-[0.5em] font-mono"
                    maxLength={6} placeholder="000000" value={otp}
                    onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
                    required autoFocus />
                </div>
                <button type="submit" disabled={loading || otp.length !== 6} className="btn-primary w-full flex items-center justify-center gap-2">
                  <KeyRound size={18} />
                  {loading ? "Verifying..." : "Verify & Sign in"}
                </button>
              </form>
              <button onClick={handleSendOTP} disabled={loading}
                className="w-full text-center text-sm text-primary-600 hover:underline mt-4">
                Didn't receive it? Resend OTP
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
