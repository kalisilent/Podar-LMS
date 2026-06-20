import { useQuery } from "@tanstack/react-query";
import { BookOpen, Users, ClipboardList, HelpCircle } from "lucide-react";
import { courseAPI, assignmentAPI, quizAPI } from "../../services/api";
import StatCard from "../../components/common/StatCard";
import CourseCard from "../../components/common/CourseCard";
import Spinner from "../../components/common/Spinner";

export default function LecturerDashboard() {
  const { data: courses, isLoading } = useQuery({
    queryKey: ["lecturerCourses"],
    queryFn: () => courseAPI.list().then((r) => r.data.results || r.data),
  });

  const { data: assignments } = useQuery({
    queryKey: ["lecturerAssignments"],
    queryFn: () => assignmentAPI.list().then((r) => r.data.results || r.data),
  });

  if (isLoading) return <Spinner />;

  const totalStudents = (courses || []).reduce((acc, c) => acc + (c.enrolled_count || 0), 0);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Lecturer dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="My courses" value={(courses || []).length} icon={BookOpen} color="primary" />
        <StatCard label="Total students" value={totalStudents} icon={Users} color="green" />
        <StatCard label="Assignments" value={(assignments || []).length} icon={ClipboardList} color="amber" />
        <StatCard label="Pending grading" value={(assignments || []).filter((a) => a.submissions_count > 0).length} icon={HelpCircle} color="red" />
      </div>

      <h2 className="text-lg font-semibold text-gray-900">My courses</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {(courses || []).map((c) => (
          <CourseCard key={c.id} course={c} />
        ))}
      </div>
    </div>
  );
}
