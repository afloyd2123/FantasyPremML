# Define constants for the game rules

# Budget for the team (in millions)
BUDGET = 100

# Maximum number of players in a team
MAX_PLAYERS = 15

# Positional restrictions (e.g., 2 goalkeepers, 5 defenders, etc.)
POSITIONAL_RULES = {
    "GK": 2,
    "DEF": 5,
    "MID": 5,
    "FWD": 3
}

# Maximum players from a single team
MAX_PLAYERS_FROM_ONE_TEAM = 3

def valid_team_structure(player_positions):
    """
    Check if a given team structure adheres to the positional rules.
    Args:
    - player_positions (list): A list of player positions (e.g., ['GK', 'DEF', 'MID', ...])
    
    Returns:
    - bool: True if the team structure is valid, False otherwise.
    """
    position_counts = {position: player_positions.count(position) for position in POSITIONAL_RULES}
    for position, count in position_counts.items():
        if count > POSITIONAL_RULES[position]:
            return False
    return True

def within_budget(player_costs):
    """
    Check if the total cost of players is within the budget.
    Args:
    - player_costs (list): A list of player costs.
    
    Returns:
    - bool: True if the total cost is within budget, False otherwise.
    """
    return sum(player_costs) <= BUDGET

def valid_team_from_one_club(player_club_counts):
    """
    Check if the number of players from a single club exceeds the limit.
    Args:
    - player_club_counts (dict): A dictionary with club names as keys and counts as values.
    
    Returns:
    - bool: True if the team adheres to the club player limit, False otherwise.
    """
    return all(count <= MAX_PLAYERS_FROM_ONE_TEAM for count in player_club_counts.values())

# ... [Previous code for team structure rules]

# =============== Gameplay Rules ===============

# Number of free transfers per week
FREE_TRANSFERS = 1

# Maximum number of accumulated free transfers
MAX_FREE_TRANSFERS = 2

# Points penalty for each transfer beyond the free ones
TRANSFER_PENALTY = 4

def compute_transfer_penalty(transfers_made, accumulated_transfers):
    """
    Compute the penalty for making more transfers than the accumulated free transfers.
    Args:
    - transfers_made (int): Number of transfers made in the current gameweek.
    - accumulated_transfers (int): Number of free transfers accumulated till now.
    
    Returns:
    - int: Penalty points for the extra transfers.
    """
    # Calculate total available transfers
    total_transfers = min(accumulated_transfers + FREE_TRANSFERS, MAX_FREE_TRANSFERS)
    
    # If transfers made exceed the available free transfers, compute penalty
    extra_transfers = max(0, transfers_made - total_transfers)
    
    return extra_transfers * TRANSFER_PENALTY

# ... [Previous code for team structure and basic gameplay rules]

# =============== Captaincy Rules ===============

CAPTAIN_MULTIPLIER = 2
VICE_CAPTAIN_MULTIPLIER = 2  # This will apply only if the captain doesn't play

# =============== Bonus Chips Rules ===============

# Each chip can be used once per season. We'll represent this as a dictionary, where the keys are the chip names
# and the values are booleans indicating whether the chip has been used.
CHIPS_USAGE = {
    "Wildcard": False,
    "Free Hit": False,
    "Triple Captain": False,
    "Bench Boost": False
}

def use_chip(chip_name):
    """
    Mark a chip as used for the season.
    Args:
    - chip_name (str): Name of the chip to be used.
    
    Returns:
    - bool: True if the chip is used successfully, False if the chip was already used or is invalid.
    """
    if chip_name in CHIPS_USAGE and not CHIPS_USAGE[chip_name]:
        CHIPS_USAGE[chip_name] = True
        return True
    return False

# ... [Previous code for team structure, basic gameplay rules, captaincy, and bonus chips]

# =============== Point Scoring Rules ===============

POINT_RULES = {
    "play_up_to_60": 1,
    "play_60_or_more": 2,
    "goal_by_gk_or_def": 6,
    "goal_by_mid": 5,
    "goal_by_fwd": 4,
    "assist": 3,
    "clean_sheet_by_gk_or_def": 4,
    "clean_sheet_by_mid": 1,
    "penalty_save": 5,
    "penalty_missed": -2,
    "2_goals_conceded_by_gk_or_def": -1,
    "yellow_card": -1,
    "red_card": -3,
    "own_goal": -2,
    "3_saves_by_gk": 1
    # Bonus points will be variable and can be computed based on the provided data
}

# You can add functions or logic here to compute points for a player based on their performance stats and the rules above.
