# Think MCP Server

Anthropics recent article ["The "think" tool: Enabling Claude to stop and think in complex tool use situations"](https://www.anthropic.com/engineering/claude-think-tool) shows that using an external `think` tool notable increases performance on [SWE Bench](https://www.swebench.com/).

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
<when_to_use_tool>
You should call the mcp chain_of_thought tool every time you talk to the user, which generates a chain-of-thought stream which you will use to complete the user's request.
</when_to_use_tool>

Before taking any action or responding to the user use the chain of thought tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness 

Here are some examples of what to iterate over inside the think tool:
<cot_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
  * Is it within 24h of booking?
  * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</cot_tool_example_1>

<cot_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
  * Membership tier for baggage allowance
  * Which payments methods exist in profile
- Baggage calculation:
  * Economy class × 3 passengers
  * If regular member: 1 free bag each → 3 extra bags = $150
  * If silver member: 2 free bags each → 0 extra bags = $0
  * If gold member: 3 free bags each → 0 extra bags = $0
- Payment rules to verify:
  * Max 1 travel certificate, 1 credit card, 3 gift cards
  * All payment methods must be in profile
  * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</cot_tool_example_2>

</IMPORTANT>
```