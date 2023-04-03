import logging

import openai

logger = logging.getLogger('logger')


def get_image(update, context):
    prompt = ' '.join(context.args)
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='1024x1024',
        response_format='url'
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=response['data'][0]['url'],
        caption=prompt
    )
