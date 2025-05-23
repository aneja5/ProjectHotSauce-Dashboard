import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import SensorsPage from "./pages/SensorsPage";
import ReportsPage from "./pages/ReportsPage";
import LoginPage from "./pages/LoginPage";
import LogoutPage from "./pages/LogoutPage";
import SettingsPage from "./pages/SettingsPage";
import RegisterUserPage from "./pages/RegisterUserPage";
import Layout from "./components/Layout";
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';

const router = createBrowserRouter([
  {
    path: "/",
    element: (
        <LoginPage />
    ),
  },
  {
    path: "/register",
    element: (
        <RegisterUserPage />
    ),
  },
  {
    path: "/dashboard",
    element: (
      <Layout title="Dashboard">
        <DashboardPage />
      </Layout>
    ),
  },
  {
    path: "/sensors",
    element: (
      <Layout title="Sensors">
        <SensorsPage />
      </Layout>
    ),
  },
  {
    path: "/reports",
    element: (
      <Layout title="Reports">
        <ReportsPage />
      </Layout>
    ),
  },
  {
    path: "/logout",
    element: (
        <LogoutPage />
    ),
  },
  {
    path: "/settings",
    element: (
        <SettingsPage />
    ),
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;