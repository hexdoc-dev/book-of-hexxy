from dataclasses import dataclass

from hexdoc.patchouli import BookContext
from hexdoc.plugin import PluginManager
from hexdoc.utils import ContextSource
from yarl import URL

MODID_BLACKLIST = {
    "hexdoc",
    "minecraft",
    "hexxybook",
}


@dataclass(kw_only=True)
class SourceBook:
    modid: str
    book_url: URL


def get_source_books(context: ContextSource):
    pm = PluginManager.of(context)
    book_ctx = BookContext.of(context)

    source_books = list[SourceBook]()

    for modid in sorted(pm.mod_plugins.keys()):
        if modid in MODID_BLACKLIST:
            continue

        metadata = book_ctx.all_metadata.get(modid)
        if metadata is None or metadata.book_url is None:
            continue

        source_book = SourceBook(
            modid=modid,
            book_url=metadata.book_url,
        )

        if modid == "hexcasting":
            source_books.insert(0, source_book)
        else:
            source_books.append(source_book)

    return source_books
