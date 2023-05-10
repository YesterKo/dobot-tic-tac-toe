import sheets_com
import minimax
import time

SHEET_ID = '1YZTYIE4sfvTNDYRF8hQObEbRfSvaMIv0aTk6Cgih7gA'
SHEET_NAME = 'Sheet1'

leht = sheets_com.Sheet(SHEET_ID, SHEET_NAME)
old_board_state = leht.get_data_from_sheet()

while True:
    time.sleep(1)
    board_state = leht.get_data_from_sheet()
    if minimax.winner(board_state): break
    if board_state != old_board_state:
        move = minimax(board)
        board_state[move[0]][move[1]] = 'O'
        leht.push_data_to_sheet(board_state)
        old_board_state = board_state

