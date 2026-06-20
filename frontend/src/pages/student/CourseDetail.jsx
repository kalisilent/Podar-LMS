import { useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Play, FileText, Link2, CheckCircle, Circle, Lock } from "lucide-react";
import toast from "react-hot-toast";
import { courseAPI } from "../../services/api";
import useAuthStore from "../../stores/authStore";
import Spinner from "../../components/common/Spinner";

export default function CourseDetail() {
  const { slug } = useParams();
  const user = useAuthStore((s) => s.user);
  const qc = useQueryClient();

  const { data: course, isLoading } = useQuery({
    queryKey: ["course", slug],
    queryFn: () => courseAPI.detail(slug).then((r) => r.data),
  });

  const { data: progress } = useQuery({
    queryKey: ["progress", slug],
    queryFn: () => courseAPI.progress(slug).then((r) => r.data).catch(() => null),
    enabled: user?.role === "student",
  });

  const enrollMutation = useMutation({
    mutationFn: () => courseAPI.enroll(slug),
    onSuccess: () => { toast.success("Enrolled!"); qc.invalidateQueries(["course", slug]); },
    onError: (e) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const completeMutation = useMutation({
    mutationFn: (lessonId) => courseAPI.markComplete(lessonId),
    onSuccess: () => qc.invalidateQueries(["progress", slug]),
  });

  if (isLoading) return <Spinner />;
  if (!course) return <p>Course not found</p>;

  const completedLessons = new Set(progress?.completed_lessons || []);
  const isEnrolled = progress !== null && progress !== undefined;
  const lessonIcon = { video: Play, pdf: FileText, text: FileText, link: Link2 };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <span className="badge-blue mb-2">{course.level}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{course.title}</h1>
            <p className="text-gray-500 mt-1">{course.code}</p>
            <p className="text-sm text-gray-600 mt-3">{course.description}</p>
            <p className="text-sm text-gray-500 mt-2">
              By {course.lecturer?.first_name} {course.lecturer?.last_name} · {course.enrolled_count} students
            </p>
          </div>
          {user?.role === "student" && !isEnrolled && (
            <div className="flex-shrink-0">
              <button onClick={() => enrollMutation.mutate()} className="btn-primary">
                {course.is_free ? "Enroll free" : `Enroll — ₹${course.price}`}
              </button>
            </div>
          )}
        </div>

        {progress && (
          <div className="mt-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-500">Progress</span>
              <span className="font-medium text-primary-600">{progress.progress_percentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-primary-500 h-2 rounded-full transition-all" style={{ width: `${progress.progress_percentage}%` }} />
            </div>
          </div>
        )}
      </div>

      {/* Sections & Lessons */}
      {course.sections?.map((section) => (
        <div key={section.id} className="card">
          <h2 className="font-semibold text-gray-900 mb-3">{section.title}</h2>
          {section.description && <p className="text-sm text-gray-500 mb-3">{section.description}</p>}
          <div className="space-y-1">
            {section.lessons?.map((lesson) => {
              const Icon = lessonIcon[lesson.lesson_type] || FileText;
              const done = completedLessons.has(lesson.id);
              return (
                <div
                  key={lesson.id}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-50 transition cursor-pointer group"
                  onClick={() => isEnrolled && !done && completeMutation.mutate(lesson.id)}
                >
                  {done ? (
                    <CheckCircle size={18} className="text-green-500" />
                  ) : isEnrolled ? (
                    <Circle size={18} className="text-gray-300 group-hover:text-primary-400" />
                  ) : (
                    <Lock size={18} className="text-gray-300" />
                  )}
                  <Icon size={16} className="text-gray-400" />
                  <span className="flex-1 text-sm text-gray-700">{lesson.title}</span>
                  {lesson.duration_minutes > 0 && (
                    <span className="text-xs text-gray-400">{lesson.duration_minutes} min</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
