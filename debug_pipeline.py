"""
Debug 脚本：用 OpenRouter (gpt-4o-mini) 跑完整 pipeline。
在 VSCode 里按 F5 启动 debug，在 mini_coding_agent.py 里打断点观察执行。

需要先设置环境变量：
    export OPENROUTER_API_KEY="sk-or-v1-..."
"""
import os
from pathlib import Path

from mini_coding_agent import (
    WorkspaceContext,
    SessionStore,
    OpenRouterModelClient,
    MiniAgent,
)


def main():
    workspace = WorkspaceContext.build("/home/obob/rasbt-mini-coding-agent")

    store = SessionStore(Path("/tmp/mini-agent-debug-sessions"))

    client = OpenRouterModelClient(
        model="openai/gpt-4o-mini",
        api_key=os.environ["OPENROUTER_API_KEY"],
        host="https://openrouter.ai",
        temperature=0.2,
        top_p=0.9,
        timeout=60,
    )

    agent = MiniAgent(
        model_client=client,
        workspace=workspace,
        session_store=store,
        approval_policy="auto",
        max_steps=6,
    )

    result = agent.ask("看一下这个仓库根目录有什么文件，再读一下 README 的开头，告诉我这是什么项目")

    print("=" * 60)
    print("Final answer:", result)
    print("=" * 60)
    print("Session saved at:", agent.session_path)


if __name__ == "__main__":
    main()
