export function LoadingSpinner({ size = "md" }: { size?: "sm" | "md" | "lg" }) {
  const sizeClass = { sm: "h-4 w-4", md: "h-6 w-6", lg: "h-8 w-8" };
  return (
    <div className="flex items-center justify-center">
      <div
        className={`${sizeClass[size]} animate-spin rounded-full border-2 border-muted-foreground/30 border-t-primary`}
      />
    </div>
  );
}

export function LoadingPage() {
  return (
    <div className="flex h-full min-h-[400px] items-center justify-center">
      <LoadingSpinner size="lg" />
    </div>
  );
}
