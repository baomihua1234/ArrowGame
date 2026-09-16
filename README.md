# 一箭又一箭

2026 秋季软件工程个人作业项目。

本项目使用 Python 和 pygame-ce 实现“一箭又一箭”小游戏，并使用 pytest 对核心游戏逻辑进行自动化测试。

---

## 一、游戏简介

游戏棋盘中存在多个不同方向的箭头。

玩家点击一个箭头后：

- 如果箭头朝向到棋盘边缘之间不存在其他箭头，则该箭头可以飞出棋盘并被消除；
- 如果箭头前方存在其他箭头，则本次操作失败，并减少一次失误机会；
- 每关拥有 3 次失误机会；
- 清空棋盘中的全部箭头即可通过当前关卡；
- 失误机会耗尽则游戏失败。

当前游戏包含 3 个关卡。

---

## 二、开发环境

- Python 3.13
- pygame-ce 2.5.8
- pytest 9.1.1
- Visual Studio 2022
- Git
- GitHub

---

## 三、项目结构

```text
ArrowGame/
│
├── ArrowGame.py
│   └── 游戏主程序、界面绘制、鼠标交互和关卡控制
│
├── game_logic.py
│   └── 游戏核心逻辑
│       ├── can_exit()
│       ├── is_level_clear()
│       ├── count_arrows()
│       └── is_solvable()
│
├── test_game_logic.py
│   └── pytest 自动化测试
│
├── requirements.txt
│   └── Python 项目依赖
│
├── .gitignore
│   └── Git 忽略规则
│
└── README.md
```

## 四、安装方法

如果是第一次下载本项目，请按照以下步骤配置环境。

### 1. 克隆项目

```bash
git clone https://github.com/baomihua1234/ArrowGame.git
```

### 2. 进入项目目录

```bash
cd ArrowGame
```

### 3. 创建 Python 虚拟环境

```bash
python -m venv .venv
```

### 4. 激活虚拟环境

Windows：

```bash
.venv\Scripts\activate
```

### 5. 安装项目依赖

```bash
python -m pip install -r requirements.txt
```

---

## 五、运行游戏

在虚拟环境已经激活的情况下运行：

```bash
python ArrowGame.py
```

启动游戏后，点击“开始游戏”即可进入第一关。

---

## 六、自动化测试

运行以下命令：

```bash
python -m pytest -v
```

当前项目包含 8 个自动化测试，主要测试：

- 前方无遮挡的箭头能够飞出；
- 前方存在其他箭头时无法飞出；
- 位于棋盘边缘的箭头判断；
- 空格不能作为箭头；
- 关卡清空判断；
- 未清空关卡判断；
- 剩余箭头数量统计；
- 关卡可解性判断。

当前测试结果：

```text
8 passed
```

---

## 七、核心算法

游戏使用二维列表保存棋盘数据。

箭头方向表示为：

```text
U = ↑
D = ↓
L = ←
R = →
. = 空格
```

核心函数 `can_exit()` 会根据箭头方向，从箭头前面的第一个格子开始一直扫描到棋盘边缘。

如果途中发现其他箭头，则说明路径被阻挡，返回 `False`。

如果一直扫描到棋盘边缘都没有遇到其他箭头，则返回 `True`。

方向变化关系：

```python
DIRECTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}
```

---

## 八、AIGC 使用说明

本项目在开发过程中使用 AIGC 辅助完成了以下工作：

- 游戏需求分析；
- 项目结构设计；
- pygame 使用方法学习；
- 箭头路径判断算法设计；
- 边界条件分析；
- pytest 测试用例设计；
- Git 与 GitHub 使用学习；
- 程序报错分析与修复。

开发过程中通过实际运行、单元测试和人工检查对 AIGC 生成的内容进行了验证和修改。

后续会在课程作业博客中详细记录 AIGC 的使用过程、Prompt、修改过程以及开发心得。

---

## 九、作者

GitHub：baomihua1234