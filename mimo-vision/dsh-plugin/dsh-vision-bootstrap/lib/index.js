/**
 * dsh-vision-bootstrap
 *
 * 在每个新会话的系统提示(system prompt)中注入一条强制指令:
 * 模型(DeepSeek)无法直接查看图片,但具有读图能力 —— 通过 mimo-vision skill
 * 调用小米 MiMo V2.5 视觉模型识别图片。
 *
 * 实现:全局 systemPrompt section(order 50,位于 persona 之后、工具指引之前),
 * 对所有 agent/会话生效。指令保持精简,详细调用方式由 skill 机制按需加载。
 */
import z from "schemastery";

const name = "dsh-vision-bootstrap";
const inject = ["systemPrompt"];

/** 系统提示片段顺序:harness identity=-100, persona=0, 本片段=50, 工具指引=100~199。 */
const VISION_SECTION_ORDER = 50;

const Config = z.object({
	enabled: z.boolean().default(true)
});

const VISION_SECTION_TEXT = [
	"## 读图能力",
	"你(DeepSeek)本身无法直接查看图片,但具有读图能力:本环境内置 `mimo-vision` skill,通过小米 MiMo V2.5 视觉模型识别图片内容。",
	"- 当用户发送图片、对话中出现图片文件/截图/图片 URL,或任务需要查看图片内容时,**必须使用 `mimo-vision` skill** 获取尽可能详细的图片描述,再基于描述继续回答;",
	"- 多张图片默认并行调用;需要对比多图时使用 together 模式;",
	"- 不要声称“看不到图片”或要求用户改用文字描述 —— 直接调用 skill 即可。"
].join("\n");

function apply(ctx, config) {
	const enabled = config.enabled ?? true;
	if (!enabled) return;
	ctx.effect(() => ctx.systemPrompt.section({
		name: "vision-bootstrap:capability",
		order: VISION_SECTION_ORDER,
		text: VISION_SECTION_TEXT
	}), "vision-bootstrap.section()");
}

export { Config, apply, inject, name };
