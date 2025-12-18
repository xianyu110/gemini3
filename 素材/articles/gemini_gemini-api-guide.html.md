# Gemini API开发指南：免费申请API Key与Python/Node.js接入教程 ​

---

Gemini API开发指南：免费申请API Key与Python/Node.js接入教程
​
Google Gemini 提供了强大的 API 接口，允许开发者将其多模态能力集成到自己的应用程序中。目前，Google AI Studio 为开发者提供了慷慨的免费额度。本文将带你从零开始接入 Gemini API。
💡 开发者福利
如果你需要更稳定、无需翻墙的 API 服务，或者需要集成多个模型（如 GPT-4, Claude），可以考虑使用聚合 API 服务。 👉
推荐平台
：
Xsimple (https://maynorai.top/list/#/home)
- 提供兼容 OpenAI 格式的 API 接口，一站式接入主流模型。
第一步：获取 API Key
​
访问 Google AI Studio
打开网址：
https://aistudio.google.com/
（需使用美国等支持地区的 IP 访问）。
登录 Google 账号
使用你的 Google 账号登录。
创建 API Key
点击左侧菜单的 "Get API key"。
点击 "Create API key" 按钮。
选择 "Create API key in new project"（在新项目中创建）。
复制生成的 API Key 并妥善保存。
第二步：环境配置
​
Gemini 提供了官方的 Python 和 Node.js SDK，也可以通过 REST API 调用。
Python 环境
​
bash
pip
install
-q
-U
google-generativeai
Node.js 环境
​
bash
npm
install
@google/generative-ai
第三步：代码示例
​
Python 接入示例
​
python
import
google.generativeai
as
genai
import
os
# 配置 API Key
genai.configure(
api_key
=
"YOUR_API_KEY"
)
# 选择模型
model
=
genai.GenerativeModel(
'gemini-2.5-pro'
)
# 发送文本消息
response
=
model.generate_content(
"请用一句话介绍你自己"
)
print
(response.text)
# 多模态输入（文本 + 图片）
# img = PIL.Image.open('image.jpg')
# response = model.generate_content(["这张图片里有什么？", img])
# print(response.text)
Node.js 接入示例
​
javascript
const
{
GoogleGenerativeAI
}
=
require
(
"@google/generative-ai"
);
// 初始化
const
genai
=
new
GoogleGenerativeAI
(
"YOUR_API_KEY"
);
const
model
=
genai.
getGenerativeModel
({ model:
"gemini-2.5-pro"
});
async
function
run
() {
// 发送文本
const
prompt
=
"请用一句话介绍你自己"
;
const
result
=
await
model.
generateContent
(prompt);
const
response
=
await
result.response;
const
text
=
response.
text
();
console.
log
(text);
}
run
();
价格与限制
​
目前 Google AI Studio 提供两种计费模式：
特性
免费版 (Free of Charge)
付费版 (Pay-as-you-go)
RPM (每分钟请求数)
15
360+
TPM (每分钟 Token 数)
32,000
2,000,000+
每日请求限制
1,500
无限制
数据隐私
数据可能用于改进模型
数据不会被用于训练
注意
：免费版虽然免费，但数据可能会被 Google 用于模型训练，
请勿在免费版 API 中发送敏感个人数据或商业机密
。
替代方案：聚合 API
​
对于国内开发者，直接使用 Google 官方 API 可能会遇到网络连接问题（Connection Timeout）。此时，使用国内的中转 API 或聚合 API 是更好的选择。
推荐使用
Xsimple API
，它具有以下优势：
✅
国内直连
：无需配置代理，速度快。
✅
OpenAI 兼容
：可以使用标准的 OpenAI SDK 调用 Gemini 模型，无需修改代码逻辑。
✅
多模型支持
：一个 Key 即可调用 Gemini、GPT-4、Claude 等所有模型。
python
# 使用 OpenAI SDK 调用 Xsimple 的 Gemini 模型
from
openai
import
OpenAI
client
=
OpenAI(
api_key
=
"YOUR_XSIMPLE_KEY"
,
base_url
=
"https://maynorai.top/list/#/home
# 示例地址，请以官网为准
)
response
=
client.chat.completions.create(
model
=
"gemini-2.5-pro"
,
messages
=
[
{
"role"
:
"user"
,
"content"
:
"你好，Gemini！"
}
]
)
print
(response.choices[
0
].message.content)
总结
​
个人学习/测试
：直接申请 Google 官方免费 API Key。
生产环境/国内部署
：建议使用
Xsimple
等聚合 API 服务，以获得更好的稳定性和访问速度。

