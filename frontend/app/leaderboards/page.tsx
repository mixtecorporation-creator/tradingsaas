"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import type { LeaderboardEntry } from "@/lib/types";
import { Trophy, Shield, UserPlus, UserMinus, TrendingUp, TrendingDown } from "lucide-react";

const PERIODS = [
  { value: "weekly", label: "This Week" },
  { value: "monthly", label: "This Month" },
  { value: "quarterly", label: "This Quarter" },
  { value: "yearly", label: "This Year" },
  { value: "all_time", label: "All Time" },
];

export default function LeaderboardsPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [period, setPeriod] = useState("monthly");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");
    api.get<LeaderboardEntry[]>(`/leaderboards?period=${period}`)
      .then(setEntries)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, [period]);

  async function toggleFollow(userId: string, isFollowing: boolean) {
    try {
      if (isFollowing) {
        await api.delete(`/leaderboards/follow/${userId}`);
      } else {
        await api.post(`/leaderboards/follow/${userId}`);
      }
      setEntries(entries.map((e) =>
        e.user_id === userId ? { ...e, is_following: !isFollowing } : e
      ));
    } catch {
      // silently handle
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Leaderboards</h1>
          <p className="text-sm text-muted-foreground">Top traders by performance</p>
        </div>
        <div className="flex gap-1 rounded-lg border bg-card p-0.5">
          {PERIODS.map((p) => (
            <button
              key={p.value}
              onClick={() => setPeriod(p.value)}
              className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
                period === p.value
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      {loading ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">Loading...</div>
      ) : entries.length === 0 ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">No traders ranked yet for this period.</div>
      ) : (
        <div className="overflow-hidden rounded-xl border">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-muted/50">
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">#</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Trader</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">PnL</th>
                <th className="hidden px-4 py-3 text-right font-medium text-muted-foreground sm:table-cell">Returns</th>
                <th className="hidden px-4 py-3 text-right font-medium text-muted-foreground md:table-cell">Win Rate</th>
                <th className="hidden px-4 py-3 text-right font-medium text-muted-foreground md:table-cell">Trades</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Follow</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr key={entry.user_id} className="border-b last:border-0 hover:bg-muted/30">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1.5">
                      {entry.rank <= 3 ? (
                        <Trophy className={`h-4 w-4 ${
                          entry.rank === 1 ? "text-yellow-500" :
                          entry.rank === 2 ? "text-gray-400" : "text-amber-600"
                        }`} aria-hidden="true" />
                      ) : (
                        <span className="text-muted-foreground w-4 text-center text-xs">{entry.rank}</span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary/10 text-xs font-medium text-primary">
                        {entry.display_name.charAt(0).toUpperCase()}
                      </div>
                      <span className="font-medium">{entry.display_name}</span>
                      {entry.verified && (
                        <Shield className="h-3.5 w-3.5 text-primary" aria-label="Verified" />
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className={`inline-flex items-center gap-1 font-medium ${
                      entry.pnl >= 0 ? "text-primary" : "text-destructive"
                    }`}>
                      {entry.pnl >= 0 ? (
                        <TrendingUp className="h-3.5 w-3.5" aria-hidden="true" />
                      ) : (
                        <TrendingDown className="h-3.5 w-3.5" aria-hidden="true" />
                      )}
                      ${Math.abs(entry.pnl).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </div>
                  </td>
                  <td className="hidden px-4 py-3 text-right sm:table-cell">
                    <span className={entry.returns != null && entry.returns >= 0 ? "text-primary" : "text-destructive"}>
                      {entry.returns != null ? `${entry.returns >= 0 ? "+" : ""}${Number(entry.returns).toFixed(2)}%` : "-"}
                    </span>
                  </td>
                  <td className="hidden px-4 py-3 text-right md:table-cell">
                    {entry.win_rate != null ? `${Number(entry.win_rate).toFixed(1)}%` : "-"}
                  </td>
                  <td className="hidden px-4 py-3 text-right md:table-cell text-muted-foreground">
                    {entry.total_trades}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => toggleFollow(entry.user_id, entry.is_following)}
                      className={`inline-flex h-7 items-center gap-1 rounded-md px-2 text-xs font-medium transition-colors ${
                        entry.is_following
                          ? "border border-border bg-card text-muted-foreground hover:bg-muted"
                          : "bg-primary text-primary-foreground hover:bg-primary/90"
                      }`}
                    >
                      {entry.is_following ? (
                        <><UserMinus className="h-3 w-3" aria-hidden="true" /> Following</>
                      ) : (
                        <><UserPlus className="h-3 w-3" aria-hidden="true" /> Follow</>
                      )}
                    </button>
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
