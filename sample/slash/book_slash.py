from sample.SlashCog import Slash_Cog
from discord.app_commands import command
from discord import Interaction
from discord.ext import commands
from sample.bin.rpg.book import editBook,readBook
# from sample.Slash_permission import is_book_editor

class Book_Slash(Slash_Cog,name = "指令包_書籍",help = False):
    @command(
        name = "book",
        description = '編輯書本，僅限編輯家使用'
    )
    # @is_book_editor()
    async def _edit_book(self,i:Interaction,id:str):
        return await editBook(id,i)
    
    @command(
        name = "read",
        description = '閱讀書本'
    )
    async def _read_book(self,i:Interaction,id:str):
        return await readBook(id,i)


async def setup(bot:commands.Bot):
    await bot.add_cog(Book_Slash(bot))
