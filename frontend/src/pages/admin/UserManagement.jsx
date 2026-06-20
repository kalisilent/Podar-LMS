import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, Shield, GraduationCap, BookOpen } from "lucide-react";
import { authAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function UserManagement() {
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["users", search, roleFilter],
    queryFn: () => authAPI.users({ search, role: roleFilter || undefined }).then((r) => r.data.results || r.data),
  });

  const users = data || [];
  const roleIcon = { student: GraduationCap, lecturer: BookOpen, admin: Shield };
  const roleBadge = { student: "badge-blue", lecturer: "badge-green", admin: "badge-red" };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">User management</h1>

      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input className="input pl-10" placeholder="Search by name or email..."
            value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <select className="input w-auto" value={roleFilter} onChange={(e) => setRoleFilter(e.target.value)}>
          <option value="">All roles</option>
          <option value="student">Students</option>
          <option value="lecturer">Lecturers</option>
          <option value="admin">Admins</option>
        </select>
      </div>

      {isLoading ? <Spinner /> : !users.length ? (
        <EmptyState title="No users found" />
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="pb-3 font-medium">User</th>
                <th className="pb-3 font-medium">Email</th>
                <th className="pb-3 font-medium text-center">Role</th>
                <th className="pb-3 font-medium text-center">Verified</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const Icon = roleIcon[u.role] || Shield;
                return (
                  <tr key={u.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xs font-semibold">
                          {u.first_name?.[0]}{u.last_name?.[0]}
                        </div>
                        <span className="font-medium text-gray-900">{u.first_name} {u.last_name}</span>
                      </div>
                    </td>
                    <td className="py-3 text-gray-500">{u.email}</td>
                    <td className="py-3 text-center">
                      <span className={`${roleBadge[u.role] || "badge-blue"} capitalize`}>{u.role}</span>
                    </td>
                    <td className="py-3 text-center">
                      {u.is_verified ? (
                        <span className="text-green-500 text-xs">✓ Verified</span>
                      ) : (
                        <span className="text-gray-400 text-xs">Pending</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
