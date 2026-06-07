"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { PostFeedItem, CommentItem } from "@/lib/types";
import { Heart, MessageSquare, Send, Trash2, TrendingUp } from "lucide-react";

export default function CommunityPage() {
  const [posts, setPosts] = useState<PostFeedItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [newPost, setNewPost] = useState("");
  const [commentText, setCommentText] = useState("");
  const [comments, setComments] = useState<Record<string, CommentItem[]>>({});
  const [openComments, setOpenComments] = useState<string | null>(null);

  useEffect(() => { loadFeed(); }, []);

  async function loadFeed() {
    try {
      setLoading(true);
      setError("");
      const data = await api.get<{ items: PostFeedItem[]; total: number }>("/community/feed");
      setPosts(data.items);
      setTotal(data.total);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load feed");
    } finally {
      setLoading(false);
    }
  }

  async function createPost() {
    if (!newPost.trim()) return;
    try {
      setError("");
      await api.post("/community/posts", { content: newPost.trim() });
      setNewPost("");
      await loadFeed();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to post");
    }
  }

  async function toggleLike(postId: string) {
    try {
      await api.post<{ liked: boolean }>(`/community/posts/${postId}/like`);
      setPosts(posts.map((p) =>
        p.id === postId
          ? { ...p, liked_by_me: !p.liked_by_me, likes_count: p.likes_count + (p.liked_by_me ? -1 : 1) }
          : p
      ));
    } catch {}
  }

  async function deletePost(postId: string) {
    try {
      await api.delete(`/community/posts/${postId}`);
      setPosts(posts.filter((p) => p.id !== postId));
    } catch {}
  }

  async function loadComments(postId: string) {
    if (openComments === postId) {
      setOpenComments(null);
      return;
    }
    setOpenComments(postId);
    try {
      const data = await api.get<CommentItem[]>(`/community/posts/${postId}/comments`);
      setComments({ ...comments, [postId]: data });
    } catch {}
  }

  async function addComment(postId: string) {
    if (!commentText.trim()) return;
    try {
      await api.post(`/community/posts/${postId}/comments`, { content: commentText.trim() });
      setCommentText("");
      await loadComments(postId);
      setPosts(posts.map((p) =>
        p.id === postId ? { ...p, comments_count: p.comments_count + 1 } : p
      ));
    } catch {}
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Community</h1>
        <p className="text-sm text-muted-foreground">Share trades, ideas, and learn from others</p>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="rounded-lg border bg-card p-4 space-y-3">
        <textarea value={newPost} onChange={(e) => setNewPost(e.target.value)}
          rows={2} placeholder="Share something with the community..."
          className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
        <div className="flex justify-between items-center">
          <span className="text-xs text-muted-foreground">{total} posts</span>
          <button onClick={createPost}
            className="inline-flex h-8 items-center gap-1.5 rounded-md bg-primary px-3 text-xs font-medium text-primary-foreground hover:bg-primary/90">
            <TrendingUp className="h-3.5 w-3.5" aria-hidden="true" />
            Post
          </button>
        </div>
      </div>

      {loading ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">Loading...</div>
      ) : posts.length === 0 ? (
        <div className="rounded-lg border p-12 text-center text-sm text-muted-foreground">No posts yet. Be the first to share!</div>
      ) : (
        <div className="space-y-4">
          {posts.map((post) => (
            <div key={post.id} className="rounded-lg border bg-card">
              <div className="p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-xs font-medium text-primary">
                      {post.display_name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{post.display_name}</p>
                      <p className="text-xs text-muted-foreground">{new Date(post.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <button onClick={() => deletePost(post.id)} className="text-muted-foreground hover:text-destructive">
                    <Trash2 className="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
                <p className="text-sm leading-relaxed">{post.content}</p>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <button onClick={() => toggleLike(post.id)}
                    className={`inline-flex items-center gap-1 transition-colors ${post.liked_by_me ? "text-primary" : "hover:text-foreground"}`}>
                    <Heart className={`h-4 w-4 ${post.liked_by_me ? "fill-current" : ""}`} aria-hidden="true" />
                    {post.likes_count}
                  </button>
                  <button onClick={() => loadComments(post.id)}
                    className="inline-flex items-center gap-1 hover:text-foreground transition-colors">
                    <MessageSquare className="h-4 w-4" aria-hidden="true" />
                    {post.comments_count}
                  </button>
                </div>
              </div>
              {openComments === post.id && (
                <div className="border-t px-4 py-3 space-y-3">
                  {(comments[post.id] || []).map((c) => (
                    <div key={c.id} className="flex gap-2 text-sm">
                      <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-medium text-primary">
                        {c.display_name.charAt(0)}
                      </div>
                      <div>
                        <p className="text-xs font-medium">{c.display_name}</p>
                        <p className="text-xs text-muted-foreground">{c.content}</p>
                      </div>
                    </div>
                  ))}
                  <div className="flex gap-2">
                    <input value={commentText} onChange={(e) => setCommentText(e.target.value)}
                      placeholder="Write a comment..."
                      className="flex h-8 flex-1 rounded-md border border-input bg-background px-2 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      onKeyDown={(e) => e.key === "Enter" && addComment(post.id)}
                    />
                    <button onClick={() => addComment(post.id)}
                      className="inline-flex h-8 items-center rounded-md bg-primary px-2 text-xs font-medium text-primary-foreground hover:bg-primary/90">
                      <Send className="h-3.5 w-3.5" aria-hidden="true" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
