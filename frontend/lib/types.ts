export interface User {
  id: string;
  email: string;
  display_name: string;
  avatar_url: string | null;
  role: string;
  email_verified_at: string | null;
  created_at: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Trade {
  id: string;
  user_id: string;
  instrument_id: string;
  direction: "long" | "short";
  entry_price: number;
  exit_price: number | null;
  quantity: number;
  entry_date: string;
  exit_date: string | null;
  pnl: number | null;
  pnl_percent: number | null;
  fees: number;
  setup: string | null;
  notes: string | null;
  tags: string[] | null;
  screenshots: string[] | null;
  setup_rating: number | null;
  execution_rating: number | null;
  emotion_before: string | null;
  emotion_after: string | null;
  mistake: string | null;
  created_at: string;
}

export interface Instrument {
  id: string;
  symbol: string;
  name: string | null;
  type: string;
  exchange: string | null;
  currency: string;
  active: boolean;
}

export interface OHLCV {
  open_time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface PageResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface CursorPageResponse<T> {
  items: T[];
  next_cursor: string | null;
  has_more: boolean;
}

export interface Watchlist {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  items: WatchlistItem[];
}

export interface WatchlistItem {
  id: string;
  watchlist_id: string;
  instrument_id: string;
  notes: string | null;
  sort_order: number;
}

export interface TraderProfile {
  id: string;
  user_id: string;
  bio: string | null;
  experience_level: string | null;
  trading_style: string[] | null;
  preferred_markets: string[] | null;
  website_url: string | null;
  twitter_handle: string | null;
  verified: boolean;
  verification_status: string;
  total_followers: number;
  created_at: string;
  updated_at: string;
}

export interface BacktestRun {
  id: string;
  user_id: string;
  instrument_id: string;
  strategy_name: string;
  strategy_config: Record<string, unknown>;
  timeframe: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  status: string;
  error_message: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface BacktestResult {
  id: string;
  backtest_run_id: string;
  total_return: number | null;
  total_return_pct: number | null;
  max_drawdown: number | null;
  max_drawdown_pct: number | null;
  sharpe_ratio: number | null;
  win_rate: number | null;
  total_trades: number | null;
  winning_trades: number | null;
  losing_trades: number | null;
  profit_factor: number | null;
  avg_win: number | null;
  avg_loss: number | null;
}

export interface LeaderboardEntry {
  user_id: string;
  display_name: string;
  avatar_url: string | null;
  rank: number;
  pnl: number;
  returns: number | null;
  win_rate: number | null;
  total_trades: number;
  verified: boolean;
  is_following: boolean;
}

export interface PerformanceSnapshot {
  id: string;
  period: string;
  period_start: string;
  period_end: string;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  total_pnl: number;
  total_pnl_pct: number | null;
  win_rate: number | null;
  profit_factor: number | null;
  sharpe_ratio: number | null;
  max_drawdown_pct: number | null;
}

export interface PostFeedItem {
  id: string;
  user_id: string;
  display_name: string;
  avatar_url: string | null;
  content: string;
  images: string[] | null;
  trade_id: string | null;
  type: string;
  likes_count: number;
  comments_count: number;
  liked_by_me: boolean;
  created_at: string;
}

export interface CommentItem {
  id: string;
  post_id: string;
  user_id: string;
  display_name: string;
  avatar_url: string | null;
  parent_id: string | null;
  content: string;
  created_at: string;
}

export interface ChatRoom {
  id: string;
  name: string;
  type: string;
  instrument_id: string | null;
  is_private: boolean;
  created_at: string;
}

export interface ChatMessage {
  id: string;
  room_id: string;
  user_id: string;
  content: string;
  created_at: string;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  description: string | null;
  price_monthly: number;
  price_yearly: number;
  features: Record<string, unknown>;
  active: boolean;
}

export interface UserSubscription {
  id: string;
  user_id: string;
  plan_id: string;
  status: string;
  current_period_start: string;
  current_period_end: string;
  created_at: string;
  canceled_at: string | null;
}

export interface Payment {
  id: string;
  user_id: string;
  amount: number;
  currency: string;
  status: string;
  provider: string;
  created_at: string;
}

export interface TradeAnalysis {
  risk_reward_ratio: number | null;
  position_size_suggestion: string | null;
  market_condition: string | null;
  key_levels: string[];
  sentiment: string | null;
  confidence: string | null;
  notes: string[];
}

export interface PerformanceSummary {
  total_trades: number;
  win_rate: number;
  profit_factor: number;
  sharpe_ratio: number | null;
  max_drawdown_pct: number | null;
  avg_hold_time: string | null;
  best_day: string | null;
  worst_day: string | null;
  improvement_tips: string[];
}

export interface LivePrice {
  symbol: string;
  name: string | null;
  price: number;
  bid: number;
  ask: number;
  change: number;
  change_pct: number;
  high_24h: number;
  low_24h: number;
  volume_24h: number;
  timestamp: string;
}

export interface Insight {
  title: string;
  description: string;
  type: string;
  severity: string;
}
