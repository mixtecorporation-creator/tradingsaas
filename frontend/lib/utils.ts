import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number, decimals = 2): string {
  const abs = Math.abs(value);
  const formatted = abs >= 1e6
    ? `${(abs / 1e6).toFixed(2)}M`
    : abs >= 1e3
    ? `${(abs / 1e3).toFixed(1)}K`
    : abs.toFixed(decimals);
  return value < 0 ? `-$${formatted}` : `$${formatted}`;
}

export function formatPercent(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

export function formatNumber(value: number, decimals = 2): string {
  return value.toFixed(decimals);
}

export function cnx(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(" ");
}
