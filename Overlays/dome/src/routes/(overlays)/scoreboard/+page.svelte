<script lang="ts">
	import { SparkWebsocket } from '$lib/js/spark_websocket.js';
	import { onDestroy, onMount } from 'svelte';
	import { InfoBar, Button } from 'fluent-svelte';
	import RandomBackgroundImage from '$lib/components/RandomBackgroundImage.svelte';
	import UpcomingMatch from '$lib/components/UpcomingMatch.svelte';
	import Webcams from '$lib/components/Webcams.svelte';
	import Branding from '$lib/components/Branding.svelte';
	import type { Config } from '$lib/js/SparkConfig';

	let config: typeof Config;

	let sw = new SparkWebsocket();
	onMount(() => {
		sw.subscribe('overlay_config', (data: typeof Config) => {
			config = data;
		});
	});
	onDestroy(() => {
		sw.close();
	});
</script>

<svelte:head>
	<title>Waiting Overlay</title>
</svelte:head>

<div class="centered">
	<RandomBackgroundImage interval={10} />
	<div style="width: 10rem; margin: auto; position: relative; top: -3rem; left: 8rem;">
		<div style="position: relative; width: 100%; aspect-ratio : 1.3 / 1; margin: auto;">
			<img
				src="/dome/dome_logo.webp"
				style="width: 100%; position: absolute; top: 0; left: 0; filter: brightness(0) blur(3rem); opacity: 1;"
				alt=""
			/>
			<img
				src="/dome/dome_logo.webp"
				style="width: 100%; position: absolute; top: 0; left: 0;"
				alt=""
			/>
		</div>
		<h1 class="title">DOME</h1>
	</div>
</div>
<iframe class="scoreboard" style="width:100%;height:100%;" src="http://localhost:6724/scoreboard" />
<div class="round_scores">
	<p>Round Scores</p>
	{#each { length: config?.['round_scores']?.['round_count'] ?? 0 } as _, i}
		<div>
			<div>{config?.['round_scores']?.['round_scores_orange'][i] ?? ''}</div>
			<div>{config?.['round_scores']?.['round_scores_blue'][i] ?? ''}</div>
		</div>
	{/each}
</div>

<div class="team_logos">
	<img src={config?.['teams'][1]['team_logo']} alt="" />
	<img src={config?.['teams'][0]['team_logo']} alt="" />
</div>
<div class="branding">
	<Branding />
</div>

<div class="webcams">
	<Webcams {config} vertical={true} />
</div>

<style type="text/scss">
	@font-face {
		font-family: 'Conthrax';
		src: url('/dome/fonts/conthrax-sb.ttf') format('truetype');
	}

	:global(body) {
		background-color: black;
	}
	.centered {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100vh;
		color: white;
		font-family: 'Conthrax', 'Anton', sans-serif;
		text-align: center;
		font-size: 2em;
		opacity: 0;
		animation: fade_in 2s 1s forwards;
	}

	.title {
		font-family: 'Conthrax', 'Anton', sans-serif;
		color: #c5c8d4;
		text-shadow: 0 0 0.4em #0008;
		font-weight: 900;
		letter-spacing: 0.2rem;
		font-size: 2.3rem;
		opacity: 1;
		transform: scaleX(1);
		margin-top: 0;
		width: 100%;
		text-align: center;
	}

	.scoreboard {
		position: absolute;
		z-index: 10;
		top: 13rem;
		left: 5rem;
		width: 55rem;
		height: 50rem;
		opacity: 0;
		animation: fade_in 2s 1s forwards;
		overflow: hidden;
		border: none;
	}

	.team_logos {
		position: absolute;
		z-index: 10;
		bottom: 5rem;
		left: 6rem;
		display:flex;
		flex-direction: row;
		gap: 19rem;
		img {
			width: 12rem;
			height: 12rem;
		}
	}

	.branding {
		position: absolute;
		z-index: 10;
		top: -12rem;
		left: 3rem;
	}

	.webcams {
		position: absolute;
		z-index: 10;
		top: 3rem;
		right: 5rem;
		opacity: 0;
		animation: fade_in 2s 1s forwards;
	}

	.round_scores {
		position: absolute;
		top: 52rem;
		left: 23rem;
		font-size: 1.5rem;
		color: white;
		font-family: 'Conthrax', 'Anton', sans-serif;
		display: flex;
		flex-direction: column;
		border: 1px solid #fff2;
		background-color: #fff1;
		border-radius: 1rem;
		p {
			position: absolute;
			font-size: 1.1rem;
			top: -3rem;
			width: 20rem;
		}
		& > div {
			display: flex;
			flex-direction: row;
			width: 10rem;
			flex-shrink: 1;
			& > div {
				text-align: center;
				padding: .5rem;
				width: 5rem;
			}
			& > div:first-child {
				text-shadow: 0 0 1rem rgba(230, 132, 19, 1);
			}
			& > div:last-child {
				text-shadow: 0 0 1rem rgb(19, 153, 230);
				border-left: 1px solid #fff2;
			}
		}
	}

	.echo_unit {
		position: absolute;
		z-index: 100;
		bottom: 0;
		opacity: 0;
		transition: all 1s;
		right: 0;
	}
	.echo_unit.visible {
		opacity: 1;
		right: 5rem;
		/* animation: echo_unit_anim 1s forwards; */
	}
	@keyframes fade_in {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
	@keyframes echo_unit_anim {
		from {
			right: 0;
			opacity: 0;
		}
		to {
			right: 5rem;
			opacity: 1;
		}
	}
</style>
