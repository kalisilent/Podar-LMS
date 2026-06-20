import { useQuery } from "@tanstack/react-query";
import { Download } from "lucide-react";
import { resultAPI, reportAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function MyGrades() {
  const { data, isLoading } = useQuery({
    queryKey: ["gpa"],
    queryFn: () => resultAPI.gpa().then((r) => r.data),
  });

  const downloadReport = async () => {
    const res = await reportAPI.gradeReport();
    const url = URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = "grade_report.pdf";
    a.click();
  };

  if (isLoading) return <Spinner />;

  const results = data?.results || [];
  const remarkColor = { Pass: "badge-green", Fail: "badge-red" };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Grades</h1>
        <button onClick={downloadReport} className="btn-secondary text-sm flex items-center gap-1.5">
          <Download size={14} /> Download PDF
        </button>
      </div>

      <div className="card">
        <div className="text-center">
          <p className="text-sm text-gray-500">Cumulative GPA</p>
          <p className="text-4xl font-bold text-primary-600">{data?.gpa || "0.00"}</p>
          <p className="text-sm text-gray-500 mt-1">{data?.total_courses || 0} courses</p>
        </div>
      </div>

      {!results.length ? (
        <EmptyState title="No grades" message="Your grades will appear here once posted." />
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="pb-3 font-medium">Course</th>
                <th className="pb-3 font-medium">Semester</th>
                <th className="pb-3 font-medium text-center">Total</th>
                <th className="pb-3 font-medium text-center">Grade</th>
                <th className="pb-3 font-medium text-center">GPA</th>
                <th className="pb-3 font-medium text-center">Remark</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r) => (
                <tr key={r.id} className="border-b border-gray-50">
                  <td className="py-3 font-medium text-gray-900">{r.course_code}</td>
                  <td className="py-3 text-gray-500">{r.semester} {r.year}</td>
                  <td className="py-3 text-center">{parseFloat(r.total_score).toFixed(1)}</td>
                  <td className="py-3 text-center font-semibold">{r.grade_letter}</td>
                  <td className="py-3 text-center">{r.grade_point}</td>
                  <td className="py-3 text-center">
                    <span className={remarkColor[r.remark] || "badge-yellow"}>{r.remark}</span>
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
