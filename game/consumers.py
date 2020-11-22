import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Player, Game
from .serializers import PlayerSerializer

logger = logging.getLogger(__file__)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        
        self.game_room = self.scope['url_route']['kwargs']['game_room']

        # Join room group
        await self.channel_layer.group_add(
            self.game_room,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.game_room,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data, **kwargs):
        
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']
        data = text_data_json['data']

        print(f'Consumer input data: {data} TYPE: {message_type}')

        if message_type == 'add.player':
            new_player = await self.add_player(data)

            print(f'NEW PLAYER: {new_player.pk}')
            logger.info(f'NEW PLAYER: {new_player.pk}')

            player_data = PlayerSerializer(new_player).data
            game_room = f'game_{player_data["player_game_id"]}'
            await self.channel_layer.group_send(
                game_room,
                {
                    'type': 'game.message',
                    'message': player_data
                }
            )
        elif message_type == 'start.game':
            print(f"STARRTING GAME.....ID: {data['game_id']} ")

    # Sending JSON messages 
    # async def echo_message(self, event):
    #     logger.info(f'>>> ECHO 1: {event}')
    #     await self.send_json(event)

    # Receive message from room group
    async def game_message(self, event):
        print(f'SENT MESSAGE: {event}')
        message = event['data']['data']
        title = event['data']['title']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'title': title
        }))


    async def add_player(self, event):
        print(f'CONSUMER ADD: {event}')
        new_player = await self._add_player(event)
        player_data = PlayerSerializer(new_player).data

        print(f'CONSUMER PLAYER: {player_data}')

        # Send the room "new player" info
        await self.channel_layer.group_send(
            player_data['player_game_id'],
            {
                'type': 'game.message',
                'message': player_data
            }
        )

        return new_player

    @database_sync_to_async
    def _add_player(self, event):
        print(f'EVENT: {event}')
        game = Game.objects.get(game_id=event.get('game_id'))
        new_player = Player.objects.create(
            game=game,
            player_game_id=game.game_id,
            nickname=event.get('nickname')
        )
        return new_player
        