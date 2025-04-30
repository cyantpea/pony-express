import { useState } from "react";
import PropTypes from "prop-types";
import { AuthContext } from "../contexts";
import { useEffect } from "react";


const tokenKey = "pony_express_token";

export default function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(tokenKey));
  const [loggedIn, setLoggedIn] = useState(!!token);
  const headers = { Authorization: `Bearer ${token}` };
  const [authLoaded, setAuthLoaded] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem(tokenKey);
    if (storedToken) {
      setToken(storedToken);
      setLoggedIn(true);
    }
    setAuthLoaded(true); 
  }, []);

  const login = (token) => {
    setToken(token);
    localStorage.setItem(tokenKey, token);
    setLoggedIn(true);
  };
  const logout = () => {
    setToken(null);
    localStorage.removeItem(tokenKey);
    setLoggedIn(false);
  };

  useEffect(() => {
    const syncToken = () => {
      const tokenInStorage = localStorage.getItem(tokenKey);
      setToken(tokenInStorage);
      setLoggedIn(!!tokenInStorage);
    };

    window.addEventListener("storage", syncToken);
    return () => window.removeEventListener("storage", syncToken);
  }, []);

  return (
    <AuthContext.Provider value={{ headers, loggedIn, authLoaded, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

AuthProvider.propTypes = {
  children: PropTypes.node,
};