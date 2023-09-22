import asyncio
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        "default": TTLCache(maxsize=10_000, ttl=5),
        "year": TTLCache(maxsize=10_000, ttl=5)
    }

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                return await event.answer('Time between requests 5 seconds')
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)


# data {'dispatcher': <Dispatcher '0x107a72990'>,
#                                 'bots': (<aiogram.client.bot.Bot object at 0x107a728d0>,),
# 'bot': <aiogram.client.bot.Bot object at 0x107a728d0>,
# 'event_from_user': User(
#     id=5914670749,
#     is_bot=False,
#     first_name='Stanislav',
#     last_name=None,
#     username='Stanislav_Zhuchenko',
#     language_code='ru',
#     is_premium=None,
#     added_to_attachment_menu=None,
#     can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None),
# 'event_chat': Chat(id=5914670749,
#                    type='private',
#                    title=None,
#                    username='Stanislav_Zhuchenko', first_name='Stanislav',
#                    last_name=None, is_forum=None, photo=None, active_usernames=None,
#                    emoji_status_custom_emoji_id=None, bio=None, has_private_forwards=None,
#                    has_restricted_voice_and_video_messages=None, join_to_send_messages=None,
#                    join_by_request=None, description=None, invite_link=None, pinned_message=None,
#                    permissions=None, slow_mode_delay=None, message_auto_delete_time=None,
#                    has_aggressive_anti_spam_enabled=None, has_hidden_members=None,
#                    has_protected_content=None, sticker_set_name=None, can_set_sticker_set=None,
#                    linked_chat_id=None, location=None),
# 'fsm_storage': <aiogram.fsm.storage.memory.MemoryStorage object at 0x107a96590>,
# 'state': <aiogram.fsm.context.FSMContext object at 0x107bf0990>,
# 'raw_state': None,
# 'handler': HandlerObject(callback=<function archive_results at 0x107a487c0>,
#                     awaitable=True, spec=FullArgSpec(
#     args=['message'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None,
#     annotations={'message': <class 'aiogram.types.message.Message'>}),
# filters=[FilterObject(callback=<bound method MagicFilter.resolve of <aiogram.utils.magic_filter.MagicFilter object at 0x107a4d950>>,
# awaitable=False, spec=FullArgSpec(args=['self', 'value'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None,
#                                   annotations={'return': typing.Any, 'self': ~MagicT, 'value': typing.Any}),
# magic=<aiogram.utils.magic_filter.MagicFilter object at 0x107a4d950>)],
# flags={'throttling_key': 'year'}),
# 'event_update': Update(update_id=83405534,
#                        message=Message(message_id=1714, date=datetime.datetime(2023, 9, 22, 13, 6, 33, tzinfo=TzInfo(UTC)),
#                                        chat=Chat(id=5914670749, type='private', title=None, username='Stanislav_Zhuchenko', first_name='Stanislav', last_name=None, is_forum=None, photo=None, active_usernames=None, emoji_status_custom_emoji_id=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None, description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None, message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None, has_protected_content=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None, location=None), message_thread_id=None, from_user=User(id=5914670749, is_bot=False, first_name='Stanislav', last_name=None, username='Stanislav_Zhuchenko', language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None), sender_chat=None, forward_from=None, forward_from_chat=None, forward_from_message_id=None, forward_signature=None, forward_sender_name=None, forward_date=None, is_topic_message=None, is_automatic_forward=None, reply_to_message=None, via_bot=None, edit_date=None, has_protected_content=None, media_group_id=None, author_signature=None, text='2023', entities=None, animation=None, audio=None, document=None, photo=None, sticker=None, video=None, video_note=None, voice=None, caption=None, caption_entities=None, has_media_spoiler=None, contact=None, dice=None, game=None, poll=None, venue=None, location=None, new_chat_members=None, left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None, message_auto_delete_timer_changed=None, migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None, invoice=None, successful_payment=None, user_shared=None, chat_shared=None, connected_website=None, write_access_allowed=None, passport_data=None, proximity_alert_triggered=None, forum_topic_created=None, forum_topic_edited=None, forum_topic_closed=None, forum_topic_reopened=None, general_forum_topic_hidden=None, general_forum_topic_unhidden=None, video_chat_scheduled=None, video_chat_started=None, video_chat_ended=None, video_chat_participants_invited=None, web_app_data=None, reply_markup=None), edited_message=None, channel_post=None, edited_channel_post=None, inline_query=None, chosen_inline_result=None, callback_query=None, shipping_query=None, pre_checkout_query=None, poll=None, poll_answer=None, my_chat_member=None, chat_member=None, chat_join_request=None), 'event_router': <Router '0x107a45290'>}

from aiogram import types, BaseMiddleware
import time


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, max_messages=5, cooldown_seconds=10):
        self.max_messages = max_messages
        self.cooldown_seconds = cooldown_seconds
        self.user_last_messages = {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.chat.id
        current_time = time.time()

        # Initialize the user's message history if not present
        if user_id not in self.user_last_messages:
            self.user_last_messages[user_id] = []

        # Remove older messages from the user's history
        self.user_last_messages[user_id] = [msg for msg in self.user_last_messages[user_id]
                                             if current_time - msg <= self.cooldown_seconds]

        # Record the timestamp of the current message
        self.user_last_messages[user_id].append(current_time)

        # Check if the user has sent too many messages in a short time
        if len(self.user_last_messages[user_id]) >= self.max_messages:
            await event.reply("You are sending messages too quickly. Please wait.")
            return False
        else:
            return await handler(event, data)

