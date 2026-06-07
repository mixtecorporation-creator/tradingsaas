"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import type { PerformanceSummary, Insight, TradeAnalysis } from "@/lib/types";
import { Sparkles, TrendingUp, TrendingDown, AlertTriangle, Lightbulb, BarChart3 } from "lucide-react";

export default function AnalyticsPage() {
  const [summary, setSummary] = useState<PerformanceSummary | null>(null);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [analyses, setAnalyses] = useState<Record<string, TradeAnalysis>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get<PerformanceSummary>("/ai/performance").catch(() => null),
      api.get<Insight[]>("/ai/insights").catch(() => []),
    ]).then(([s, i]) => {
      if (s && Object.keys(s).length > 0) setSummary(s);
      setInsights(i);
    }).catch(() => setError("Failed to load analytics"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="space-y-6">
      <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">Loading...</div>
    </div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Sparkles className="h-5 w-5 text-primary" aria-hidden="true" />
        <div>
          <h1 className="text-2xl font-bold tracking-tight">AI Analytics</h1>
          <p className="text-sm text-muted-foreground">AI-powered insights and performance analysis</p>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      {!summary && insights.length === 0 ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">
          Log some trades first to unlock AI-powered analytics and insights.
        </div>
      ) : (
        <>
          {summary && (
            <div className="rounded-xl border bg-card p-6">
              <h2 className="text-sm font-semibold mb-4 flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-primary" aria-hidden="true" />
                Performance Summary
              </h2>
              <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                <div className="text-center">
                  <p className="text-xs text-muted-foreground">Total Trades</p>
                  <p className="text-2xl font-bold">{summary.total_trades}</p>
                </div>
                <div className="text-center">
                  <p className="text-xs text-muted-foreground">Win Rate</p>
                  <p className="text-2xl font-bold">{summary.win_rate}%</p>
                </div>
                <div className="text-center">
                  <p className="text-xs text-muted-foreground">Profit Factor</p>
                  <p className="text-2xl font-bold">{summary.profit_factor}</p>
                </div>
                <div className="text-center">
                  <p className="text-xs text-muted-foreground">Sharpe</p>
                  <p className="text-2xl font-bold">{summary.sharpe_ratio ?? "-"}</p>
                </div>
              </div>

              {summary.improvement_tips.length > 0 && (
                <div className="mt-4 border-t pt-4 space-y-2">
                  <p className="text-xs font-medium text-muted-foreground">Improvement Tips</p>
                  {summary.improvement_tips.map((tip, i) => (
                    <div key={i} className="flex items-start gap-2 text-sm">
                      <Lightbulb className="h-4 w-4 mt-0.5 shrink-0 text-primary" aria-hidden="true" />
                      <span className="text-muted-foreground">{tip}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {insights.length > 0 && (
            <div className="rounded-xl border bg-card p-6">
              <h2 className="text-sm font-semibold mb-4 flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" aria-hidden="true" />
                AI Insights
              </h2>
              <div className="space-y-3">
                {insights.map((insight, i) => (
                  <div key={i} className={`rounded-lg border p-3 ${
                    insight.severity === "high" ? "border-destructive/30 bg-destructive/5" :
                    insight.severity === "medium" ? "border-yellow-500/30 bg-yellow-500/5" :
                    "border-border/40"
                  }`}>
                    <div className="flex items-start gap-2">
                      {insight.severity === "high" ? (
                        <AlertTriangle className="h-4 w-4 mt-0.5 shrink-0 text-destructive" aria-hidden="true" />
                      ) : insight.severity === "medium" ? (
                        <AlertTriangle className="h-4 w-4 mt-0.5 shrink-0 text-yellow-500" aria-hidden="true" />
                      ) : (
                        <Lightbulb className="h-4 w-4 mt-0.5 shrink-0 text-primary" aria-hidden="true" />
                      )}
                      <div>
                        <p className="text-sm font-medium">{insight.title}</p>
                        <p className="text-xs text-muted-foreground">{insight.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
