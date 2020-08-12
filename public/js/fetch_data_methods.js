function buildpregame(db) {

    db.collection("caster_preferences").doc(client_name)
        .get()
        .then(doc => {
            if (doc.exists) {
                if (doc.data()['swap_sides']) {
                    left_side = "away";
                    right_side = "home";
                } else {
                    left_side = "home";
                    right_side = "away"
                }
                // set logos
                setImage("home_logo", doc.data()[left_side + "_logo"]);
                setImage("away_logo", doc.data()[right_side + "_logo"]);

                // set team names
                var home_team_name = doc.data()[left_side + '_team'];
                var away_team_name = doc.data()[right_side + '_team'];
                write("home_team_name", home_team_name, "home_roster");
                write("away_team_name", away_team_name, "away_roster");

                var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_all_players_vrml";
                httpGetAsync(url, function (data) {
                    buildRosterTable(data, home_team_name);
                    buildRosterTable(data, away_team_name);
                });

                // get home team data via firestore...
                db.collection("series").doc("vrml_season_2").collection("teams").doc(doc.data()[left_side + '_team'])
                    .get()
                    .then(function (team) {
                        if (team.exists) {
                            // set division...
                            setImage("home_rank", team.data()['division_logo']);

                            // set home mmr
                            write("home_mmr", "MMR: " + team.data()['mmr'] + " (" + team.data()['wins'] + " - " + team.data()['losses'] + ")");

                            // add home roster...
                            entry = "";
                            Object.keys(team.data()['roster']).forEach(key => {
                                entry += "<tr><th>" + team.data()['roster'][key] + "</th></tr>";
                            });
                            write("home_roster", entry);

                        } else {
                            setImage("home_rank", "");
                            write("home_mmr", " ");
                            write("home_roster", " ");
                        }
                    });
                // get away team data via firestore...
                db.collection("series").doc("vrml_season_2").collection("teams").doc(doc.data()[right_side + '_team'])
                    .get()
                    .then(function (team) {
                        if (team.exists) {
                            // set division...
                            setImage("away_rank", team.data()['division_logo']);

                            // set away mmr
                            write("away_mmr", "MMR: " + team.data()['mmr'] + " (" + team.data()['wins'] + " - " + team.data()['losses'] + ")");

                            // add away roster...
                            entry = "";
                            Object.keys(team.data()['roster']).forEach(key => {
                                entry += "<tr><th>" + team.data()['roster'][key] + "</th></tr>";
                            });
                            write("away_roster", entry);

                        } else {
                            setImage("away_rank", "");
                            write("away_mmr", " ");
                            write("away_roster", " ");
                        }
                    });
            }
        });
}

function buildRosterTable(data, team_name, write_to) {
    table = "";
    data = JSON.parse(data);
    data["TeamPlayers"].forEach(team => {
        if (team.Name == team_name) {
            team.Players.forEach(p => {
               table += "<tr><th>" + p.Name + "</th></tr>";
            })
        }
    })
    write(write_to, table);
}

// adds a row to the end of the table
function addMatchOverview(doc, matchRow, list, matches) {
    var rowNode = matchRow.cloneNode(true);

    rowNode.classList.remove('hide');
    rowNode.getElementsByClassName('match_id')[0].innerText = doc.id;
    rowNode.getElementsByClassName('custom_id')[0].innerText = doc.data()['custom_id'];
    rowNode.getElementsByClassName('match_time')[0].innerText = doc.data()['match_time'];
    rowNode.getElementsByClassName('session_id')[0].innerText = doc.data()['session_id'];
    rowNode.getElementsByClassName('client_name')[0].innerText = doc.data()['client_name'];
    rowNode.getElementsByClassName('version')[0].innerText = doc.data()['version'];
    rowNode.getElementsByClassName('blue_team_score')[0].innerText = doc.data()['blue_team_score'];
    rowNode.getElementsByClassName('orange_team_score')[0].innerText = doc.data()['orange_team_score'];
    rowNode.getElementsByClassName('finish_reason')[0].innerText = doc.data()['finish_reason'];

    var dateStr = doc.data()['match_time'];
    dateStr = dateStr.replace(" ", "T");
    dateStr += "Z";
    rowNode.getElementsByClassName('match_time_elapsed')[0].innerText = timeSince(new Date(dateStr));

    list.appendChild(rowNode);
    matches.push(rowNode);

}


function getCurrentMatchStats(db) {
    db.collection('series').doc(series_name).collection('match_stats')
        .orderBy("match_time", "desc")
        .where("client_name", "==", client_name)
        .where("disabled", "==", false)
        .limit(1)
        .get()
        .then(querySnapshot => {
            if (!querySnapshot.empty) {
                var recent_custom_id = querySnapshot.docs[0].data().custom_id;
                var recent_session_id = querySnapshot.docs[0].data().session_id;
                console.log("Most recent Stats Id:");
                console.log(recent_custom_id);
                db.collection('series').doc(series_name).collection('match_stats')
                    .orderBy("match_time", "desc")
                    .where("custom_id", "==", recent_custom_id)
                    .where("session_id", "==", recent_session_id)
                    .where("disabled", "==", false)
                    .where("client_name", "==", client_name) // Probably not necessary, but possible because of sha256 collisions
                    .get()
                    .then(querySnapshot => {
                        processMatchStatsSnapshot(querySnapshot);
                    });
            }
        });
}

// gets the match stats for each player in the match
function processMatchStatsSnapshot(querySnapshot) {
    if (!querySnapshot.empty) {

        var players = {}

        var playerPromises = [];
        var first = true;

        querySnapshot.docs.forEach(match => {
            if (!('disabled' in match.data()) || match.data()['disabled'] == false) {

                // don't add matches that were *just* added if there is a previous match anyway
                var match_time = Date.parse(match.data()['match_time']) - (new Date()).getTimezoneOffset() * 60000
                if (first && (Date.now() - match_time) < 60000) {
                    // skip
                    console.log("last match was very recent, skipping it in the overlay");
                } else {
                    playerPromises.push(
                        // get all players
                        match.ref.collection('players')
                            .get());
                }

                first = false;
            }
        });

        Promise.all(playerPromises).then(playersQueries => {

            playersQueries.forEach(playersQuery => {
                if (!playersQuery.empty) {
                    playersQuery.docs.forEach(player => {
                        if (player.id != client_name) { // TODO remove true
                            if (players.hasOwnProperty(player.id)) {
                                players[player.id] = mergeSum(players[player.id], player.data());
                            } else {
                                players[player.id] = player.data();
                            }
                        }
                    });
                }
            });

            console.log("Player data:");
            console.log(players);

            setPlayerMatchStats(players);
        });
    }
}

function setPlayerMatchStats(players) {

    // which stats to include in the tables
    var statList = [
        "possession_time",
        "shots_taken",
        "assists",
        "saves",
        "steals",
        "stuns"
    ]

    var teamStats = {
        "blue": {
        },
        "orange": {
        }
    };

    // add the stats as keys to the teamStats object
    Object.keys(teamStats).forEach(color => {
        statList.forEach(key => {
            teamStats[color][key] = 0;
        })
    })

    // the strings for the player stats tables
    var playerTables = {
        "blue": "",
        "orange": ""
    }

    // loop through all players to count up the team stats
    Object.keys(players).forEach(key => {

        const p = players[key];

        // skip players who were never in the match
        if (sumOfStats(p) == 0) {
            console.log("skipping player");
        } else {
            playerTables[p.team_color] +=
                "<tr><td>" + p.player_name +
                "</td><td>" + p.points +
                "</td><td>" + p.assists +
                "</td><td>" + p.saves +
                "</td><td>" + p.steals +
                "</td><td>" + p.stuns +
                "</td><td>" + toMinutesString(p.possession_time) +
                "</td><td>" + p.shots_taken +
                "</td></tr>";
            teamStats[p.team_color].possession_time += p.possession_time;
            teamStats[p.team_color].shots_taken += p.shots_taken;
            teamStats[p.team_color].assists += p.assists;
            teamStats[p.team_color].saves += p.saves;
            teamStats[p.team_color].steals += p.steals;
            teamStats[p.team_color].stuns += p.stuns;
        }
    });

    var totalStats = mergeSum(teamStats.blue, teamStats.orange);

    console.log("Blue team stats:");
    console.log(teamStats.blue);
    console.log("Orange team stats:");
    console.log(teamStats.orange);

    Object.keys(teamStats).forEach(color => {
        Object.keys(teamStats[color]).forEach(stat => {
            var homeaway = "home";
            if (color == "blue") {
                homeaway = "away";
            }
            write(homeaway + "_team_" + stat + "_perc", teamCentage(teamStats[color][stat], totalStats[stat]) + "%");
            if (stat == "possession_time") {
                write(homeaway + "_team_" + stat, toMinutesString(teamStats[color][stat]));

            } else {
                write(homeaway + "_team_" + stat, teamStats[color][stat]);

            }
        });

        write(color + "_player_stats_board", playerTables[color]);
    });
}