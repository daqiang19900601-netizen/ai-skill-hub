# 🚀 AI Skill Hub

**跨AI工具的本地技能管理系统** - 一套Prompt，随处使用！

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)

---

## ✨ 特性

- 🎯 **跨平台兼容** - 一套Prompt/Skill同时支持 Claude Code、Cursor、Trae、VS Code Agent、GitHub Copilot 等
- 📦 **本地优先** - 所有数据存储在本地，零隐私风险
- 🔄 **版本控制** - 内置Git集成，像管理代码一样管理你的AI提示词
- 📊 **智能分析** - Token计数、复杂度评估、优化建议
- 🔍 **全文搜索** - 快速查找你的Skills
- 🌐 **社区分享** - 一键分享到GitHub Gist，从URL安装他人Skills
- 🚀 **CLI驱动** - 命令行操作，开发者友好

---

## 📦 安装

### 方式一：从源码安装

```bash
git clone https://github.com/YOUR_USERNAME/ai-skill-hub.git
cd ai-skill-hub
pip install -r requirements.txt
pip install -e .
```

### 方式二：使用pip（发布后）

```bash
pip install ai-skill-hub
```

---

## 🚀 快速开始

### 1. 创建你的第一个Skill

```bash
skill init -n "python-code-review" -d "Python代码审查助手" -t "python,code-review,ai" -a "Your Name"
```

### 2. 查看所有Skills

```bash
skill list
```

### 3. 导出给特定AI工具使用

```bash
skill export python-code-review --tool claude
skill export python-code-review --tool cursor
```

### 4. 分析Skill的Token使用情况

```bash
skill analyze python-code-review
```

### 5. 搜索Skills

```bash
skill search -q "python"
```

---

## 📖 完整命令参考

### 核心命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `skill init` | 创建新Skill | `skill init -n my-skill -d "描述" -t "tag1,tag2"` |
| `skill show` | 查看Skill详情 | `skill show my-skill` |
| `skill list` | 列出所有Skills | `skill list --tag python` |
| `skill export` | 导出Skill | `skill export my-skill --tool claude` |
| `skill analyze` | 分析Skill | `skill analyze my-skill` |
| `skill search` | 搜索Skills | `skill search -q "关键词"` |
| `skill update` | 更新Skill | `skill update my-skill -d "新描述"` |
| `skill delete` | 删除Skill | `skill delete my-skill` |

### 分享命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `skill share` | 分享到GitHub Gist | `skill share my-skill` |
| `skill install` | 从Gist安装 | `skill install https://gist.github.com/xxx` |

### 其他命令

| 命令 | 说明 |
|------|------|
| `skill status` | 查看存储状态和统计 |
| `skill config` | 查看/设置配置 |

---

## 🔧 支持的AI工具

| 工具 | 导出参数 | 格式 |
|------|----------|------|
| 通用 | `--tool generic` | Markdown |
| Claude Code | `--tool claude` | XML标签格式 |
| Cursor | `--tool cursor` | 注释格式 |
| Trae | `--tool trae` | Markdown |
| VS Code Agent | `--tool vscode` | 代码注释格式 |
| GitHub Copilot | `--tool github-copilot` | 注释格式 |

---

## 📁 项目结构

```
ai-skill-hub/
├── ai_skill_hub/
│   ├── __init__.py          # 包初始化
│   ├── main.py              # CLI入口和命令定义
│   ├── storage.py           # 本地存储管理
│   ├── exporter.py          # 多格式导出器
│   ├── analyzer.py          # 分析和优化
│   ├── git_integration.py   # Git版本控制
│   └── sharing.py           # 社区分享功能
├── requirements.txt         # Python依赖
├── setup.py                 # 安装配置
├── pyproject.toml           # 项目元数据
├── .gitignore               # Git忽略规则
└── LICENSE                  # MIT许可证
```

---

## 💡 使用场景

### 场景一：多工具用户

你在不同项目使用不同的AI工具？一套Skill，到处导出！

```bash
# 创建一次
skill init -n "react-component" -d "React组件生成器"

# 到处使用
skill export react-component --tool claude
skill export react-component --tool cursor
skill export react-component --tool trae
```

### 场景二：团队协作

分享最佳实践给团队：

```bash
# 分享到Gist
skill share my-best-practice

# 团队成员安装
skill install https://gist.github.com/user/abc123
```

### 场景三：版本控制

```bash
# 自动Git提交每次修改
skill update my-skill -d "更新描述"
# 自动创建commit: "Update skill: my-skill"

# 查看历史
skill history
```

### 场景四：Token优化

```bash
skill analyze my-skill
# 输出: Token数、复杂度、优化建议
```

---

## 🔐 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `GITHUB_TOKEN` | GitHub Personal Access Token（用于Gist分享） | 仅分享时需要 |

获取GitHub Token：
1. 访问 https://github.com/settings/tokens
2. 生成新Token，勾选 `gist` 权限
3. 设置环境变量：`export GITHUB_TOKEN=your_token_here`

---

## 🎯 示例Skills

### 代码审查Skill

```yaml
name: code-reviewer
description: 专业代码审查助手
tags: [code-review, best-practices, security]
content: |
  你是一位资深代码审查专家。请审查以下代码：
  
  1. 代码质量和可读性
  2. 潜在的安全漏洞
  3. 性能优化建议
  4. 最佳实践符合度
  
  代码：
  {code}
variables:
  code: "待审查的代码"
```

### 文档生成Skill

```yaml
name: doc-generator
description: 自动生成技术文档
tags: [documentation, api, technical]
content: |
  请为以下代码生成完整的技术文档，包括：
  - 功能概述
  - API参考
  - 使用示例
  - 注意事项
variables:
  code: "需要文档的代码"
  language: "编程语言"
```

---

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🌟 Star History

如果你觉得这个项目有用，请给我们一个 ⭐ Star！

---

## 📮 反馈

- 有问题？创建 [Issue](https://github.com/YOUR_USERNAME/ai-skill-hub/issues)
- 有想法？创建 [Discussion](https://github.com/YOUR_USERNAME/ai-skill-hub/discussions)

---

**Happy Skill Managing! 🚀**
