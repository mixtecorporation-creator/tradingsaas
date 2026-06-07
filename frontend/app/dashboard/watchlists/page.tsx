"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import type { Watchlist } from "@/lib/types";
import { Plus, Trash2, Eye, EyeOff } from "lucide-react";

export default function WatchlistsPage() {
  const [watchlists, setWatchlists] = useState<Watchlist[]>([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState("");
  const [expanded, setExpanded] = useState<string | null>(null);
  const [addSymbol, setAddSymbol] = useState("");
  const [error, setError] = useState("");

  useEffect(() => { loadWatchlists(); }, []);

  async function loadWatchlists() {
    try {
      setLoading(true);
      setError("");
      const data = await api.get<Watchlist[]>("/watchlists");
      setWatchlists(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }

  async function createWatchlist() {
    if (!newName.trim()) return;
    try {
      await api.post("/watchlists", { name: newName.trim() });
      setNewName("");
      await loadWatchlists();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to create");
    }
  }

  async function deleteWatchlist(id: string) {
    try {
      await api.delete(`/watchlists/${id}`);
      await loadWatchlists();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to delete");
    }
  }

  async function addItem(watchlistId: string) {
    if (!addSymbol.trim()) return;
    try {
      await api.post(`/watchlists/${watchlistId}/items`, { instrument_symbol: addSymbol.trim() });
      setAddSymbol("");
      await loadWatchlists();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to add item");
    }
  }

  async function removeItem(watchlistId: string, itemId: string) {
    try {
      await api.delete(`/watchlists/${watchlistId}/items/${itemId}`);
      await loadWatchlists();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to remove");
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Watchlists</h1>
        <p className="text-sm text-muted-foreground">Track instruments you care about</p>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="flex gap-2">
        <input
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="New watchlist name"
          className="flex h-9 w-full max-w-xs rounded-lg border border-input bg-card px-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          onKeyDown={(e) => e.key === "Enter" && createWatchlist()}
        />
        <button
          onClick={createWatchlist}
          className="inline-flex h-9 items-center gap-1.5 rounded-lg bg-primary px-3 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          <Plus className="h-4 w-4" aria-hidden="true" />
          Create
        </button>
      </div>

      {loading ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">
          Loading...
        </div>
      ) : watchlists.length === 0 ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">
          No watchlists yet. Create one above.
        </div>
      ) : (
        <div className="space-y-3">
          {watchlists.map((wl) => (
            <div key={wl.id} className="rounded-lg border bg-card">
              <div className="flex items-center justify-between px-4 py-3">
                <button
                  onClick={() => setExpanded(expanded === wl.id ? null : wl.id)}
                  className="flex items-center gap-2 text-sm font-medium"
                >
                  {expanded === wl.id ? <EyeOff className="h-4 w-4" aria-hidden="true" /> : <Eye className="h-4 w-4" aria-hidden="true" />}
                  {wl.name}
                  <span className="text-xs text-muted-foreground">({wl.items.length})</span>
                </button>
                <button
                  onClick={() => deleteWatchlist(wl.id)}
                  className="text-muted-foreground hover:text-destructive"
                >
                  <Trash2 className="h-4 w-4" aria-hidden="true" />
                </button>
              </div>
              {expanded === wl.id && (
                <div className="border-t px-4 py-3 space-y-2">
                  {wl.items.map((item) => (
                    <div key={item.id} className="flex items-center justify-between rounded-md bg-muted/50 px-3 py-2 text-sm">
                      <span className="font-mono text-xs">{item.instrument_id.slice(0, 8)}...</span>
                      <button
                        onClick={() => removeItem(wl.id, item.id)}
                        className="text-muted-foreground hover:text-destructive"
                      >
                        <Trash2 className="h-3.5 w-3.5" aria-hidden="true" />
                      </button>
                    </div>
                  ))}
                  <div className="flex gap-2 pt-1">
                    <input
                      value={addSymbol}
                      onChange={(e) => setAddSymbol(e.target.value)}
                      placeholder="Symbol (e.g. BTC/USD)"
                      className="flex h-8 flex-1 rounded-md border border-input bg-background px-2 text-xs ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      onKeyDown={(e) => e.key === "Enter" && addItem(wl.id)}
                    />
                    <button
                      onClick={() => addItem(wl.id)}
                      className="inline-flex h-8 items-center rounded-md bg-primary px-2.5 text-xs font-medium text-primary-foreground hover:bg-primary/90"
                    >
                      Add
                    </button>
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
