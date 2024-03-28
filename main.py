import itertools
import random

def collect_team_codes(num_teams):
    team_codes = []
    for i in range(num_teams):
        while True:
            code = input(f"Enter code for team {i + 1}: ").strip()
            if code and code not in team_codes:
                team_codes.append(code)
                break
            else:
                print("Invalid input or duplicate team code. Please try again.")
    return team_codes

def collect_round_results(paired_teams, teams):
    for match in paired_teams:
        while True:
            result = input(f"Enter the winning team code for the match ({match[0][0]} vs {match[1][0]}): ").strip()
            if result in [match[0][0], match[1][0]]:
                teams[result] += 1
                break
            else:
                print(f"Invalid input. Please enter one of the following codes: {match[0][0]}, {match[1][0]}")

def power_match(teams, rounds, byes_given):
    for current_round in range(1, rounds + 1):
        print(f"\nRound {current_round} pairings:")

        # Handle byes for an odd number of teams
        if len(teams) % 2 == 1:
            sorted_teams_for_bye = sorted(teams.items(), key=lambda x: (x[1], random.random()))
            for team in sorted_teams_for_bye:
                if team[0] not in byes_given:
                    byes_given.add(team[0])
                    print(f"{team[0]} receives a bye.")
                    teams[team[0]] += 1  # Increment win for bye
                    break

        # Sort teams by win count and randomly within the same win count
        sorted_teams = sorted([team for team in teams.items() if team[0] not in byes_given],
                              key=lambda x: (-x[1], random.random()))

        # Group teams by win count
        grouped_teams = {k: list(v) for k, v in itertools.groupby(sorted_teams, key=lambda x: x[1])}

        # Flatten the list of teams for pairing
        pairing_list = []
        for win_group in sorted(grouped_teams.keys(), reverse=True):
            group_teams = grouped_teams[win_group]
            if len(pairing_list) % 2 == 1:
                pairing_list.append(group_teams.pop(0))
            pairing_list.extend(group_teams)

        # Create pairings
        paired_teams = [pairing_list[i:i + 2] for i in range(0, len(pairing_list), 2)]

        # Display pairings
        for match in paired_teams:
            print(f"{match[0][0]} vs {match[1][0]}")

        # Collect results from user
        collect_round_results(paired_teams, teams)

        # Display current standings
        print("\nCurrent standings:")
        for team_code, win_count in sorted(teams.items(), key=lambda x: -x[1]):
            print(f"{team_code}: {win_count} wins")

# Start of the interactive part
print("Welcome to the Debate Pairings System!")
while True:
    try:
        num_teams = int(input("Enter the number of teams: "))
        if num_teams > 0:
            break
        else:
            print("The number of teams must be greater than zero.")
    except ValueError:
        print("Invalid input. Please enter a number.")

team_codes = collect_team_codes(num_teams)
teams = {code: 0 for code in team_codes}
byes_given = set()

while True:
    try:
        num_rounds = int(input("Enter the number of rounds: "))
        if num_rounds > 0:
            break
        else:
            print("The number of rounds must be greater than zero.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Run the power matching for the specified number of rounds
power_match(teams, num_rounds, byes_given)