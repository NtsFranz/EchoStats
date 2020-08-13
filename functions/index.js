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

app.get('/prematch_overlay', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("prematch_overlay", {
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

app.get('/casterdesk', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;
    const live = req.query.live || true;   // live by default

    res.render("casterdesk", {
        client_name,
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