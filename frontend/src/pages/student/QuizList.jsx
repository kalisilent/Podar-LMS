import { useQuery } from "@tanstack/react-query";
import { Clock, CheckCircle, Play } from "lucide-react";
import { quizAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function QuizList() {
  const { data: quizzes, isLoading } = useQuery({
    queryKey: ["quizzes"],
    queryFn: () => quizAPI.list().then((r) => r.data.results || r.data),
  });

  const { data: attempts } = useQuery({
    queryKey: ["myAttempts"],
    queryFn: () => quizAPI.myAttempts().then((r) => r.data.results || r.data),
  });

  if (isLoading) return <Spinner />;

  const attemptMap = new Map();
  (attempts || []).forEach((a) => {
    if (!attemptMap.has(a.quiz) || a.score > attemptMap.get(a.quiz).score) {
      attemptMap.set(a.quiz, a);
    }
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Quizzes</h1>
      {!quizzes?.length ? (
        <EmptyState title="No quizzes" message="No quizzes available right now." />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {quizzes.map((q) => {
            const best = attemptMap.get(q.id);
            return (
              <div key={q.id} className="card">
                <h3 className="font-semibold text-gray-900">{q.title}</h3>
                <p className="text-sm text-gray-500 mt-1">{q.questions_count} questions · {q.time_limit_minutes} min</p>
                <p className="text-sm text-gray-500">Pass: {q.pass_percentage}%</p>

                {best ? (
                  <div className="mt-3 flex items-center gap-2">
                    <CheckCircle size={16} className={best.passed ? "text-green-500" : "text-red-500"} />
                    <span className="text-sm font-medium">{best.passed ? "Passed" : "Failed"} — {best.percentage}%</span>
                  </div>
                ) : (
                  <button className="btn-primary text-sm mt-3 flex items-center gap-1.5">
                    <Play size={14} /> Start quiz
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
