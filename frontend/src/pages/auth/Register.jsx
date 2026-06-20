import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import toast from "react-hot-toast";
import useAuthStore from "../../stores/authStore";

export default function Register() {
  const [form, setForm] = useState({ email: "", username: "", first_name: "", last_name: "", password: "", password2: "", role: "student" });
  const { register, loading } = useAuthStore();
  const navigate = useNavigate();
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.password2) { toast.error("Passwords don't match"); return; }
    try {
      await register(form);
      toast.success("Account created!");
      navigate("/dashboard");
    } catch (err) {
      const msg = err.response?.data;
      toast.error(typeof msg === "string" ? msg : Object.values(msg || {}).flat().join(", ") || "Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gray-50">
      <div className="w-full max-w-md">
        <div className="flex items-center gap-2 mb-8 justify-center">
          <BookOpen size={28} className="text-primary-600" />
          <span className="text-2xl font-bold text-gray-900">Podar LMS</span>
        </div>
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Create account</h2>
          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">First name</label>
                <input className="input" value={form.first_name} onChange={set("first_name")} required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Last name</label>
                <input className="input" value={form.last_name} onChange={set("last_name")} required />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input className="input" value={form.username} onChange={set("username")} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input type="email" className="input" value={form.email} onChange={set("email")} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select className="input" value={form.role} onChange={set("role")}>
                <option value="student">Student</option>
                <option value="lecturer">Lecturer</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input type="password" className="input" value={form.password} onChange={set("password")} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm password</label>
              <input type="password" className="input" value={form.password2} onChange={set("password2")} required />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
              {loading ? "Creating..." : "Create account"}
            </button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-4">
            Already have an account? <Link to="/login" className="text-primary-600 font-medium hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
