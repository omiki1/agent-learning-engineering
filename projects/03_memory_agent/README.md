# Project 03｜Memory Agent

SQLite 版长期偏好记忆，支持 set/get/list/delete，并按 `user_id` 隔离。数据库默认写在系统临时目录，避免污染课程目录。

```powershell
python projects/03_memory_agent/main.py --demo
python projects/03_memory_agent/main.py set alice language zh-CN
python projects/03_memory_agent/main.py list alice
python projects/03_memory_agent/main.py delete alice language
```

扩展：加入 `expires_at`、冲突来源、用户导出；再实现向量召回并比较，不要把结构化偏好全部改成向量。

