import { useQuery } from "@tanstack/react-query";
import { BookOpen, ClipboardList, Award, Clock } from "lucide-react";
import { courseAPI, assignmentAPI } from "../../services/api";
import StatCard from "../../components/common/StatCard";
import CourseCard from "../../components/common/CourseCard";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function Dashboard() {
  const { data: enrollments, isLoading } = useQuery({
    queryKey: ["myEnrollments"],
    queryFn: () => courseAPI.myEnrollments().then((r) => r.data.results || r.data),
  });

  const { data: submissions } = useQuery({
    queryKey: ["mySubmissions"],
    queryFn: () => assignmentAPI.mySubmissions().then((r) => r.data.results || r.data),
  });

  if (isLoading) return <Spinner />;

  const courses = enrollments || [];
  const completed = courses.filter((e) => e.completed).length;
  const pending = (submissions || []).filter((s) => s.status === "submitted").length;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Enrolled courses" value={courses.length} icon={BookOpen} color="primary" />
        <StatCard label="Completed" value={completed} icon={Award} color="green" />
        <StatCard label="Pending submissions" value={pending} icon={ClipboardList} color="amber" />
        <StatCard label="In progress" value={courses.length - completed} icon={Clock} color="red" />
      </div>

      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">My courses</h2>
        {courses.length === 0 ? (
          <EmptyState title="No courses yet" message="Browse the catalog to get started." />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {courses.map((enrollment) => (
              <CourseCard key={enrollment.id} course={{ ...enrollment.course, progress_percentage: enrollment.progress_percentage }} enrolled />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
