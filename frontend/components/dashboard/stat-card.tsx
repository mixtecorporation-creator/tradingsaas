import { cn } from "@/lib/utils";

interface StatCardProps {
  title: string;
  value: string;
  change?: string;
  className?: string;
}

export function StatCard({ title, value, change, className }: StatCardProps) {
  const isPositive = change?.startsWith("+");
  const isNegative = change?.startsWith("-");

  return (
    <div className={cn("rounded-lg border bg-card p-4", className)}>
      <p className="text-sm text-muted-foreground">{title}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
      {change && (
        <p
          className={cn(
            "mt-1 text-xs",
            isPositive && "text-green-600",
            isNegative && "text-red-600",
            !isPositive && !isNegative && "text-muted-foreground",
          )}
        >
          {change}
        </p>
      )}
    </div>
  );
}
