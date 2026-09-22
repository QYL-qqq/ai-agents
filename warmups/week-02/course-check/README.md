# W2｜Course Check

这是一个不影响未来课程项目的课堂工作台。三节课始终使用这一项目，依次观察：

1. 命令在哪个目录执行；
2. 程序使用哪个项目环境；
3. 一项修改怎样出现在 Git diff 中，并被保存为本地 commit。

完整步骤以课程网站的 W2 Guide 为准。

## 恢复并运行项目

在本目录中执行：

```bash
uv sync --locked
COURSE_MODE=fixture uv run --locked python course_check.py
COURSE_MODE=fixture uv run --locked pytest -q
```

初始输出中的签名是：

```text
signature: teacher
```

程序报告当前事实，测试只检查已经写下的规则；测试通过不等于全部课堂任务已经完成。

## 留下公开签名

第三课时在 VS Code 中把 [`signature.toml`](signature.toml) 的教师默认值改为教师分配的公开课程代号：

```toml
[student]
signature = "s07"
```

不要写姓名、完整学号、密码、token 或其他个人信息。

随后从仓库根核对：

```bash
git status --short
git diff -- warmups/week-02/course-check/signature.toml
```

确认 diff 只有签名变化后，只暂存这一文件并形成一条本地提交：

```bash
git add warmups/week-02/course-check/signature.toml
git commit -m "w2: set public signature"
```

本周不执行 `git push`。commit 只保存本地历史，不会自动改变 GitHub 上的 remote。

本工作台不构成 W3 或后续项目的代码基础；W3 会从新的正式仓库独立开始。
