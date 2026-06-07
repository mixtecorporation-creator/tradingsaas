"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import type { BacktestRun, BacktestResult } from "@/lib/types";
import { Beaker, Play, RefreshCw } from "lucide-react";

const STRATEGIES = ["sma_crossover", "macd", "rsi", "bollinger", "custom"] as const;

export default function BacktestsPage() {
  const [runs, setRuns] = useState<BacktestRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedRun, setSelectedRun] = useState<string | null>(null);
  const [result, setResult] = useState<BacktestResult | null>(null);

  const [form, setForm] = useState({
    instrument_symbol: "BTC/USD",
    strategy_name: "sma_crossover",
    timeframe: "1d",
    start_date: "2025-01-01",
    end_date: "2026-01-01",
    initial_capital: 10000,
  });

  useEffect(() => { loadRuns(); }, []);

  async function loadRuns() {
    try {
      setLoading(true);
      setError("");
      const data = await api.get<{ items: BacktestRun[]; total: number }>("/backtests");
      setRuns(data.items);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }

  async function runBacktest() {
    try {
      setError("");
      await api.post("/backtests", form);
      await loadRuns();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Backtest failed");
    }
  }

  async function loadResult(runId: string) {
    if (selectedRun === runId) {
      setSelectedRun(null);
      setResult(null);
      return;
    }
    setSelectedRun(runId);
    setResult(null);
    try {
      const data = await api.get<BacktestResult>(`/backtests/${runId}/result`);
      setResult(data);
    } catch {
      setResult(null);
    }
  }

  function formatPct(val: number | null | undefined) {
    if (val === null || val === undefined) return "-";
    return `${val >= 0 ? "+" : ""}${Number(val).toFixed(2)}%`;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Backtesting</h1>
        <p className="text-sm text-muted-foreground">Test your strategies against historical data</p>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="rounded-lg border bg-card p-4 space-y-4">
        <h2 className="text-sm font-semibold">New Backtest</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Symbol</label>
            <input value={form.instrument_symbol} onChange={(e) => setForm({ ...form, instrument_symbol: e.target.value })}
              className="flex h-8 w-full rounded-md border border-input bg-background px-2 text-xs" />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Strategy</label>
            <select value={form.strategy_name} onChange={(e) => setForm({ ...form, strategy_name: e.target.value })}
              className="flex h-8 w-full rounded-md border border-input bg-background px-2 text-xs">
              {STRATEGIES.map((s) => <option key={s} value={s}>{s.replace(/_/g, " ")}</option>)}
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Timeframe</label>
            <select value={form.timeframe} onChange={(e) => setForm({ ...form, timeframe: e.target.value })}
              className="flex h-8 w-full rounded-md border border-input bg-background px-2 text-xs">
              <option value="1h">1h</option>
              <option value="4h">4h</option>
              <option value="1d">1d</option>
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Start Date</label>
            <input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })}
              className="flex h-8 w-full rounded-md border border-input bg-background px-2 text-xs" />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">End Date</label>
            <input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })}
              className="flex h-8 w-full rounded-md border border-input bg-background px-2 text-xs" />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Initial Capital</label>
            <input type="number" value={form.initial_capital} onChange={(e) => setForm({ ...form, initial_capital: Number(e.target.value) })}
              className="flex h-8 w-full rounded-md border border-input bg-background px-2 text-xs" />
          </div>
        </div>
        <button onClick={runBacktest}
          className="inline-flex h-8 items-center gap-1.5 rounded-md bg-primary px-3 text-xs font-medium text-primary-foreground hover:bg-primary/90">
          <Play className="h-3.5 w-3.5" aria-hidden="true" />
          Run Backtest
        </button>
      </div>

      {loading ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">Loading...</div>
      ) : runs.length === 0 ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">No backtests yet. Configure and run one above.</div>
      ) : (
        <div className="space-y-3">
          {runs.map((run) => (
            <div key={run.id} className="rounded-lg border bg-card">
              <button onClick={() => loadResult(run.id)} className="flex w-full items-center justify-between px-4 py-3 text-left">
                <div className="flex items-center gap-3">
                  <Beaker className={`h-4 w-4 ${
                    run.status === "completed" ? "text-primary" :
                    run.status === "failed" ? "text-destructive" : "text-muted-foreground"
                  }`} aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium">{run.strategy_name.replace(/_/g, " ")}</p>
                    <p className="text-xs text-muted-foreground">
                      {run.instrument_id.slice(0, 8)}... &middot; {run.timeframe} &middot; {new Date(run.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <span className={`text-xs font-medium ${
                  run.status === "completed" ? "text-primary" :
                  run.status === "failed" ? "text-destructive" : "text-muted-foreground"
                }`}>
                  {run.status === "running" ? <RefreshCw className="h-3.5 w-3.5 animate-spin" aria-hidden="true" /> : run.status}
                </span>
              </button>
              {selectedRun === run.id && result && (
                <div className="border-t px-4 py-3">
                  <div className="grid grid-cols-3 gap-3 sm:grid-cols-4 text-center">
                    <div>
                      <p className="text-xs text-muted-foreground">Return</p>
                      <p className={`text-sm font-bold ${(result.total_return_pct ?? 0) >= 0 ? "text-primary" : "text-destructive"}`}>
                        {formatPct(result.total_return_pct)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Win Rate</p>
                      <p className="text-sm font-bold">{result.win_rate != null ? `${Number(result.win_rate).toFixed(1)}%` : "-"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Trades</p>
                      <p className="text-sm font-bold">{result.total_trades ?? "-"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Sharpe</p>
                      <p className="text-sm font-bold">{result.sharpe_ratio != null ? Number(result.sharpe_ratio).toFixed(2) : "-"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Max DD</p>
                      <p className="text-sm font-bold text-destructive">{formatPct(result.max_drawdown_pct)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Profit Factor</p>
                      <p className="text-sm font-bold">{result.profit_factor != null ? Number(result.profit_factor).toFixed(2) : "-"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Avg Win</p>
                      <p className="text-sm font-bold text-primary">{formatPct(result.avg_win != null ? (result.avg_win / 100) : null)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Avg Loss</p>
                      <p className="text-sm font-bold text-destructive">{formatPct(result.avg_loss != null ? -(result.avg_loss / 100) : null)}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
