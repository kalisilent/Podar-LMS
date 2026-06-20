import { Routes, Route, Navigate } from "react-router-dom";
import useAuthStore from "./stores/authStore";

// Layouts
import StudentLayout from "./components/layout/StudentLayout";
import AdminLayout from "./components/layout/AdminLayout";

// Auth pages
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

// Student pages
import StudentDashboard from "./pages/student/Dashboard";
import CourseCatalog from "./pages/student/CourseCatalog";
import CourseDetail from "./pages/student/CourseDetail";
import MyAssignments from "./pages/student/MyAssignments";
import MyGrades from "./pages/student/MyGrades";
import QuizList from "./pages/student/QuizList";
import ForumPage from "./pages/student/ForumPage";
import Profile from "./pages/student/Profile";

// Admin pages
import AdminDashboard from "./pages/admin/Dashboard";
import UserManagement from "./pages/admin/UserManagement";
import CourseManagement from "./pages/admin/CourseManagement";

// Lecturer pages
import LecturerDashboard from "./pages/lecturer/Dashboard";
import Gradebook from "./pages/lecturer/Gradebook";

function ProtectedRoute({ children, roles }) {
  const user = useAuthStore((s) => s.user);
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
}

function GuestRoute({ children }) {
  const user = useAuthStore((s) => s.user);
  if (user) {
    const home = user.role === "admin" ? "/admin" : user.role === "lecturer" ? "/lecturer" : "/dashboard";
    return <Navigate to={home} replace />;
  }
  return children;
}

export default function App() {
  return (
    <Routes>
      {/* Auth */}
      <Route path="/login" element={<GuestRoute><Login /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><Register /></GuestRoute>} />

      {/* Student */}
      <Route element={<ProtectedRoute roles={["student"]}><StudentLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<StudentDashboard />} />
        <Route path="/courses" element={<CourseCatalog />} />
        <Route path="/courses/:slug" element={<CourseDetail />} />
        <Route path="/assignments" element={<MyAssignments />} />
        <Route path="/grades" element={<MyGrades />} />
        <Route path="/quizzes" element={<QuizList />} />
        <Route path="/forums/:forumId" element={<ForumPage />} />
        <Route path="/profile" element={<Profile />} />
      </Route>

      {/* Lecturer */}
      <Route element={<ProtectedRoute roles={["lecturer"]}><StudentLayout /></ProtectedRoute>}>
        <Route path="/lecturer" element={<LecturerDashboard />} />
        <Route path="/lecturer/gradebook" element={<Gradebook />} />
        <Route path="/lecturer/courses/:slug" element={<CourseDetail />} />
      </Route>

      {/* Admin */}
      <Route element={<ProtectedRoute roles={["admin"]}><AdminLayout /></ProtectedRoute>}>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/users" element={<UserManagement />} />
        <Route path="/admin/courses" element={<CourseManagement />} />
      </Route>

      {/* Redirects */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
