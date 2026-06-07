export const TRADE_DIRECTIONS = ["long", "short"] as const;
export const EXPERIENCE_LEVELS = ["beginner", "intermediate", "advanced", "professional"] as const;
export const TRADING_STYLES = ["day_trader", "swing_trader", "scalper", "position_trader"] as const;
export const TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"] as const;
export const LEADERBOARD_PERIODS = ["weekly", "monthly", "quarterly", "yearly", "all_time"] as const;
export const POST_TYPES = ["trade_idea", "analysis", "journal", "general"] as const;
export const EMOTIONS = [
  "confident", "anxious", "excited", "fearful", "greedy",
  "patient", "impulsive", "neutral", "frustrated", "satisfied",
] as const;
export const MISTAKES = [
  "fomo", "revenge_trading", "oversizing", "no_stop_loss",
  "moved_stop_loss", "early_exit", "late_exit", "ignored_plan",
  "overtrading", "chasing",
] as const;
