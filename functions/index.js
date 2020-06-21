const functions = require('firebase-functions');
const express = require('express');

// firestore
const admin = require('firebase-admin');
admin.initializeApp();
let db = admin.firestore();

const engines = require('consolidate');

const app = express();
app.engine('hbs', engines.handlebars);
app.set('views', './views');
app.set('view engine', 'hbs');

/*
app.get('/get_team_name_from_list', async (req, res) => {
    // get player list
    let player_list = req.query.player_list;
    if (!player_list) {
        res.sendStatus(400);
    }
    try {
        player_list = JSON.parse(player_list);
    } catch (SyntaxError) {
        res.sendStatus(400);
    }

    // get teams that the players are on
    teams = [];
    var playerPromises = [];
    let playersRef = db.collection('players');
    player_list.forEach(p => {
        console.log(p);
        // get the player in question from the db
        playerPromises.push(
            playersRef.get(p)
        );
    });

    Promise.all(playerPromises).then(doc => {
        console.log(doc.data());
        if (doc.exists) {
            teams.push(doc.data().team_name);
        }
    });

    console.log(teams);

    // find which team is the most likely
    counts = {}
    teams.forEach(t => {
        counts[t] = counts[t] ? counts[t] + 1 : 1;
    });
    // get the team with the max count
    team_name = Object.keys(counts).reduce((a, b) => {
        counts[a] > counts[b] ? a : b
    });
    likelihood = counts[team_name] / teams.length;

    // return the result
    likelihood = 0;
    res.json({
        'team_name': team_name,
        'likelihood': likelihood
    });
});
*/

app.get('/most_recent_match', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("match_data", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

app.get('/group_recent_matches', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;

    res.render("group_recent_matches", {
        client_name,
        custom_id,
        series_name
    });
});


exports.app = functions.https.onRequest(app);