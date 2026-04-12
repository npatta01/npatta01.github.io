---
title: Claude Code Tracing
date: 2026-03-29
tags:
  - claude
  - tracing
  - openrouter
categories:
  - claude
---

Tracing Claude Code is useful when you want to inspect prompts, understand tool usage, or keep an eye on cost. The three approaches I use most are:

1. `claude-code-logger` for full request and response inspection
2. Arize's `claude-code-tracing` plugin for Phoenix traces
3. OpenRouter for hosted usage visibility and cost tracking

<!--more-->

| Need | Best option |
| --- | --- |
| Full prompt and response visibility | `claude-code-logger` |
| Structured traces in Phoenix | `claude-code-tracing` |
| Team usage and cost dashboard | OpenRouter |

## 1. Trace with `claude-code-logger`

[`claude-code-logger`](https://github.com/dreampulse/claude-code-logger) is a local proxy that sits between Claude Code and the upstream Anthropic-compatible API. It is the easiest option when you want to see the live conversation, tool activity, and streaming responses in one place.

Start the logger in one terminal:

```bash
npx claude-code-logger start
```

Then start Claude Code in another terminal and point it at the proxy:

```bash
ANTHROPIC_BASE_URL=http://localhost:8000/ claude
```

Useful variants:

```bash
# show full prompts instead of truncated output
npx claude-code-logger start --verbose

# save a local log you can grep later
npx claude-code-logger start 2>&1 | tee claude-session.log
```

Why this is nice:

- You can watch the conversation as it streams.
- You can inspect tool usage and prompt context.
- It is great for debugging strange Claude Code behavior.

Trade-offs:

- This is effectively a man-in-the-middle proxy, so it sees everything Claude Code sends.
- It is best for local debugging, not long-term analytics.
- Avoid using it in environments where prompts may contain secrets or sensitive code unless you are comfortable logging that data locally.

## 2. Trace with Phoenix using `claude-code-tracing`

If you want structured traces in Phoenix, the cleanest path is Arize's [`claude-code-tracing`](https://github.com/Arize-ai/arize-claude-code-plugin) plugin. It hooks into Claude Code and emits OpenInference spans for sessions, turns, model calls, tool usage, and subagents.

This one matters because it is not a normal "drop a script into `.claude/hooks`" setup. The tracing plugin is installed through the Claude Code plugin system.

Install the marketplace and tracing plugin:

```bash
claude plugin marketplace add Arize-ai/arize-claude-code-plugin
claude plugin install claude-code-tracing@arize-claude-plugin
```

Then launch Claude Code in your project:

```bash
cd your-project
claude
```

Inside Claude Code, run the guided setup command:

```text
/setup-claude-code-tracing
```

That setup flow walks you through:

- choosing Phoenix or Arize AX as the backend
- collecting the endpoint and any credentials
- writing the tracing config for you
- validating that tracing is working

For Phoenix, the usual local endpoint is:

```text
http://localhost:6006
```

If you want to understand what the setup command is writing, the minimal Phoenix config in `.claude/settings.local.json` looks like this:

```json
{
  "env": {
    "PHOENIX_ENDPOINT": "http://localhost:6006",
    "ARIZE_TRACE_ENABLED": "true"
  }
}
```

If your Phoenix instance requires auth, add the API key too:

```json
{
  "env": {
    "PHOENIX_ENDPOINT": "http://localhost:6006",
    "PHOENIX_API_KEY": "your-phoenix-api-key",
    "ARIZE_TRACE_ENABLED": "true"
  }
}
```

After setup, restart Claude Code so the tracing hooks are active:

```bash
claude
```

What you get in Phoenix:

- turn traces for each prompt and response
- LLM spans with model metadata and token counts
- tool spans with input, output, and duration
- subagent spans when Claude spawns extra work
- session grouping by `session_id`

Helpful debugging commands:

```bash
ARIZE_DRY_RUN=true claude
ARIZE_VERBOSE=true claude
tail -f /tmp/arize-claude-code.log
```

Why this is nice:

- It gives you much richer observability than a single custom hook.
- Phoenix setup does not require Python.
- `/setup-claude-code-tracing` is much easier than wiring all 9 hook events by hand.

Trade-offs:

- It depends on the Claude Code plugin system, so install and setup happen inside that workflow.
- It is meant for structured tracing, not raw packet-level request inspection.
- If you switch to Arize AX instead of Phoenix, you will need extra Python packages for the cloud exporter.

## 3. Trace via OpenRouter

If the main goal is usage visibility and cost tracking, OpenRouter is the cleanest setup. Claude Code can talk to OpenRouter through its Anthropic-compatible endpoint, and then requests show up in the OpenRouter activity dashboard.

Use environment variables like this:

```bash
export OPENROUTER_API_KEY="<your-openrouter-api-key>"
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""

# optional: use OpenRouter's free model router
export ANTHROPIC_MODEL="openrouter/free"
```

Important details:

- `ANTHROPIC_API_KEY` should be explicitly set to an empty string so Claude Code does not fall back to direct Anthropic auth.
- `ANTHROPIC_MODEL="openrouter/free"` routes requests to OpenRouter's free model router. It can make a Claude Code session free, but the selected backend model can change based on availability and required capabilities.
- If you were previously logged in directly with Anthropic, run `/logout` once before retrying.
- The native Claude Code install does not read a project `.env` file, so put these in your shell profile or export them before launching `claude`.

Start Claude Code normally:

```bash
claude
```

Then verify inside Claude Code:

```text
/status
```

You should see the auth token source and the base URL pointing at `https://openrouter.ai/api`. From there, usage should appear in the OpenRouter dashboard.

The two OpenRouter screens I use most after that are:

- `Activity -> Logs -> Generations` for per-request tokens, cost, provider, finish reason, and generation details
- `Observability -> Broadcast` when I want OpenRouter to fan traces out to another tool like LangSmith

Why this is nice:

- Hosted activity and cost visibility
- Useful for teams
- No local proxy to keep running

Trade-offs:

- It is observability at the provider layer, not full packet-level debugging.
- You should still think carefully about provider-side logging and privacy settings.

## Screenshot Files

These are the names I am using for the screenshots in this post bundle:

- `static/claude-code-logger-startup.png` for the local proxy startup screen
- `static/claude-status-openrouter.png` for the Claude Code `/status` screen showing OpenRouter routing
- `static/openrouter-logs-generations.png` for the OpenRouter generations table
- `static/openrouter-generation-details.png` for the OpenRouter generation details modal
- `static/openrouter-observability-broadcast.png` for the OpenRouter Broadcast destination screen
- `static/langsmith-openrouter-trace-system-prompt.png` for the LangSmith trace showing the captured system prompt

## Captured System Prompt

One thing that stood out in the OpenRouter trace is that the request metadata includes the Claude Code billing header:

```text
x-anthropic-billing-header: cc_version=2.1.86.543; cc_entrypoint=cli; cch=7aefd;
```

And the captured system message starts with:

```text
You are Claude Code, Anthropic's official CLI for Claude.
```

I saved the full raw prompt capture in `claude_code_system_prompt.txt` next to this post and render it below directly from that file.

{{< include-text file="content/post/2026/claude_tracing/claude_code_system_prompt.txt" summary="Full captured Claude Code system prompt" >}}

## Which One I Reach For

I usually pick the method based on the question I am trying to answer:

- "What exact prompt and response did Claude send?" Use `claude-code-logger`.
- "I want session and tool traces in Phoenix." Use `claude-code-tracing`.
- "How much is this costing, and who is using it?" Use OpenRouter.

## References

- [claude-code-logger](https://github.com/dreampulse/claude-code-logger)
- [Arize Claude Code Plugin](https://github.com/Arize-ai/arize-claude-code-plugin)
- [Arize Claude Code Tracing docs](https://arize.com/docs/ax/integrations/platforms/claude-code/claude-code-tracing)
- [OpenRouter Claude Code integration guide](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration)
- [OpenRouter Free Models Router](https://openrouter.ai/openrouter/free/apps)
