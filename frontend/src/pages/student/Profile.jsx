import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Save } from "lucide-react";
import toast from "react-hot-toast";
import useAuthStore from "../../stores/authStore";
import { authAPI } from "../../services/api";

export default function Profile() {
  const { user, updateUser } = useAuthStore();
  const [form, setForm] = useState({
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    phone: user?.phone || "",
    bio: user?.bio || "",
  });

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const mutation = useMutation({
    mutationFn: (data) => authAPI.updateProfile(data),
    onSuccess: (res) => { updateUser(res.data); toast.success("Profile updated"); },
    onError: () => toast.error("Update failed"),
  });

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Profile</h1>

      <div className="card">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xl font-bold">
            {user?.first_name?.[0]}{user?.last_name?.[0]}
          </div>
          <div>
            <p className="font-semibold text-gray-900">{user?.first_name} {user?.last_name}</p>
            <p className="text-sm text-gray-500">{user?.email}</p>
            <span className="badge-blue mt-1 capitalize">{user?.role}</span>
          </div>
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">First name</label>
              <input className="input" value={form.first_name} onChange={set("first_name")} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Last name</label>
              <input className="input" value={form.last_name} onChange={set("last_name")} />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
            <input className="input" value={form.phone} onChange={set("phone")} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
            <textarea className="input" rows={3} value={form.bio} onChange={set("bio")} />
          </div>
          <button onClick={() => mutation.mutate(form)} className="btn-primary flex items-center gap-1.5">
            <Save size={16} /> Save changes
          </button>
        </div>
      </div>
    </div>
  );
}
