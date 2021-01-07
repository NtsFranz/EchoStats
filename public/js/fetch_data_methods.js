var debug_log = false;

var games = {
    echoarena: { casterprefs: "caster_preferences" },
    onward: { casterprefs: "caster_preferences_onward" }
}

// gets data from caster_preferences and sets the home/away team names, rosters, team stats, etc with options
function buildpregame(db, previousMatches = true, teamStats = true, roster = true, live = true, get_team_ranking = false, game = 'echoarena') {
    if (client_name == "") return;
    db.collection(games[game]['casterprefs']).doc(client_name)
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
                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_all_players_vrml?game=" + game;
                    httpGetAsync(url, function (data) {
                        buildRosterTable(data, home_team_name, "home");
                        buildRosterTable(data, away_team_name, "away");

                        fadeInWhenDone();
                    });
                }

                if (teamStats) {
                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_stats?team_name=" + home_team_name + "&game=" + game;
                    httpGetAsync(url, function (data) {
                        buildTeamVRMLStats(data, "home");

                        fadeInWhenDone();
                    });

                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_stats?team_name=" + away_team_name + "&game=" + game;
                    httpGetAsync(url, function (data) {
                        buildTeamVRMLStats(data, "away");

                        fadeInWhenDone();
                    });
                }

                if (previousMatches || get_team_ranking) {

                    // get previous matches
                    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_matches_recaps_vrml?game=" + game;
                    httpGetAsync(url, function (data) {
                        var matches;
                        try {
                            matches = JSON.parse(data);

                            getPreviousMatchesVRMLPage(matches, home_team_name, "home");
                            getPreviousMatchesVRMLPage(matches, away_team_name, "away");
                            getPreviousHead2HeadMatchesVRMLPage(matches, home_team_name, away_team_name);
                            getPreviousMapHistory(matches, home_team_name, "home");
                            getPreviousMapHistory(matches, away_team_name, "away");
                        } catch (e) {
                            console.error("Can't parse json response: " + data)
                        }

                    });

                    // get the home team's page
                    db.collection('series').doc(default_season).collection('teams').doc(home_team_name)
                        .get().then(doc => {
                            if (doc.exists) {
                                Array.from(document.getElementsByClassName("home_team_page")).forEach(e => {
                                    e.href = doc.data()['vrml_team_page'];
                                });
                                write("home_rank", "#" + doc.data()['rank']);
                            }
                        });

                    // get the away team's page
                    db.collection('series').doc(default_season).collection('teams').doc(away_team_name)
                        .get().then(doc => {
                            if (doc.exists) {
                                if (previousMatches) {
                                    Array.from(document.getElementsByClassName("away_team_page")).forEach(e => {
                                        e.href = doc.data()['vrml_team_page'];
                                    });
                                }
                                else if (get_team_ranking) {
                                    write("away_rank", "#" + doc.data()['rank']);
                                }
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

function vrmlTeamNamesSame(team1, team2) {
    return (team1 == team2 ||
        (team1.includes("aka") && team1.includes(team2)) ||
        (team2.includes("aka") && team2.includes(team1)));
}

function getTeamNameLogo(db, game = 'echoarena') {
    if (client_name == "") return;
    db.collection(games[game]['casterprefs']).doc(client_name)
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

function getCasterPrefs(game = 'echoarena', live = true, callback) {
    if (client_name == "") return;

    if (live) {
        db.collection(games[game]['casterprefs']).doc(client_name)
            .onSnapshot(doc => {
                if (doc.exists) {
                    callback(doc.data());
                }
            });
    } else {
        db.collection(games[game]['casterprefs']).doc(client_name).get()
            .then(doc => {
                if (doc.exists) {
                    callback(doc.data());
                }
            });
    }
}

// returns a js array of caster data
function getCasterList(db, game = 'echoarena', callback) {
    if (game != 'onward') return [];

    var promises = [];

    var casterprefs = {};
    promises.push(db.collection(games[game]['casterprefs']).doc(client_name).get()
        .then(doc => {
            if (doc.exists) {
                casterprefs = doc.data();
            }
        })
    );

    firebase.storage().ref('/OnwardVRML/casters').listAll().then((res) => {
        var urls = [];
        var count = res.items.length;
        // loop through all the image files in the directory
        res.items.forEach(function (i) {
            promises.push(i.getDownloadURL().then((url) => {
                urls.push({
                    "name": i.name.split('.').slice(0, -1).join('.'),
                    "url": url,
                });

                console.log(urls[urls.length - 1]);
            }));
        });

        // once all the images were fetched and the current casters were fetched 
        Promise.all(promises).then(() => {
            // sort list first
            urls.sort((a, b) => {
                return a.name.toLowerCase() > b.name.toLowerCase();
            });

            // use the list in a callback
            if (callback != null) {
                callback(urls, casterprefs);
            }
            return urls;
        });
    });
}

// returns a js array of caster data
function getMapList(db, game = 'onward', callback) {
    if (game != 'onward') return [];

    var promises = [];

    var casterprefs = {};
    promises.push(db.collection(games[game]['casterprefs']).doc(client_name).get()
        .then(doc => {
            if (doc.exists) {
                casterprefs = doc.data();
            }
        })
    );

    firebase.storage().ref('/OnwardVRML/maps').listAll().then((res) => {
        var urls = [];
        var count = res.items.length;
        // loop through all the image files in the directory
        res.items.forEach(function (i) {
            promises.push(i.getDownloadURL().then((url) => {
                urls.push({
                    "name": i.name.split('.').slice(0, -1).join('.'),
                    "url": url,
                });

                console.log(urls[urls.length - 1]);
            }));
        });

        // once all the images were fetched and the current casters were fetched 
        Promise.all(promises).then(() => {
            // sort list first
            urls.sort((a, b) => {
                return a.name.toLowerCase() > b.name.toLowerCase();
            });

            // use the list in a callback
            if (callback != null) {
                callback(urls, casterprefs);
            }
            return urls;
        });
    });
}

function showSelectedCasters(elemClassName, casterprefs) {
    var elems = document.getElementsByClassName(elemClassName);
    var i = 0;
    Array.from(elems).forEach(e => {
        var casterName = casterprefs['caster_' + i + '_name'];
        Array.from(e.querySelectorAll('div')).forEach(d => {
            if (casterName == "") casterName = "None";
            if (d.innerText == casterName) {
                d.classList.add('selected');
            }
            else {
                d.classList.remove('selected');
            }
        });
        i += 1;
    });
}


function showSelectedMaps(elemClassName, casterprefs) {
    var elems = document.getElementsByClassName(elemClassName);
    var i = 0;
    Array.from(elems).forEach(e => {
        var mapName = casterprefs['map_' + i + '_name'];
        Array.from(e.querySelectorAll('div')).forEach(d => {
            if (mapName == "") mapName = "None";
            if (d.innerText == mapName) {
                d.classList.add('selected');
            }
            else {
                d.classList.remove('selected');
            }
        });
        i += 1;
    });
}

function getCasters(game = "echoarena") {
    getCasterPrefs(game, true, (data) => {

        write('caster_0_name', data['caster_0_name']);
        if (data['caster_0_webcam']) {
            setImage('caster_0_img', "");
        } else {
            setImage('caster_0_img', data['caster_0_img']);
        }
        writeChecked('caster_0_webcam', data['caster_0_webcam']);

        write('caster_1_name', data['caster_1_name']);
        if (data['caster_1_webcam']) {
            setImage('caster_1_img', "");
        } else {
            setImage('caster_1_img', data['caster_1_img']);
        }
        writeChecked('caster_1_webcam', data['caster_1_webcam']);

        write('analyst_name', data['caster_2_name'], "analyst_box");
        if (data['caster_2_webcam']) {
            setImage('analyst_img', "");
        } else {
            setImage('analyst_img', data['caster_2_img']);
        }
        writeChecked('analyst_webcam', data['caster_2_webcam']);

    });
}

function getMaps(game = "onward") {
    getCasterPrefs(game, true, (data) => {
        for (var i = 0; i < 3; i++) {
            const j = i;
            write('map_' + j + '_name', data['map_' + j + '_name']);
            setImage('map_' + j + '_img', data['map_' + j + '_img']);
        }

    });
}

function addListOfCastersToElems(casterList, elemClassName, onClickEvent) {
    var elems = document.getElementsByClassName(elemClassName);
    let i = 0;
    Array.from(elems).forEach(e => {
        let j = i;  // so that the value doesn't change with reference, js is weird
        addImageButton(e, "None", "", j, onClickEvent);
        casterList.forEach(c => {
            addImageButton(e, c.name, c.url, j, onClickEvent);
        });
        i += 1;
    });
}

function addListOfMapsToElems(list, elemClassName, onClickEvent) {
    var elems = document.getElementsByClassName(elemClassName);
    let i = 0;
    Array.from(elems).forEach(e => {
        let j = i;  // so that the value doesn't change with reference, js is weird
        addImageButton(e, "None", "", j, onClickEvent);
        list.forEach(c => {
            addImageButton(e, c.name, c.url, j, onClickEvent);
        });
        i += 1;
    });
}

function addImageButton(parent, name, url, index, onClickEvent) {
    var a = document.createElement("a");
    var div = document.createElement("div");
    var img = document.createElement("img");
    var p = document.createElement("p");

    p.innerText = name;
    img.src = url;

    div.appendChild(p);
    div.appendChild(img);
    a.appendChild(div);
    a.addEventListener("click", () => { onClickEvent(name, url, index); });
    parent.appendChild(a);
}

function getPreviousMatchesVRMLPage(matches, team_name, side) {
    table = "";
    matches.forEach(m => {
        if (m['DatePlayed'].length > 0 &&
            (m['HomeTeam'] == team_name || m['AwayTeam'] == team_name)) {
            table += genPreviousMatchVRMLPage(m, team_name);
        }
    });
    write(side + "_recent_matches", table);
}

function getPreviousHead2HeadMatchesVRMLPage(matches, home_team_name, away_team_name) {
    table = "";
    matches.forEach(m => {
        if (m['DatePlayed'].length > 0) {
            if ((m['HomeTeam'] == home_team_name || m['AwayTeam'] == home_team_name) &&
                (m['HomeTeam'] == away_team_name || m['AwayTeam'] == away_team_name)) {
                table += genPreviousHead2HeadMatchVRMLPage(m, home_team_name, away_team_name, true);
            }
        }
    });
    write("prev_head2head", table, "previous_matchups");
}

function getPreviousMapHistory(matches, team_name, side) {
    maps = {};
    matches.forEach(m => {
        if (m['DatePlayed'].length > 0) {
            // if we are on one of the teams
            if ((m['HomeTeam'] == team_name || m['AwayTeam'] == team_name)) {
                var side = m['HomeTeam'] == team_name ? "Home" : "Away";
                m['MapsSet'].forEach(map => {
                    if (!maps.hasOwnProperty(map['MapName'])) {
                        maps[map['MapName']] = 0;
                    }
                    maps[map['MapName']] += map[side + "Score"] - map[otherSide(side) + "Score"];
                });
            }
        }
    });

    // Create maps array
    var mapsArray = Object.keys(maps).map(key => {
        return [key, maps[key]];
    });

    // Sort the array based on the second element
    mapsArray.sort((first, second) => {
        return second[1] - first[1];
    });

    var table = "";
    // if the length is zero, we want table to be completely empty so it goes away
    if (mapsArray.length > 0) {
        table += "<tr>";
        mapsArray.forEach(m => {
            table += "<tr>";
            table += "<td>" + m[0] + "</td>";
            table += "<td>" + m[1] + "</td>";
            table += "</tr>";
        });
        table += "</tr>";
    }

    write("map_history_body_" + side, table, "map_history_" + side);
}

function buildTeamVRMLStats(data, side) {
    table = "";
    data = JSON.parse(data);

    setImage(side + "_division", data.DivisionLogo);
    write(side + "_mmr", "MMR: " + data.MMR + " (" + data.W + " - " + data.L + ")");
    write(side + "_only_mmr", data.MMR);
    write(side + "_record", data.W + "-" + data.L);
}

function buildRosterTable(data, team_name, side) {
    table = "";
    data = JSON.parse(data);
    data["TeamPlayers"].forEach(team => {
        if (vrmlTeamNamesSame(team.Name, team_name)) {
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
        if (vrmlTeamNamesSame(match.HomeTeam, team_name)) {
            table += genPreviousMatchVRMLAPI(match, team_name);
        } else if (vrmlTeamNamesSame(match.AwayTeam, team_name)) {
            table += genPreviousMatchVRMLAPI(match, team_name);
        }
    })
    write(side + "_recent_matches", table);
}

function genPreviousMatchVRMLAPI(match, team_name, side) {
    var out = "<tr><td>";
    if (vrmlTeamNamesSame(match.WinningTeam, team_name)) {
        out += '<i class="icofont-arrow-up" style="color: green;"></i></td><td>';
    } else {
        out += '<i class="icofont-arrow-down" style="color: #b50a0a;"></i></i></td><td>';
    }
    if (vrmlTeamNamesSame(match.HomeTeam, team_name)) {
        out += match.AwayTeam + "</td><td>(" + match.HomeScore + "-" + match.AwayScore + ")";
    } else {
        out += match.HomeTeam + "</td><td>(" + match.AwayScore + "-" + match.HomeScore + ")";
    }
    out += "</td></tr>";
    return out;
}

function genPreviousMatchVRMLPage(match, team_name) {
    var out = "<tr>";

    // whether this team won or not
    if (vrmlTeamNamesSame(match['WinningTeam'], team_name)) {
        out += '<td><i class="icofont-arrow-up" style="color: green;"></i></td>';
    } else {
        out += '<td><i class="icofont-arrow-down" style="color: #b50a0a;"></i></td>';
    }

    // what is the other team's name and write the scores in the correct order
    if (vrmlTeamNamesSame(match['HomeTeam'], team_name)) {
        out += '<td><a href="' + '#' + '" target="blank">' + match['AwayTeam'] + "</a></td><td>" + match['HomeScore'] + " - " + match['AwayScore'] + "</td>";
    } else {
        out += '<td><a href="' + '#' + '" target="blank">' + match['HomeTeam'] + "</a></td><td>" + match['AwayScore'] + " - " + match['HomeScore'] + "</td>";
    }
    out += "</tr>";
    return out;
}

function genPreviousHead2HeadMatchVRMLPage(match, home_team_name, away_team_name, by_round = false) {
    var out = "<tr>";

    out += "<td>" + match["DatePlayed"] + "</td>";

    var side = "Away"
    if (match['HomeTeam'] == home_team_name) {
        side = "Home";
    }

    // home team
    if (match['WinningTeam'] == home_team_name) {
        out += '<td><i class="icofont-arrow-up" style="color: green;"></i></td>';
    } else {
        out += '<td><i class="icofont-arrow-down" style="color: #b50a0a;"></i></td>';
    }
    out += "<td>" + match[side + 'Team'] + "</td>"
    out += "<td>" + match[side + 'Score'] + " - ";

    // swap sides
    side = otherSide(side);

    // away team
    out += match[side + 'Score'] + "</td>";
    out += "<td>" + match[side + "Team"] + "</td>"
    if (match['WinningTeam'] == away_team_name) {
        out += '<td><i class="icofont-arrow-up" style="color: green;"></i></td>';
    } else {
        out += '<td><i class="icofont-arrow-down" style="color: #b50a0a;"></i></td>';
    }

    out += "</tr>";


    // add the individual rounds
    if (by_round) {
        match['MapsSet'].forEach(map => {
            out += "<tr>";
            out += "<td colspan=3>" + map['MapName'] + "</td>";
            out += "<td>" + map[otherSide(side) + 'Score'] + " - " + map[side + 'Score'] + "</td>";
            out += "</tr>";
        });
    }

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


// adds a row to the end of the table
function createMatchRowHTML(doc) {
    var row = "<tr>";

    var dateStr = doc.data()['match_time'];
    dateStr = dateStr.replace(" ", "T");
    dateStr += "Z";
    row += "<td>" + timeSince(new Date(dateStr)) + "</td>";
    row += "<td>" + doc.data()['version'] + "</td>";
    row += "<td>" + doc.data()['orange_team_score'] + "</td>";
    row += "<td>" + doc.data()['blue_team_score'] + "</td>";
    row += "<td>" + doc.data()['finish_reason'] + "</td>";


    row += "</tr>";

    return row;
}

function getCurrentMatchStats(db, long = false, live = false, onlyaftercasterprefs = false, dataProcessingCallback = null, game = 'echoarena') {
    if (onlyaftercasterprefs) {
        if (client_name != "") {
            db.collection(games[game]['casterprefs']).doc(client_name)
                .onSnapshot(doc => {
                    if (doc.exists) {
                        lastCasterTime = doc.data()['last_modified'];
                        doGetCurrentMatchStats(db, long, live, lastCasterTime, dataProcessingCallback);
                    }
                });
        }
    } else {
        doGetCurrentMatchStats(db, long, live, onlyaftercasterprefs, dataProcessingCallback);
    }
}


function doGetCurrentMatchStats(db, long = false, live = false, lastCasterTime = null, dataProcessingCallback = null) {
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
                    db.collection('series').doc(series_name).collection('match_stats')
                        .orderBy("match_time", "desc")
                        .where("custom_id", "==", recent_custom_id)
                        .where("session_id", "==", recent_session_id)
                        .where("disabled", "==", false)
                        .where("client_name", "==", client_name) // not necessary, but possible because of sha256 collisions on custom_id
                        .get()
                        .then(querySnapshot => {
                            processMatchStatsSnapshot(querySnapshot, long, lastCasterTime, dataProcessingCallback);
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
                    db.collection('series').doc(series_name).collection('match_stats')
                        .orderBy("match_time", "desc")
                        .where("custom_id", "==", recent_custom_id)
                        .where("session_id", "==", recent_session_id)
                        .where("disabled", "==", false)
                        .where("client_name", "==", client_name) // Probably not necessary, but possible because of sha256 collisions on custom_id
                        .get()
                        .then(querySnapshot => {
                            processMatchStatsSnapshot(querySnapshot, long, lastCasterTime, dataProcessingCallback);
                        });
                }
            });
    }

}

// gets the match stats for each player in the match
function processMatchStatsSnapshot(querySnapshot, long = false, lastCasterTime = null, dataProcessingCallback = null) {
    if (!querySnapshot.empty) {

        var players = {}

        var playerPromises = [];
        var first = true;

        var matchRows = "";

        querySnapshot.docs.forEach(match => {
            if (!('disabled' in match.data()) || match.data()['disabled'] == false) {

                // don't add matches that were *just* added if there is a previous match anyway
                var match_time = Date.parse(match.data()['match_time']) - (new Date()).getTimezoneOffset() * 60000
                if (querySnapshot.docs.length > 1 &&    // if there are other rounds available anyway
                    (Date.now() - match_time) < 60000   // if the round wasn't started less than a minute ago
                ) {
                    // skip
                    console.log("last match was very recent, skipping it in the overlay");
                } else {
                    if (lastCasterTime != null && match_time / 1000 < lastCasterTime.seconds) {
                        // skip
                        console.log("round was before last caster prefs switch, skipping it in the overlay");
                    } else {

                        playerPromises.push(
                            // get all players
                            match.ref.collection('players').get()
                        );

                        // add matches to a round history
                        matchRows += createMatchRowHTML(match);
                    }
                }

                // add atlas links
                writeHREF("atlas_player_join", "atlas://j/" + match.data()['session_id'], "atlas_buttons");
                writeHREF("atlas_spectator_join", "atlas://s/" + match.data()['session_id'], "atlas_buttons");

                first = false;
            }
        });

        write("prev_round_scores", matchRows, "round_scores");

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

            if (debug_log) {
                console.log("Player data:");
                console.log(players);
            }

            setPlayerMatchStats(players, long, dataProcessingCallback);
        });
    }
}

function setPlayerMatchStats(players, long = false, dataProcessingCallback = null) {

    // which stats to include in the tables
    var statList = [
        "points",
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
        },
        "spectator": {
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

            teamStats[p.team_color].points += p.points;
            teamStats[p.team_color].possession_time += p.possession_time;
            teamStats[p.team_color].shots_taken += p.shots_taken;
            teamStats[p.team_color].assists += p.assists;
            teamStats[p.team_color].saves += p.saves;
            teamStats[p.team_color].steals += p.steals;
            teamStats[p.team_color].stuns += p.stuns;
        }
    });

    var totalStats = mergeSum(teamStats.blue, teamStats.orange);

    if (debug_log) {
        console.log("Blue team stats:");
        console.log(teamStats.blue);
        console.log("Orange team stats:");
        console.log(teamStats.orange);
    }

    Object.keys(teamStats).forEach(color => {
        Object.keys(teamStats[color]).forEach(stat => {
            if (color != "spectator") {
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
            }
        });

        write(color + "_player_stats_board", playerTables[color]);
    });

    if (dataProcessingCallback != null) {
        dataProcessingCallback({
            "team_stats": teamStats,
            "player_stats": players
        });
    }

    fadeInWhenDone();
}

function autocompleteCasters(input, db, game = 'echoarena') {
    db.collection(games[game]['casterprefs'])
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

function autocompleteTeamInputs(data) {

    data = JSON.parse(data);
    teams = [];

    data.forEach(t => {
        teams.push(t['Name']);
        teamLogosDict[t['Name']] = t;
    })

    Array.from(document.getElementsByClassName("team_input")).forEach(e => {
        autocomplete(e, teams, 0, getTeamLogos);
    });

    // Array.from(document.getElementsByClassName('custom_team_input_form')).forEach(elem => {
    //     elem.addEventListener('submit', handleForm);
    //     // elem.addEventListener('submit', e => {
    //     //     e.preventDefault();
    //     //     getTeamLogos();
    //     //     e.preventDefault();
    //     //     return false;
    //     // });
    // });
}

function handleForm(event) { event.preventDefault(); }

function getTeamLogos(inputElement) {
    if (inputElement.classList.contains('home_team_name')) {
        writeValue('home_team_logo', teamLogosDict[inputElement.value]['Logo']);
        setImage('home_team_logo_img', teamLogosDict[inputElement.value]['Logo']);
    } else if (inputElement.classList.contains('away_team_name')) {
        writeValue('away_team_logo', teamLogosDict[inputElement.value]['Logo']);
        setImage('away_team_logo_img', teamLogosDict[inputElement.value]['Logo']);
    }

    // home_team_name = document.getElementsByClassName('away_team_name')[0].value;}

    // away_team_name = document.getElementsByClassName('away_team_name')[0].value;

    // Array.from(document.getElementsByClassName("home_team_name")).forEach(tname => {
    //     tname.addEventListener("input", function (event) {
    //         Array.from(document.getElementsByClassName("home_team_logo")).forEach(tlogo => {
    //             tlogo.value = teamLogosDict[tname.value]['Logo'];
    //         });
    //     });
    // });
    // Array.from(document.getElementsByClassName("away_team_name")).forEach(tname => {
    //     tname.addEventListener("input", function (event) {
    //         Array.from(document.getElementsByClassName("away_team_logo")).forEach(tlogo => {
    //             tlogo.value = teamLogosDict[tname.value]['Logo'];
    //         });
    //     });
    // });
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
function get_upcoming_matches(game = "echoarena") {
    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_upcoming_matches_vrml?game=" + game;
    httpGetAsync(url, showUpcomingMatches);
}