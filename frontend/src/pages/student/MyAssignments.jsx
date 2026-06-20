import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Upload, Clock, CheckCircle, AlertCircle } from "lucide-react";
import { format } from "date-fns";
import toast from "react-hot-toast";
import { assignmentAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function MyAssignments() {
  const { data: assignments, isLoading } = useQuery({
    queryKey: ["assignments"],
    queryFn: () => assignmentAPI.list().then((r) => r.data.results || r.data),
  });

  const { data: submissions } = useQuery({
    queryKey: ["mySubmissions"],
    queryFn: () => assignmentAPI.mySubmissions().then((r) => r.data.results || r.data),
  });

  const [submitting, setSubmitting] = useState(null);
  const [file, setFile] = useState(null);
  const qc = useQueryClient();

  const submitMutation = useMutation({
    mutationFn: ({ id, formData }) => assignmentAPI.submit(id, formData),
    onSuccess: () => {
      toast.success("Submitted!");
      setSubmitting(null);
      setFile(null);
      qc.invalidateQueries(["mySubmissions"]);
    },
    onError: () => toast.error("Submission failed"),
  });

  const handleSubmit = (assignmentId) => {
    if (!file) { toast.error("Select a file"); return; }
    const formData = new FormData();
    formData.append("file_upload", file);
    submitMutation.mutate({ id: assignmentId, formData });
  };

  if (isLoading) return <Spinner />;

  const submissionMap = new Map((submissions || []).map((s) => [s.assignment, s]));
  const statusIcon = { submitted: Clock, graded: CheckCircle, late: AlertCircle, returned: AlertCircle };
  const statusColor = { submitted: "text-amber-500", graded: "text-green-500", late: "text-red-500", returned: "text-red-500" };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Assignments</h1>

      {!assignments?.length ? (
        <EmptyState title="No assignments" message="No assignments have been posted yet." />
      ) : (
        <div className="space-y-3">
          {assignments.map((a) => {
            const sub = submissionMap.get(a.id);
            const Icon = sub ? statusIcon[sub.status] || Clock : null;
            const isPastDue = new Date(a.due_date) < new Date();

            return (
              <div key={a.id} className="card">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{a.title}</h3>
                    <p className="text-sm text-gray-500 mt-1">{a.course_title}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      Due: {format(new Date(a.due_date), "MMM d, yyyy h:mm a")}
                      {isPastDue && !sub && <span className="text-red-500 ml-2">Overdue</span>}
                    </p>
                    <p className="text-sm text-gray-500">Marks: {a.total_marks}</p>
                  </div>

                  <div className="text-right">
                    {sub ? (
                      <div className="flex items-center gap-1.5">
                        <Icon size={16} className={statusColor[sub.status]} />
                        <span className="text-sm capitalize">{sub.status}</span>
                        {sub.grade !== null && (
                          <span className="ml-2 font-semibold">{sub.grade}/{a.total_marks}</span>
                        )}
                      </div>
                    ) : (
                      <button onClick={() => setSubmitting(a.id)} className="btn-primary text-sm">
                        <Upload size={14} className="inline mr-1" /> Submit
                      </button>
                    )}
                  </div>
                </div>

                {submitting === a.id && (
                  <div className="mt-4 pt-4 border-t border-gray-100 flex items-center gap-3">
                    <input type="file" onChange={(e) => setFile(e.target.files[0])} className="text-sm" />
                    <button onClick={() => handleSubmit(a.id)} className="btn-primary text-sm">Upload</button>
                    <button onClick={() => setSubmitting(null)} className="btn-secondary text-sm">Cancel</button>
                  </div>
                )}

                {sub?.feedback && (
                  <div className="mt-3 p-3 bg-gray-50 rounded-lg text-sm">
                    <span className="font-medium">Feedback:</span> {sub.feedback}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
