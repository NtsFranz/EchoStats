var matchRow;
var list;
var db;
var matches = [];

function Start(db) {

    currentCaster = document.getElementById('current-caster-name');
    if (client_name != "") {
        currentCaster.innerText = "Caster Desk for: " + client_name;
    } else {
        currentCaster.innerHTML = "<span style='font-weight:900; color: #900;'>User not set.</span>";
    }

    buildpregame(
        db, 
        previousMatches = true, 
        teamStats = true, 
        roster = true, 
        live = true, 
        get_team_ranking = false, 
        game = 'echoarena'
    );

    getCurrentMatchStats(
        db, 
        long = true, 
        live = true, 
        onlyaftercasterprefs = false);

    autocompleteCasters(document.getElementById("player_search"), db, game = 'echoarena');
}
