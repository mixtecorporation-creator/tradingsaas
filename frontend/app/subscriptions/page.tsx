"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import type { SubscriptionPlan, UserSubscription, Payment } from "@/lib/types";
import { Check, CreditCard, Shield } from "lucide-react";

export default function SubscriptionsPage() {
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [mySub, setMySub] = useState<UserSubscription | null>(null);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [billing, setBilling] = useState<"monthly" | "yearly">("monthly");
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get<SubscriptionPlan[]>("/subscriptions/plans"),
      api.get<UserSubscription | null>("/subscriptions/my").catch(() => null),
      api.get<Payment[]>("/subscriptions/payments").catch(() => []),
    ]).then(([plansData, subData, paymentsData]) => {
      setPlans(plansData);
      setMySub(subData);
      setPayments(paymentsData);
    }).catch(() => setError("Failed to load subscriptions"))
      .finally(() => setLoading(false));
  }, []);

  async function subscribe(planId: string) {
    try {
      setError("");
      const sub = await api.post<UserSubscription>("/subscriptions/subscribe", {
        plan_id: planId, billing,
      });
      setMySub(sub);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to subscribe");
    }
  }

  async function cancelSub() {
    try {
      await api.post("/subscriptions/cancel");
      setMySub(null);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to cancel");
    }
  }

  if (loading) {
    return <div className="mx-auto max-w-4xl space-y-6">
      <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">Loading...</div>
    </div>;
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Premium</h1>
        <p className="text-sm text-muted-foreground">Unlock advanced features and support the platform</p>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      {mySub && (
        <div className="rounded-lg border border-primary/30 bg-primary/5 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield className="h-5 w-5 text-primary" aria-hidden="true" />
            <div>
              <p className="text-sm font-medium">Active Subscription</p>
              <p className="text-xs text-muted-foreground">
                Status: {mySub.status} &middot; Renews {new Date(mySub.current_period_end).toLocaleDateString()}
              </p>
            </div>
          </div>
          <button onClick={cancelSub} className="text-xs text-muted-foreground hover:text-destructive underline">
            Cancel
          </button>
        </div>
      )}

      <div className="flex gap-1 rounded-lg border bg-card p-0.5 w-fit">
        {(["monthly", "yearly"] as const).map((b) => (
          <button key={b} onClick={() => setBilling(b)}
            className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
              billing === b ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
            }`}>
            {b === "monthly" ? "Monthly" : "Yearly"}
            {b === "yearly" && <span className="ml-1 text-[10px] opacity-80">-20%</span>}
          </button>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {plans.map((plan) => {
          const price = billing === "monthly" ? plan.price_monthly : plan.price_yearly;
          return (
            <div key={plan.id} className={`rounded-xl border bg-card p-6 flex flex-col ${
              plan.name === "Pro" ? "border-primary/40 ring-1 ring-primary/20" : "border-border/40"
            }`}>
              <h3 className="text-lg font-semibold">{plan.name}</h3>
              <p className="mt-1 text-3xl font-bold tracking-tight">
                ${price}
                <span className="ml-0.5 text-sm font-normal text-muted-foreground">/{billing === "monthly" ? "mo" : "yr"}</span>
              </p>
              <p className="mt-1 text-sm text-muted-foreground">{plan.description}</p>
              <ul className="mt-6 flex-1 space-y-3">
                {(plan.features?.items as string[] || []).map((f: string, i: number) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                    {f}
                  </li>
                ))}
              </ul>
              <button onClick={() => subscribe(plan.id)}
                className={`mt-6 inline-flex h-10 w-full items-center justify-center rounded-md text-sm font-medium transition-all ${
                  plan.name === "Pro"
                    ? "bg-primary text-primary-foreground shadow-lg shadow-primary/20 hover:bg-primary/90"
                    : "border border-border/60 bg-card text-foreground hover:bg-muted"
                }`}>
                {plan.name === "Free" ? "Current Plan" : "Subscribe"}
              </button>
            </div>
          );
        })}
      </div>

      {payments.length > 0 && (
        <div className="rounded-lg border bg-card p-6">
          <h2 className="text-sm font-semibold mb-4">Payment History</h2>
          <div className="space-y-2">
            {payments.map((pmt) => (
              <div key={pmt.id} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <CreditCard className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
                  <span>{new Date(pmt.created_at).toLocaleDateString()}</span>
                </div>
                <span className="font-medium">${pmt.amount}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
