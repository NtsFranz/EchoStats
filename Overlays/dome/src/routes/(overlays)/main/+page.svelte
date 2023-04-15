<script lang="ts">
	import MainBar from '$lib/components/MainBar.svelte';
	import { SparkWebsocket } from '$lib/js/spark_websocket.js';
	import type { Frame } from '$lib/js/Frame';
	import type { CameraTransform } from '$lib/js/CameraTransform';
	import type { Config } from '$lib/js/SparkConfig';
	import { onDestroy, onMount } from 'svelte';
	import DomeMinimap from '$lib/components/DomeMinimap.svelte';
	import LiveJoust from '$lib/components/LiveJoust.svelte';
	import FullScreenThreeRaw from '$lib/components/FullScreenThreeRaw.svelte';
	import DomeMinimapStatic from '$lib/components/DomeMinimapStatic.svelte';

	let config: typeof Config;
	let frame: Frame;
	let camera_transform: CameraTransform;

	let sw = new SparkWebsocket();
	let interval;
	onMount(() => {
		sw.subscribe('overlay_config', (data: typeof Config) => {
			config = data;
		});

		sw.subscribe('frame_30hz', (data: Frame) => {
			frame = data;
		});

		interval = setInterval(fetchWriteAPI, 16.6);
	});
	onDestroy(() => {
		sw.close();
		if (interval) clearInterval(interval);
	});

	function fetchWriteAPI() {
		fetch('http://localhost:6723/echovr/camera_transform')
			.then((resp) => resp.json())
			.then((resp) => (camera_transform = resp));
	}

	let defaultFrame = {
		disc: {
			position: [0.0, 0.0, 0.0],
			forward: [0.001, -0.001, 1.0],
			left: [1.0, 0.001, -0.001],
			up: [-0.001, 1.0, 0.001],
			velocity: [0.0, 0.0, 0.0],
			bounce_count: 0
		},
		orange_team_restart_request: 0,
		sessionid: '9F24AA5B-EE16-4C13-B571-E77BD70CCA63',
		game_clock_display: '04:59.05',
		game_status: 'playing',
		sessionip: '15.181.199.88',
		match_type: 'Echo_Arena',
		map_name: 'mpl_arena_a',
		right_shoulder_pressed2: 0.0,
		teams: [
			{
				players: [
					{
						name: 'Mashpatato',
						rhand: {
							pos: [-3.6820002, 1.4740001, -28.418001],
							forward: [0.64300001, 0.65500003, 0.39700001],
							left: [-0.11400001, 0.59400004, -0.79700005],
							up: [-0.75800002, 0.46700001, 0.45600003]
						},
						playerid: 0,
						userid: 3410666632343237,
						is_emote_playing: false,
						number: 77,
						level: 50,
						stunned: false,
						ping: 40,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [-3.6720002, 1.654, -28.440001],
							forward: [0.059000004, 0.091000006, 0.99400002],
							left: [0.99700004, 0.052000001, -0.064000003],
							up: [-0.058000002, 0.99400002, -0.088000007]
						},
						body: {
							position: [-3.6720002, 1.654, -28.440001],
							forward: [0.053000003, 0.0020000001, 0.99900007],
							left: [0.99900007, -0.001, -0.053000003],
							up: [0.001, 1.0, -0.0020000001]
						},
						holding_right: 'none',
						lhand: {
							pos: [-3.4360001, 0.86500007, -28.452002],
							forward: [0.59600002, -0.80200005, -0.019000001],
							left: [0.565, 0.43700001, -0.70000005],
							up: [0.57000005, 0.40700001, 0.71400005]
						},
						blocking: false,
						velocity: [1.3050001, -0.81000006, 17.014],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'GiggidyGao',
						rhand: {
							pos: [3.5720003, 0.96000004, -43.292004],
							forward: [-0.125, -0.78300005, 0.60900003],
							left: [0.83000004, -0.41900003, -0.36800003],
							up: [0.54300004, 0.46000001, 0.70200002]
						},
						playerid: 1,
						userid: 3631519736868913,
						is_emote_playing: false,
						number: 7,
						level: 50,
						stunned: false,
						ping: 51,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [3.8480003, 1.7240001, -43.215],
							forward: [-0.104, -0.20700002, 0.97300005],
							left: [0.98600006, -0.148, 0.074000001],
							up: [0.12900001, 0.96700007, 0.22000001]
						},
						body: {
							position: [3.8480003, 1.7240001, -43.215],
							forward: [-0.078000002, 0.001, 0.99700004],
							left: [0.99700004, -0.0020000001, 0.078000002],
							up: [0.0020000001, 1.0, -0.001]
						},
						holding_right: 'none',
						lhand: {
							pos: [3.9390001, 1.031, -43.116001],
							forward: [-0.63600004, -0.21700001, 0.74100006],
							left: [0.54500002, 0.55400002, 0.63000005],
							up: [-0.54700005, 0.80400002, -0.23400001]
						},
						blocking: false,
						velocity: [-0.58500004, -0.18000001, 9.9000006],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'Your_Sun',
						rhand: {
							pos: [-3.3610001, 0.93500006, -30.121002],
							forward: [0.95600003, -0.185, 0.22600001],
							left: [0.069000006, -0.60800004, -0.79100001],
							up: [0.28400001, 0.77200001, -0.56900001]
						},
						playerid: 6,
						userid: 3228978890541231,
						is_emote_playing: false,
						number: 0,
						level: 50,
						stunned: false,
						ping: 64,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [-3.3600001, 1.1860001, -30.360001],
							forward: [0.21200001, -0.11400001, 0.97100008],
							left: [0.97500002, -0.041000001, -0.21800001],
							up: [0.065000005, 0.99300003, 0.10300001]
						},
						body: {
							position: [-3.3600001, 1.1860001, -30.360001],
							forward: [0.12400001, -0.109, 0.98600006],
							left: [0.98900002, 0.1, -0.11300001],
							up: [-0.086000003, 0.98900002, 0.12]
						},
						holding_right: 'none',
						lhand: {
							pos: [-3.0330002, 0.59500003, -30.347002],
							forward: [0.90900004, -0.354, -0.22000001],
							left: [-0.23900001, -0.010000001, -0.97100008],
							up: [0.34100002, 0.93500006, -0.093000002]
						},
						blocking: false,
						velocity: [1.886, -0.76400006, 14.949],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'mkbf',
						rhand: {
							pos: [-3.4090002, 1.205, -27.397001],
							forward: [0.53600001, 0.551, 0.64000005],
							left: [0.59500003, 0.29200003, -0.74900001],
							up: [-0.59900004, 0.78200006, -0.17200001]
						},
						playerid: 7,
						userid: 5379083635501527,
						is_emote_playing: false,
						number: 8,
						level: 50,
						stunned: false,
						ping: 33,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [-3.4320002, 1.3690001, -27.826002],
							forward: [0.16800001, -0.010000001, 0.98600006],
							left: [0.98500007, -0.044000003, -0.16800001],
							up: [0.045000002, 0.99900007, 0.003]
						},
						body: {
							position: [-3.4320002, 1.3690001, -27.826002],
							forward: [0.13700001, 0.001, 0.99100006],
							left: [0.99100006, -0.0020000001, -0.13700001],
							up: [0.0020000001, 1.0, -0.001]
						},
						holding_right: 'none',
						lhand: {
							pos: [-3.1930001, 0.66700006, -27.731001],
							forward: [0.83700001, -0.51000005, 0.19900002],
							left: [0.42900002, 0.38500002, -0.81700003],
							up: [0.34, 0.76900005, 0.54100001]
						},
						blocking: false,
						velocity: [1.6200001, -0.81000006, 20.798],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					}
				],
				team: 'BLUE TEAM',
				possession: false,
				stats: {
					points: 0,
					possession_time: 0.0,
					interceptions: 0,
					blocks: 0,
					steals: 0,
					catches: 0,
					passes: 0,
					saves: 0,
					goals: 0,
					stuns: 0,
					assists: 0,
					shots_taken: 0
				}
			},
			{
				players: [
					{
						name: 'bandini02',
						rhand: {
							pos: [-3.7230003, 0.68800002, 32.252003],
							forward: [-0.049000002, 0.042000003, -0.99800003],
							left: [-0.99900007, -0.016000001, 0.048],
							up: [-0.014, 0.99900007, 0.043000001]
						},
						playerid: 2,
						userid: 3298023356907880,
						is_emote_playing: false,
						number: 0,
						level: 50,
						stunned: false,
						ping: 56,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [-3.8160002, 1.011, 32.75],
							forward: [0.061000004, -0.11000001, -0.99200004],
							left: [-0.99800003, 0.028000001, -0.064000003],
							up: [0.035, 0.99400002, -0.108]
						},
						body: {
							position: [-3.8160002, 1.011, 32.75],
							forward: [0.060000002, -0.001, -0.99800003],
							left: [-0.99800003, -0.0020000001, -0.060000002],
							up: [-0.001, 1.0, -0.001]
						},
						holding_right: 'none',
						lhand: {
							pos: [-3.8300002, 0.57700002, 32.332001],
							forward: [0.37100002, 0.034000002, -0.92800003],
							left: [-0.72500002, 0.63500005, -0.266],
							up: [0.58000004, 0.77200001, 0.26000002]
						},
						blocking: false,
						velocity: [0.62900001, 0.090000004, -11.493001],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'nighas',
						rhand: {
							pos: [-3.8170002, 0.75200003, 31.908001],
							forward: [-0.21000001, -0.133, -0.96900004],
							left: [-0.95000005, -0.20700002, 0.23400001],
							up: [-0.23200001, 0.96900004, -0.083000004]
						},
						playerid: 3,
						userid: 5732512190094328,
						is_emote_playing: false,
						number: 1,
						level: 44,
						stunned: false,
						ping: 44,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [-3.5540001, 0.91100007, 32.480003],
							forward: [0.056000002, -0.063000001, -0.99600005],
							left: [-0.98900002, 0.134, -0.064000003],
							up: [0.13800001, 0.98900002, -0.055000003]
						},
						body: {
							position: [-3.5540001, 0.91100007, 32.480003],
							forward: [0.043000001, -0.001, -0.99900007],
							left: [-0.99900007, -0.001, -0.043000001],
							up: [-0.001, 1.0, -0.001]
						},
						holding_right: 'none',
						lhand: {
							pos: [-3.6170001, 0.38100001, 32.335003],
							forward: [0.84200007, 0.034000002, -0.53800005],
							left: [-0.53400004, -0.087000005, -0.84100002],
							up: [-0.075000003, 0.99600005, -0.055000003]
						},
						blocking: false,
						velocity: [0.40500003, 0.49500003, -15.395],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'Papichulo1120',
						rhand: {
							pos: [4.6010003, 0.64300001, 46.018002],
							forward: [-0.28200001, 0.648, -0.70700002],
							left: [-0.76900005, -0.59300005, -0.23700002],
							up: [-0.57300001, 0.47700003, 0.66600001]
						},
						playerid: 4,
						userid: 3705441826161189,
						is_emote_playing: false,
						number: 69,
						level: 50,
						stunned: false,
						ping: 47,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [4.73, 0.96000004, 46.513],
							forward: [-0.28100002, 0.15400001, -0.94700003],
							left: [-0.95600003, 0.042000003, 0.29100001],
							up: [0.084000006, 0.98700005, 0.13500001]
						},
						body: {
							position: [4.73, 0.96000004, 46.513],
							forward: [-0.22100002, -0.001, -0.97500002],
							left: [-0.97500002, -0.0020000001, 0.22100002],
							up: [-0.0020000001, 1.0, -0.001]
						},
						holding_right: 'none',
						lhand: {
							pos: [4.4430003, 0.60900003, 46.450001],
							forward: [-0.51900005, 0.81600004, -0.25500003],
							left: [-0.31600001, 0.094000004, 0.94400007],
							up: [0.79400003, 0.57000005, 0.21000001]
						},
						blocking: false,
						velocity: [-0.67500001, 0.81100005, -3.4230001],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'EdAtac',
						rhand: {
							pos: [4.0310001, 0.89700001, 43.880001],
							forward: [-0.60500002, 0.60300004, -0.52100003],
							left: [-0.12900001, 0.57100004, 0.81000006],
							up: [0.78600001, 0.55700004, -0.26800001]
						},
						playerid: 5,
						userid: 4595613807205227,
						is_emote_playing: false,
						number: 1,
						level: 50,
						stunned: false,
						ping: 76,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [4.0320001, 1.0730001, 44.173],
							forward: [-0.060000002, -0.047000002, -0.99700004],
							left: [-0.99800003, 0.0, 0.060000002],
							up: [-0.003, 0.99900007, -0.047000002]
						},
						body: {
							position: [4.0320001, 1.0730001, 44.173],
							forward: [-0.061000004, -0.0020000001, -0.99800003],
							left: [-0.99800003, -0.001, 0.061000004],
							up: [-0.001, 1.0, -0.0020000001]
						},
						holding_right: 'none',
						lhand: {
							pos: [4.0170002, 0.62900001, 44.049004],
							forward: [-0.090000004, -0.001, -0.99600005],
							left: [-0.99600005, 0.0070000002, 0.090000004],
							up: [0.0070000002, 1.0, -0.0020000001]
						},
						blocking: false,
						velocity: [0.0, 0.0, -4.9970002],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					}
				],
				team: 'ORANGE TEAM',
				possession: false,
				stats: {
					points: 0,
					possession_time: 0.0,
					interceptions: 0,
					blocks: 0,
					steals: 0,
					catches: 0,
					passes: 0,
					saves: 0,
					goals: 0,
					stuns: 0,
					assists: 0,
					shots_taken: 0
				}
			},
			{
				players: [
					{
						name: 'anonymous',
						rhand: {
							pos: [-4.25, 0.0, -9.6200008],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						playerid: 12,
						userid: 1095645014069982721,
						is_emote_playing: false,
						number: 1,
						level: 1,
						stunned: false,
						ping: 40,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [-4.0, 0.0, -10.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						body: {
							position: [-4.0, 0.0, -10.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						holding_right: 'none',
						lhand: {
							pos: [-3.7500002, -0.25, -10.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						blocking: false,
						velocity: [0.0, 0.0, 0.0],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: '6475616c67616d650a',
						rhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						playerid: 8,
						userid: 2410975075615485,
						is_emote_playing: false,
						number: 1,
						level: 3,
						stunned: false,
						ping: 87,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						body: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						holding_right: 'none',
						lhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						blocking: false,
						velocity: [0.0, 0.0, 0.0],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'www.ignitevr.gg',
						rhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						playerid: 9,
						userid: 2540488886071982,
						is_emote_playing: false,
						number: 0,
						level: 1,
						stunned: false,
						ping: 60,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						body: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						holding_right: 'none',
						lhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						blocking: false,
						velocity: [0.0, 0.0, 0.0],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'Virtex_Bot',
						rhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						playerid: 10,
						userid: 3468933396486405,
						is_emote_playing: false,
						number: 0,
						level: 1,
						stunned: false,
						ping: 124,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						body: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						holding_right: 'none',
						lhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						blocking: false,
						velocity: [0.0, 0.0, 0.0],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					},
					{
						name: 'enterthedome.com',
						rhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						playerid: 11,
						userid: 8059404087464094,
						is_emote_playing: false,
						number: 1,
						level: 1,
						stunned: false,
						ping: 69,
						packetlossratio: 0.0,
						invulnerable: false,
						holding_left: 'none',
						possession: false,
						head: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						body: {
							position: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						holding_right: 'none',
						lhand: {
							pos: [0.0, 0.0, 0.0],
							forward: [0.0, 0.0, 1.0],
							left: [1.0, 0.0, 0.0],
							up: [0.0, 1.0, 0.0]
						},
						blocking: false,
						velocity: [0.0, 0.0, 0.0],
						stats: {
							possession_time: 0.0,
							points: 0,
							saves: 0,
							goals: 0,
							stuns: 0,
							passes: 0,
							catches: 0,
							steals: 0,
							blocks: 0,
							interceptions: 0,
							assists: 0,
							shots_taken: 0
						}
					}
				],
				team: 'SPECTATORS',
				possession: false,
				stats: {
					points: 0,
					possession_time: 0.0,
					interceptions: 0,
					blocks: 0,
					steals: 0,
					catches: 0,
					passes: 0,
					saves: 0,
					goals: 0,
					stuns: 0,
					assists: 0,
					shots_taken: 0
				}
			}
		],
		blue_round_score: 0,
		orange_points: 0,
		player: {
			vr_left: [-0.99900007, 0.0, -0.049000002],
			vr_position: [-4.211, 1.3010001, 40.609001],
			vr_forward: [0.049000002, -0.001, -0.99900007],
			vr_up: [0.0, 1.0, -0.001]
		},
		private_match: false,
		blue_team_restart_request: 0,
		tournament_match: false,
		orange_round_score: 0,
		rules_changed_by: '[INVALID]',
		total_round_count: 1,
		left_shoulder_pressed2: 0.0,
		left_shoulder_pressed: 0.0,
		pause: {
			paused_state: 'unpaused',
			unpaused_team: 'none',
			paused_requested_team: 'none',
			unpaused_timer: 0.0,
			paused_timer: 0.0
		},
		right_shoulder_pressed: 0.0,
		blue_points: 0,
		last_throw: {
			arm_speed: 0.0,
			total_speed: 0.0,
			off_axis_spin_deg: 0.0,
			wrist_throw_penalty: 0.0,
			rot_per_sec: 0.0,
			pot_speed_from_rot: 0.0,
			speed_from_arm: 0.0,
			speed_from_movement: 0.0,
			speed_from_wrist: 0.0,
			wrist_align_to_throw_deg: 0.0,
			throw_align_to_movement_deg: 0.0,
			off_axis_penalty: 0.0,
			throw_move_penalty: 0.0
		},
		client_name: 'anonymous',
		game_clock: 299.05121,
		possession: [-1, -1],
		last_score: {
			disc_speed: 0.0,
			team: 'orange',
			goal_type: '[NO GOAL]',
			point_amount: 0,
			distance_thrown: 0.0,
			person_scored: '[INVALID]',
			assist_scored: '[INVALID]'
		},
		rules_changed_at: 0,
		err_code: 0
	};
</script>

<svelte:head>
	<title>Main Overlay</title>
</svelte:head>
<!-- 
<div style="position: absolute; bottom: 0rem; left: 5rem;height: 25rem;">
	<PlayerListOrange frame={defaultFrame} />
</div>

<div style="position: absolute; bottom: 0rem; right: 12rem;height: 25rem;">
	<PlayerListBlue frame={defaultFrame} />
</div> -->

<FullScreenThreeRaw
	free_cam_fov={config?.['caster_prefs']['free_cam_fov'] ?? 50}
	{frame}
	{camera_transform}
/>

<LiveJoust {frame} teamIndex={1} color={'#ffa500'} />
<LiveJoust {frame} teamIndex={0} color={'#0095ff'} />

<MainBar {frame} {config} />

<div
	style="margin: auto; bottom: 0; right: 0; position: absolute; width: 30%; overflow: hidden; border: 0 solid #fff6; border-radius: 1em 0 0 0;"
>
	<div id="goals3DMap" style="height: 20em; position: relative;">
		<DomeMinimapStatic {frame} {camera_transform} />
	</div>
</div>
