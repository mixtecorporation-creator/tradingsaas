import { useEffect, useCallback } from "react";
import { wsClient } from "@/lib/ws-client";

export function useWebSocket(path: string, handlers?: Record<string, (data: unknown) => void>) {
  useEffect(() => {
    wsClient.connect(path);
    return () => wsClient.disconnect();
  }, [path]);

  useEffect(() => {
    if (!handlers) return;
    const cleanups = Object.entries(handlers).map(([type, handler]) =>
      wsClient.on(type, handler),
    );
    return () => cleanups.forEach((cleanup) => cleanup());
  }, [handlers]);

  const send = useCallback((data: Record<string, unknown>) => {
    wsClient.send(data);
  }, []);

  return { send };
}
