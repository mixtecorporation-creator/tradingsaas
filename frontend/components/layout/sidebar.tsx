"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import { Avatar } from "@/components/ui/avatar";
import {
  LayoutDashboard,
  TrendingUp,
  LineChart,
  BookOpen,
  Beaker,
  User,
  Trophy,
  Users,
  CreditCard,
  MessageSquare,
  LogOut,
  BarChart3,
} from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/charts", label: "Charts", icon: LineChart },
  { href: "/dashboard/markets", label: "Markets", icon: BarChart3 },
  { href: "/dashboard/trades", label: "Journal", icon: BookOpen },
  { href: "/dashboard/backtests", label: "Backtests", icon: Beaker },
  { href: "/dashboard/watchlists", label: "Watchlists", icon: TrendingUp },
  { href: "/dashboard/analytics", label: "Analytics", icon: LineChart },
  { href: "/leaderboards", label: "Leaderboards", icon: Trophy },
  { href: "/community", label: "Community", icon: Users },
  { href: "/community/chat", label: "Chat", icon: MessageSquare },
  { href: "/subscriptions", label: "Premium", icon: CreditCard },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="flex h-full w-60 flex-col border-r bg-card">
      <div className="flex h-14 items-center border-b px-4">
        <Link href="/dashboard" className="flex items-center gap-2 font-semibold">
          <TrendingUp className="h-5 w-5 text-primary" />
          <span>TradeSaaS</span>
        </Link>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-3 scrollbar-thin">
        {navItems.map((item) => {
          const active = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t p-3">
        <Link
          href="/profile/settings"
          className="flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors hover:bg-accent"
        >
          <Avatar src={user?.avatar_url} name={user?.display_name || "User"} size="sm" />
          <div className="flex-1 truncate">
            <p className="text-sm font-medium">{user?.display_name}</p>
            <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
          </div>
        </Link>
        <button
          onClick={logout}
          className="mt-1 flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-accent hover:text-destructive"
        >
          <LogOut className="h-4 w-4" />
          Sign out
        </button>
      </div>
    </aside>
  );
}
