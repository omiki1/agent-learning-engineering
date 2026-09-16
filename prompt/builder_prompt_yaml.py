import os
import yaml

class BuilderPromptYaml:
    _prompt = None
    @classmethod
    def get_prompt(cls,filename):
        dir = os.path.dirname(os.path.abspath(__file__))

        with open(f"{dir}\\{filename}", 'r',encoding='utf-8') as f:
            config = yaml.safe_load(f)
        _prompt = f"""
一 角色:{config['role']}
二 任务:{"\n".join(config['task'])}
三 规则:{"\n".join(config['rule'])}\n
四 输出:{"\n".join(config['output'])}\n
五 示例:{"\n".join(config['example'])}\n
                 """
        return _prompt

if __name__ =="__main__":
   # dd =['理解用户需求', '根据用户输入问题，发送邮件']
   # print("\n".join(dd))
   p = BuilderPromptYaml.get_prompt("send_email_agent.yaml")
   print(p)