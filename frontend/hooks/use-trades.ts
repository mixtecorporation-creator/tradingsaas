import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";

export function useTrades(params?: Record<string, string>) {
  const search = params ? `?${new URLSearchParams(params)}` : "";
  return useQuery({
    queryKey: ["trades", params],
    queryFn: () => api.get<{ items: any[]; total: number; limit: number; offset: number }>(`/trades${search}`),
  });
}

export function useTrade(id: string) {
  return useQuery({
    queryKey: ["trade", id],
    queryFn: () => api.get<any>(`/trades/${id}`),
    enabled: !!id,
  });
}

export function useCreateTrade() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Record<string, unknown>) => api.post<any>("/trades", data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["trades"] }),
  });
}

export function useDeleteTrade() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/trades/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["trades"] }),
  });
}

export function useTradeStats() {
  return useQuery({
    queryKey: ["trade-stats"],
    queryFn: () => api.get<Record<string, unknown>>("/trades/stats"),
  });
}
