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


    try {
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
    } catch (e) {
        console.log("Persistence already running");
    }

    firebase.auth().signInAnonymously().catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
        console.log("failed auth");
    });

    var db = firebase.firestore()

    // var series_name = ""; // TODO set this from a dropdown or something
    // var client_name = ""; // TODO set this from a dropdown or something
    // var custom_id = ""; // TODO set this from a dropdown or something

    if (series_name == "") {
        series_name = "vrml_season_2";
    }

    if (live.toLowerCase() == 'true') {
        if (client_name != "" && custom_id == "") {
            db.collection('series').doc(series_name).collection('match_stats')
                .orderBy("match_time", "desc")
                .where("client_name", "==", client_name)
                .where("disabled", "==", false)
                .limit(1)
                .onSnapshot(querySnapshot => {
                    if (!querySnapshot.empty) {
                        var recent_custom_id = querySnapshot.docs[0].data().custom_id;
                        var recent_session_id = querySnapshot.docs[0].data().session_id;
                        console.log("Most recent Stats Id: " + recent_custom_id);
                        console.log("Most recent Session Id: " + recent_custom_id);
                        db.collection('series').doc(series_name).collection('match_stats')
                            .orderBy("match_time", "desc")
                            .where("custom_id", "==", recent_custom_id)
                            .where("session_id", "==", recent_session_id)
                            .where("disabled", "==", false)
                            .where("client_name", "==", client_name) // Probably not necessary, but possible because of sha256 collisions
                            .onSnapshot(querySnapshot => {
                                processSnapshot(querySnapshot);
                            });
                    }
                });
        } else {
            write("orangestats", "Please specify either a client_name or custom_id");
        }
    } else {
        if (client_name != "" && custom_id == "") {
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
                                processSnapshot(querySnapshot);
                            });
                    }
                });
        } else {
            write("orangestats", "Please specify either a client_name or custom_id");
        }
    }


});

function processSnapshot(querySnapshot) {
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

            processData(players);
        });
    }
}

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
    console.log("Blue team stats:");
    console.log(teamStats.blue);
    console.log("Orange team stats:");
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
    var a = Math.round(team / total * 100)
    if (a > 0) {
        return a;
    } else {
        return '0';
    }
}

// adds numeric values from ob2 to ob1
function mergeSum(ob1, ob2) {
    var sum = {}
    Object.keys(ob1).forEach(key => {
        if (ob2.hasOwnProperty(key)) {
            if ((typeof ob2[key]) == "number") {
                sum[key] = ob1[key] + ob2[key]
            } else {
                sum[key] = ob1[key];
            }
        }
    })
    return sum;
}