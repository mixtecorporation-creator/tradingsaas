"use client";

import { useState } from "react";
import Link from "next/link";
import { useTrades } from "@/hooks/use-trades";
import { formatCurrency } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/shared/empty-state";

export default function TradesPage() {
  const [filter, setFilter] = useState("");

  const { data, isLoading } = useTrades({ limit: "50" });

  const trades = data?.items || [];
  const filtered = filter
    ? trades.filter((t: any) =>
        (t.tags || []).some((tag: string) => tag.toLowerCase().includes(filter.toLowerCase()))
      )
    : trades;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Trade Journal</h1>
          <p className="text-sm text-muted-foreground">
            {data?.total ? `${data.total} trades recorded` : "Log and review your trades"}
          </p>
        </div>
        <Link
          href="/dashboard/trades/new"
          className="inline-flex h-9 items-center justify-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          New Trade
        </Link>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Filter by tag..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="flex h-9 max-w-xs rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm"
        />
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-16 w-full rounded-lg" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState
          title={trades.length === 0 ? "No trades recorded yet" : "No trades match your filter"}
          description="Start journaling to track your performance and identify patterns."
          action={
            <Link
              href="/dashboard/trades/new"
              className="inline-flex h-9 items-center justify-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground"
            >
              Record your first trade
            </Link>
          }
        />
      ) : (
        <div className="overflow-hidden rounded-lg border">
          <table className="w-full">
            <thead>
              <tr className="border-b bg-muted/50 text-left text-sm text-muted-foreground">
                <th className="px-4 py-3 font-medium">Symbol</th>
                <th className="px-4 py-3 font-medium">Direction</th>
                <th className="px-4 py-3 font-medium">Entry</th>
                <th className="px-4 py-3 font-medium">Exit</th>
                <th className="px-4 py-3 font-medium">P&L</th>
                <th className="px-4 py-3 font-medium">Tags</th>
                <th className="px-4 py-3 font-medium">Date</th>
                <th className="px-4 py-3 font-medium"></th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {filtered.map((trade: any) => (
                <tr key={trade.id} className="text-sm hover:bg-muted/30">
                  <td className="px-4 py-3 font-medium">{trade.instrument_id?.slice(0, 8)}</td>
                  <td className="px-4 py-3">
                    <Badge variant={trade.direction === "long" ? "success" : "danger"}>
                      {trade.direction}
                    </Badge>
                  </td>
                  <td className="px-4 py-3">${parseFloat(trade.entry_price).toFixed(2)}</td>
                  <td className="px-4 py-3">
                    {trade.exit_price ? `$${parseFloat(trade.exit_price).toFixed(2)}` : "-"}
                  </td>
                  <td className={`px-4 py-3 font-medium ${trade.pnl > 0 ? "text-green-500" : trade.pnl < 0 ? "text-red-500" : ""}`}>
                    {trade.pnl ? formatCurrency(parseFloat(trade.pnl)) : "Open"}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1 flex-wrap">
                      {(trade.tags || []).slice(0, 3).map((tag: string) => (
                        <Badge key={tag} variant="outline">{tag}</Badge>
                      ))}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {new Date(trade.entry_date).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3">
                    <Link href={`/dashboard/trades/${trade.id}`} className="text-primary hover:underline">
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
