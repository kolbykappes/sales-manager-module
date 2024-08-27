"""
File: log.extensions.py (Logging Extensions)

Extensions:
- loggable: A decorator function that can be used to wrap important functions, controller endpoints, and external API calls. 
            It logext
         the entry and exit of the wrapped function, along with the provided arguments and result.
- configure_logger: A function that loads the logger configuration from a file and sets up the logger with the specified sinks and levels.

Examples in main():
The main function demonstrates the usage of the loggable decorator and the configure_logger function. It showcases various logging scenarios, including:
- Logging messages with extra data and context using logger.info and logger.contextualize.
- Logging a dictionary with nested dictionaries and lists.
- Logging the entry and exit of a decorated function, along with the provided arguments and result.
- Logging messages with additional key-value pairs using kwargs.
- Logging messages outside of the contextualized block.
- Logging messages with a custom sink (not implemented in the provided code).
Note: The main function also includes some anti-patterns, such as embedding data in log messages using string formatting. It is recommended 
      to use kwargs for structured logging.
"""

import os
import sys
import functools
import configparser
from loguru import logger


def loggable(func=None, *, entry=True, exit=True, level="DEBUG"):
    def decorator(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    if func is None:
        return decorator
    else:
        return decorator(func)


def configure_logger(file_path="log/logger.ini"):
    config = _load_config(file_path)
    logger.remove()

    default_level = config.get("logger", "default_level", fallback="INFO")
    logger.level(default_level)

    sinks = [s.strip() for s in config.get("logger", "sinks", fallback="").split(",")]

    for sink in sinks:
        section = f"sink:{sink}"
        if config.has_section(section):
            _configure_sink(config, section)
        else:
            print(
                f"Warning: log.extensions.py - Configuration for sink '{sink}' not found. Skipping."
            )

    return logger


#
# Private functions
#
def _load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def _get_sink_config(config, section):
    return {
        "type": config.get(section, "type", fallback="stderr"),
        "level": config.get(section, "level", fallback="INFO"),
        "format": config.get(
            section, "format", fallback="{time} | {level: <8} | {message}"
        ),
    }


def _configure_stderr_sink(config, section, sink_config):
    sink_config["colorize"] = config.getboolean(section, "colorize", fallback=False)
    logger.add(sys.stderr, **sink_config)


def _configure_file_sink(config, section, sink_config):
    filename = config.get(
        section, "filename", fallback="logs/{}.log".format(section.split(":")[1])
    )
    sink_config.update(
        {
            "rotation": config.get(section, "rotation", fallback="1 day"),
            "retention": config.get(section, "retention", fallback="1 week"),
            "compression": config.get(section, "compression", fallback="zip"),
        }
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    logger.add(filename, **sink_config)


def _configure_custom_sink(config, section, sink_config):
    function_name = config.get(section, "function", fallback=None)
    if not function_name:
        print(
            f"Warning: log.extensions.py - No function specified for custom sink '{section}'. Skipping."
        )
        return

    sink_function = globals().get(function_name)
    if not sink_function:
        print(
            f"Warning: log.extensions.py - Custom sink function '{function_name}' not found. Skipping."
        )
        return

    logger.add(sink_function, **sink_config)


def _configure_sink(config, section):
    sink_config = _get_sink_config(config, section)
    sink_type = sink_config["type"]

    sink_handlers = {
        "stderr": _configure_stderr_sink,
        "file": _configure_file_sink,
        "custom": _configure_custom_sink,
    }

    handler = sink_handlers.get(sink_type)
    if handler:
        if sink_config[
            "type"
        ]:  # type got us to the handler, loguru doesn't know 'type' so we remove it
            del sink_config["type"]
        handler(config, section, sink_config)
    else:
        print(
            f"Warning: log.extensions.py - Unknown sink type '{sink_type}' for sink '{section}'. Skipping."
        )


def main():

    # The log.extensions.py script has two tools:
    # 1. loggable decorator
    # 2. configure_logger function

    # Any client seeking to use loguru for logging
    # should use configure_logger to establish the desired
    # configuration, and to ease the task of instrumenting
    # you code.
    configure_logger()

    logger.info("Logger(s) configured", handlers=logger.level)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # This decorator function is used to wrap important functions,
    # controller endpoints, external API calls.  This results in the
    # ability to track processing times and if configured, to see the
    # inbound and outbound parameters and results.
    @loggable(entry=True, exit=True, level="INFO")
    def example_function5(x, y, lester="welcome"):
        logger.info("Inside example function")
        mydict = {
            "keya": "valueA",
            "nested_dict": {"key": "value", "key2": "value2", "key3": "value3"},
            "nestedlist": [{"key4": "value4", "key5": "value5"}],
        }
        # Log a dictionary - note that logger will deserialize this dictionary in the log
        # so any nested dictionaries or lists will be displayed in a readable format.
        # By giving the kwarg a 'this_dict' key, the key will be included in the serialized
        # JSON message.
        logger.info("Dictionary logging", this_dict=mydict, lester=lester)
        return x + y

    # In critical sections of an application it's important to log contextual information
    # that allows for easier debugging and tracking of the application's state.  An
    # application should always log key contextual information on major events.
    # Using contextualize method along with a scoping construct (with block) allows for
    # easy management of the context.  When the scope is exited, the context is cleared.
    with logger.contextualize(user="John Doe", session_id="12345"):
        logger.info("Generic messages under a contextualize block")
        logger.info("Another message with kwarg", rando_var="Some extra information")

    logger.info("This message outside the contextualized block won't have context.")

    # simple kwarg entries should be made in the logger.info call to identify key variables.
    logger.info(
        "Random kwargs, Starting process", task="initialization", status="begin"
    )

    # using contextualize also preserves context as the processing calls deeper functions and methods.
    # notice that the logged output from example_function maintains the context user and session_id.
    with logger.contextualize(user="Jane Doe", session_id="ABCDE"):
        logger.info("Session started")

        # Call the decorated function
        result = example_function5(5, 7)

        # Log the result with more extra data
        logger.info("Process completed", task="calculation", result=result)
    logger.info("Session ended - no context printed on this line.")

    # Call the decorated function
    # This will result in the decorator logging the call.
    result = example_function5(5, 7)
    logger.info("example_function returned", result=result)

    # Variables should be logged via the kwargs parameters and string formatting should be avoided.
    # This is because logext
    # should be easily parsible by log management systems. Using kwargs ensures
    # a structured output.
    ## THIS IS AN ANTI-PATTERN
    logger.info(
        f"ANTI-PATTERN embedding data in a log message.  example_function returned {result}"
    )
    ## End ANTI-PATTERN

    # another method for managing context is to use the bind() method.
    # this method returns a new logger object with the contextual parameters
    # bound to it.  This new logger can be used until the context is no longer needed.
    # This is also a convenient way to create a different logger tagged with a specific
    # identifier like an AUDIT logger.

    logger2 = logger.bind(user="Jim Doe", session_id="XYABCD")
    logger2.info("Message with context", extra_data="Some extra information")
    logger.info("Context is cleared (we switched back to the original logger)")

    # Log after clearing context
    logger.info("Session ended")


if __name__ == "__main__":
    main()

# custom sink example
# If you need a custom sink you:
# 1) Should create a function that will be called by the logger and handle the message
# -----
# def my_custom_sink(message):
#    print(f"Custom sink: {message}")
# -----
# 2) You will also need to add the custom sink to the configure_logger function
# ---------
# [logger]
# sinks = console, file_main, file_error, custom_sink
# ---------
# Custom sinks can be used to send log messages to other systems or to perform other actions.
# 3) Add a configuration of the sink like below
# ---------
# [sink:custom_sink]
# type = custom
# level = INFO
# format = CUSTOM: {time} |{level: <8}| {message}
# function = my_custom_sink
# ----------

##  Here is the typical output from the main routine above:
# 2024-07-22T14:28:16.744574-0400 | INFO     | __main__:main:49 | Generic messages under a contextualize block | {'user': 'John Doe', 'session_id': '12345'}
# 2024-07-22T14:28:16.745355-0400 | INFO     | __main__:main:50 | Another message with kwarg | {'user': 'John Doe', 'session_id': '12345', 'rando_var': 'Some extra information'}
# 2024-07-22T14:28:16.745478-0400 | INFO     | __main__:main:52 | This message outside the contextualized block won't have context. | {}
# 2024-07-22T14:28:16.745555-0400 | INFO     | __main__:main:55 | Random kwargs, Starting process | {'task': 'initialization', 'status': 'begin'}
# 2024-07-22T14:28:16.745632-0400 | INFO     | __main__:main:61 | Session started | {'user': 'John Doe', 'session_id': 'ABCDE'}
# 2024-07-22T14:28:16.748302-0400 | INFO     | log.extensions:loggable:59 | In:example_function via loguru_ext.py:19 args=(5, 7), kwargs={} | {'user': 'John Doe', 'session_id': 'ABCDE'}
# 2024-07-22T14:28:16.748396-0400 | INFO     | __main__:example_function:21 | Inside example function | {'user': 'John Doe', 'session_id': 'ABCDE'}
# 2024-07-22T14:28:16.748467-0400 | INFO     | __main__:example_function:40 | Dictionary logging | {'user': 'John Doe', 'session_id': 'ABCDE', 'this_dict': {'keya': 'valueA', 'nested_dict': {'key': 'value', 'key2': 'value2', 'key3': 'value3'}, 'nestedlist': [{'key4': 'value4', 'key5': 'value5'}]}}
# 2024-07-22T14:28:16.748535-0400 | INFO     | log.extensions:loggable:62 | Out:example_function result=12 | {'user': 'John Doe', 'session_id': 'ABCDE'}
# 2024-07-22T14:28:16.748602-0400 | INFO     | __main__:main:67 | Process completed | {'user': 'John Doe', 'session_id': 'ABCDE', 'task': 'calculation', 'result': 12}
# 2024-07-22T14:28:16.748672-0400 | INFO     | __main__:main:68 | Session ended - no context printed on this line. | {}
# 2024-07-22T14:28:16.749164-0400 | INFO     | log.extensions:loggable:59 | In:example_function via loguru_ext.py:19 args=(5, 7), kwargs={} | {}
# 2024-07-22T14:28:16.749234-0400 | INFO     | __main__:example_function:21 | Inside example function | {}
# 2024-07-22T14:28:16.749298-0400 | INFO     | __main__:example_function:40 | Dictionary logging | {'this_dict': {'keya': 'valueA', 'nested_dict': {'key': 'value', 'key2': 'value2', 'key3': 'value3'}, 'nestedlist': [{'key4': 'value4', 'key5': 'value5'}]}}
# 2024-07-22T14:28:16.749362-0400 | INFO     | log.extensions:loggable:62 | Out:example_function result=12 | {}
# 2024-07-22T14:28:16.749424-0400 | INFO     | __main__:main:73 | example_function returned | {'result': 12}
# 2024-07-22T14:28:16.749488-0400 | INFO     | __main__:main:79 | ANTI-PATTERN example_function returned 12 | {}
# 2024-07-22T14:28:16.749567-0400 | INFO     | __main__:main:89 | Message with context | {'user': 'John Doe', 'session_id': '12345', 'extra_data': 'Some extra information'}
# 2024-07-22T14:28:16.749631-0400 | INFO     | __main__:main:90 | Context is cleared (we switched back to the original logger) | {}
# 2024-07-22T14:28:16.749692-0400 | INFO     | __main__:main:93 | Session ended | {}
