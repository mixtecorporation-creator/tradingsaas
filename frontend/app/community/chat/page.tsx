"use client";

import { useState, useEffect, useRef } from "react";
import { api } from "@/lib/api-client";
import { wsClient } from "@/lib/ws-client";
import type { ChatRoom, ChatMessage } from "@/lib/types";
import { MessageSquare, Send } from "lucide-react";

export default function ChatPage() {
  const [rooms, setRooms] = useState<ChatRoom[]>([]);
  const [activeRoom, setActiveRoom] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.get<ChatRoom[]>("/community/chat/rooms")
      .then(setRooms)
      .catch(() => setError("Failed to load rooms"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!activeRoom) return;
    api.get<ChatMessage[]>(`/community/chat/rooms/${activeRoom}/messages`)
      .then(setMessages);
  }, [activeRoom]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (!activeRoom) return;
    const unsub = wsClient.on("message", (data) => {
      const msg = data as { room_id: string; user_id: string; content: string };
      if (msg.room_id === activeRoom) {
        setMessages((prev) => [...prev, {
          id: crypto.randomUUID(),
          room_id: activeRoom,
          user_id: msg.user_id || "unknown",
          content: msg.content,
          created_at: new Date().toISOString(),
        }]);
      }
    });
    wsClient.connect(`/chat/${activeRoom}`);
    return () => {
      unsub();
      wsClient.disconnect();
    };
  }, [activeRoom]);

  function sendMessage() {
    if (!input.trim()) return;
    wsClient.send({ type: "message", content: input.trim() });
    setInput("");
  }

  return (
    <div className="flex gap-4 h-[calc(100vh-8rem)]">
      <div className="w-56 shrink-0 space-y-1">
        <h2 className="text-sm font-semibold mb-3">Rooms</h2>
        {rooms.map((room) => (
          <button key={room.id} onClick={() => setActiveRoom(room.id)}
            className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm transition-colors ${
              activeRoom === room.id ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:text-foreground hover:bg-muted"
            }`}>
            <MessageSquare className="h-4 w-4 shrink-0" aria-hidden="true" />
            {room.name}
          </button>
        ))}
      </div>

      <div className="flex-1 rounded-lg border bg-card flex flex-col">
        {activeRoom ? (
          <>
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((msg) => (
                <div key={msg.id} className="flex gap-2 text-sm">
                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-medium text-primary">
                    {msg.user_id.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <p className="text-xs font-medium text-muted-foreground">
                      {msg.user_id.slice(0, 8)} &middot; {new Date(msg.created_at).toLocaleTimeString()}
                    </p>
                    <p className="text-sm">{msg.content}</p>
                  </div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>
            <div className="border-t p-3 flex gap-2">
              <input value={input} onChange={(e) => setInput(e.target.value)}
                placeholder="Type a message..."
                className="flex h-9 flex-1 rounded-md border border-input bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              />
              <button onClick={sendMessage}
                className="inline-flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90">
                <Send className="h-4 w-4" aria-hidden="true" />
              </button>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-sm text-muted-foreground">
            {loading ? "Loading rooms..." : "Select a room to start chatting"}
          </div>
        )}
      </div>
    </div>
  );
}
