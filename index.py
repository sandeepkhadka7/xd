import asyncio
from quart import Quart, request, jsonify
from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError, UserNotMutualContactError
import os

app = Quart(__name__)

API_ID = '26539643'
API_HASH = '8ea9208b3f88c073b13a6a5b6e1f670d'
SESSION_NAME = 'jaishreeram'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@app.route('/search', methods=['GET'])
async def search_user():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    try:
        username = username.lstrip('@')
        await client.start()
        if not await client.is_user_authorized():
            return jsonify({'error': 'Client is not authorized'}), 401

        user = await client.get_entity(username)

        user_info = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone if hasattr(user, 'phone') else None,
            'is_bot': user.bot
        }
        return jsonify(user_info)
    except UsernameNotOccupiedError:
        return jsonify({'error': 'Username not found'}), 404
    except UserNotMutualContactError:
        return jsonify({'error': 'User is not a mutual contact'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        await client.disconnect()

if __name__ == '__main__':
    app.run(debug=True)
