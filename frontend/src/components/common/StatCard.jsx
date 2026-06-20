export default function StatCard({ label, value, icon: Icon, color = "primary" }) {
  const c = { primary: "bg-primary-50 text-primary-600", green: "bg-green-50 text-green-600", amber: "bg-amber-50 text-amber-600", red: "bg-red-50 text-red-600" };
  return (
    <div className="card flex items-center gap-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${c[color]}`}><Icon size={22} /></div>
      <div>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        <p className="text-sm text-gray-500">{label}</p>
      </div>
    </div>
  );
}
