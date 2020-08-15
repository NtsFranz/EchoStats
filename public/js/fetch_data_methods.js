function buildpregame(db, previousMatches = true, teamStats = true, roster = true, live = true) {
    if (client_name == "") return;
    db.collection("caster_preferences").doc(client_name)
        .onSnapshot(doc => {
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
                write("home_team_name", home_team_name);
                write("away_team_name", away_team_name);

                // write "vs" title
                write("match_title", doc.data()[left_side + '_team'] + " vs " + doc.data()[right_side + '_team']);

                if (roster) {
                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_all_players_vrml";
                    httpGetAsync(url, function (data) {
                        buildRosterTable(data, home_team_name, "home");
                        buildRosterTable(data, away_team_name, "away");

                        fadeInWhenDone();
                    });
                }

                if (teamStats) {
                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_stats?team_name=" + home_team_name;
                    httpGetAsync(url, function (data) {
                        buildTeamVRMLStats(data, "home");

                        fadeInWhenDone();
                    });

                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_stats?team_name=" + away_team_name;
                    httpGetAsync(url, function (data) {
                        buildTeamVRMLStats(data, "away");

                        fadeInWhenDone();
                    });
                }

                if (previousMatches) {
                    // get the home team's page
                    db.collection('series').doc(default_season).collection('teams').doc(home_team_name)
                        .get().then(doc => {
                            if (!doc.empty) {
                                var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_vrml_match_history_direct?team_page=" + doc.data()['vrml_team_page'];
                                httpGetAsync(url, function (data) {
                                    getPreviousMatchesVRMLPage(data, home_team_name, "home");
                                    getPreviousHead2HeadMatchesVRMLPage(data, home_team_name, away_team_name);
                                });

                                Array.from(document.getElementsByClassName("home_team_page")).forEach(e => {
                                    e.href = doc.data()['vrml_team_page'];
                                });
                            }
                        });

                    // get the away team's page
                    db.collection('series').doc(default_season).collection('teams').doc(away_team_name)
                        .get().then(doc => {
                            if (!doc.empty) {
                                var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_vrml_match_history_direct?team_page=" + doc.data()['vrml_team_page'];
                                httpGetAsync(url, function (data) {
                                    getPreviousMatchesVRMLPage(data, away_team_name, "away");
                                });

                                Array.from(document.getElementsByClassName("away_team_page")).forEach(e => {
                                    e.href = doc.data()['vrml_team_page'];
                                });
                            }
                        });
                }
            }
        });
}

function fadeInWhenDone() {
    Array.from(document.getElementsByClassName("fade_in_when_done")).forEach(e => {
        e.style.opacity = "1";
    });
}

function getTeamNameLogo(db) {
    if (client_name == "") return;
    db.collection("caster_preferences").doc(client_name)
        .onSnapshot(doc => {
            if (doc.exists) {
                if (doc.data()['swap_sides']) {
                    left_side = "away";
                    right_side = "home";
                } else {
                    left_side = "home";
                    right_side = "away"
                }

                // set logos
                setImage(left_side + "_logo", doc.data().home_logo);
                setImage(right_side + "_logo", doc.data().away_logo);

                // set team names
                write(left_side + "_team_name", doc.data().home_team);
                write(right_side + "_team_name", doc.data().away_team);
            }
        });

    fadeInWhenDone();
}

function getPreviousMatchesVRMLPage(data, team_name, side) {
    table = "";
    var matches;
    try {
        matches = JSON.parse(data).matches;
    } catch (e) {
        console.error("Can't parse json response: " + data)
        return;
    }
    matches.forEach(m => {
        if (m.match_time.length > 0) {
            table += genPreviousMatchVRMLPage(m, team_name);
        }
    });
    write(side + "_recent_matches", table);
}

function getPreviousHead2HeadMatchesVRMLPage(data, home_team_name, away_team_name) {
    table = "";
    var matches;
    try {
        matches = JSON.parse(data).matches;
    } catch (e) {
        console.error("Can't parse json response: " + data)
        return;
    }
    matches.forEach(m => {
        if (m.match_time.length > 0) {
            if ((m.home_team == home_team_name || m.away_team == home_team_name) &&
                (m.home_team == away_team_name || m.away_team == away_team_name)) {
                table += genPreviousHead2HeadMatchVRMLPage(m, home_team_name, away_team_name);
            }
        }
    });
    write("prev_head2head", table);
}

function buildTeamVRMLStats(data, side) {
    table = "";
    data = JSON.parse(data);

    setImage(side + "_rank", data.DivisionLogo);
    write(side + "_mmr", "MMR: " + data.MMR + " (" + data.W + " - " + data.L + ")");
}

function buildRosterTable(data, team_name, side) {
    table = "";
    data = JSON.parse(data);
    data["TeamPlayers"].forEach(team => {
        if (team.Name == team_name) {
            team.Players.forEach(p => {
                table += "<tr><td>" + p.Name + "</td></tr>";
            })
        }
    })
    write(side + "_roster", table);
}

function getPreviousMatches(data, team_name, side) {
    table = "";
    data = JSON.parse(data);
    data.forEach(match => {
        if (match.HomeTeam == team_name) {
            table += genPreviousMatchVRMLAPI(match, team_name);
        } else if (match.AwayTeam == team_name) {
            table += genPreviousMatchVRMLAPI(match, team_name);
        }
    })
    write(side + "_recent_matches", table);
}

function genPreviousMatchVRMLAPI(match, team_name, side) {
    var out = "<tr><td>";
    if (match.WinningTeam == team_name) {
        out += '<i class="icofont-arrow-up" style="color: green;"></i></td><td>';
    } else {
        out += '<i class="icofont-arrow-down" style="color: #b50a0a;"></i></i></td><td>';
    }
    if (match.HomeTeam != team_name) {
        out += match.HomeTeam + "</td><td>(" + match.AwayScore + "-" + match.HomeScore + ")";
    } else {
        out += match.AwayTeam + "</td><td>(" + match.HomeScore + "-" + match.AwayScore + ")";
    }
    out += "</td></tr>";
    return out;
}

function genPreviousMatchVRMLPage(match, team_name) {
    var out = "<tr>";
    if (match.winning_team == team_name) {
        out += '<td><i class="icofont-arrow-up" style="color: green;"></i></td>';
    } else {
        out += '<td><i class="icofont-arrow-down" style="color: #b50a0a;"></i></td>';
    }
    if (match.home_team != team_name) {
        out += '<td><a href="' + match.match_page + '" target="blank">' + match.home_team + "</a></td><td>" + match.away_team_score + " - " + match.home_team_score + "</td>";
    } else {
        out += '<td><a href="' + match.match_page + '" target="blank">' + match.away_team + "</a></td><td>" + match.home_team_score + " - " + match.away_team_score + "</td>";
    }
    out += "</tr>";
    return out;
}

function genPreviousHead2HeadMatchVRMLPage(match, home_team_name, away_team_name) {
    var out = "<tr>";

    out += "<td>" + match.match_time + "</td>";

    var side = "away"
    if (match.home_team == home_team_name) {
        side = "home";
    }

    // home team
    if (match[side + "_team_won"]) {
        out += '<td><i class="icofont-arrow-up" style="color: green;"></i></td>';
    } else {
        out += '<td><i class="icofont-arrow-down" style="color: #b50a0a;"></i></td>';
    }
    out += "<td>" + match[side + "_team"] + "</td>"
    out += "<td>" + match[side + "_team_score"] + " - ";

    // swap sides
    if (side == "home") {
        side = "away";
    } else {
        side = "home";
    }

    // away team
    out += match[side + "_team_score"] + "</td>";
    out += "<td>" + match[side + "_team"] + "</td>"
    if (match[side + "_team_won"]) {
        out += '<td><i class="icofont-arrow-up" style="color: green;"></i></td>';
    } else {
        out += '<td><i class="icofont-arrow-down" style="color: #b50a0a;"></i></td>';
    }

    out += "</tr>";
    return out;
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


function getCurrentMatchStats(db, long = false, live = false) {

    if (live) {
        db.collection('series').doc(series_name).collection('match_stats')
            .orderBy("match_time", "desc")
            .where("client_name", "==", client_name)
            .where("disabled", "==", false)
            .limit(1)
            .onSnapshot(querySnapshot => {
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
                        .where("client_name", "==", client_name) // Probably not necessary, but possible because of sha256 collisions on custom_id
                        .get()
                        .then(querySnapshot => {
                            processMatchStatsSnapshot(querySnapshot, long);
                        });
                }
            });
    } else {
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
                        .where("client_name", "==", client_name) // Probably not necessary, but possible because of sha256 collisions on custom_id
                        .get()
                        .then(querySnapshot => {
                            processMatchStatsSnapshot(querySnapshot, long);
                        });
                }
            });
    }

}

// gets the match stats for each player in the match
function processMatchStatsSnapshot(querySnapshot, long = false) {
    if (!querySnapshot.empty) {

        var players = {}

        var playerPromises = [];
        var first = true;

        querySnapshot.docs.forEach(match => {
            if (!('disabled' in match.data()) || match.data()['disabled'] == false) {

                // don't add matches that were *just* added if there is a previous match anyway
                var match_time = Date.parse(match.data()['match_time']) - (new Date()).getTimezoneOffset() * 60000
                if (querySnapshot.docs.length > 1 && (Date.now() - match_time) < 60000) {
                    // skip
                    console.log("last match was very recent, skipping it in the overlay");
                } else {
                    playerPromises.push(
                        // get all players
                        match.ref.collection('players').get()
                    );
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

            setPlayerMatchStats(players, long);
        });
    }
}

function setPlayerMatchStats(players, long = false) {

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
                "</td><td>" + p.stuns;
            if (long) {
                playerTables[p.team_color] +=
                    "</td><td>" + toMinutesString(p.possession_time) +
                    "</td><td>" + p.shots_taken
            }
            playerTables[p.team_color] += "</td></tr>";

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

    fadeInWhenDone();
}

function autocompleteCasters(input, db) {
    db.collection('caster_preferences')
        .get()
        .then(querySnapshot => {
            if (!querySnapshot.empty) {
                var names = [];
                querySnapshot.forEach(doc => {
                    names.push(doc.id);
                });
                autocomplete(input, names, 0);
            }
        });
}

function setupEventsOverlay(db) {
    db.collection('series').doc(series_name).collection('match_stats')
        .orderBy("match_time", "desc")
        .where("client_name", "==", client_name)
        .limit(1)
        .onSnapshot(querySnapshot => {
            if (!querySnapshot.empty) {

                var version = querySnapshot.docs[0].data()['version'];
                console.log(version);

                querySnapshot.docs[0].ref.collection('events')
                    .where("event_type", "==", "joust_speed")
                    .onSnapshot(eventsSnapshot => {
                        if (!eventsSnapshot.empty) {
                            // loop through all the events for this match
                            eventsSnapshot.docs.forEach(e => {
                                // if we haven't already used this event
                                if (!completedEvents.hasOwnProperty(e.id)) {
                                    completedEvents[e.id] = "";
                                    if (!freshPage) {
                                        var d = e.data();
                                        if (d['other_player_id'] < 15000) {
                                            var color = d['other_player_name'];
                                            write('joust_time_' + color, round(d['other_player_id'] / 1000.0, 2) + " s");
                                            if (version == "1.8.5") {
                                                console.log("Joust time: " + (d['other_player_id'] / 1000.0) + " s, Max speed: " + magnitude(d['x2'], d['y2'], d['z2']) + " m/s")
                                                write('joust_speed_' + color, round(magnitude(d['x2'], d['y2'], d['z2']), 1) + " m/s");
                                            } else {
                                                console.log("Joust time: " + (d['other_player_id'] / 1000.0) + " s, Max speed: " + d['x2'] + " m/s, Tube Exit Speed: " + d['y2'] + " m/s")
                                                write('joust_speed_' + color, round(d['x2'], 1) + " m/s");
                                            }

                                            var joustStatsElem = document.getElementById('joust_stats_' + color);
                                            joustStatsElem.classList.add('visible');
                                            var clonedNode = joustStatsElem.cloneNode(true);
                                            joustStatsElem.parentNode.replaceChild(clonedNode, joustStatsElem);
                                        }
                                    }
                                }
                            });
                            freshPage = false;

                        }
                    });
            }
        });
}


// get upcoming matches
function get_upcoming_matches() {
    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_upcoming_matches"
    httpGetAsync(url, showUpcomingMatches);
}