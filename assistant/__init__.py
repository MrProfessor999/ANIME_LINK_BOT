"""
initial assistant's modules
"""
from animeSupport import BOT_LOAD, BOT_NOLOAD, log


def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]

    if BOT_LOAD or BOT_NOLOAD:
        to_load = BOT_LOAD
        if to_load:
            if not all(any(mod == module_name for module_name in all_modules) for mod in to_load):
                log.error("Invalid Module name for bot!")
                quit(1)

        else:
            to_load = all_modules

        if BOT_NOLOAD:
            log.info("Not loaded: {}".format(BOT_NOLOAD))
            return [item for item in to_load if item not in BOT_NOLOAD]

        return to_load

    return all_modules


ALL_SETTINGS = sorted(__list_all_modules())
log.info("bot module loaded: %s", str(ALL_SETTINGS))
__all__ = ALL_SETTINGS + ["ALL_SETTINGS"]
