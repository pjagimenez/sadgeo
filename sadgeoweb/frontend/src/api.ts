export async function request<T>(
  path: string,
  method = "GET",
  body?: unknown,
): Promise<T> {
  const headers: Record<string, string> = {};
  if (method !== "GET") {
    const tokenResponse = await fetch("/api/auth/csrf", {
      credentials: "same-origin",
    });
    if (!tokenResponse.ok)
      throw new Error("Não foi possível obter a proteção CSRF.");
    const token = await tokenResponse.json();
    headers[token.headerName] = token.token;
    headers["Content-Type"] = "application/json";
  }
  const response = await fetch(path, {
    method,
    credentials: "same-origin",
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    let message = `Falha na operação (HTTP ${response.status}).`;
    try {
      const data = await response.json();
      if (data.message) message = data.message;
    } catch {
      /* Keep the HTTP status when no JSON body is available. */
    }
    throw new Error(message);
  }
  return response.status === 204 ? (undefined as T) : response.json();
}
