from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class SHUKLA(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="SHUKLAMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Validate LOGGER_ID before using it
        if not config.LOGGER_ID:
            LOGGER(__name__).error("LOGGER_ID is not set in configuration.")
            return

        try:
            # Ensure LOGGER_ID is treated as integer
            logger_id = int(config.LOGGER_ID)
            
            await self.send_message(
                chat_id=logger_id,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (ValueError, TypeError):
            LOGGER(__name__).error(
                f"Invalid LOGGER_ID format. Expected integer, got: {config.LOGGER_ID}"
            )
            return
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel and the LOGGER_ID is correct."
            )
            return
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__} - {str(ex)}."
            )
            return

        try:
            logger_id = int(config.LOGGER_ID)
            a = await self.get_chat_member(logger_id, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as an admin in your log group/channel."
                )
                return
        except (ValueError, TypeError):
            LOGGER(__name__).error(
                f"Invalid LOGGER_ID format for admin check: {config.LOGGER_ID}"
            )
            return
        except Exception as e:
            LOGGER(__name__).error(
                f"Failed to check admin status: {type(e).__name__} - {str(e)}"
            )
            return

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
