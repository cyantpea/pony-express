import { useQuery } from "@tanstack/react-query";
import api from "./api/api";
import { useContext } from "react";
import { AuthContext } from "./contexts";


export const useChats = () => {
    const { data, error } = useQuery({
        queryKey: ["chats"],
        queryFn: () => api.get("/chats"),
        retry: false,
    });

    
    const chats = (data?.chats || []).sort((a,b) => a.name.localeCompare(b.name));
    return { chats, error };
}

export const useChatMessages = (chatId) => {
    const { data, error } = useQuery({
        queryKey: ["messages", chatId],
        queryFn: () => api.get(`/chats/${chatId}/messages`),
        retry: false,
    });

    
    const messages = (data?.messages || [].sort((a,b) => new Date(a.created_at) - newDate(b.created_at)));
    
    return { messages, error };
}

export const useChatMembers = (chatId) => {
    const { data, error } = useQuery({
        queryKey: ["accounts", chatId],
        queryFn: () => api.get(`/chats/${chatId}/accounts`),
        retry: false,
    });

    const members = (data?.accounts || [])
    return { members, error };
}

export const useUsername = (accountId) => {
    console.log("useUsername", accountId);
    if (accountId == null) 
        return { username: "[removed]", error: null };

    const { data, error } = useQuery({
        queryKey: ["username", accountId],
        queryFn: () => api.get("/accounts/" + accountId),
        retry: false,
    });
    console.log("useUsername data", data);

    const username = data?.username || "[removed]";
    console.log("username", username);
    return { username, error };
}

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