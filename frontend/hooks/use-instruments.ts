import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type { Instrument, OHLCV } from "@/lib/types";

export function useInstruments() {
  return useQuery({
    queryKey: ["instruments"],
    queryFn: () => api.get<Instrument[]>("/instruments"),
  });
}

export function useInstrument(symbol: string) {
  return useQuery({
    queryKey: ["instrument", symbol],
    queryFn: () => api.get<Instrument>(`/instruments/${symbol}`),
    enabled: !!symbol,
  });
}

export function useOHLCV(symbol: string, timeframe = "1d", limit = 100) {
  return useQuery({
    queryKey: ["ohlcv", symbol, timeframe, limit],
    queryFn: () =>
      api.get<OHLCV[]>(`/instruments/${symbol}/ohlcv?timeframe=${timeframe}&limit=${limit}`),
    enabled: !!symbol,
    refetchInterval: timeframe === "1m" ? 60_000 : undefined,
  });
}
