import { cn } from "@/lib/utils";

interface BadgeProps {
  variant?: "default" | "success" | "danger" | "warning" | "outline";
  children: React.ReactNode;
  className?: string;
}

const variantClasses = {
  default: "bg-primary/10 text-primary",
  success: "bg-green-500/10 text-green-600 dark:text-green-400",
  danger: "bg-red-500/10 text-red-600 dark:text-red-400",
  warning: "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400",
  outline: "border border-border text-muted-foreground",
};

export function Badge({ variant = "default", children, className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantClasses[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
