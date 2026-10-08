import hashlib
import os

from mcp.server.mcpserver import MCPServer, Context

EMAIL = "24f1000574@ds.study.iitm.ac.in"

mcp = MCPServer("solve-challenge-server")


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the first 16 SHA-256 hex characters for the exam challenge."""

    headers = ctx.headers or {}
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    normalized_email = EMAIL.strip().lower()
    message = f"{challenge}:{normalized_email}"

    return hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )