"use client";

import { useState, useEffect, useRef } from "react";
import { wsClient } from "@/lib/ws-client";
import type { LivePrice } from "@/lib/types";
import { TrendingUp, TrendingDown } from "lucide-react";

interface Props {
  symbols: string[];
}

export function PriceTicker({ symbols }: Props) {
  const [prices, setPrices] = useState<Map<string, LivePrice>>(new Map());
  const connectedRef = useRef(false);

  useEffect(() => {
    if (connectedRef.current) return;
    if (symbols.length === 0) return;
    connectedRef.current = true;

    const unsub = wsClient.on("tick", (data) => {
      const tick = data as LivePrice;
      if (symbols.includes(tick.symbol)) {
        setPrices((prev) => {
          const next = new Map(prev);
          next.set(tick.symbol, tick);
          return next;
        });
      }
    });

    wsClient.connect("/market");

    return () => {
      unsub();
      wsClient.disconnect();
      connectedRef.current = false;
    };
  }, [symbols]);

  if (prices.size === 0) return null;

  return (
    <div className="flex gap-4 overflow-x-auto py-2 px-4 border-b bg-card/50 scrollbar-thin">
      {Array.from(prices.values()).map((p) => (
        <div key={p.symbol} className="flex shrink-0 items-center gap-2 text-sm">
          <span className="font-medium">{p.symbol.replace("/", "")}</span>
          <span className="tabular-nums">${p.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
          <span className={`inline-flex items-center gap-0.5 text-xs tabular-nums ${
            p.change_pct >= 0 ? "text-green-500" : "text-red-500"
          }`}>
            {p.change_pct >= 0 ? <TrendingUp className="h-3 w-3" aria-hidden="true" /> : <TrendingDown className="h-3 w-3" aria-hidden="true" />}
            {p.change_pct >= 0 ? "+" : ""}{p.change_pct.toFixed(2)}%
          </span>
        </div>
      ))}
    </div>
  );
}
