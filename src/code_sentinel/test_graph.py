from code_sentinel.agents.workflow import app
from IPython.display import display, Image

print(">>> generate graph")
print(app.get_graph().draw_mermaid())

print(">>> start to run workflow")
bad_style_code = """
public class testManager { 
    public void run() {
        String x = "这是一个非常非常非常非常长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长的字符串";
        System.out.println("Debug info"); 
    }
}
"""

inputs = {
    "diff_content": bad_style_code,
    "language": "Java",
    "repo_context": "", # 暂时为空
    "security_comments": [],
    "performance_comments": [],
    "style_comments": []
}

for output in app.stream(inputs):
    for key, value in output.items():
        print(f"node completed! {key}")
        print(f">>>> the current state: {value}")

print("\n>>> all finished")