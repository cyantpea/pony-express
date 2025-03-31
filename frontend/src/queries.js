import { useQuery } from "@tanstack/react-query";
import api from "./api/api";


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

export const useUsername = (accountId) => {
    if (accountId == null) 
        return { username: "[removed]", error: null };

    const { data, error } = useQuery({
        queryKey: ["username"],
        queryFn: () => api.get("/accounts/" + accountId),
        retry: false,
    });

    const username = data?.username || "[removed]";
    return { username, error };
}