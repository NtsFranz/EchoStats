<svelte:head>
	<link rel="stylesheet" href="http://localhost:6724/css/styles.css">

	<link rel="stylesheet" type="text/css" href="http://localhost:6724/css/autocomplete_styles.css">
	<script type="text/javascript" src="http://localhost:6724/js/autocomplete.js"></script>

	<script src="http://localhost:6724/js/util.js"></script>
	<script src="http://localhost:6724/js/fetch_utils.js"></script>
</svelte:head>

<script>
    import 'bulma';
</script>

<style global>

    body {
        font-family: 'Inconsolata', monospace;
    }

    h1 {
        font-size: 2em;
    }

    .content {
        margin: 0 10em;
    }

    .content ul li {
        list-style: none;
        margin-top: 2em;
    }

    .checkbox_grid {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
    }

    .ignite_background_logo {
        float: left;
        width: 10em;
        position: absolute;
        left: 10em;
        bottom: 0;
        opacity: .1;
        transform: scale(6);
        z-index: -1;
    }

    .match_setup_flex {
        max-width: 80em;
        margin: auto;
        display: flex;
        flex-wrap: wrap;
    }

    .match_setup_flex > div {
        flex-grow: 1;
        margin: 0 1em;
    }

    @media (max-width: 2100px) {
        .content {
            margin: 0 1em;
        }
    }

    .team_logo_img {
        width: 7.8em;
    }

    input {
        font-size: .8em;
    }

    .blur-in-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 50%;
        height: 100%;
        /*  transform: scale(10);  */
        filter: blur(1em);
        opacity: 0;
        transition: opacity 1s;
    }

    .blur-in-background[src=""] {
        opacity: .3 !important;
    }

    #swap_sides_button.is-loading img {
        opacity: 0;
    }


    .orange.input,
    .orange.textarea {
        border-color: #d18100
    }

    .orange.input:active,
    .orange.input:focus,
    .orange.is-active.input,
    .orange.is-active.textarea,
    .orange.is-focused.input,
    .orange.is-focused.textarea,
    .orange.textarea:active,
    .orange.textarea:focus {
        box-shadow: 0 0 0 .125em rgba(209, 84, 0, 0.25)
    }

    .blue.input,
    .blue.textarea {
        border-color: #0073d1
    }

    .blue.input:active,
    .blue.input:focus,
    .blue.is-active.input,
    .blue.is-active.textarea,
    .blue.is-focused.input,
    .blue.is-focused.textarea,
    .blue.textarea:active,
    .blue.textarea:focus {
        box-shadow: 0 0 0 .125em rgba(0, 63, 209, 0.25)
    }

    .hide {
        display: none !important;
    }

    .caster_img {
        display: block;
        width: 5em;
        margin: 1em auto;
    }

    .score_inputs {
        display: flex;
        flex-direction: column;
        width: fit-content;
    }

    .score_input {
        max-width: 7em;
    }

    #upcoming_matches_body img {
        height: 3em;
        max-width: unset;
    }

    #upcoming_matches_body td {
        padding: 0 .6em;
    }


    #upcoming_matches_body tr:hover {
        background-color: #0001;
        cursor: pointer;
    }


    .content ul li {
        list-style: none;
        margin-top: 2em;
    }

    .card.internal {
        padding: 1em;
        margin: 1em;
        border: 1px solid #0002;
    }

    .card.internal .tag {
        position: absolute;
        top: -2em;
        left: 0;
    }

    .collapsible {
        transition: all .1s;
        height: 9em;
        overflow: hidden;
        opacity: 1;
    }

    .collapsed {
        height: 0;
        margin: -1em;
        opacity: 0;
    }

    div.small_br {
        height: .5em;
    }
</style>

<slot/>