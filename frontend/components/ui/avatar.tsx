"use client";

import { cn } from "@/lib/utils";

interface AvatarProps {
  src?: string | null;
  name: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizeMap = { sm: "h-8 w-8 text-xs", md: "h-10 w-10 text-sm", lg: "h-14 w-14 text-lg" };

export function Avatar({ src, name, size = "md", className }: AvatarProps) {
  if (src) {
    return (
      <img
        src={src}
        alt={name}
        width={size === "sm" ? 32 : size === "lg" ? 56 : 40}
        height={size === "sm" ? 32 : size === "lg" ? 56 : 40}
        className={cn("rounded-full object-cover", sizeMap[size], className)}
      />
    );
  }

  const initials = name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <div
      className={cn(
        "flex items-center justify-center rounded-full bg-primary/10 font-medium text-primary",
        sizeMap[size],
        className,
      )}
    >
      {initials}
    </div>
  );
}
