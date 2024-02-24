from bot.bot_factory import create_bot
from bridge.context import Context
from bridge.reply import Reply
from common import const
from common.log import logger
from common.singleton import singleton
from config import conf
from translate.factory import create_translator
from voice.factory import create_voice

"""
这段代码定义了一个名为 `Bridge` 的类，它作为不同类型的机器人服务（如聊天、语音转文本、文本转语音和翻译）的中间件或桥梁。该类使用了单例模式（通过 `@singleton` 装饰器），确保整个应用中只有一个 `Bridge` 实例。以下是代码主要功能的概要：

1. **配置服务类型**：在初始化时，`Bridge` 类根据配置（从 `conf()` 获取的设置）决定每种服务（chat, voice_to_text, text_to_voice, translate）将使用的提供者。例如，聊天服务可以配置为使用 ChatGPT、OpenAI、Azure ChatGPT、百度等。

2. **动态服务创建**：`get_bot` 方法根据请求的服务类型（例如 "chat" 或 "text_to_voice"）动态创建并返回相应的服务实例。如果所请求的服务实例尚未创建，它会根据配置的服务类型创建一个新实例，并将其存储在内部字典中以供后续使用。这避免了重复创建相同类型的服务实例。

3. **服务请求处理**：类提供了几个方法（`fetch_reply_content`, `fetch_voice_to_text`, `fetch_text_to_voice`, `fetch_translate`），通过这些方法可以处理不同类型的请求。例如，`fetch_reply_content` 方法用于获取聊天服务的回复，而 `fetch_voice_to_text` 方法则用于将语音文件转换为文本。

4. **支持多种机器人和翻译服务**：代码支持与多个机器人提供商和翻译服务提供商的集成，包括但不限于 OpenAI、Google、百度、科大讯飞、QWEN、Gemini、LinkAI 和 ClaudeAI。服务类型和提供商可以通过配置灵活指定。

5. **灵活的配置和重置功能**：通过读取 `config` 配置文件，`Bridge` 类可以灵活配置使用哪种服务提供商。此外，提供了 `reset_bot` 方法来重置服务实例，该方法通过重新调用 `__init__` 方法来实现。

总之，这段代码实现了一个灵活、可配置的服务桥接功能，允许应用根据配置动态选择和使用不同的机器人和翻译服务提供商，从而处理聊天、语音转文本、文本转语音和翻译等多种请求。
"""




@singleton
class Bridge(object):
    def __init__(self):
        self.btype = {
            "chat": const.CHATGPT,
            "voice_to_text": conf().get("voice_to_text", "openai"),
            "text_to_voice": conf().get("text_to_voice", "google"),
            "translate": conf().get("translate", "baidu"),
        }
        model_type = conf().get("model") or const.GPT35
        if model_type in ["text-davinci-003"]:
            self.btype["chat"] = const.OPEN_AI
        if conf().get("use_azure_chatgpt", False):
            self.btype["chat"] = const.CHATGPTONAZURE
        if model_type in ["wenxin", "wenxin-4"]:
            self.btype["chat"] = const.BAIDU
        if model_type in ["xunfei"]:
            self.btype["chat"] = const.XUNFEI
        if model_type in [const.QWEN]:
            self.btype["chat"] = const.QWEN
        if model_type in [const.GEMINI]:
            self.btype["chat"] = const.GEMINI

        if conf().get("use_linkai") and conf().get("linkai_api_key"):
            self.btype["chat"] = const.LINKAI
            if not conf().get("voice_to_text") or conf().get("voice_to_text") in ["openai"]:
                self.btype["voice_to_text"] = const.LINKAI
            if not conf().get("text_to_voice") or conf().get("text_to_voice") in ["openai", const.TTS_1, const.TTS_1_HD]:
                self.btype["text_to_voice"] = const.LINKAI

        if model_type in ["claude"]:
            self.btype["chat"] = const.CLAUDEAI
        self.bots = {}
        self.chat_bots = {}

    def get_bot(self, typename):
        if self.bots.get(typename) is None:
            logger.info("create bot {} for {}".format(self.btype[typename], typename))
            if typename == "text_to_voice":
                self.bots[typename] = create_voice(self.btype[typename])
            elif typename == "voice_to_text":
                self.bots[typename] = create_voice(self.btype[typename])
            elif typename == "chat":
                self.bots[typename] = create_bot(self.btype[typename])
            elif typename == "translate":
                self.bots[typename] = create_translator(self.btype[typename])
        return self.bots[typename]

    def get_bot_type(self, typename):
        return self.btype[typename]

    def fetch_reply_content(self, query, context: Context) -> Reply:
        return self.get_bot("chat").reply(query, context)

    def fetch_voice_to_text(self, voiceFile) -> Reply:
        return self.get_bot("voice_to_text").voiceToText(voiceFile)

    def fetch_text_to_voice(self, text) -> Reply:
        return self.get_bot("text_to_voice").textToVoice(text)

    def fetch_translate(self, text, from_lang="", to_lang="en") -> Reply:
        return self.get_bot("translate").translate(text, from_lang, to_lang)

    def find_chat_bot(self, bot_type: str):
        if self.chat_bots.get(bot_type) is None:
            self.chat_bots[bot_type] = create_bot(bot_type)
        return self.chat_bots.get(bot_type)

    def reset_bot(self):
        """
        重置bot路由
        """
        self.__init__()
