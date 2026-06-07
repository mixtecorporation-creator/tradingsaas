"use client";

import { useAuth } from "@/lib/auth-context";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import { StatCard } from "@/components/dashboard/stat-card";
import { Skeleton } from "@/components/ui/skeleton";
import Link from "next/link";
import { useTrades } from "@/hooks/use-trades";
import { formatCurrency, formatPercent } from "@/lib/utils";

export default function DashboardPage() {
  const { user } = useAuth();

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: () => api.get<any>("/trades/stats"),
  });

  const { data: tradesData, isLoading: tradesLoading } = useTrades({ limit: "5" });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome back, {user?.display_name}
        </h1>
        <p className="text-sm text-muted-foreground">Here&apos;s your trading overview</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {statsLoading ? (
          [...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-24 rounded-lg" />
          ))
        ) : (
          <>
            <StatCard
              title="Total P&L"
              value={formatCurrency(stats?.total_pnl || 0)}
              change={stats?.total_pnl ? formatPercent((stats.total_pnl / (stats.total_trades || 1)) * 10) : "0%"}
            />
            <StatCard
              title="Win Rate"
              value={`${stats?.win_rate || 0}%`}
            />
            <StatCard title="Total Trades" value={`${stats?.total_trades || 0}`} />
            <StatCard
              title="Profit Factor"
              value={`${stats?.profit_factor?.toFixed(2) || "0.00"}`}
            />
          </>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-lg border p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium">Recent Trades</h3>
            <Link href="/dashboard/trades" className="text-sm text-primary hover:underline">
              View all
            </Link>
          </div>
          {tradesLoading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : tradesData?.items?.length ? (
            <div className="space-y-2">
              {tradesData.items.slice(0, 5).map((trade: any) => (
                <div key={trade.id} className="flex items-center justify-between rounded-md bg-muted/50 px-3 py-2 text-sm">
                  <div className="flex items-center gap-2">
                    <span className={trade.direction === "long" ? "text-green-500" : "text-red-500"}>
                      {trade.direction === "long" ? "▲" : "▼"}
                    </span>
                    <span className="font-medium">{trade.instrument_id?.slice(0, 8)}</span>
                    <span className="text-muted-foreground">
                      ${Number(trade.entry_price).toFixed(2)}
                    </span>
                  </div>
                  <span className={Number(trade.pnl) > 0 ? "text-green-500" : Number(trade.pnl) < 0 ? "text-red-500" : ""}>
                    {trade.pnl ? formatCurrency(Number(trade.pnl)) : "Open"}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No trades yet. Start journaling to see your history.</p>
          )}
        </div>

        <div className="rounded-lg border p-6">
          <h3 className="font-medium mb-4">Performance Summary</h3>
          {statsLoading ? (
            <Skeleton className="h-32 w-full" />
          ) : Number(stats?.total_trades) > 0 ? (
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <p className="text-xs text-muted-foreground">Winning Trades</p>
                <p className="text-lg font-semibold text-green-500">{stats?.winning_trades || 0}</p>
              </div>
              <div className="space-y-1">
                <p className="text-xs text-muted-foreground">Losing Trades</p>
                <p className="text-lg font-semibold text-red-500">{stats?.losing_trades || 0}</p>
              </div>
              <div className="space-y-1">
                <p className="text-xs text-muted-foreground">Best Trade</p>
                <p className="text-lg font-semibold text-green-500">
                  {stats?.largest_win ? formatCurrency(Number(stats.largest_win)) : "-"}
                </p>
              </div>
              <div className="space-y-1">
                <p className="text-xs text-muted-foreground">Worst Trade</p>
                <p className="text-lg font-semibold text-red-500">
                  {stats?.largest_loss ? formatCurrency(Number(stats.largest_loss)) : "-"}
                </p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">Your stats will appear once you have enough data.</p>
          )}
        </div>
      </div>
    </div>
  );
}
