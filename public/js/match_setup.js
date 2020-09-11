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
            db.collection("caster_preferences").doc(client_name).set({
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

    get_upcoming_matches();

    autocompleteCasters(document.getElementById("player_search"), db);

    var url = "https://ignitevr.gg/cgi-bin/EchoStats.cgi/get_team_logos"
    httpGetAsync(url, autocompleteTeamInputs);

}


function showUpcomingMatches(data) {


    data = JSON.parse(data);
    console.log(data);
    data.forEach(match => {
        addMatchUpcoming(match);
    });

    if (client_name == "") return;

    // get the match that is currently set
    db.collection("caster_preferences").doc(client_name).get().then(doc => {
        if (!doc.empty) {
            side_bool = doc.data()['swap_sides'];
            if (side_bool) {
                swapSidesButton.classList.add("sides_swapped");
                swapSidesButton.innerHTML = "Home/Away is swapped";
            } else {
                swapSidesButton.classList.remove("sides_swapped");
                swapSidesButton.innerHTML = "Home/Away is <em>not</em> swapped";
            }
            Array.from(sortableList.getElementsByTagName('tr')).forEach(r => {
                if (r.getElementsByClassName('home_team_name')[0].innerText == doc.data()['home_team'] &&
                    r.getElementsByClassName('away_team_name')[0].innerText == doc.data()['away_team']) {
                    r.classList.add('match-selected');
                    return;
                }
            });
        }
    });
}

function toggleSides() {
    if (client_name != "") {
        db.collection("caster_preferences").doc(client_name).set({
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
    rowNode.getElementsByClassName('home_team_logo')[0].getElementsByTagName("img")[0].src = data['HomeTeamLogo'];
    rowNode.getElementsByClassName('home_team_name')[0].innerText = data['HomeTeam'];
    rowNode.getElementsByClassName('away_team_name')[0].innerText = data['AwayTeam'];
    rowNode.getElementsByClassName('away_team_logo')[0].getElementsByTagName("img")[0].src = data['AwayTeamLogo'];
    var castersString = data['CasterName'];
    if (data['CoCasterName'] != "") {
        castersString += ", " + data['CoCasterName'];
    }
    rowNode.getElementsByClassName('casters')[0].innerText = castersString;

    if (client_name != "") {
        var createClickHandler = function (row) {
            return function () {
                db.collection("caster_preferences").doc(client_name).set({
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