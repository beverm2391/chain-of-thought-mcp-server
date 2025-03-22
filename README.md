# Think MCP Server

This MCP Server uses Groq's API to call LLMs which expose raw chain-of-thought tokens from Qwen's [qwq model](https://qwenlm.github.io/blog/qwq-32b/).

## Installation 

1. Clone this repository to your local machine.
2. Get a Groq API key from [here](https://console.groq.com/keys).
3. Update your mcp configuration with:

```json
"mcp_servers": {
  "chain_of_thought": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/cot-mcp-server",
        "run",
        "src/server.py"
      ],
      "env": {
        "GROQ_API_KEY": "your-groq-api-key"
      }
    }
}
```

The path should be the local path to this repository. You can get this easily by running `pwd` in the terminal from the root of the repository.

## Instructing The AI To Use This MCP Server

I personally prefer the agent call this tool on every request to increase performance. I add this to my rules for the agent:

```xml
<IMPORTANT>
You should call the mcp chain_of_thought tool every time you talk to the user, which generates a chain-of-thought stream which you will use to complete the user's request.
</IMPORTANT>
```

Obviously, you can change this to whatever you want.