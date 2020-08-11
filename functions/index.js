const functions = require('firebase-functions');
const express = require('express');
const https = require('https');

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
app.get('/prematch_overlay', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("match_data_prematch", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

app.get('/midmatch_overlay', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;
    const show_on_load = req.query.show_on_load || false;

    res.render("midmatch_overlay", {
        client_name,
        custom_id,
        series_name,
        live,
        show_on_load
    });
});

app.get('/live_events_overlay', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const show_on_load = req.query.show_on_load || false;

    res.render("live_events_overlay", {
        client_name,
        custom_id,
        series_name,
        show_on_load
    });
});


app.get('/prematch_overlay_2', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("prematch_overlay_2", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

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

app.get('/all_recent_matches', (req, res) => {
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("all_recent_matches", {
        series_name,
        live
    });
});

app.get('/fastest_jousts', (req, res) => {
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("fastest_jousts", {
        series_name,
        live
    });
});

app.get('/match_setup', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    
    res.render("match_setup", {
        client_name,
        custom_id,
        series_name
    });
});

app.get('/get_upcoming_matches', (req, res) => {
    https.get("https://vrmasterleague.com/Services.asmx/GetMatchesThisWeek?game=echoarena&max=100", (resp) => {
        let data = '';

        // A chunk of data has been recieved.
        resp.on('data', (chunk) => {
            data += chunk;
        });

        // The whole response has been received. Print out the result.
        resp.on('end', () => {
            res.send(JSON.parse(data));
        });

    }).on("error", (err) => {
        console.log("Error: " + err.message);
        res.send(err.message);
    });
});

exports.app = functions.https.onRequest(app);