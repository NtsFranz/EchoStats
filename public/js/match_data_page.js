document.addEventListener('DOMContentLoaded', function () {
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    // // The Firebase SDK is initialized and available here!
    //
    // firebase.auth().onAuthStateChanged(user => { });
    // firebase.database().ref('/path/to/ref').on('value', snapshot => { });
    // firebase.messaging().requestPermission().then(() => { });
    // firebase.storage().ref('/path/to/ref').getDownloadURL().then(() => { });
    //
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥



    firebase.firestore().enablePersistence()
        .catch(function (err) {
            if (err.code == 'failed-precondition') {
                // Multiple tabs open, persistence can only be enabled
                // in one tab at a a time.
                // ...
            } else if (err.code == 'unimplemented') {
                // The current browser does not support all of the
                // features required to enable persistence
                // ...
            }
        });
    // Subsequent queries will use persistence, if it was enabled successfully

    var db = firebase.firestore()

    if (series_name == "") {
        series_name = "vrml_season_1";
    }

    if (client_name != "" && custom_id == "") {
        db.collection('series').doc(series_name).collection('match_stats')
            .orderBy("match_time", "desc")
            .where("client_name", "==", client_name)
            .limit(1)
            .get()
            .then(querySnapshot => {
                if (!querySnapshot.empty) {
                    recent_custom_id = querySnapshot.docs[0].data().custom_id;
                    console.log(recent_custom_id);
                    db.collection('series').doc(series_name).collection('match_stats')
                        .orderBy("match_time", "desc")
                        .where("custom_id", "==", recent_custom_id)
                        .where("client_name", "==", client_name)    // Probably not necessary, but possible because of sha256 collisions
                        .get()
                        .then(querySnapshot => {
                            if (!querySnapshot.empty) {

                                players = {}
            
                                var playerPromises = [];
            
                                querySnapshot.docs.forEach(match => {
                                    playerPromises.push(
                                        // get all players
                                        match.ref.collection('players')
                                        .get());
                                });
            
                                Promise.all(playerPromises).then(playersQueries => {
            
                                    playersQueries.forEach(playersQuery => {
                                        if (!playersQuery.empty) {
                                            playersQuery.docs.forEach(player => {
                                                if (players.hasOwnProperty(player.id)) {
                                                    players[player.id] = mergeSum(players[player.id], player.data());
                                                } else {
                                                    players[player.id] = player.data();
                                                }
                                            });
                                        }
                                    });
                                    console.log(players);
            
                                    processData(players);
                                });
            
                            }
                        });
                }
            });

    } else if (custom_id != "") {
        db.collection('series').doc(series_name).collection('match_stats')
            .orderBy("match_time", "desc")
            .where("custom_id", "==", custom_id)
            .get()
            .then(querySnapshot => {
                if (!querySnapshot.empty) {

                    players = {}

                    var playerPromises = [];

                    querySnapshot.docs.forEach(match => {
                        playerPromises.push(
                            // get all players
                            match.ref.collection('players')
                            .get());
                    });

                    Promise.all(playerPromises).then(playersQueries => {

                        playersQueries.forEach(playersQuery => {
                            if (!playersQuery.empty) {
                                playersQuery.docs.forEach(player => {
                                    if (players.hasOwnProperty(player.id)) {
                                        players[player.id] = mergeSum(players[player.id], player.data());
                                    } else {
                                        players[player.id] = player.data();
                                    }
                                });
                            }
                        });



                        console.log(players);

                        processData(players);
                    });

                }
            });
    } else {
        write("orangestats", "Please specify either a client_name or custom_id");
    }


});

function processData(players) {

    bluePlayersTable = "";
    orangePlayersTable = "";
    teamStatsHeaders = {
        "possession_time": "POSSESSION",
        "shots_taken": "SHOTS TAKEN",
        "assists": "ASSISTS",
        "saves": "SAVES",
        "steals": "STEALS",
        "stuns": "STUNS"
    };
    teamStats = {
        "blue": {
            "possession_time": 0,
            "shots_taken": 0,
            "assists": 0,
            "saves": 0,
            "steals": 0,
            "stuns": 0
        },
        "orange": {
            "possession_time": 0,
            "shots_taken": 0,
            "assists": 0,
            "saves": 0,
            "steals": 0,
            "stuns": 0
        }
    };
    // loop through all players
    Object.keys(players).forEach(key => {
        const p = players[key];
        // console.log(p);
        table = "";
        table +=
            "<tr><td>" + p.player_name +
            "</td><td>" + p.points +
            "</td><td>" + p.assists +
            "</td><td>" + p.saves +
            "</td><td>" + p.steals +
            "</td><td>" + p.stuns +
            "</td></tr>";
        if (p.team_color == "blue") {
            bluePlayersTable += table;
            teamStats.blue.possession_time += p.possession_time;
            teamStats.blue.shots_taken += p.shots_taken;
            teamStats.blue.assists += p.assists;
            teamStats.blue.saves += p.saves;
            teamStats.blue.steals += p.steals;
            teamStats.blue.stuns += p.stuns;
        } else if (p.team_color == "orange") {
            orangePlayersTable += table;
            teamStats.orange.possession_time += p.possession_time;
            teamStats.orange.shots_taken += p.shots_taken;
            teamStats.orange.assists += p.assists;
            teamStats.orange.saves += p.saves;
            teamStats.orange.steals += p.steals;
            teamStats.orange.stuns += p.stuns;
        }
    });
    var totalStats = mergeSum(teamStats.blue, teamStats.orange);
    console.log(teamStats.blue);
    console.log(teamStats.orange);
    var teamStatsText = "";
    Object.keys(teamStatsHeaders).forEach(function (key) {
        teamStatsText += "<tr><td>" + teamStatsHeaders[key] + "</td><td>" +
            teamCentage(teamStats.blue[key], totalStats[key]) + "%</td></tr>";
    });
    write("bluestats", teamStatsText);
    teamStatsText = "";
    Object.keys(teamStatsHeaders).forEach(function (key) {
        teamStatsText += "<tr><td>" + teamCentage(teamStats.orange[key], totalStats[key]) + "%</td><td>" +
            teamStatsHeaders[key] + "</td></tr>";
    });
    write("orangestats", teamStatsText);
    write("blueplayerhead", "<tr><td>PLAYER</td><td>POINTS</td><td>ASSISTS</td><td>SAVES</td><td>STEALS</td><td>STUNS</td></tr>");
    write("blueplayerstable", bluePlayersTable);
    write("orangeplayerhead", "<tr><td>PLAYER</td><td>POINTS</td><td>ASSISTS</td><td>SAVES</td><td>STEALS</td><td>STUNS</td></tr>");
    write("orangeplayerstable", orangePlayersTable);
}

function write(id, data) {
    var element = document.getElementById(id);
    element.innerHTML = data;
    element.style.visibility = 'visible';
}

function teamCentage(team, total) {
    a = Math.round(team / total * 100)
    if (a > 0) {
        return a;
    } else {
        return '0';
    }
}

// adds numeric values from ob2 to ob1
function mergeSum(ob1, ob2) {
    sum = {}
    Object.keys(ob1).forEach(key => {
        if (ob2.hasOwnProperty(key) && (typeof ob2[key]) == "number") {
            sum[key] = ob1[key] + ob2[key]
        }
    })
    return sum;
}