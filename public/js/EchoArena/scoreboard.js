function Start(db) {
    buildpregame(
        db, 
        previousMatches = false, 
        teamStats = true, 
        roster = false, 
        live = false, 
        get_team_ranking = true,
        game = 'echoarena');
    getCurrentMatchStats(db, true, false);
}
