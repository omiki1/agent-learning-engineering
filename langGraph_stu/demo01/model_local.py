"""demo01 专用模型工厂。

与 model/my_model.py 的唯一区别：显式设置 timeout / max_retries。
目的：请求卡住时 60 秒就抛明确异常，而不是静默假死最长 10 分钟
（OpenAI SDK 默认请求超时 600 秒 + 2 次重试）。

之所以单独放一份、不去改 model/my_model.py：那个文件被 agent/、demo/ 等
多个目录共用，改动会波及所有 demo。这里只影响 langGraph_stu/demo01。
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# demo01/model_local.py -> demo01 -> langGraph_stu -> stu_agent(项目根，.env 所在)
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))


class LocalModel:
    _model = None

    @staticmethod
    def get_model():
        if LocalModel._model is None:
            LocalModel._model = ChatOpenAI(
                model=os.getenv("MODEL_NAME"),
                api_key=os.getenv("GLM_API_KEY"),
                base_url=os.getenv("BASE_URL"),
                streaming=False,
                # 单次请求 60 秒超时，最多重试 2 次：卡住会明确报错，不会无限等
                timeout=60,
                max_retries=2,
                # 关闭思考模式：智谱 GLM 4.x 默认可能开启思维链
                extra_body={"thinking": {"type": "disabled"}},
            )
        return LocalModel._model


if __name__ == "__main__":
    model = LocalModel.get_model()
    print("模型:", model.model_name, "base_url:", model.openai_api_base)
    print("请求超时:", model.request_timeout, "最大重试:", model.max_retries)
    print("回复:", model.invoke("只回复两个字：收到").content)
