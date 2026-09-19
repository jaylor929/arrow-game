# 箭途

软件工程课程第二次个人作业：“一箭又一箭”风格小游戏。

## 游戏简介

“箭途”是一个点击式箭头解谜小游戏。玩家需要观察棋盘中箭头的方向和相互阻挡关系，按照合适的顺序点击箭头，使所有箭头依次飞出棋盘。

游戏规则：

- 箭头前方没有其他箭头阻挡时，箭头飞出棋盘并消失；
- 前方有阻挡时，箭头不能飞出，并给出碰撞反馈；
- 点击被阻挡的箭头会消耗一次失误机会；
- 清除本关全部箭头后进入下一关；
- 失误次数耗尽时本关失败，可以重新开始。

## 开发环境

- 操作系统：Windows 11
- 编程语言：Python 3.14.7
- 图形库：Pygame-ce 2.5.8
- 开发工具：VS Code
- AIGC 工具：DeepSeek、豆包

## 安装和运行方法

安装 Python 3.10 以上版本。

安装 Pygame-ce：

```bash
pip install pygame-ce -i https://pypi.tuna.tsinghua.edu.cn/simple
```

进入项目目录：

```bash
cd arrow-game
```

运行游戏：

```bash
python main.py
```

## 游戏操作说明

- 鼠标左键点击箭头：尝试让该箭头飞出棋盘；
- 点击“重新开始”：将当前关卡恢复到初始状态；
- 点击“返回主界面”：回到开始界面；
- 点击“下一关”：进入下一关；
- 点击“退出”：退出游戏。

## 项目结构

```text
arrow-game/
├── main.py
├── assets/
│   └── menu_bg.jpg
└── README.md
```

## 游戏截图

<img width="2004" height="1264" alt="image" src="https://github.com/user-attachments/assets/bcdc8fb0-7b70-4182-b557-7f9bebae7242" />
开始界面
<img width="2004" height="1264" alt="image" src="https://github.com/user-attachments/assets/9fdd2820-6283-40fa-8518-17f8186a9413" />
游戏界面
<img width="2004" height="1264" alt="image" src="https://github.com/user-attachments/assets/52e6b58a-f3a5-4d4f-8ff8-bfc9db210e65" />
通关界面
<img width="2004" height="1264" alt="image" src="https://github.com/user-attachments/assets/0dea09a3-1e6a-4908-9d03-555fb09b66b8" />
失败界面

## 关卡说明

游戏共 3 关，均为 7×7 棋盘，每关都可正常通关。

## 素材来源

- 开始界面背景图：来自 Pexels，作者 <Min An>，链接：https://www.pexels.com/zh-cn/photo/1403550/
- 音效：由代码生成，无外部素材；
- 字体：使用系统自带的新宋体。

## 说明

本项目为软件工程课程个人作业，使用 AIGC 工具辅助开发，代码经过本人理解、修改和测试。
