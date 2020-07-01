var matchRow;
var matchRowAddSplitter;
var sortableList;
var db;

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
                console.log("failed precondition for persistence");
            } else if (err.code == 'unimplemented') {
                // The current browser does not support all of the
                // features required to enable persistence
                // ...
                console.log("browser doesn't support persistence");
            }
        });
    // Subsequent queries will use persistence, if it was enabled successfully

    db = firebase.firestore();

    // Initialize the FirebaseUI Widget using Firebase.
    var ui = new firebaseui.auth.AuthUI(firebase.auth());

    firebase.auth().signInAnonymously().catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
        console.log("failed auth");
    });




    matchRow = document.getElementsByClassName('list-group-item')[0];
    matchRowSplitter = document.getElementsByClassName('match_group_splitter')[0];
    sortableList = document.getElementById('match_list');

    // get season names
    if (series_name == "") {
        series_name = "vrml_season_2";
    }

    // loop through matches
    db.collection('series').doc(series_name).collection('match_stats')
        .orderBy("match_time", "desc")
        .where("client_name", "==", client_name)
        .limit(30)
        .get()
        .then(querySnapshot => {
            if (!querySnapshot.empty) {
                var custom_id = querySnapshot.docs[0].data()['custom_id'];
                var session_id = querySnapshot.docs[0].data()['session_id'];
                var splitter_count = 0;
                var valid_row_count = 0;
                querySnapshot.docs.forEach(doc => {
                    var new_custom_id = doc.data()['custom_id'];
                    var new_session_id = doc.data()['session_id'];
                    if (custom_id != new_custom_id || session_id != new_session_id) {
                        addSplitter();
                        splitter_count++;
                        if (valid_row_count == 0) {
                            splitter_count = 0;
                        }
                    }
                    custom_id = new_custom_id;
                    session_id = new_session_id;

                    valid_row_count += addMatch(doc, splitter_count < 1);
                });
            }
        });


    // Simple list
    var options = {
        animation: 200,
        ghostClass: 'list-group-item-ghost',
        handle: ".match_group_splitter"
    };
    options['onEnd'] = function (evt) {
        splitMatches();
    };
    Sortable.create(match_list, options);



});


// adds a row to the end of the table
function addMatch(doc, first = false) {
    var disabled = false; // whether this is disabled or not
    var rowNode = matchRow.cloneNode(true);
    rowNode.classList.remove('hide');
    if (first) {
        rowNode.classList.add('match_highlighted')
    }
    if (doc.data()['disabled']) {
        rowNode.classList.add('disabled_match');
        disabled = true;
    }
    rowNode.getElementsByClassName('match_id')[0].innerText = doc.id;
    rowNode.getElementsByClassName('custom_id')[0].innerText = doc.data()['custom_id'];
    rowNode.getElementsByClassName('match_time')[0].innerText = doc.data()['match_time'];
    rowNode.getElementsByClassName('session_id')[0].innerText = doc.data()['session_id'];
    var len = doc.data()['game_clock_start'] - doc.data()['game_clock_end'];
    var game_clock_duration_elem = rowNode.getElementsByClassName('game_clock_duration')[0];
    game_clock_duration_elem.innerHTML = Math.round(len) + game_clock_duration_elem.innerHTML;
    game_clock_duration_elem.getElementsByTagName('div')[0].style.width = 100 * len / 600 + '%';
    rowNode.getElementsByClassName('blue_team_score')[0].innerText = doc.data()['blue_team_score'];
    rowNode.getElementsByClassName('orange_team_score')[0].innerText = doc.data()['orange_team_score'];
    rowNode.getElementsByClassName('finish_reason')[0].innerText = doc.data()['finish_reason'];

    rowNode.getElementsByClassName('remove')[0].addEventListener('click', function () {
        disableMatch(doc.id, rowNode);
        splitMatches();
    });

    sortableList.appendChild(rowNode);

    return disabled ? 0 : 1; // returns the number of valid rows added
}

function addSplitter(elementAfter = null) {
    var splitterNode = matchRowSplitter.cloneNode(true);
    splitterNode.classList.remove('hide');

    if (elementAfter == null) {
        sortableList.appendChild(splitterNode);
    } else {
        sortableList.insertBefore(splitterNode, elementAfter);
    }
}

function splitMatches() {
    var elems = sortableList.getElementsByTagName('tr');
    if (elems.length == 0) {
        return;
    }

    // loop through all the matches
    var last_custom_id = "";
    var last_session_id = "";
    var last_elem_was_split = true;
    var splitting = false; // true when setting new custom_ids until a splitter is found
    var new_custom_id = "";
    var splitter_count = 0;
    var valid_row_count = 0;
    Array.from(elems).forEach((elem) => {
        // ignore hidden elements
        if (!elem.classList.contains('hide')) {

            // is this elem a split node or not?
            var elem_is_split = elem.classList.contains('match_group_splitter');


            // if this is match row
            if (!elem_is_split) {
                if (!elem.classList.contains('disabled_match')) {
                    valid_row_count++;
                }

                // add back a splitter as the top element if it isn't there anymore
                if (splitter_count == 0) {
                    addSplitter(elem);
                    splitter_count++;
                    if (valid_row_count == 0) {
                        splitter_count = 1;
                    }
                }

                var custom_id_elem = elem.getElementsByClassName('custom_id')[0];
                var session_id_elem = elem.getElementsByClassName('session_id')[0];
                var custom_id = custom_id_elem.innerText;
                var session_id = session_id_elem.innerText;

                if (splitter_count <= 1) {
                    elem.classList.add('match_highlighted');
                } else {
                    elem.classList.remove('match_highlighted');
                }

                // if the there was a splitter
                if (last_elem_was_split) {
                    // if the current match ids are the same
                    if (custom_id == last_custom_id) {
                        // we need to change the custom id here, since there is a split, but the same custom id
                        var match_id = elem.getElementsByClassName('match_id')[0].innerText;
                        new_custom_id = sha256(Date.now().toString()).toUpperCase();
                        setNewCustomId(match_id, new_custom_id, custom_id_elem);
                        custom_id = new_custom_id;
                    }
                } else {
                    // if the custom ids should be the same, since there was no splitter
                    if (custom_id != last_custom_id) {
                        // we need to change the custom id here, since the custom id changed, but it shouldn't have
                        var match_id = elem.getElementsByClassName('match_id')[0].innerText;
                        setNewCustomId(match_id, last_custom_id, custom_id_elem);
                        custom_id = last_custom_id;
                    }
                }

                last_custom_id = custom_id;

            } else {
                // if we got two splitters in a row, remove one
                if (last_elem_was_split) {
                    elem.parentNode.removeChild(elem);
                } else {
                    splitter_count++;
                    if (valid_row_count == 0) {
                        splitter_count = 1;
                    }
                }
                splitting = false;
            }

            last_elem_was_split = elem_is_split;
        }

    });

}

function setNewCustomId(match_id, new_custom_id, custom_id_elem) {
    custom_id_elem.innerText = new_custom_id;
    db.collection('series').doc(series_name).collection('match_stats').doc(match_id)
        .update({
            custom_id: new_custom_id
        })
        .then(function () {
            console.log("Document successfully written! custom_id: " + new_custom_id);
        })
        .catch(function (error) {
            console.error("Error writing document: ", error);
        });
}

function disableMatch(match_id, row) {
    var disable = !row.classList.contains('disabled_match');
    if (disable) {
        row.classList.add('disabled_match');
    } else {
        row.classList.remove('disabled_match');
    }
    db.collection('series').doc(series_name).collection('match_stats').doc(match_id)
        .update({
            disabled: disable
        })
        .then(function () {
            console.log("Document successfully written!\t" + (disable ? 'disabled' : 'enabled'));
        })
        .catch(function (error) {
            console.error("Error writing document: ", error);
        });
}