<script lang="ts">
	import { SparkWebsocket } from '$lib/js/spark_websocket.js';
	import { onDestroy, onMount } from 'svelte';
	import { InfoBar, Button } from 'fluent-svelte';
	import RandomBackgroundImage from '$lib/components/RandomBackgroundImage.svelte';
	import UpcomingMatch from '$lib/components/UpcomingMatch.svelte';
	import type { Config } from '$lib/js/SparkConfig';
	import Webcams from '$lib/components/Webcams.svelte';

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
	<div style="width: 40rem; position: relative; z-index: 10;">
		<div style="width: 20rem; margin: auto;">
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
		<p>{config?.['caster_prefs']?.['waiting_message'] ?? ''}</p>
		<div style="height:20rem;" />
	</div>
</div>
<img
	src="https://cdn.discordapp.com/attachments/1024102109282570281/1048070865339809833/dome2.png"
	class="echo_unit"
	class:visible={config?.['caster_prefs']?.['show_echo_unit']}
	alt=""
/>
<div class="upcoming_match">
	<UpcomingMatch {config} />
</div>
<div class="webcams">
	<Webcams {config} />
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
		font-size: 4rem;
		opacity: 1;
		transform: scaleX(1);
		margin-top: 0;
		width: 100%;
		text-align: center;
	}

	.upcoming_match {
		position: absolute;
		z-index: 10;
		top: 10rem;
		left: 10rem;
		opacity: 0;
		animation: fade_in 2s 1s forwards;
	}
	.webcams {
		position: absolute;
		z-index: 10;
		bottom: 2rem;
		left: 10rem;
		opacity: 0;
		animation: fade_in 2s 1s forwards;
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
