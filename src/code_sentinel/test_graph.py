from code_sentinel.agents.workflow import app
from IPython.display import display, Image

print(">>> generate graph")
print(app.get_graph().draw_mermaid())

print(">>> start to run workflow")
bad_code = """
+ public User login(String name, String pass) {
+     String sql = "SELECT * FROM user WHERE name='" + name + "'";
+     System.out.println("Debug: " + sql);
+     return db.query(sql);
+ }
"""

inputs= {
    "diff_content": bad_code,
    "language": "java",
    "security_comments": [],
    "performance_comments": [],
    "style_comments": []
}

for output in app.stream(inputs):
    for key, value in output.items():
        print(f"node completed! {key}")
        print(f">>>> the current state: {value}")

print("\n>>> all finished")