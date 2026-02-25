# pylint: disable=missing-module-docstring
from mindnlp.transformers import pipeline

# Text Generation Demo
generator = pipeline(model="openai-community/gpt2")
outputs = generator("I can't believe you did such a ", do_sample=False)
print(outputs)

# [{'generated_text': "I can't believe you did such a icky thing to me. I'm so sorry. I'm so sorry. I'm so sorry. I'm so sorry. I'm so sorry. I'm so sorry. I'm so sorry. I"}]

# Chat Demo
chat1 = [
            {"role": "system", "content": "This is a system message."},
            {"role": "user", "content": "This is a test"},
            {"role": "assistant", "content": "This is a reply"},
        ]
chat2 = [
            {"role": "system", "content": "This is a system message."},
            {"role": "user", "content": "This is a second test"},
            {"role": "assistant", "content": "This is a reply"},
        ]
outputs = generator(chat1, do_sample=False, max_new_tokens=10)
print(outputs)

outputs = generator([chat1, chat2], do_sample=False, max_new_tokens=10)
print(outputs)
<<<<<<< HEAD

=======
>>>>>>> d17ae193f9b210255c1cef567810d071c7096b57
def hello():
 print("Hello")  # ✅ 1个空格
 print("World") # ❌ 2个空格（同一层级不一致）

# 违反：驼峰命名（首字母小写）
userName = "John"              # 应该是 user_name
firstName = "John"             # 应该是 first_name
getUserInfo = get_user_info()  # 应该是 get_user_info
totalCount = 100               # 应该是 total_count

# 违反：驼峰命名（首字母大写）- 通常用于类名
UserName = "John"              # 变量名不能用类名风格
FirstName = "John"             # 应该是 first_name
