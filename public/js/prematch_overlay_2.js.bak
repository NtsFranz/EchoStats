var left_side;
var right_side;

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

    if (client_name == "") {
        console.log("No client_name");
        document.body.innerHTML = "<div style='color:black;'>Must specify a client_name. ex: <a href=\'/prematch_overlay?client_name=NtsFranz\'>prematch_overlay?client_name=NtsFranz</a></div>";
    } else {
        buildpregame2(db);
    }
});

function buildpregame2(db) {
    db.collection("caster_preferences").doc(client_name)
        .get()
        .then(doc => {
            if (doc.exists) {
                console.log(doc.data()['swap_sides']);
                if (doc.data()['swap_sides']) {
                    left_side = "away";
                    right_side = "home";
                } else {
                    left_side = "home";
                    right_side = "away"
                }
                // set logos
                setImage(left_side + "logo", doc.data()['home_logo']);
                setImage(right_side + "logo", doc.data()['away_logo']);

                // set team names
                write(left_side + "_team_name", doc.data()[left_side + '_team']);
                write(right_side + "_team_name", doc.data()[right_side + '_team']);

                // get home team data via firestore...
                db.collection("series").doc("vrml_season_2").collection("teams").doc(doc.data()[left_side + '_team'])
                    .get()
                    .then(function (team) {
                        if (team.exists) {
                            // set division...
                            setImage("homerank", team.data()['division_logo']);

                            // set home mmr
                            write("homemmr", "MMR: " + team.data()['mmr'] + " (" + team.data()['wins'] + " - " + team.data()['losses'] + ")");

                        } else {
                            setImage("homerank", "");
                            write("homemmr", " ");
                        }
                    });
                // get away team data via firestore...
                db.collection("series").doc("vrml_season_2").collection("teams").doc(doc.data()[right_side + '_team'])
                    .get()
                    .then(function (team) {
                        if (team.exists) {
                            // set division...
                            setImage("awayrank", team.data()['division_logo']);

                            // set home mmr
                            write("awaymmr", "MMR: " + team.data()['mmr'] + " (" + team.data()['wins'] + " - " + team.data()['losses'] + ")");

                        } else {
                            setImage("awayrank", "");
                            write("awaymmr", " ");
                        }


                        // document.getElementById("background_container").style.opacity = 1;
                    });

            }
        });
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
        var blueplayers = [];
        var orangeplayers = [];
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
            blueplayers.push(p.player_name);

        } else if (p.team_color == "orange") {
            orangePlayersTable += table;
            teamStats.orange.possession_time += p.possession_time;
            teamStats.orange.shots_taken += p.shots_taken;
            teamStats.orange.assists += p.assists;
            teamStats.orange.saves += p.saves;
            teamStats.orange.steals += p.steals;
            teamStats.orange.stuns += p.stuns;
            orangeplayers.push(p.player_name);
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

// get upcoming matches
function get_team_stats(team_name) {
    // var url = "/get_upcoming_matches"
    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_stats?team_name=" + team_name;
    httpGetAsync(url, showTeamStates);
}

function showTeamStates(data) {
    data = JSON.parse(data);
    console.log(data);
}

function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function write(id, data) {
    var element = document.getElementById(id);
    if (element) {
        element.innerHTML = data;
        element.style.visibility = 'visible';
    }
}

function setImage(id, src_) {
    var element = document.getElementById(id);
    if (element) {
        element.src = src_;
        element.style.visibility = 'visible';
    }
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