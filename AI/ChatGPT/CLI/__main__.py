import readline

from AI.ChatGPT.chatgpt import Conversation
from AI.ChatGPT.CLI.custom_rich import CustomCodeBlock
from AI.ChatGPT.errors import ChatgptError
from rich.live import Live
from rich.markdown import Markdown
from rich.console import Console


def _rendering(response, **args):
    console = Console()
    markdown = Markdown("")
    last_response = ""
    theme = "gruvbox-dark"

    try:
        with console.screen():
            with Live(console=console, vertical_overflow="visible", auto_refresh=False, **args) as live:
                for i in response:
                    live._redirect_stdout = False
                    last_response = i
                    markdown = Markdown(
                        i, code_theme=theme, inline_code_theme=theme, inline_code_lexer="Python")
                    markdown.elements["code_block"] = CustomCodeBlock
                    console.clear_live()
                    live.update(markdown)
                    live.refresh()
                live.refresh()
        # console.clear()
    except KeyboardInterrupt:
        response.close()
    console.print(Markdown(last_response, code_theme=theme, inline_code_theme=theme, inline_code_lexer="Python"))

# access_token="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"
# email="charleskromeo@gmail.com", password="Tuxedo8294!"
# chazzcoin@gmail.com Flatrock8294!
def main():
    conversation = Conversation(email="chazzcoin@gmail.com", password="Flatrock8294!")
    try:
        while True:
            try:
                message = input('> ')
                readline.add_history(message)

                if not message:
                    continue

                if message == 'exit':
                    break

                elif message == 'reset':
                    conversation.reset()
                    continue

                elif message == 'clear':
                    print('\033c', end='')
                    continue

                response = conversation.stream(
                    message, only_new_characters=False)

                _rendering(response)
                print('\n')

            except ChatgptError as cgpt:
                print("> ERROR: {}".format(cgpt.message))

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()