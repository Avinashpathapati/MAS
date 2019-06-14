import numpy as np
from optparse import OptionParser


def feedback_from_1_or_2(cur_player_guess,code,colorList):

	code_loc_list = {}
	for col in colorList:
		code_loc_list[col] = []

	feedback_pos = {}
	for game_pos in range(0,game_size):
		feedback_pos[game_pos] = ''

	for i in range(0,len(cur_player_guess)):
		if cur_player_guess[i] == code[i]:
			feedback_pos[i] = 'b'
			code_loc_list[cur_player_guess[i]].append(i)


	for i in range(0,len(cur_player_guess)):
		if feedback_pos[i] == '':
			fdback_loc_val = ''
			for j in range(0,len(code)):
				if cur_player_guess[i] == code[j] and not j in code_loc_list[code[j]]:
					fdback_loc_val = 'w'
					code_loc_list[code[j]].append(j)
					break

			if not fdback_loc_val == '':
				feedback_pos[i] = fdback_loc_val

	feedback = ''
	for i in range(0,len(cur_player_guess)):
		feedback = feedback + feedback_pos[i]

	return feedback


def get_feedbacks(cur_player_guess,code_1,code_2,color_list):

	feedback_one = feedback_from_1_or_2(cur_player_guess,code_1,color_list)
	feedback_two = feedback_from_1_or_2(cur_player_guess,code_2,color_list)
	return feedback_one,feedback_two

def find_total_match(str1, str2):
	ct = 0
	for i in range(0,str1):
		if str1[i] == str2[i]:
			ct = ct+1
	return ct

def make_guess(cur_player,valid_states,code_comb_list,cur_code,colorList):

	code_pref_list = [-1]*10
	#print(valid_states)
	for i in range(0,len(code_comb_list)):
		guess_code = code_comb_list[i]
		one_match_code = ''
		two_match_code = ''
		three_match_code = ''
		if valid_states[guess_code] == 1 :
			feedback_cur = feedback_from_1_or_2(guess_code,cur_code,colorList)
			# print('----------')
			# print(feedback_cur)
			# print(guess_code)
			# print(cur_code)
			# print('--------')
			if feedback_cur == 'w':
				code_pref_list[0] = i
				break;
			elif feedback_cur == 'b':
				code_pref_list[1] = i
			elif feedback_cur == 'ww':
				code_pref_list[2] = i
			elif feedback_cur == 'wb' or feedback_cur == 'bw':
				code_pref_list[3] = i
			elif feedback_cur == 'bb':
				code_pref_list[4] = i
			elif feedback_cur == 'www':
				code_pref_list[5] = i
			elif feedback_cur == 'wbw' or feedback_cur == 'wwb' or feedback_cur == 'bww':
				code_pref_list[6] = i
			elif feedback_cur == 'bbb':
				code_pref_list[7] = i
			elif feedback_cur == '':
				code_pref_list[8] = i



	best_guess_code = -1
	for val in code_pref_list:
		if not val == -1:
			best_guess_code = code_comb_list[val]
			break;
	return best_guess_code



def filter_inval_states_aft_mov(feedback,guess_code,valid_states,colorList,org_code):
	for code in valid_states:
		if valid_states[code] == 1:

			fdback_for_code = feedback_from_1_or_2(code,guess_code,colorList)
			fdback_for_code2 = feedback_from_1_or_2(org_code,guess_code,colorList)
			# print('-----------')
			# print(fdback_for_code)
			# print(fdback_for_code2)
			# print(org_code)
			# print(guess_code)
			# print(code)
			# print('-------------')

			# print('----------')
			# print(guess_code)
			# print(code)
			# print(org_code)
			# print(fdback_for_code)
			# print(fdback_for_code2)
			# print('---------')
			if feedback == fdback_for_code:
				valid_states[code] = 1
			else:
				valid_states[code] = 0

	return valid_states


def play_game(gsize,colorList):

	valid_states_1 = {}
	valid_states_2 = {}
	code_comb_list = []
	code_1_in = np.random.randint(65,size=1)
	code_2_in = np.random.randint(65,size=1)
	ct = 0
	code_1 = ''
	code_2 = ''
	for i in range(0,len(colorList)):
		code_comb_1 = colorList[i]
		for j in range(0,len(colorList)):
			code_comb_2 = code_comb_1 + colorList[j]
			for k in range(0,len(colorList)):
				code_comb_3 = code_comb_2 + colorList[k]
				ct = ct+1
				if ct == code_1_in:
					code_1 = code_comb_3
				if ct == code_2_in:
					code_2 = code_comb_3
				code_comb_list.append(code_comb_3)
				valid_states_1[code_comb_3] = 1
				valid_states_2[code_comb_3] = 1


	t_num_moves = 30
	cur_move = 0
	#code_1 = "bbr"
	#code_2 = "gbb"
	# print('*********')
	# print(code_1)
	# print(code_2)
	# print('*********')
	while(cur_move < t_num_moves):
		# print('--------------')
		# print(valid_states_1)
		# print(valid_states_2)
		# print('------------')
		if cur_move %2 == 0:
			guess_code = make_guess(1,valid_states_1,code_comb_list,code_1,colorList)
			print('cur guess ',str(1),' ',guess_code,' ',code_2)

		else:
			guess_code = make_guess(2,valid_states_2,code_comb_list,code_2,colorList)
			print('cur guess ',str(2),' ',guess_code,' ',code_1)

		feedback_one,feedback_two = get_feedbacks(guess_code,code_1,code_2,colorList)
		if (cur_move %2 == 0) and feedback_two == 'bbb':
			print('player one wins')
			break;
		if not (cur_move %2 == 0) and feedback_one == 'bbb':
			print('player 2 wins')
			break;
		if cur_move %2 == 0:
			valid_states_1 = filter_inval_states_aft_mov(feedback_two,guess_code,valid_states_1,colorList,code_2)
		else:
			valid_states_2 = filter_inval_states_aft_mov(feedback_one,guess_code,valid_states_2,colorList,code_1)
		cur_move  += 1



if __name__ == "__main__":
	#commandline arguments reading
	color_list = ['r','g','b','y']
	game_size = 3
	play_game(3,color_list)
	#feedback_from_1_or_2("gyr","ygb",color_list)



