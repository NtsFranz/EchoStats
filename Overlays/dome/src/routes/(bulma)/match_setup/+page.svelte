<script lang="ts">
	import { SparkWebsocket } from '$lib/js/spark_websocket.js';
	import { onDestroy, onMount } from 'svelte';
	import { Config } from '$lib/js/SparkConfig';

	let teamLogosDict = {};
	let casterLogosDict = {};

	let alt_team_inputs = [];
	let team_inputs = [];
	let caster_inputs = [];

	let upcomingMatchExpanded = false;

	let config: Config = Object.assign({}, Config);

	let sw = new SparkWebsocket();

	let isLoading = true;
	let dirty = false;

	onMount(() => {
		fetch('https://api.ignitevr.gg/dome/get_team_list')
			.then((r) => r.text())
			.then((r) => {
				autocompleteTeamInputs(r);
			});
		sw.subscribe('overlay_config', (data: typeof config) => {
			// merge the objects so that we retain default values from the definition
			let newConfig = {
				...config,
				...data
			};

			// deep merge
			newConfig['caster_prefs'] = {
				...config['caster_prefs'],
				...data['caster_prefs']
			};

			config = newConfig;

			console.log(config);

			autocompleteCasterInputs();

			isLoading = false;
		});
	});

	onDestroy(() => sw.close());

	function post(url: string, data: object) {
		fetch(url, {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	function swapSides() {
		isLoading = true;
		fetch('http://localhost:6724/api/set_team_details/orange', {
			method: 'POST',
			body: JSON.stringify({
				team_logo: config['teams'][0]['team_logo'],
				team_name: config['teams'][0]['team_name']
			})
		});

		fetch('http://localhost:6724/api/set_team_details/blue', {
			method: 'POST',
			body: JSON.stringify({
				team_logo: config['teams'][1]['team_logo'],
				team_name: config['teams'][1]['team_name']
			})
		});
	}

	function swapSidesAlt() {
		isLoading = true;

		let temp_name = config['caster_prefs']['alt_orange_team_name'];
		let temp_logo = config['caster_prefs']['alt_orange_team_logo'];

		config['caster_prefs']['alt_orange_team_name'] = config['caster_prefs']['alt_blue_team_name'];
		config['caster_prefs']['alt_orange_team_logo'] = config['caster_prefs']['alt_blue_team_logo'];

		config['caster_prefs']['alt_blue_team_name'] = temp_name;
		config['caster_prefs']['alt_blue_team_logo'] = temp_logo;

		post('http://localhost:6724/api/set_caster_prefs', config['caster_prefs']);
	}

	function setTeamNamesSource(checked: boolean) {
		post('http://localhost:6724/api/set_team_names_source/' + (checked ? '1' : '0'), '{}');
	}

	function sendAllToSpark() {
		post('http://localhost:6724/api/set_team_details/blue', {
			team_logo: config['teams'][0]['team_logo'],
			team_name: config['teams'][0]['team_name']
		});

		post('http://localhost:6724/api/set_team_details/orange', {
			team_logo: config['teams'][1]['team_logo'],
			team_name: config['teams'][1]['team_name']
		});

		post(
			'http://localhost:6724/api/set_team_names_source/' +
				(config['team_names_source'] ? '1' : '0'),
			'{}'
		);

		// caster prefs
		post('http://localhost:6724/api/set_caster_prefs', config['caster_prefs']);

		// round scores
		config['round_scores']['round_scores_manual'] = config['round_scores']['manual_round_scores'];
		post('http://localhost:6724/api/set_round_scores', config['round_scores']);

		dirty = false;
	}

	let timeout: ReturnType<typeof setTimeout> | null = null;

	function manualValueChanged() {
		if (timeout != null) clearTimeout(timeout);

		// Make a new timeout set to go off in 2000ms (2 seconds)
		timeout = setTimeout(sendAllToSpark, 2000);
	}

	function autocompleteTeamInputs(data: string) {
		let parsed = JSON.parse(data);
		let teams: string[] = [];

		parsed.forEach((t: any) => {
			teams.push(t['teamName']);
			teamLogosDict[t['teamName']] = t['teamLogo'];
		});

		team_inputs.forEach((e) => {
			autocomplete(e, teams, 0, teamAutocompleteFinished);
		});
		alt_team_inputs.forEach((e) => {
			autocomplete(e, teams, 0, altTeamAutocompleteFinished);
		});
	}

	function teamAutocompleteFinished(inputElement) {
		if (inputElement.classList.contains('team_name_input_orange')) {
			post('http://localhost:6724/api/set_team_details/orange', {
				team_name: inputElement.value,
				team_logo: teamLogosDict[inputElement.value]
			});
		} else if (inputElement.classList.contains('team_name_input_blue')) {
			post('http://localhost:6724/api/set_team_details/blue', {
				team_name: inputElement.value,
				team_logo: teamLogosDict[inputElement.value]
			});
		}
	}

	function altTeamAutocompleteFinished(inputElement) {
		if (inputElement.classList.contains('team_name_input_orange')) {
			config['caster_prefs']['alt_orange_team_name'] = inputElement.value;
			config['caster_prefs']['alt_orange_team_logo'] = teamLogosDict[inputElement.value];
		} else if (inputElement.classList.contains('team_name_input_blue')) {
			config['caster_prefs']['alt_blue_team_name'] = inputElement.value;
			config['caster_prefs']['alt_blue_team_logo'] = teamLogosDict[inputElement.value];
		}
		post('http://localhost:6724/api/set_caster_prefs', config['caster_prefs']);
	}

	let casterNames: string[] = [];
	fetch('http://localhost:6724/api/vrml_api/echoarena/casters')
		.then((r) => r.json())
		.then((parsed) => {
			casterNames = [];

			parsed.forEach((t) => {
				casterNames.push(t['name']);
				casterLogosDict[t['name']] = 'https://vrmasterleague.com' + t['logo'];
			});

			autocompleteCasterInputs();
		});

	function autocompleteCasterInputs() {
		caster_inputs.forEach((e) => {
			autocomplete(e, casterNames, 0, (elem) => {
				let index = e.id.match(/caster_(\d+)_name_input/);
				let postData = {};
				postData[`caster_${index[1]}_name`] = elem.value;
				postData[`caster_${index[1]}_img`] = casterLogosDict[elem.value];
				post('http://localhost:6724/api/set_caster_prefs', postData);
			});
		});
	}

	function timeDifference(comparison, now) {
		let msPerMinute = 60 * 1000;
		let msPerHour = msPerMinute * 60;
		let msPerDay = msPerHour * 24;
		let msPerMonth = msPerDay * 30;
		let msPerYear = msPerDay * 365;

		let elapsed = comparison - now;

		if (elapsed < -msPerMinute) {
			return Math.round(-elapsed / msPerMinute) + ' minutes ago';
		}

		if (elapsed < 0) {
			return Math.round(-elapsed / 1000) + ' seconds ago';
		}

		if (elapsed < msPerMinute) {
			return Math.round(elapsed / 1000) + ' seconds';
		} else if (elapsed < msPerHour) {
			return Math.round(elapsed / msPerMinute) + ' minutes';
		} else if (elapsed < msPerDay) {
			return Math.round(elapsed / msPerHour) + ' hours';
		} else if (elapsed < msPerMonth) {
			return Math.round(elapsed / msPerDay) + ' days';
		} else if (elapsed < msPerYear) {
			return Math.round(elapsed / msPerMonth) + ' months';
		} else {
			return Math.round(elapsed / msPerYear) + ' years';
		}
	}
</script>

<svelte:head>
	<title>Match Setup</title>
	<link rel="stylesheet" href="http://localhost:6724/css/lib/bulma.min.css" />
	<link rel="stylesheet" href="http://localhost:6724/css/styles.css" />

	<link rel="stylesheet" type="text/css" href="http://localhost:6724/css/autocomplete_styles.css" />
	<script type="text/javascript" src="http://localhost:6724/js/autocomplete.js"></script>
</svelte:head>

<section class="hero is-medium">
	<div class="hero-body" style="background-color: #0003;padding: 4rem 1.5rem;; overflow: hidden;">
		<div class="container has-text-centered">
			<h2 class="title is-1">Match Setup</h2>
			<img class="ignite_background_logo" src="http://localhost:6724/img/ignite_logo.png" alt="" />
			<p class="subtitle" style="font-size: 1.2em;">Enter custom team names and logos here.</p>
		</div>
	</div>
</section>
<div class="content">
	<div class="box match_setup_flex" style="position: relative; top: -2em;font-size: 1.5em;">
		<nav class="breadcrumb" aria-label="breadcrumbs" style="position: absolute; top: -5em;">
			<ul>
				<li><a href="https://localhost:6724/">Home</a></li>
				<li><a href="/dome">DOME</a></li>
				<li class="is-active"><a href="#" aria-current="page">Match Setup</a></li>
			</ul>
		</nav>

		<div class="card internal">
			<span class="tag is-black">Teams</span>
			<table class="match_selection_table manual_input">
				<tbody>
					<tr>
						<td>
							<img
								class="team_logo_img team_logo_orange"
								src={config['teams'][1]['team_logo']}
								alt=""
								style="float:right;"
							/>
						</td>

						<td>
							Team Name:
							<form on:submit|preventDefault class="custom_team_input_form">
								<input
									autocomplete="off"
									type="text"
									bind:this={team_inputs[0]}
									class="input orange team_name_input_orange team_input force_visible"
									bind:value={config['teams'][1]['team_name']}
									on:change={manualValueChanged}
								/>
							</form>
							<div class="small_br" />
							Logo URL:<br />
							<input
								class="input orange logo_url_input team_logo_input_orange"
								bind:value={config['teams'][1]['team_logo']}
								on:change={manualValueChanged}
							/>
						</td>

						<td style="padding: 3em 0;">
							<div
								class="button is-dark"
								id="swap_sides_button"
								style="margin: auto; display: block; max-width: 4em;"
								class:is-loading={isLoading}
								on:click={swapSides}
							>
								<img
									src="http://localhost:6724/img/swap-horizontal-bold.png"
									style="height: 1.5em;"
									alt="swap sides button"
								/>
							</div>
						</td>

						<td>
							Team Name:
							<form on:submit|preventDefault class="custom_team_input_form">
								<input
									autocomplete="off"
									type="text"
									bind:this={team_inputs[1]}
									class="input blue team_name_input_blue team_input force_visible"
									style="text-align: right;"
									bind:value={config['teams'][0]['team_name']}
									on:change={manualValueChanged}
								/>
							</form>
							<div class="small_br" />
							Logo URL:<br />
							<input
								class="input blue logo_url_input team_logo_input_blue"
								bind:value={config['teams'][0]['team_logo']}
								on:change={manualValueChanged}
							/>
						</td>

						<td>
							<img
								class="team_logo_img team_logo_blue"
								src={config['teams'][0]['team_logo']}
								alt=""
								style="float:left;"
							/>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<!-- Upcoming Match Teams -->
		<div class="card internal">
			<a href="#" on:click={() => (upcomingMatchExpanded = !upcomingMatchExpanded)}
				><span class="tag is-black">Upcoming Match Teams +</span></a
			>
			<div class="collapsible" class:collapsed={!upcomingMatchExpanded}>
				<table>
					<tbody>
						<tr>
							<td>
								<img
									class="team_logo_img team_logo_orange"
									src={config['caster_prefs']['alt_orange_team_logo']}
									alt=""
									style="float:right;"
								/>
							</td>

							<td>
								Team Name:
								<form on:submit|preventDefault class="custom_team_input_form">
									<input
										autocomplete="off"
										type="text"
										bind:this={alt_team_inputs[0]}
										class="input orange team_name_input_orange alt_team_input force_visible"
										bind:value={config['caster_prefs']['alt_orange_team_name']}
										on:change={manualValueChanged}
									/>
								</form>
								<div class="small_br" />
								Logo URL:<br />
								<input
									class="input orange logo_url_input team_logo_input_orange"
									bind:value={config['caster_prefs']['alt_orange_team_logo']}
									on:change={manualValueChanged}
								/>
							</td>

							<td style="padding: 3em 0;">
								<div
									class="button is-dark"
									style="margin: auto; display: block; max-width: 4em;"
									class:is-loading={isLoading}
									on:click={swapSidesAlt}
								>
									<img
										src="http://localhost:6724/img/swap-horizontal-bold.png"
										style="height: 1.5em;"
										alt="swap sides button"
									/>
								</div>
							</td>

							<td>
								Team Name:
								<form on:submit|preventDefault class="custom_team_input_form">
									<input
										autocomplete="off"
										type="text"
										bind:this={alt_team_inputs[1]}
										class="input blue team_name_input_blue alt_team_input force_visible"
										style="text-align: right;"
										bind:value={config['caster_prefs']['alt_blue_team_name']}
										on:change={manualValueChanged}
									/>
								</form>
								<div class="small_br" />
								Logo URL:<br />
								<input
									class="input blue logo_url_input team_logo_input_blue"
									bind:value={config['caster_prefs']['alt_blue_team_logo']}
									on:change={manualValueChanged}
								/>
							</td>

							<td>
								<img
									class="team_logo_img team_logo_blue"
									src={config['caster_prefs']['alt_blue_team_logo']}
									alt=""
									style="float:left;"
								/>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<!-- Casters -->
		<div class="card internal">
			<span class="tag is-black">Casters</span>
			<label for="num_casters_input">Num Casters:</label>
			<input
				id="num_casters_input"
				autocomplete="off"
				type="number"
				class="input"
				min="0"
				bind:value={config['caster_prefs']['num_casters']}
				style="max-width: 8em;"
				on:change={manualValueChanged}
			/>

			<table class="caster_selection_table">
				<thead>
					<tr class="match_group_item">
						{#each { length: config['caster_prefs']['num_casters'] } as _, i}
							<th>Caster {i + 1}</th>
						{/each}
					</tr>
				</thead>
				<tbody>
					<tr>
						{#each { length: config['caster_prefs']['num_casters'] } as _, i}
							<td>
								Name:
								<form on:submit|preventDefault class="custom_team_input_form">
									<input
										autocomplete="off"
										type="text"
										bind:this={caster_inputs[i]}
										class="input caster_input force_visible"
										id={`caster_${i}_name_input`}
										bind:value={config['caster_prefs'][`caster_${i}_name`]}
										on:keyup={manualValueChanged}
									/>
								</form>
								<br />
								Logo URL:<br />
								<input
									class="input logo_url_input"
									bind:value={config['caster_prefs'][`caster_${i}_img`]}
									on:keyup={manualValueChanged}
								/>
								<img class="caster_img" alt="" src={config['caster_prefs'][`caster_${i}_img`]} />
								<br />
								VDO.Ninja URL:<br />
								<input
									class="input"
									bind:value={config['caster_prefs'][`caster_${i}_vdo`]}
									on:keyup={manualValueChanged}
								/>
							</td>
						{/each}
					</tr>
				</tbody>
			</table>
		</div>

		<div class="card internal" style="max-width: 25em;">
			<span class="tag is-black">Round Scores</span>
			<form id="score_selection_form">
				<table class="score_selection_table">
					<thead>
						<tr class="match_group_item">
							<th class="" colspan="3">
								<label class="checkbox" style="margin-left: 3em;">
									<input
										bind:checked={config['round_scores']['manual_round_scores']}
										type="checkbox"
										on:change={sendAllToSpark}
									/>
									Use Manual Round Scores
								</label>
							</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>
								<fieldset
									class="round_count_dropdown_fieldset"
									disabled={!config['round_scores']['manual_round_scores']}
								/>
							</td>
							<td>
								<fieldset class="score_inputs">
									<table>
										<thead>
											<tr>
												<th>
													<label for="round_count_input">Round Count:</label>
													<br />
													<input
														id="round_count_input"
														autocomplete="off"
														type="number"
														class="input"
														min="1"
														max="12"
														bind:value={config['round_scores']['round_count']}
														style="max-width: 8em;"
														on:change={manualValueChanged}
													/>
												</th>
												<th>Orange</th>
												<th>Blue</th>
											</tr>
										</thead>
										{#each { length: config['round_scores']['round_count'] } as _, i}
											<tr>
												<td>Round {i + 1}:</td>
												<td>
													<input
														autocomplete="off"
														type="number"
														class="input score_input orange"
														bind:value={config['round_scores']['round_scores_orange'][i]}
														on:input={manualValueChanged}
													/>
												</td>
												<td>
													<input
														autocomplete="off"
														type="number"
														class="input score_input blue"
														bind:value={config['round_scores']['round_scores_blue'][i]}
														on:input={manualValueChanged}
													/>
												</td>
											</tr>
										{/each}
									</table>
								</fieldset>
							</td>
						</tr>
					</tbody>
				</table>
			</form>
		</div>

		<div class="card internal">
			<span class="tag is-black">Settings</span>
			<form id="overlay_settings_form">
				<table>
					<tr>
						<th>Overlay Settings</th>
					</tr>
					<tr>
						<td>
							<label class="checkbox" style="margin-left: 3em;">
								<input
									bind:checked={config['caster_prefs']['show_upcoming_match']}
									type="checkbox"
									on:change={sendAllToSpark}
								/>
								Show upcoming match (waiting page)
							</label>
						</td>
					</tr>
					<tr>
						<td>
							<label class="checkbox" style="margin-left: 3em;">
								<input
									bind:checked={config['caster_prefs']['show_echo_unit']}
									type="checkbox"
									on:change={sendAllToSpark}
								/>
								Show Echo Unit (waiting page)
							</label>
						</td>
					</tr>
					<tr>
						<td>
							<label class="checkbox" style="margin-left: 3em;">
								<input
									bind:value={config['caster_prefs']['free_cam_fov']}
									type="range"
									min="50"
									max="100"
									on:mouseup={sendAllToSpark}
								/>
								{config['caster_prefs']['free_cam_fov']}deg Free Cam FOV
							</label>
						</td>
					</tr>
				</table>
			</form>
		</div>

		<div class="card internal">
			<span class="tag is-black">Match Info</span>
			<form>
				<table>
					<tr>
						<td>
							<label>
								Waiting Message
								<input
									class="input"
									bind:value={config['caster_prefs']['waiting_message']}
									on:change={manualValueChanged}
								/>
							</label>
						</td>
					</tr>
					<tr>
						<td>
							<label>
								Replay Viewer Screen VDO Ninja Code
								<input
									class="input"
									bind:value={config['caster_prefs']['remote_screen_1']}
									on:change={manualValueChanged}
								/>
							</label>
						</td>
					</tr>
				</table>
			</form>
		</div>
	</div>
	<!-- end of match_setup_flex -->
</div>

<style>
	.match_setup_flex {
		max-width: 80em;
		margin: auto;
		display: flex;
		flex-wrap: wrap;
	}
</style>
