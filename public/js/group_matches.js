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
            } else if (err.code == 'unimplemented') {
                // The current browser does not support all of the
                // features required to enable persistence
                // ...
            }
        });
    // Subsequent queries will use persistence, if it was enabled successfully

    db = firebase.firestore();

    matchRow = document.getElementsByClassName('list-group-item')[0];
    matchRowSplitter = document.getElementsByClassName('match_group_splitter')[0];
    sortableList = document.getElementById('match_list');

    // get season names
    if (series_name == "") {
        series_name = "vrml_season_1";
    }

    // loop through season names
    db.collection('series').doc(series_name).collection('match_stats')
        .orderBy("match_time", "desc")
        .where("client_name", "==", client_name)
        .limit(10)
        .get()
        .then(querySnapshot => {
            if (!querySnapshot.empty) {
                var custom_id = querySnapshot.docs[0].data()['custom_id'];
                querySnapshot.docs.forEach(doc => {
                    var new_custom_id = doc.data()['custom_id'];
                    if (custom_id != new_custom_id) {
                        addSplitter();
                    }
                    custom_id = new_custom_id;

                    addMatch(doc);
                });
            }
        });


    // Simple list
    Sortable.create(match_list, {
        animation: 200,
        ghostClass: 'list-group-item-ghost',
        handle: ".match_group_splitter"
    });

});


// adds a row to the end of the table
function addMatch(doc) {
    var rowNode = matchRow.cloneNode(true);
    rowNode.classList.remove('hide');
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

    sortableList.appendChild(rowNode);
}

function addSplitter(elementBefore = null) {
    var splitterNode = matchRowSplitter.cloneNode(true);
    splitterNode.classList.remove('hide');

    if (elementBefore == null) {
        sortableList.appendChild(splitterNode);
    } else {
        sortableList.insertAfter(splitterNode, elementBefore);
    }
}

function splitMatches() {
    var elems = sortableList.getElementsByTagName('tr');
    if (elems.length == 0) {
        return;
    }

    // loop through all the matches
    var last_custom_id = "";
    var last_elem_was_split = true;
    Array.from(elems).forEach((elem) => {
        // ignore hidden elements
        if (!elem.classList.contains('hide')) {

            // is this elem a split node or not?
            var elem_is_split = elem.classList.contains('match_group_splitter');

            // if this is match row
            if (!elem_is_split) {
                var custom_id = elem.getElementsByClassName('custom_id')[0].innerText;

                // if the there was a splitter
                if (last_elem_was_split) {
                    // if the current match ids are the same
                    if (custom_id == last_custom_id) {

                        // we need to change the custom id here, since there is a split, but the same custom id
                        var id = elem.getElementsByClassName('match_id')[0].innerText;
                        var new_custom_id = sha256(Date.now().toString());
                        db.collection('series').doc(series_name).collection('match_stats').doc(id).set({
                                custom_id: new_custom_id
                            })
                            .then(function () {
                                console.log("Document successfully written!");
                            })
                            .catch(function (error) {
                                console.error("Error writing document: ", error);
                            });
                    }
                }

                last_custom_id = custom_id;

            }

            last_elem_was_split = elem_is_split;
        }

    });

}