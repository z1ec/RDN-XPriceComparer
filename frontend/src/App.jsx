import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    }
    if (username) {
      localStorage.setItem("username", username);
    }
  }, [token, username]);

  const handleLogin = (name) => {
    setUsername(name);
    setToken(localStorage.getItem("token") || "");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken("");
    setUsername("");
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return <Dashboard onLogout={handleLogout} />;
}
