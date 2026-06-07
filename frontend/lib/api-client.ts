"use client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

export function getAccessToken(): string | null {
  return accessToken;
}

async function request<T>(
  method: string,
  path: string,
  body?: unknown,
  options?: RequestInit,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers as Record<string, string>),
  };

  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    credentials: "include",
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new ApiError(response.status, error.detail || "Request failed");
  }

  return response.json();
}

export const api = {
  get: <T>(path: string, options?: RequestInit) => request<T>("GET", path, undefined, options),
  post: <T>(path: string, body?: unknown, options?: RequestInit) => request<T>("POST", path, body, options),
  put: <T>(path: string, body?: unknown, options?: RequestInit) => request<T>("PUT", path, body, options),
  patch: <T>(path: string, body?: unknown, options?: RequestInit) => request<T>("PATCH", path, body, options),
  delete: <T>(path: string, options?: RequestInit) => request<T>("DELETE", path, undefined, options),
};

export { ApiError };
