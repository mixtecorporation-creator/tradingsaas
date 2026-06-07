"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Sidebar } from "./sidebar";
import { Skeleton } from "@/components/ui/skeleton";
import { PriceTicker } from "@/components/market/price-ticker";
import { api } from "@/lib/api-client";
import type { Instrument } from "@/lib/types";

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [tickerSymbols, setTickerSymbols] = useState<string[]>([]);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/auth/login");
    }
  }, [user, isLoading, router]);

  useEffect(() => {
    if (!user) return;
    api.get<Instrument[]>("/instruments")
      .then((insts) => setTickerSymbols(insts.map((i) => i.symbol)))
      .catch(() => {});
  }, [user]);

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="space-y-4 w-80">
          <Skeleton className="h-8 w-48 mx-auto" />
          <Skeleton className="h-4 w-64 mx-auto" />
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex flex-1 flex-col overflow-hidden bg-background">
        {tickerSymbols.length > 0 && <PriceTicker symbols={tickerSymbols} />}
        <div className="flex-1 overflow-y-auto">
          <div className="container mx-auto p-6">{children}</div>
        </div>
      </main>
    </div>
  );
}
