import { Inbox } from "lucide-react";
export default function EmptyState({ title = "No data", message = "Nothing here yet." }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-gray-400">
      <Inbox size={48} strokeWidth={1} />
      <p className="mt-3 font-medium text-gray-600">{title}</p>
      <p className="text-sm">{message}</p>
    </div>
  );
}
