import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Check, ChevronDown } from "lucide-react";
import toast from "react-hot-toast";
import { assignmentAPI, courseAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function Gradebook() {
  const qc = useQueryClient();
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedAssignment, setSelectedAssignment] = useState("");
  const [grading, setGrading] = useState(null); // submission id being graded
  const [gradeForm, setGradeForm] = useState({ grade: "", feedback: "" });

  const { data: courses } = useQuery({
    queryKey: ["lecturerCourses"],
    queryFn: () => courseAPI.list().then((r) => r.data.results || r.data),
  });

  const { data: assignments } = useQuery({
    queryKey: ["assignments", selectedCourse],
    queryFn: () => assignmentAPI.list({ course: selectedCourse }).then((r) => r.data.results || r.data),
    enabled: !!selectedCourse,
  });

  const { data: submissions, isLoading: subsLoading } = useQuery({
    queryKey: ["submissions", selectedAssignment],
    queryFn: () => assignmentAPI.submissions(selectedAssignment).then((r) => r.data.results || r.data),
    enabled: !!selectedAssignment,
  });

  const gradeMutation = useMutation({
    mutationFn: ({ id, data }) => assignmentAPI.grade(id, data),
    onSuccess: () => {
      toast.success("Graded!");
      setGrading(null);
      setGradeForm({ grade: "", feedback: "" });
      qc.invalidateQueries(["submissions", selectedAssignment]);
    },
    onError: () => toast.error("Grading failed"),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Gradebook</h1>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <select className="input w-auto min-w-[200px]" value={selectedCourse}
          onChange={(e) => { setSelectedCourse(e.target.value); setSelectedAssignment(""); }}>
          <option value="">Select course</option>
          {(courses || []).map((c) => (
            <option key={c.id} value={c.id}>{c.code} — {c.title}</option>
          ))}
        </select>

        {selectedCourse && (
          <select className="input w-auto min-w-[200px]" value={selectedAssignment}
            onChange={(e) => setSelectedAssignment(e.target.value)}>
            <option value="">Select assignment</option>
            {(assignments || []).map((a) => (
              <option key={a.id} value={a.id}>{a.title}</option>
            ))}
          </select>
        )}
      </div>

      {/* Submissions table */}
      {!selectedAssignment ? (
        <EmptyState title="Select an assignment" message="Choose a course and assignment above to view submissions." />
      ) : subsLoading ? (
        <Spinner />
      ) : !submissions?.length ? (
        <EmptyState title="No submissions" message="No students have submitted this assignment yet." />
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="pb-3 font-medium">Student</th>
                <th className="pb-3 font-medium">Submitted</th>
                <th className="pb-3 font-medium">File</th>
                <th className="pb-3 font-medium text-center">Status</th>
                <th className="pb-3 font-medium text-center">Grade</th>
                <th className="pb-3 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {submissions.map((s) => (
                <tr key={s.id} className="border-b border-gray-50">
                  <td className="py-3 font-medium text-gray-900">{s.student_name}</td>
                  <td className="py-3 text-gray-500">
                    {new Date(s.submitted_at).toLocaleDateString()}
                    {s.is_late && <span className="badge-red ml-2">Late</span>}
                  </td>
                  <td className="py-3">
                    {s.file_upload ? (
                      <a href={s.file_upload} target="_blank" rel="noreferrer"
                        className="text-primary-600 hover:underline text-xs">Download</a>
                    ) : (
                      <span className="text-gray-400 text-xs">Text only</span>
                    )}
                  </td>
                  <td className="py-3 text-center capitalize">
                    <span className={
                      s.status === "graded" ? "badge-green" :
                      s.status === "late" ? "badge-red" : "badge-yellow"
                    }>{s.status}</span>
                  </td>
                  <td className="py-3 text-center font-semibold">
                    {s.grade !== null ? s.grade : "—"}
                  </td>
                  <td className="py-3 text-right">
                    {s.status !== "graded" ? (
                      grading === s.id ? (
                        <div className="flex items-center gap-2 justify-end">
                          <input type="number" className="input w-20 text-sm" placeholder="Grade"
                            value={gradeForm.grade}
                            onChange={(e) => setGradeForm({ ...gradeForm, grade: e.target.value })} />
                          <input className="input w-32 text-sm" placeholder="Feedback"
                            value={gradeForm.feedback}
                            onChange={(e) => setGradeForm({ ...gradeForm, feedback: e.target.value })} />
                          <button className="btn-primary text-xs px-2 py-1.5"
                            onClick={() => gradeMutation.mutate({ id: s.id, data: gradeForm })}>
                            <Check size={14} />
                          </button>
                        </div>
                      ) : (
                        <button className="btn-secondary text-xs"
                          onClick={() => { setGrading(s.id); setGradeForm({ grade: "", feedback: "" }); }}>
                          Grade
                        </button>
                      )
                    ) : (
                      <span className="text-xs text-gray-400">Done</span>
                    )}
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
