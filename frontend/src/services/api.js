import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({ baseURL: API_URL });

// Attach access token to every request
api.interceptors.request.use((config) => {
  const tokens = JSON.parse(localStorage.getItem("tokens") || "{}");
  if (tokens.access) {
    config.headers.Authorization = `Bearer ${tokens.access}`;
  }
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const tokens = JSON.parse(localStorage.getItem("tokens") || "{}");
      if (tokens.refresh) {
        try {
          const { data } = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: tokens.refresh,
          });
          localStorage.setItem(
            "tokens",
            JSON.stringify({ access: data.access, refresh: data.refresh || tokens.refresh })
          );
          original.headers.Authorization = `Bearer ${data.access}`;
          return api(original);
        } catch {
          localStorage.removeItem("tokens");
          localStorage.removeItem("user");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// ── API helpers ──────────────────────────────────────

export const authAPI = {
  login: (data) => api.post("/auth/login/", data),
  register: (data) => api.post("/auth/register/", data),
  logout: (data) => api.post("/auth/logout/", data),
  profile: () => api.get("/auth/profile/"),
  updateProfile: (data) => api.put("/auth/profile/", data),
  changePassword: (data) => api.post("/auth/change-password/", data),
  adminDashboard: () => api.get("/auth/admin-dashboard/"),
  users: (params) => api.get("/auth/users/", { params }),
  sendOTP: (data) => api.post("/auth/send-otp/", data),
  verifyOTP: (data) => api.post("/auth/verify-otp/", data),
};

export const courseAPI = {
  list: (params) => api.get("/courses/", { params }),
  detail: (slug) => api.get(`/courses/${slug}/`),
  create: (data) => api.post("/courses/create/", data),
  enroll: (slug) => api.post(`/courses/${slug}/enroll/`),
  unenroll: (slug) => api.post(`/courses/${slug}/unenroll/`),
  myEnrollments: () => api.get("/courses/my-enrollments/"),
  progress: (slug) => api.get(`/courses/${slug}/progress/`),
  markComplete: (lessonId) => api.post(`/courses/lessons/${lessonId}/complete/`),
  sections: (courseId) => api.get(`/courses/${courseId}/sections/`),
};

export const assignmentAPI = {
  list: (params) => api.get("/assignments/", { params }),
  detail: (id) => api.get(`/assignments/${id}/`),
  submit: (assignmentId, data) => api.post(`/assignments/${assignmentId}/submit/`, data, {
    headers: { "Content-Type": "multipart/form-data" },
  }),
  submissions: (assignmentId) => api.get(`/assignments/${assignmentId}/submissions/`),
  grade: (submissionId, data) => api.post(`/assignments/submissions/${submissionId}/grade/`, data),
  mySubmissions: () => api.get("/assignments/my-submissions/"),
};

export const quizAPI = {
  list: (params) => api.get("/quizzes/", { params }),
  detail: (id) => api.get(`/quizzes/${id}/`),
  start: (id) => api.post(`/quizzes/${id}/start/`),
  submit: (attemptId, data) => api.post(`/quizzes/attempts/${attemptId}/submit/`, data),
  myAttempts: () => api.get("/quizzes/my-attempts/"),
};

export const forumAPI = {
  threads: (forumId) => api.get(`/forums/${forumId}/threads/`),
  threadDetail: (id) => api.get(`/forums/threads/${id}/`),
  createThread: (forumId, data) => api.post(`/forums/${forumId}/threads/`, data),
  createPost: (threadId, data) => api.post(`/forums/threads/${threadId}/posts/`, data),
  upvote: (postId) => api.post(`/forums/posts/${postId}/upvote/`),
};

export const notificationAPI = {
  list: () => api.get("/notifications/"),
  markRead: (id) => api.post(`/notifications/${id}/read/`),
  markAllRead: () => api.post("/notifications/mark-all-read/"),
  unreadCount: () => api.get("/notifications/unread-count/"),
};

export const paymentAPI = {
  createOrder: (data) => api.post("/payments/create-order/", data),
  verify: (data) => api.post("/payments/verify/", data),
  history: () => api.get("/payments/history/"),
};

export const resultAPI = {
  list: (params) => api.get("/results/", { params }),
  gpa: () => api.get("/results/gpa/"),
};

export const reportAPI = {
  gradeReport: () => api.get("/reports/grade-report/", { responseType: "blob" }),
  courseAnalytics: (courseId) => api.get(`/reports/course-analytics/${courseId}/`),
};

export const certificateAPI = {
  list: () => api.get("/certificates/"),
  generate: (slug) => api.post(`/certificates/generate/${slug}/`),
};
