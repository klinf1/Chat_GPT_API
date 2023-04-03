INFO_MESSAGE = ('Welcome to my telegram bot, that '
                'connects to OpenAI API and can be '
                'used like ChatGPT service, provided on their website!\n'
                'Current functions include:\n'
                '-Message history storage: this bot provides up to '
                '2000 tokens of previous message history to the OpenAI, '
                'that help keep your chat cohesive.\n'
                '-Temperature setting. ChatGPT uses temperature '
                'to see how deterministic an answer should be. '
                'It varies from 0 to 1. If temperature is 0, '
                'ChatGPT always uses the most probable answer, '
                'and if it is 1, the answer is always chosen at random. '
                'Default value is 0,5. In order to change it, '
                'use /settemperature your_value.\n'
                '-System message setting. It helps set up'
                'the character of your bot. Default setting is'
                ' <You are a helpful assistant>. To change it, use '
                '/setsystem your_message.\n'
                'This bot can also generate images! In order to do so, use /image your_prompt.')
