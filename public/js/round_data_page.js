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


    firebase.auth().signInAnonymously().catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
        console.log("failed auth");
    });


    var db = firebase.firestore()

    db.collection('series').doc('vrml_season_2').collection('match_stats')
        .orderBy("match_time", "desc")
        .where("client_name", "==", client_name)
        .limit(1)
        .get()
        .then(querySnapshot => {
            if (!querySnapshot.empty) {
                //We know there is one doc in the querySnapshot
                const lastMatchDoc = querySnapshot.docs[0];

                console.log(lastMatchDoc.data());

                // get all players
                lastMatchDoc.ref.collection('players')
                    .onSnapshot(playersQuery => {
                        if (!playersQuery.empty) {

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
                            playersQuery.docs.map(player => {

                                p = player.data();
                                
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
                    });
            }
        });
});

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

function mergeSum(ob1, ob2) {
    let sum = {};

    Object.keys(ob1).forEach(key => {
        if (ob2.hasOwnProperty(key)) {
            sum[key] = ob1[key] + ob2[key]
        }
    })
    return sum;
}