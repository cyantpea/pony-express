import { useContext, useEffect } from "react";
import { AuthContext } from "./contexts";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import api from "./api/api.js";

export const useAuth = () => {
  return useContext(AuthContext);
};

export const useAccount = () => {
  const { headers, loggedIn, token } = useContext(AuthContext);
  const query = useQuery({
    enabled: loggedIn,
    queryKey: ["account"],
    queryFn: async () => {
      return await api.get("/accounts/me", { Authorization: `Bearer ${token}`, ...headers });
    }
  });
  return query;
}

export const useLoggedOut = () => {
  const { loggedIn } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!loggedIn) {
      navigate("/");
    }
  }, [loggedIn, navigate]);
};
