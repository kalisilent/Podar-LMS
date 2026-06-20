import { Link } from "react-router-dom";
import { Users, BookOpen } from "lucide-react";

export default function CourseCard({ course, enrolled = false }) {
  return (
    <Link to={`/courses/${course.slug}`} className="card hover:shadow-md transition group block">
      {course.thumbnail ? (
        <img src={course.thumbnail} alt="" className="w-full h-40 object-cover rounded-lg mb-4" />
      ) : (
        <div className="w-full h-40 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg mb-4 flex items-center justify-center">
          <BookOpen size={40} className="text-white/80" />
        </div>
      )}
      <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 transition line-clamp-2">{course.title}</h3>
      <p className="text-sm text-gray-500 mt-1">{course.code} · {course.level}</p>
      <div className="flex items-center justify-between mt-3 text-sm text-gray-500">
        <span className="flex items-center gap-1"><Users size={14} />{course.enrolled_count || 0}</span>
        {course.is_free ? <span className="badge-green">Free</span> : <span className="font-semibold text-gray-900">₹{course.price}</span>}
      </div>
      {enrolled && course.progress_percentage !== undefined && (
        <div className="mt-3">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-gray-500">Progress</span>
            <span className="font-medium text-primary-600">{course.progress_percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div className="bg-primary-500 h-1.5 rounded-full transition-all" style={{ width: `${course.progress_percentage}%` }} />
          </div>
        </div>
      )}
    </Link>
  );
}
