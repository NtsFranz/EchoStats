var matchRow;
var matchRowAddSplitter;
var sortableList;
var swapSidesButton;
var db;
var side_bool;
var teamLogosDict = {};


function Start(db) {

    matchRow = document.getElementsByClassName('list-group-item')[0];
    matchRowSplitter = document.getElementsByClassName('match_group_splitter')[0];
    sortableList = document.getElementById('match_list');
    swapSidesButton = document.getElementById('swap_sides_button');
    swapSidesButton.onclick = toggleSides;

    currentCaster = document.getElementById('current-caster-name');
    if (client_name != "") {
        currentCaster.innerText = "Setting overlay for: " + client_name;
    } else {
        currentCaster.innerHTML = "<span style='font-weight:900; color: #900;'>Overlay user not set.</span>";
    }

    var manualClickHandler = function (row) {
        return function () {
            if (client_name == "") return;
            db.collection("caster_preferences_onward").doc(client_name).set({
                home_team: row.getElementsByClassName('home_team_name')[0].value,
                home_logo: row.getElementsByClassName('home_team_logo')[0].value,
                away_logo: row.getElementsByClassName('away_team_logo')[0].value,
                away_team: row.getElementsByClassName('away_team_name')[0].value,
                last_modified: firebase.firestore.FieldValue.serverTimestamp()
            }, {
                merge: true
            })
                .catch(function (error) {
                    // The document probably doesn't exist.
                    console.error("Error updating document: ", error);
                });

            // unselect all the other rows
            Array.from(sortableList.getElementsByTagName('tr')).forEach(r => {
                r.classList.remove('match-selected');
            });
            // select the correct row
            row.classList.add('match-selected');
        };
    };

    rowNode = document.getElementById('manual_input');
    rowNode.onclick = manualClickHandler(rowNode);

    get_upcoming_matches("onward");

    autocompleteCasters(document.getElementById("player_search"), db, game = 'onward');

    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_logos?game=onward"
    httpGetAsync(url, autocompleteTeamInputs);

    getTeamNameLogo(db, 'onward');

    var casterList = getCasterList(db, 'onward', (list, casterprefs) => {
        addListOfCastersToElems(list, "caster_list", (caster_name, caster_img, index) => {
            if (client_name != "") {
                if (caster_name == "None") caster_name = "";
                db.collection('caster_preferences_onward').doc(client_name).set({
                    ["caster_" + index + "_name"]: caster_name,
                    ["caster_" + index + "_img"]: caster_img
                }, {
                    merge: true
                }).catch(function (error) {
                    // The document probably doesn't exist.
                    console.error("Error updating document: ", error);
                });

                getCasterPrefs(game, true, (casterprefs) => {
                    showSelectedCasters("caster_list", casterprefs);
                });
            }
        });

        showSelectedCasters("caster_list", casterprefs);
    });

    var mapList = getMapList(db, 'onward', (list, casterprefs) => {
        addListOfMapsToElems(list, "map_list", (map_name, map_img, index) => {
            if (client_name != "") {
                if (map_name == "None") map_name = "";
                db.collection('caster_preferences_onward').doc(client_name).set({
                    ["map_" + index + "_name"]: map_name,
                    ["map_" + index + "_img"]: map_img
                }, {
                    merge: true
                }).catch(function (error) {
                    // The document probably doesn't exist.
                    console.error("Error updating document: ", error);
                });

                getCasterPrefs(game, true, (casterprefs) => {
                    showSelectedMaps("map_list", casterprefs);
                });
            }
        });
    });

    var casterListHeaders = Array.from(document.getElementsByClassName('caster_list_header'));
    var casterLists = Array.from(document.getElementsByClassName('caster_list'));
    var webcamButtons = Array.from(document.getElementsByClassName('caster_webcam'));

    var mapListHeaders = Array.from(document.getElementsByClassName('map_list_header'));
    var mapLists = Array.from(document.getElementsByClassName('map_list'));


    for (var i = 0; i < casterListHeaders.length; i++) {
        let j = i;
        casterListHeaders[i].addEventListener('click', () => {
            if (casterLists[j].classList.contains('expanded')) {
                casterLists[j].classList.remove('expanded');
            } else {
                casterLists[j].classList.add('expanded');
            }
        });

        // webcam checkboxes
        webcamButtons[j].addEventListener('click', () => {
            db.collection('caster_preferences_onward').doc(client_name).set({
                ["caster_" + j + "_webcam"]: webcamButtons[j].checked
            }, {
                merge: true
            }).catch(function (error) {
                // The document probably doesn't exist.
                console.error("Error updating document: ", error);
            });
        });
    }

    // map list expansion
    for (var i = 0; i < mapListHeaders.length; i++) {
        let j = i;
        mapListHeaders[i].addEventListener('click', () => {
            if (mapLists[j].classList.contains('expanded')) {
                mapLists[j].classList.remove('expanded');
            } else {
                mapLists[j].classList.add('expanded');
            }
        });
    }



    getCasters(game = 'onward');
    getMaps(game = 'onward');

}


function showUpcomingMatches(data) {


    data = JSON.parse(data);
    console.log(data);
    data.forEach(match => {
        addMatchUpcoming(match);
    });

    // get the match that is currently set
    getCasterPrefs(game = "onward", true, (data) => {
        side_bool = data['swap_sides'];
        if (side_bool) {
            swapSidesButton.classList.add("sides_swapped");
            swapSidesButton.innerHTML = "Home/Away is swapped";
        } else {
            swapSidesButton.classList.remove("sides_swapped");
            swapSidesButton.innerHTML = "Home/Away is <em>not</em> swapped";
        }
        Array.from(sortableList.getElementsByTagName('tr')).forEach(r => {
            if (r.getElementsByClassName('upcoming_home_team_name').length > 0 &&
                r.getElementsByClassName('upcoming_home_team_name')[0].innerText == data['home_team'] &&
                r.getElementsByClassName('upcoming_away_team_name')[0].innerText == data['away_team']) {
                r.classList.add('match-selected');
                return;
            }
        });
    });
}

function toggleSides() {
    if (client_name != "") {
        db.collection("caster_preferences_onward").doc(client_name).set({
            swap_sides: !side_bool
        }, {
            merge: true
        })
            .catch(function (error) {
                // The document probably doesn't exist.
                console.error("Error updating document: ", error);
            });
        side_bool = !side_bool;

        if (side_bool) {
            swapSidesButton.classList.add("sides_swapped");
            swapSidesButton.innerHTML = "Home/Away is swapped";
        } else {
            swapSidesButton.classList.remove("sides_swapped");
            swapSidesButton.innerHTML = "Home/Away is <em>not</em> swapped";
        }
    }
}

// adds a row to the end of the table
function addMatchUpcoming(data) {
    var rowNode = matchRow.cloneNode(true);
    rowNode.classList.remove('hide');

    // rowNode.getElementsByClassName('match_id')[0].innerText = doc.id;
    rowNode.getElementsByClassName('match_time')[0].innerText = data['DateScheduled'];
    rowNode.getElementsByClassName('upcoming_home_team_logo')[0].getElementsByTagName("img")[0].src = data['HomeTeamLogo'];
    rowNode.getElementsByClassName('upcoming_home_team_name')[0].innerText = data['HomeTeam'];
    rowNode.getElementsByClassName('upcoming_away_team_name')[0].innerText = data['AwayTeam'];
    rowNode.getElementsByClassName('upcoming_away_team_logo')[0].getElementsByTagName("img")[0].src = data['AwayTeamLogo'];
    var castersString = data['CasterName'];
    if (data['CoCasterName'] != "") {
        castersString += ", " + data['CoCasterName'];
    }
    rowNode.getElementsByClassName('casters')[0].innerText = castersString;

    if (client_name != "") {
        var createClickHandler = function (row) {
            return function () {
                db.collection("caster_preferences_onward").doc(client_name).set({
                    home_team: data['HomeTeam'],
                    home_logo: data['HomeTeamLogo'],
                    away_logo: data['AwayTeamLogo'],
                    away_team: data['AwayTeam'],
                    last_modified: firebase.firestore.FieldValue.serverTimestamp()
                }, {
                    merge: true
                })
                    .catch(function (error) {
                        // The document probably doesn't exist.
                        console.error("Error updating document: ", error);
                    });

                // unselect all the other rows
                Array.from(sortableList.getElementsByTagName('tr')).forEach(r => {
                    r.classList.remove('match-selected');
                });
                // select the correct row
                row.classList.add('match-selected');

                console.log("set: " + data['HomeTeam'] + " vs " + data['AwayTeam']);
            };
        };

        rowNode.onclick = createClickHandler(rowNode);
    }
    sortableList.appendChild(rowNode);
}