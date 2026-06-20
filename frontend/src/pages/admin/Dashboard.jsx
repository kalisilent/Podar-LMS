import { useQuery } from "@tanstack/react-query";
import { Users, BookOpen, GraduationCap, IndianRupee } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { authAPI } from "../../services/api";
import StatCard from "../../components/common/StatCard";
import Spinner from "../../components/common/Spinner";

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"];

export default function AdminDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ["adminDashboard"],
    queryFn: () => authAPI.adminDashboard().then((r) => r.data),
  });

  if (isLoading) return <Spinner />;

  const roleData = [
    { name: "Students", value: data?.total_students || 0 },
    { name: "Lecturers", value: data?.total_lecturers || 0 },
    { name: "Admins", value: Math.max(0, (data?.total_users || 0) - (data?.total_students || 0) - (data?.total_lecturers || 0)) },
  ];

  // Placeholder monthly data — replace with real API data
  const monthlyData = [
    { month: "Jan", enrollments: 12 }, { month: "Feb", enrollments: 19 },
    { month: "Mar", enrollments: 28 }, { month: "Apr", enrollments: 35 },
    { month: "May", enrollments: 24 }, { month: "Jun", enrollments: 42 },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Admin dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total users" value={data?.total_users || 0} icon={Users} color="primary" />
        <StatCard label="Students" value={data?.total_students || 0} icon={GraduationCap} color="green" />
        <StatCard label="Courses" value={data?.total_courses || 0} icon={BookOpen} color="amber" />
        <StatCard label="Revenue" value={`₹${data?.total_revenue || 0}`} icon={IndianRupee} color="red" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Enrollment trend */}
        <div className="card">
          <h2 className="font-semibold text-gray-900 mb-4">Monthly enrollments</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="enrollments" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* User distribution */}
        <div className="card">
          <h2 className="font-semibold text-gray-900 mb-4">User distribution</h2>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={roleData} cx="50%" cy="50%" innerRadius={60} outerRadius={100}
                paddingAngle={4} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                {roleData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Quick stats */}
      <div className="card">
        <h2 className="font-semibold text-gray-900 mb-2">Recent activity</h2>
        <p className="text-sm text-gray-500">
          {data?.recent_enrollments || 0} new enrollments in the last 30 days
        </p>
      </div>
    </div>
  );
}
