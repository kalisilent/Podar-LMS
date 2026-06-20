import { NavLink } from "react-router-dom";
import { LayoutDashboard, BookOpen, ClipboardList, Award, HelpCircle, MessageSquare, User, X } from "lucide-react";
import clsx from "clsx";

const studentLinks = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/courses", icon: BookOpen, label: "Courses" },
  { to: "/assignments", icon: ClipboardList, label: "Assignments" },
  { to: "/quizzes", icon: HelpCircle, label: "Quizzes" },
  { to: "/grades", icon: Award, label: "Grades" },
  { to: "/profile", icon: User, label: "Profile" },
];

const lecturerLinks = [
  { to: "/lecturer", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/courses", icon: BookOpen, label: "My Courses" },
  { to: "/lecturer/gradebook", icon: Award, label: "Gradebook" },
  { to: "/profile", icon: User, label: "Profile" },
];

export default function Sidebar({ role = "student", open, onClose }) {
  const links = role === "lecturer" ? lecturerLinks : studentLinks;

  return (
    <>
      {/* Mobile overlay */}
      {open && <div className="fixed inset-0 bg-black/40 z-40 lg:hidden" onClick={onClose} />}

      <aside
        className={clsx(
          "fixed top-0 left-0 z-50 h-full w-64 bg-white border-r border-gray-200 flex flex-col transition-transform duration-200 lg:translate-x-0 lg:static lg:z-auto",
          open ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-5 border-b border-gray-100">
          <span className="text-xl font-bold text-primary-700">Podar LMS</span>
          <button onClick={onClose} className="lg:hidden text-gray-400 hover:text-gray-600">
            <X size={20} />
          </button>
        </div>

        {/* Nav links */}
        <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
          {links.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onClose}
              className={({ isActive }) =>
                clsx(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition",
                  isActive
                    ? "bg-primary-50 text-primary-700"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                )
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
}
