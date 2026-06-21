import { useState } from "react";
import { Outlet, NavLink } from "react-router-dom";
import { LayoutDashboard, Users, BookOpen, X, Menu, Sparkles } from "lucide-react";
import Navbar from "./Navbar";
import clsx from "clsx";

const AI_TOOLS_URL = "https://podarenterprise.com/lms1/podar-sim-lab/";

const adminLinks = [
  { to: "/admin", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/admin/users", icon: Users, label: "Users" },
  { to: "/admin/courses", icon: BookOpen, label: "Courses" },
];

export default function AdminLayout() {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden">
      {open && <div className="fixed inset-0 bg-black/40 z-40 lg:hidden" onClick={() => setOpen(false)} />}
      <aside className={clsx(
        "fixed top-0 left-0 z-50 h-full w-64 bg-gray-900 flex flex-col transition-transform lg:translate-x-0 lg:static",
        open ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex items-center justify-between h-16 px-5 border-b border-gray-800">
          <span className="text-xl font-bold text-white">Podar LMS <span className="text-primary-400 text-sm">Admin</span></span>
          <button onClick={() => setOpen(false)} className="lg:hidden text-gray-400"><X size={20} /></button>
        </div>
        <nav className="flex-1 py-4 px-3 space-y-1">
          {adminLinks.map(({ to, icon: Icon, label }) => (
            <NavLink key={to} to={to} end onClick={() => setOpen(false)}
              className={({ isActive }) => clsx(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition",
                isActive ? "bg-primary-600 text-white" : "text-gray-400 hover:bg-gray-800 hover:text-white"
              )}>
              <Icon size={18} />{label}
            </NavLink>
          ))}
        </nav>

        {/* AI Tools Button */}
        <div className="p-3 border-t border-gray-800">
          <a
            href={AI_TOOLS_URL}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setOpen(false)}
            className="flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition bg-gradient-to-r from-purple-500 to-indigo-500 text-white hover:from-purple-600 hover:to-indigo-600 shadow-md hover:shadow-lg"
          >
            <Sparkles size={18} />
            AI Tools
            <span className="ml-auto text-xs bg-white/20 px-2 py-0.5 rounded-full">New</span>
          </a>
        </div>
      </aside>
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar onMenuClick={() => setOpen(true)} />
        <main className="flex-1 overflow-y-auto p-4 lg:p-6 bg-gray-50"><Outlet /></main>
      </div>
    </div>
  );
}
