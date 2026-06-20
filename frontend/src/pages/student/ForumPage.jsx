import { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { MessageSquare, Pin, ThumbsUp, Send } from "lucide-react";
import { format } from "date-fns";
import toast from "react-hot-toast";
import { forumAPI } from "../../services/api";
import Spinner from "../../components/common/Spinner";
import EmptyState from "../../components/common/EmptyState";

export default function ForumPage() {
  const { forumId } = useParams();
  const qc = useQueryClient();
  const [selectedThread, setSelectedThread] = useState(null);
  const [newThread, setNewThread] = useState({ title: "", content: "" });
  const [reply, setReply] = useState("");
  const [showNew, setShowNew] = useState(false);

  const { data: threads, isLoading } = useQuery({
    queryKey: ["threads", forumId],
    queryFn: () => forumAPI.threads(forumId).then((r) => r.data.results || r.data),
  });

  const { data: threadDetail } = useQuery({
    queryKey: ["thread", selectedThread],
    queryFn: () => forumAPI.threadDetail(selectedThread).then((r) => r.data),
    enabled: !!selectedThread,
  });

  const createThread = useMutation({
    mutationFn: (data) => forumAPI.createThread(forumId, data),
    onSuccess: () => { qc.invalidateQueries(["threads"]); setShowNew(false); setNewThread({ title: "", content: "" }); toast.success("Thread created"); },
  });

  const postReply = useMutation({
    mutationFn: (data) => forumAPI.createPost(selectedThread, data),
    onSuccess: () => { qc.invalidateQueries(["thread", selectedThread]); setReply(""); },
  });

  if (isLoading) return <Spinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Discussion forum</h1>
        <button onClick={() => setShowNew(!showNew)} className="btn-primary text-sm">New thread</button>
      </div>

      {showNew && (
        <div className="card space-y-3">
          <input className="input" placeholder="Thread title" value={newThread.title}
            onChange={(e) => setNewThread({ ...newThread, title: e.target.value })} />
          <textarea className="input" rows={3} placeholder="What's on your mind?"
            value={newThread.content} onChange={(e) => setNewThread({ ...newThread, content: e.target.value })} />
          <button onClick={() => createThread.mutate(newThread)} className="btn-primary text-sm">Post</button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="space-y-2">
          {!threads?.length ? <EmptyState title="No threads" /> : threads.map((t) => (
            <div key={t.id} onClick={() => setSelectedThread(t.id)}
              className={`card cursor-pointer transition ${selectedThread === t.id ? "ring-2 ring-primary-500" : "hover:shadow-md"}`}>
              <div className="flex items-start gap-2">
                {t.is_pinned && <Pin size={14} className="text-primary-500 mt-1" />}
                <div>
                  <h3 className="font-medium text-gray-900 text-sm">{t.title}</h3>
                  <p className="text-xs text-gray-500 mt-1">
                    {t.author?.first_name} · {t.replies_count} replies
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="lg:col-span-2">
          {threadDetail ? (
            <div className="card space-y-4">
              <h2 className="text-lg font-semibold">{threadDetail.title}</h2>
              <p className="text-gray-700 text-sm">{threadDetail.content}</p>
              <div className="border-t pt-4 space-y-3">
                {threadDetail.posts?.map((p) => (
                  <div key={p.id} className="flex gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xs font-semibold">
                      {p.author?.first_name?.[0]}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span className="font-medium text-gray-700">{p.author?.first_name}</span>
                        <span>{format(new Date(p.created_at), "MMM d, h:mm a")}</span>
                      </div>
                      <p className="text-sm text-gray-700 mt-1">{p.content}</p>
                      <button className="flex items-center gap-1 text-xs text-gray-400 mt-1 hover:text-primary-500">
                        <ThumbsUp size={12} /> {p.upvotes}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <input className="input flex-1" placeholder="Write a reply..." value={reply}
                  onChange={(e) => setReply(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && reply && postReply.mutate({ content: reply })} />
                <button onClick={() => reply && postReply.mutate({ content: reply })} className="btn-primary">
                  <Send size={16} />
                </button>
              </div>
            </div>
          ) : (
            <div className="card text-center text-gray-400 py-16">
              <MessageSquare size={32} className="mx-auto mb-2" />
              <p>Select a thread to view</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
