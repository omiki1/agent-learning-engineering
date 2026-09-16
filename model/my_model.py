from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
# 始终加载项目根目录下的 .env,不依赖当前工作目录
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_PROJECT_ROOT, '.env'))
# GLM_API_KEY
class MyModel:
    _model = None
    _local_model = None
    _router_model = None
    @staticmethod
    def get_model():
        if MyModel._model is None:
            MyModel._model = ChatOpenAI(
                model = os.getenv('MODEL_NAME'),
                api_key=os.getenv('GLM_API_KEY'),
                base_url=os.getenv('BASE_URL'),
                streaming= False,
                # 关闭思考模式：智谱 GLM 4.x 默认可能开启思维链，按需关闭
                extra_body={"thinking": {"type": "disabled"}}
            )
        return MyModel._model

    @staticmethod
    def get_router_model():
        """专用于结构化输出(如路由判断)的非流式模型实例。

        流式模式(streaming=True)下 with_structured_output(function_calling)
        偶发拿不到 tool_call 而返回 None/超时,路由场景必须用非流式。
        """
        if MyModel._router_model is None:
            MyModel._router_model = ChatOpenAI(
                model = os.getenv('MODEL_NAME'),
                api_key=os.getenv('GLM_API_KEY'),
                base_url=os.getenv('BASE_URL'),
                streaming= False,
                # 关闭思考模式：智谱 GLM 4.x 默认可能开启思维链，按需关闭
                extra_body={"thinking": {"type": "disabled"}}
            )
        return MyModel._router_model
if __name__ == '__main__':
    model = MyModel.get_model()
    for chunk in model.stream("天空为什么是蓝色"):
        print(chunk.content, end="", flush=True)


