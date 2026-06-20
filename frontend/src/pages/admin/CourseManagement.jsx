import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, Eye, Users } from "lucide-react";
import { courseAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function CourseManagement() {
  const [search, setSearch] = useState("");
  const [level, setLevel] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["adminCourses", search, level],
    queryFn: () => courseAPI.list({ search, level: level || undefined }).then((r) => r.data.results || r.data),
  });

  const courses = data || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Course management</h1>
        <span className="text-sm text-gray-500">{courses.length} courses</span>
      </div>

      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input className="input pl-10" placeholder="Search courses..."
            value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <select className="input w-auto" value={level} onChange={(e) => setLevel(e.target.value)}>
          <option value="">All levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      {isLoading ? <Spinner /> : !courses.length ? (
        <EmptyState title="No courses" />
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="pb-3 font-medium">Course</th>
                <th className="pb-3 font-medium">Instructor</th>
                <th className="pb-3 font-medium text-center">Level</th>
                <th className="pb-3 font-medium text-center">Students</th>
                <th className="pb-3 font-medium text-center">Lessons</th>
                <th className="pb-3 font-medium text-right">Price</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((c) => (
                <tr key={c.id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-3">
                    <div>
                      <p className="font-medium text-gray-900">{c.title}</p>
                      <p className="text-xs text-gray-400">{c.code}</p>
                    </div>
                  </td>
                  <td className="py-3 text-gray-500">{c.lecturer_name}</td>
                  <td className="py-3 text-center capitalize">
                    <span className="badge-blue">{c.level}</span>
                  </td>
                  <td className="py-3 text-center">
                    <span className="flex items-center justify-center gap-1 text-gray-600">
                      <Users size={14} /> {c.enrolled_count || 0}
                    </span>
                  </td>
                  <td className="py-3 text-center text-gray-600">{c.total_lessons || 0}</td>
                  <td className="py-3 text-right font-medium">
                    {c.is_free ? <span className="badge-green">Free</span> : `₹${c.price}`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
