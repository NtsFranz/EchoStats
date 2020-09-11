function Start(db) {
    buildpregame(db, false, true, false, live=false, get_team_ranking=true);
    getCurrentMatchStats(db, true, false);
}
