
from flask import Blueprint, jsonify, make_response
from App.Server import server

info_controllers = Blueprint('info', __name__, url_prefix='')


@info_controllers.route('/', methods=['GET'])
def index():
    return "Food Waste Predictions is running!"


@info_controllers.route('/health', methods=['GET'])
def health():
    is_health: bool = server.is_mongo_client_healthy()
    status = 'pass' if is_health else 'fail'
    return make_response(jsonify({'status': status}), 200)


# def get_game_by_id(id_game: str) -> InteractiveGame:
#     try:
#         game = server.get_game(id_game)
#         return game
#     except Exception:
#         traceback.print_exc()
#         abort(404)
#
#
# @game_controllers.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# @game_controllers.route('/game', methods=['GET'])
# def get_games():
#     finished_status = request.args.get(FINISHED)
#     only_id: str = request.args.get(ONLY_ID)
#     only_id: bool = True if only_id is None else str_to_bool(only_id)
#
#     game_ids = []
#     if finished_status is None:
#         game_ids = server.get_list_all_games(only_id)
#     else:
#         is_finished = str_to_bool(finished_status)
#         game_ids = server.get_games_by_status(is_finished, only_id)
#     return jsonify(game_ids), 200
#
#
# @game_controllers.route('/game/<string:id_game>', methods=['GET'])
# def get_game(id_game: str):
#     game = get_game_by_id(id_game)
#     response = {
#         **to_dict(game),
#         '_winner': game.get_winner(CARDS_TO_USE)
#     }
#     return jsonify(response), 200
#
#
# @game_controllers.route('/game', methods=['POST'])
# def create_game():
#     player = request.json.get(PLAYER_NAME)
#     if player is None:
#         return jsonify({'error': f"No '{PLAYER_NAME}' field was provided"}), 400
#
#     game = InteractiveGame(NUM_RANKS, SUITS, SPECIAL_RANKS, player)
#     id_game = game.get_id()
#     response = {
#         '_id': id_game
#     }
#     server.add_game(game)
#     return jsonify(response), 201
#
#
# @game_controllers.route('/game/<string:id_game>/hand', methods=['GET'])
# def take_player_hand(id_game: str):
#     try:
#         game = get_game_by_id(id_game)
#         update_hand = game.take_hand()
#         if update_hand:
#             server.update_game(game)
#         pretty_hand_p1 = game.get_hand_player(1)
#         pretty_hand_p2 = game.get_hand_player(2)
#         hand_p1 = [{idx: card} for idx, card in enumerate(pretty_hand_p1)]
#         hand_p2 = [{idx: card} for idx, card in enumerate(pretty_hand_p2)]
#         response = {
#             '_id': id_game,
#             '_name_p1': game.get_name_player(1),
#             '_name_p2': game.get_name_player(2),
#             '_len_deck_p1': game.get_deck_len_player(1),
#             '_len_deck_p2': game.get_deck_len_player(2),
#             '_hand_p1': hand_p1,
#             '_hand_p2': hand_p2,
#             '_num_turns': game.get_num_turns(),
#             '_current_target': game.get_target_rank()
#         }
#         return jsonify(response), 200
#     except Exception as e:
#         traceback.print_exc()
#         return make_response(jsonify({'error': str(e)}), 400)
#
#
# @game_controllers.route('/game/<string:id_game>/hand', methods=['PUT'])
# def play_turn(id_game: str):
#     try:
#         game = get_game_by_id(id_game)
#         has_card_indexes: bool = CARD_INDEXES in request.json
#         if not request.json or not has_card_indexes:
#             return jsonify({'error': f"No '{CARD_INDEXES}' field was provided"}), 400
#         if type(request.json[CARD_INDEXES]) is not list:
#             return jsonify({'error': f"'{CARD_INDEXES}' must be a list of indexes"}), 400
#
#         idx_hand_p1: List[int] = request.json[CARD_INDEXES]
#         hand_p1 = game.get_hand_player(1, False)
#         hand_p2 = game.get_hand_player(2, False)
#         turn_winner, idx_hand_p2 = game.play_turn(idx_hand_p1)
#         server.update_game(game)
#
#         target_approx_p1 = sum([card.get_rank() for idx, card in enumerate(hand_p1) if idx in idx_hand_p1])
#         target_approx_p2 = sum([card.get_rank() for idx, card in enumerate(hand_p2) if idx in idx_hand_p2])
#         response = {
#             '_id': id_game,
#             '_name_p1': game.get_name_player(1),
#             '_name_p2': game.get_name_player(2),
#             '_indexes_hand_p1': idx_hand_p1,
#             '_indexes_hand_p2': idx_hand_p2,
#             '_len_deck_p1': game.get_deck_len_player(1),
#             '_len_deck_p2': game.get_deck_len_player(2),
#             '_hand_p1': [{idx: str(card)} for idx, card in enumerate(hand_p1)],
#             '_hand_p2': [{idx: str(card)} for idx, card in enumerate(hand_p2)],
#             '_num_turns': game.get_num_turns(),
#             '_turn_winner': turn_winner,
#             '_winner': game.get_winner(CARDS_TO_USE),
#             '_current_target': game.get_target_rank(),
#             '_current_target_approx_p1': target_approx_p1,
#             '_current_target_approx_p2': target_approx_p2,
#         }
#         return jsonify(response), 200
#     except Exception as e:
#         traceback.print_exc()
#         return make_response(jsonify({'error': str(e)}), 400)
#
#
# @game_controllers.route('/game/<string:id_game>', methods=['DELETE'])
# def delete_game(id_game: str):
#     server.delete_game(id_game)
#     return make_response(jsonify({'success': True}), 200)
