import random

judges = ["Alex", "Daniel", "Kshitij", "Neel", "Felix", "Surya"]

def get_team_codes(num_teams):
    teams = []
    for i in range(num_teams):
        code = input(f"Enter team {i + 1} code: ")
        teams.append({
            'code': code,
            'wins': 0,
            'losses': 0,
            'past_opponents': [],
            'bye': False  # Track if the team has had a bye
        })
    return teams

def record_match_results(pairings):
    for (team1, team2), judge in pairings:
        result = input(f"Enter result for match {team1['code']} vs {team2['code']} judged by {judge} (W for {team1['code']}, L for {team2['code']}): ").upper()
        if result == 'W':
            team1['wins'] += 1
            team2['losses'] += 1
        elif result == 'L':
            team1['losses'] += 1
            team2['wins'] += 1

def pair_teams(teams):
    # Sort teams based on wins, losses and whether they have had a bye
    sorted_teams = sorted(teams, key=lambda x: (-x['wins'], x['losses'], x['bye'], random.random()))
    
    if len(sorted_teams) % 2 != 0:
        # Give a bye to the lowest-ranked team that hasn't had one yet (if possible)
        for team in reversed(sorted_teams):
            if not team['bye']:
                team['bye'] = True
                team['wins'] += 1  # Increment wins for the bye
                print(f"Team {team['code']} gets a bye.")
                sorted_teams.remove(team)
                break
        else:
            print("All teams have had a bye, no bye will be given this round.")

    pairings = []
    judge_index = 0
    while sorted_teams:
        team1 = sorted_teams.pop(0)
        for team2 in sorted_teams:
            if team2['code'] not in team1['past_opponents']:
                pairings.append(((team1, team2), judges[judge_index % len(judges)]))
                judge_index += 1
                team1['past_opponents'].append(team2['code'])
                team2['past_opponents'].append(team1['code'])
                sorted_teams.remove(team2)
                break

    return pairings

def print_pairings(pairings):
    print("This round's pairings:")
    for (team1, team2), judge in pairings:
        print(f"Match: {team1['code']} vs {team2['code']} judged by {judge}")

def print_round_results(teams):
    print("\nRound results:")
    for team in teams:
        print(f"Team {team['code']} - Wins: {team['wins']}, Losses: {team['losses']}")

def main():
    num_teams = int(input("Enter the number of teams competing: "))
    teams = get_team_codes(num_teams)
    num_rounds = int(input("\nEnter the number of rounds in the tournament: "))

    for round_number in range(1, num_rounds + 1):
        print(f"\n--- Round {round_number} ---\n")
        pairings = pair_teams(teams)
        
        if not pairings and len(teams) % 2 != 0:
            print("Not enough teams to continue the tournament without byes.")
            break

        print_pairings(pairings)  # Print the pairings for the round
        record_match_results(pairings)
        print_round_results(teams)

if __name__ == "__main__":
    main()
