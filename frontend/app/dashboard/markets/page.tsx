"use client";

import { useState, useEffect, useRef } from "react";
import { api } from "@/lib/api-client";
import { wsClient } from "@/lib/ws-client";
import type { LivePrice } from "@/lib/types";
import { TrendingUp, TrendingDown, Search } from "lucide-react";

export default function MarketsPage() {
  const [prices, setPrices] = useState<LivePrice[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const wsRef = useRef(false);

  useEffect(() => {
    api.get<LivePrice[]>("/instruments/live")
      .then(setPrices)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (wsRef.current) return;
    wsRef.current = true;

    const unsub = wsClient.on("tick", (data) => {
      const tick = data as LivePrice;
      setPrices((prev) =>
        prev.map((p) => (p.symbol === tick.symbol ? tick : p)),
      );
    });

    prices.forEach((p) => wsClient.connect(`/market/${p.symbol}`));

    return () => {
      unsub();
      wsClient.disconnect();
      wsRef.current = false;
    };
  }, [prices.length]);

  const filtered = prices.filter(
    (p) =>
      p.symbol.toLowerCase().includes(search.toLowerCase()) ||
      (p.name && p.name.toLowerCase().includes(search.toLowerCase())),
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Markets</h1>
          <p className="text-sm text-muted-foreground">Real-time prices across all instruments</p>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
          <input value={search} onChange={(e) => setSearch(e.target.value)}
            placeholder="Filter markets..."
            className="flex h-9 w-56 rounded-md border border-input bg-background pl-9 pr-3 py-1 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
      </div>

      {loading ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">Loading live prices...</div>
      ) : (
        <div className="rounded-lg border bg-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="text-left px-4 py-3 font-medium text-muted-foreground">Symbol</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Name</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Price</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Bid</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Ask</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Change</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Change %</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">24h High</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">24h Low</th>
                  <th className="text-right px-4 py-3 font-medium text-muted-foreground">Volume</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((p) => (
                  <tr key={p.symbol} className="border-b last:border-0 hover:bg-muted/30 transition-colors">
                    <td className="px-4 py-3 font-medium">{p.symbol}</td>
                    <td className="px-4 py-3 text-right text-muted-foreground">{p.name}</td>
                    <td className="px-4 py-3 text-right tabular-nums font-medium">
                      ${p.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-muted-foreground">
                      ${p.bid.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-muted-foreground">
                      ${p.ask.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className={`px-4 py-3 text-right tabular-nums ${p.change >= 0 ? "text-green-500" : "text-red-500"}`}>
                      {p.change >= 0 ? "+" : ""}{p.change.toFixed(2)}
                    </td>
                    <td className={`px-4 py-3 text-right tabular-nums ${p.change_pct >= 0 ? "text-green-500" : "text-red-500"}`}>
                      <span className="inline-flex items-center gap-1">
                        {p.change_pct >= 0 ? <TrendingUp className="h-3.5 w-3.5" aria-hidden="true" /> : <TrendingDown className="h-3.5 w-3.5" aria-hidden="true" />}
                        {p.change_pct >= 0 ? "+" : ""}{p.change_pct.toFixed(2)}%
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-muted-foreground">
                      ${p.high_24h.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-muted-foreground">
                      ${p.low_24h.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-muted-foreground">
                      {p.volume_24h.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={10} className="px-4 py-12 text-center text-sm text-muted-foreground">
                      No markets found. Seed market data to see instruments.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
