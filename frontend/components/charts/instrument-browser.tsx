"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

interface InstrumentBrowserProps {
  onSelect?: (symbol: string) => void;
  selectedSymbol?: string;
}

export function InstrumentBrowser({ onSelect, selectedSymbol }: InstrumentBrowserProps) {
  const [search, setSearch] = useState("");

  const { data: instruments, isLoading } = useQuery({
    queryKey: ["instruments"],
    queryFn: () => api.get<any[]>("/instruments"),
  });

  const filtered = (instruments || []).filter(
    (inst: any) =>
      inst.symbol.toLowerCase().includes(search.toLowerCase()) ||
      (inst.name && inst.name.toLowerCase().includes(search.toLowerCase())),
  );

  return (
    <div className="space-y-2">
      <input
        type="text"
        placeholder="Search instruments..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm"
      />
      <div className="max-h-60 overflow-y-auto space-y-1 scrollbar-thin">
        {isLoading ? (
          <div className="space-y-2 p-2">
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} className="h-8 w-full" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <p className="py-4 text-center text-sm text-muted-foreground">No instruments found</p>
        ) : (
          filtered.map((inst: any) => (
            <button
              key={inst.id}
              onClick={() => onSelect?.(inst.symbol)}
              className={`flex w-full items-center justify-between rounded-md px-3 py-2 text-sm transition-colors hover:bg-accent ${
                selectedSymbol === inst.symbol ? "bg-accent font-medium" : ""
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="font-medium">{inst.symbol}</span>
                {inst.name && inst.name !== inst.symbol && (
                  <span className="text-xs text-muted-foreground">{inst.name}</span>
                )}
              </div>
              <Badge variant="outline">{inst.type}</Badge>
            </button>
          ))
        )}
      </div>
    </div>
  );
}
