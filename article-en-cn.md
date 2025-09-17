# Gemini CLI: Custom slash commands
# Gemini CLI：自定义斜杠命令

![Gemini CLI Custom Slash Commands](resources/custom_slash_commands_header.max-2600x2600.png)

Today, Google announced support for custom slash commands in Gemini CLI. This feature allows users to define reusable prompts to streamline their interactions with Gemini CLI and improve workflow efficiency. Slash commands can be defined in local `.toml` files or through Model Context Protocol (MCP) prompts.
今天，谷歌宣布在 Gemini CLI 中支持自定义斜杠命令。此功能允许用户定义可重用的提示，以简化他们与 Gemini CLI 的交互并提高工作流程效率。斜杠命令可以在本地 `.toml` 文件中定义，也可以通过模型上下文协议 (MCP) 提示来定义。

To use slash commands, you need to update to the latest version of Gemini CLI.
要使用斜杠命令，您需要更新到最新版本的 Gemini CLI。

### Creating Custom Slash Commands with `.toml` files
### 使用 `.toml` 文件创建自定义斜杠命令

Custom slash commands are based on `.toml` files. The file name defines the command name, and the file's content specifies the command's behavior. The `.toml` file has a minimal set of required keys, with `prompt` being the only mandatory one. You can use `{{args}}` to pass arguments and `!{...}` to execute shell commands within the prompt.
自定义斜杠命令基于 `.toml` 文件。文件名定义了命令名称，文件内容指定了命令的行为。`.toml` 文件有一组最少的必需键，其中 `prompt` 是唯一强制性的。您可以使用 `{{args}}` 传递参数，并使用 `!{...}` 在提示中执行 shell 命令。

For example, a `/review <issue_number>` command can be created to review a GitHub pull request. The `review.toml` file would contain a prompt that uses `gh` CLI commands to view the PR, its diff, and post a review.
例如，可以创建一个 `/review <issue_number>` 命令来审查 GitHub 拉取请求。`review.toml` 文件将包含一个提示，该提示使用 `gh` CLI 命令查看 PR、其差异并发布审查。

![Review Command](resources/custom_slash_commands_review.gif)

Commands can be namespaced by organizing them into sub-directories. For instance, a command defined in `.gemini/commands/git/commit.toml` would be invoked as `/git:commit`.
通过将命令组织到子目录中，可以对命令进行命名空间划分。例如，在 `.gemini/commands/git/commit.toml` 中定义的命令将作为 `/git:commit` 调用。

![Namespace Command](resources/custom_slash_commands_namespaces.gif)

Custom slash commands can be user-scoped (available across all projects) by placing them in `~/.gemini/commands/` or project-scoped (available only within a specific project) by placing them in `.gemini/commands/`.
通过将自定义斜杠命令放置在 `~/.gemini/commands/` 中，可以使其在用户范围内（在所有项目中可用），或者通过将其放置在 `.gemini/commands/` 中，可以使其在项目范围内（仅在特定项目中可用）。

### Building a `/plan` command
### 构建 `/plan` 命令

The article provides a step-by-step guide to creating a `/plan` command:
本文提供了创建 `/plan` 命令的分步指南：

1.  **Create the command file**: Create a file named `plan.toml` in `~/.gemini/commands/`.
1.  **创建命令文件**：在 `~/.gemini/commands/` 中创建一个名为 `plan.toml` 的文件。
2.  **Add the command definition**: Add a `description` and a `prompt` to the `plan.toml` file. The prompt instructs Gemini to act as a strategist, investigate the codebase, and create a detailed plan to achieve a given goal without writing any code.
2.  **添加命令定义**：向 `plan.toml` 文件添加 `description` 和 `prompt`。该提示指示 Gemini 充当战略家，调查代码库，并创建一个详细的计划来实现给定的目标，而无需编写任何代码。
3.  **Use the command**: You can then use the command in Gemini CLI like this: `/plan How can I make the project more performant?`.
3.  **使用命令**：然后，您可以在 Gemini CLI 中像这样使用该命令：`/plan How can I make the project more performant?`。

### Integration with MCP Prompts
### 与 MCP 提示集成

Gemini CLI also integrates with MCP by supporting MCP Prompts as slash commands. The name and description of the MCP prompt are used as the slash command's name and description, and arguments are supported.
Gemini CLI 还通过支持 MCP 提示作为斜杠命令与 MCP 集成。MCP 提示的名称和描述将用作斜杠命令的名称和描述，并且支持参数。

![MCP Command](resources/custom_slash_commands_mcp.gif)

To get started, you can upgrade your Gemini CLI and refer to the Custom Commands documentation.
要开始使用，您可以升级您的 Gemini CLI 并参阅自定义命令文档。
