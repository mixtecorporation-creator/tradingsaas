"use client";

import { useState, useEffect, useRef } from "react";
import { api } from "@/lib/api-client";
import { wsClient } from "@/lib/ws-client";
import { useInstruments, useOHLCV } from "@/hooks/use-instruments";
import { PriceChart } from "@/components/charts/price-chart";
import { Skeleton } from "@/components/ui/skeleton";
import type { OHLCV } from "@/lib/types";
import { Wifi, WifiOff } from "lucide-react";

export default function ChartsPage() {
  const [selectedSymbol, setSelectedSymbol] = useState("BTC/USD");
  const [timeframe, setTimeframe] = useState("1d");
  const [liveCandle, setLiveCandle] = useState<OHLCV | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(false);

  const { data: instruments } = useInstruments();
  const { data: ohlcv, isLoading } = useOHLCV(selectedSymbol, timeframe, 200);

  useEffect(() => {
    if (wsRef.current) return;
    wsRef.current = true;

    const unsubCandle = wsClient.on("candle", (data) => {
      const c = data as OHLCV & { symbol: string; timeframe: string };
      if (c.symbol === selectedSymbol) {
        setLiveCandle({
          open_time: c.open_time,
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
          volume: c.volume,
        });
      }
    });

    wsClient.connect(`/market/${selectedSymbol}`);
    setConnected(true);

    const interval = setInterval(() => {
      wsClient.send({ type: "ping" });
    }, 30000);

    return () => {
      unsubCandle();
      clearInterval(interval);
      wsClient.disconnect();
      wsRef.current = false;
      setConnected(false);
    };
  }, [selectedSymbol]);

  const chartData = liveCandle && timeframe === "1d"
    ? [...(ohlcv || []), liveCandle]
    : ohlcv || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Charts</h1>
          <p className="text-sm text-muted-foreground">Live market data and technical analysis</p>
        </div>
        <div className={`flex items-center gap-1.5 text-xs ${
          connected ? "text-green-500" : "text-muted-foreground"
        }`}>
          {connected ? (
            <><Wifi className="h-3.5 w-3.5" aria-hidden="true" /> Live</>
          ) : (
            <><WifiOff className="h-3.5 w-3.5" aria-hidden="true" /> Disconnected</>
          )}
        </div>
      </div>

      <div className="flex items-center gap-3">
        <select
          value={selectedSymbol}
          onChange={(e) => setSelectedSymbol(e.target.value)}
          className="flex h-9 rounded-md border border-input bg-background px-3 py-1 text-sm"
        >
          {(instruments || []).map((inst: any) => (
            <option key={inst.id} value={inst.symbol}>{inst.symbol}</option>
          ))}
        </select>

        <div className="flex gap-1">
          {["1h", "4h", "1d", "1w"].map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`inline-flex h-8 items-center rounded-md px-3 text-xs font-medium transition-colors ${
                timeframe === tf
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-muted-foreground hover:bg-accent"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-lg border bg-card">
        {isLoading ? (
          <Skeleton className="h-[400px] w-full rounded-lg" />
        ) : chartData.length > 0 ? (
          <PriceChart data={chartData} symbol={selectedSymbol} />
        ) : (
          <div className="flex h-[400px] items-center justify-center text-sm text-muted-foreground">
            No data available. Seed market data to see charts.
          </div>
        )}
      </div>
    </div>
  );
}
