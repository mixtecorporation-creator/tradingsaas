"use client";

import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import { formatCurrency, formatPercent } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

export default function TradeDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const queryClient = useQueryClient();

  const { data: trade, isLoading } = useQuery({
    queryKey: ["trade", id],
    queryFn: () => api.get<any>(`/trades/${id}`),
    enabled: !!id,
  });

  const deleteMutation = useMutation({
    mutationFn: () => api.delete(`/trades/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["trades"] });
      router.push("/dashboard/trades");
    },
  });

  if (isLoading) {
    return <div className="space-y-4"><Skeleton className="h-8 w-48" /><Skeleton className="h-64 w-full" /></div>;
  }

  if (!trade) {
    return <div className="text-center py-12 text-muted-foreground">Trade not found</div>;
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Trade Details</h1>
          <p className="text-sm text-muted-foreground">
            {new Date(trade.entry_date).toLocaleString()}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => router.back()}
            className="inline-flex h-9 items-center rounded-md border border-input bg-background px-3 text-sm"
          >
            Back
          </button>
          <button
            onClick={() => deleteMutation.mutate()}
            className="inline-flex h-9 items-center rounded-md bg-destructive px-3 text-sm text-destructive-foreground"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="rounded-lg border p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-muted-foreground">Direction</p>
            <Badge variant={trade.direction === "long" ? "success" : "danger"} className="mt-1">
              {trade.direction}
            </Badge>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">P&L</p>
            <p className={`mt-1 text-lg font-semibold ${trade.pnl > 0 ? "text-green-500" : trade.pnl < 0 ? "text-red-500" : ""}`}>
              {trade.pnl ? formatCurrency(parseFloat(trade.pnl)) : "Open"}
              {trade.pnl_percent ? ` (${formatPercent(parseFloat(trade.pnl_percent))})` : ""}
            </p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Entry Price</p>
            <p className="mt-1 font-medium">${parseFloat(trade.entry_price).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Exit Price</p>
            <p className="mt-1 font-medium">{trade.exit_price ? `$${parseFloat(trade.exit_price).toFixed(2)}` : "-"}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Quantity</p>
            <p className="mt-1 font-medium">{parseFloat(trade.quantity).toFixed(4)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Fees</p>
            <p className="mt-1 font-medium">${parseFloat(trade.fees).toFixed(2)}</p>
          </div>
        </div>

        {trade.tags?.length > 0 && (
          <div>
            <p className="text-xs text-muted-foreground mb-2">Tags</p>
            <div className="flex gap-1 flex-wrap">
              {trade.tags.map((tag: string) => (
                <Badge key={tag} variant="outline">{tag}</Badge>
              ))}
            </div>
          </div>
        )}

        {trade.notes && (
          <div>
            <p className="text-xs text-muted-foreground mb-1">Notes</p>
            <p className="text-sm whitespace-pre-wrap">{trade.notes}</p>
          </div>
        )}

        {trade.setup && (
          <div>
            <p className="text-xs text-muted-foreground mb-1">Setup</p>
            <p className="text-sm">{trade.setup}</p>
          </div>
        )}

        {(trade.emotion_before || trade.emotion_after || trade.mistake) && (
          <div className="grid grid-cols-3 gap-4 pt-2 border-t">
            {trade.emotion_before && (
              <div>
                <p className="text-xs text-muted-foreground">Before Trade</p>
                <p className="text-sm font-medium capitalize">{trade.emotion_before}</p>
              </div>
            )}
            {trade.emotion_after && (
              <div>
                <p className="text-xs text-muted-foreground">After Trade</p>
                <p className="text-sm font-medium capitalize">{trade.emotion_after}</p>
              </div>
            )}
            {trade.mistake && (
              <div>
                <p className="text-xs text-muted-foreground">Mistake</p>
                <p className="text-sm font-medium capitalize">{trade.mistake.replace(/_/g, " ")}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
