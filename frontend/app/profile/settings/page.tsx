"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { api } from "@/lib/api-client";
import type { TraderProfile } from "@/lib/types";
import { Shield, RefreshCw } from "lucide-react";

export default function SettingsPage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState<TraderProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    bio: "",
    experience_level: "",
    website_url: "",
    twitter_handle: "",
  });

  useEffect(() => {
    api.get<TraderProfile>("/profiles/me")
      .then((data) => {
        setProfile(data);
        setForm({
          bio: data.bio ?? "",
          experience_level: data.experience_level ?? "",
          website_url: data.website_url ?? "",
          twitter_handle: data.twitter_handle ?? "",
        });
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  async function saveProfile() {
    try {
      setSaving(true);
      setError("");
      setSuccess("");
      const updated = await api.put<TraderProfile>("/profiles/me", {
        bio: form.bio || null,
        experience_level: form.experience_level || null,
        website_url: form.website_url || null,
        twitter_handle: form.twitter_handle || null,
      });
      setProfile(updated);
      setSuccess("Profile saved");
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">
          <RefreshCw className="mx-auto h-5 w-5 animate-spin" aria-hidden="true" />
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground">Manage your account and profile</p>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}
      {success && (
        <div className="rounded-lg border border-primary/30 bg-primary/10 px-3 py-2 text-sm text-primary">
          {success}
        </div>
      )}

      <div className="rounded-lg border bg-card p-6 space-y-4">
        <h2 className="text-sm font-semibold">Account</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground">Email</p>
            <p className="text-sm">{user?.email}</p>
          </div>
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground">Display Name</p>
            <p className="text-sm">{user?.display_name}</p>
          </div>
        </div>
      </div>

      <div className="rounded-lg border bg-card p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold">Profile</h2>
          {profile?.verified && (
            <span className="inline-flex items-center gap-1 rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
              <Shield className="h-3 w-3" aria-hidden="true" />
              Verified
            </span>
          )}
        </div>
        <div className="space-y-3">
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Bio</label>
            <textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })}
              rows={3}
              className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              placeholder="Tell other traders about yourself"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Experience Level</label>
            <select value={form.experience_level} onChange={(e) => setForm({ ...form, experience_level: e.target.value })}
              className="flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
              <option value="">Select...</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="professional">Professional</option>
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Website</label>
            <input value={form.website_url} onChange={(e) => setForm({ ...form, website_url: e.target.value })}
              className="flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              placeholder="https://"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">Twitter</label>
            <input value={form.twitter_handle} onChange={(e) => setForm({ ...form, twitter_handle: e.target.value })}
              className="flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              placeholder="@handle"
            />
          </div>
        </div>
        <button onClick={saveProfile} disabled={saving}
          className="inline-flex h-9 items-center gap-1.5 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50">
          {saving ? "Saving..." : "Save Profile"}
        </button>
      </div>

      <div className="rounded-lg border bg-card p-6 space-y-4">
        <h2 className="text-sm font-semibold">Verification</h2>
        <p className="text-xs text-muted-foreground">
          Status: <span className="font-medium text-foreground capitalize">{profile?.verification_status ?? "unverified"}</span>
        </p>
        {!profile?.verified && (
          <p className="text-xs text-muted-foreground">
            Verification is required for leaderboard eligibility and creator monetization.
          </p>
        )}
      </div>
    </div>
  );
}
