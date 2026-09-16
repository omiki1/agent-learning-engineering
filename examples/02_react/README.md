# 02 Mini ReAct

该例子用确定性 `PlanModel` 演示三轮轨迹：先搜索课程文件，再统计结果，最后回答。它不模拟隐藏推理，只产生可观察 Action。

```powershell
python examples/02_react/main.py
python examples/02_react/main.py --repeat --max-steps 3
```

第二个命令故意让模型重复调用，展示重复轨迹检测。

