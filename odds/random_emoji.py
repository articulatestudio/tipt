heart_emoji = u"\U0001F49A"
circle_emoji = u"\U0001F535"
fourleaf_emoji = u"\U0001F340"
negative_emoji = u"\U0001F171"
brightness_emoji = u"\U0001F506"
money_emoji = u"\U0001F4B0"
bank_emoji = u"\U0001F4B7"
cloud_emoji = u"\U0001F326"
pool_emoji = u"\U0001F3B1"
down_up_emoji = u"\U00002B06" + u"\U00002B07"
victory_emoji = u"\U0000270C"
negative_square_emoji = u"\U0000274E"
squade_emoji = u"\U00002660"
horse_race_emoji = u"\U0001F3C7"
keycap_emoji = u"\U0001F51F"
joker_emoji = u"\U0001F0CF"
white_emoji = u"\U00002705"
exclamation_emoji = u"\U00002757"
round_emoji = u"\U0001F4CD"
lg_circle_emoji = u"\U0001F534"
tangerine_emoji = u"\U0001F34A"
balloon_emoji = u"\U0001F388"
orange_emoji = u"\U0001F4D9"
moneywing_emoji = u"\U0001F4B8"
wave_emoji = u"\U0001F30A"
horse_emoji = u"\U0001F434"
diamond_emoji = u"\u2666"
yellow_heart_emoji = u"\U0001F49B"
Emoji_List = {'Bet 365': heart_emoji + yellow_heart_emoji, 'William Hill': circle_emoji, 'Paddy Power':fourleaf_emoji,
              'Betway': negative_emoji, 'BetBright': brightness_emoji, 'Betfred': money_emoji,
              'Boylesports': bank_emoji, 'Sky Bet': cloud_emoji,'888sport': pool_emoji,
              'Betfair': down_up_emoji, 'BetVictor': victory_emoji,'Comeon': negative_emoji,
              'NetBet': squade_emoji, 'RaceBets': horse_race_emoji, '10Bet': keycap_emoji, '21Bet': joker_emoji,
              'Stan James': white_emoji, 'Titan Bet': exclamation_emoji, 'Unibet': heart_emoji,
              'Winner': round_emoji, '32Red': lg_circle_emoji, '188bet': tangerine_emoji,
              'Matchbook': balloon_emoji, 'BetfairExchange': orange_emoji, 'Tote Pools': moneywing_emoji, 'Coral ': wave_emoji}


def random_emoji(vendor):
    """
    Get the random emoji.
    """
    try:
        return Emoji_List[vendor]
    except Exception as e:
        print ('random_emoji: {}'.format(e))
        return diamond_emoji
