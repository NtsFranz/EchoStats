# Generates Echopedia pages for all players
import ScrapeESL
import ScrapeVRML


# Find all players that have ever participated in ESL or VRML
# ScrapeESL.scrapeESLCups()
# ScrapeESL.scrapeESLTeams()
# ScrapeESL.scrapeESLMatchPages()
# ScrapeESL.add_matches_as_list()

ScrapeVRML.scrapeVRMLTeams()
ScrapeVRML.scrapeVRMLPlayers()
ScrapeVRML.add_teams_to_players()


# Team join history from ESL history page