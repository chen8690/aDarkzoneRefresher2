# darkzone-refresh（DSH Skill bundle）

把「暗区突围 · 武装派遣 自动刷新」脚本打包成的 DeepSeek Harness **skill bundle**。
装上之后，目标 profile 里的任何 AI 会话都能在「会话技能目录」中看到 `darkzone-refresh`，
并在任务匹配时用 `skill("darkzone-refresh")` 加载完整操作说明。

## 结构

```
package.json        声明 dsh.bundle.patch → cordis.patch.yml
cordis.patch.yml    插入 @deepseek-ai/dsh-skill-filesystem，指向本包 ./skills
release.json        来源 / 版本元数据
lib/index.js        解析 skill 根目录的辅助函数
skills/
  darkzone-refresh/ 真正的 skill：SKILL.md + 可运行脚本 + references
```

## 安装

把本包放进目标 profile 的 `~/.dsh/profiles/<profile>/node_modules/<scope>/<pkg>/`
（或 `npm publish` 后用 `dsh plugin add` 安装），重启 DSH 即可。
用法与脚本说明见 `skills/darkzone-refresh/README.md` 与 `skills/darkzone-refresh/SKILL.md`。

## License

MIT
