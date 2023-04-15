<script lang="ts">
	import type { Config } from '../js/SparkConfig';
	import type { Frame } from '$lib/js/Frame';
	import JoustTime from './JoustTime.svelte';
	import RoundWins from './RoundWins.svelte';
	import ScoreView from './ScoreView.svelte';

	export let frame: Frame | null = null;
	export let config: typeof Config | null = null;
</script>

{#if frame}
	<div class="team_info">
		<div>
			<p>{config?.['teams'][1]['team_name']}</p>
			<img src={config?.['teams'][1]['team_logo']} alt="" />
		</div>
		<div>
			<img src={config?.['teams'][0]['team_logo']} alt="" />
			<p>{config?.['teams'][0]['team_name']}</p>
		</div>
	</div>

	<div class="main-box">
		<div class="default-view">
			<div class="roster orange">
				{#if frame['teams'][1]['players']}
					{#each frame['teams'][1]['players'] as p}
						<p class:possession={p['possession']} class:invulnerable={p['invulnerable']}>
							{p['name']}
						</p>
					{/each}
				{/if}
			</div>
			<div class="score orange">{frame['orange_points']}</div>
			<div class="score blue">{frame['blue_points']}</div>
			<div class="roster blue">
				{#if frame['teams'][0]['players']}
					{#each frame['teams'][0]['players'] as p}
						<p class:possession={p['possession']} class:invulnerable={p['invulnerable']}>
							{p['name']}
						</p>
					{/each}
				{/if}
			</div>
		</div>
	</div>

	<div class="clock-box">
		<div class="clock">{frame['game_clock_display'].substring(0, 5)}</div>
		<div class="round-wins"><RoundWins {frame} /></div>
	</div>
	<ScoreView {frame} />
{/if}
<img class="dome_logo" src="/dome/dome_logo_square.webp" alt="" />

<style type="text/scss">
	:root {
		--primary: #6f61e9;
		--secondary: #5ea5ec;
		--primary-dark: #4255e6;
		--secondary-dark: #3a75e5;
		--text: #c5c8d4;
	}

	@font-face {
		font-family: 'Conthrax';
		src: url('$lib/fonts/conthrax-sb.ttf') format('truetype');
	}

	.main-box {
		// background: linear-gradient(var(--primary), var(--primary-dark));
		// background: linear-gradient(#fffd, #aaad);
		color: #fff;
		border-radius: 1rem;
		height: 5rem;
		position: relative;
		margin: auto;
		display: flex;
		flex-wrap: nowrap;
		width: 50rem;
		//box-shadow: 0 1rem 1rem #000a;
		//opacity: .9;
		// overflow: hidden;
		margin-top: 2rem;
	}

	.dome_logo {
		width: 5rem;
		height: 5rem;
		position: absolute;
		left: 2rem;
		bottom: 2rem;
		filter: brightness(10);
		opacity: 0.2;
		margin: 0 0.3rem;
	}

	.clock-box {
		// background: linear-gradient(var(--secondary-dark), var(--secondary));
		// background: linear-gradient(var(--primary), var(--primary-dark));
		height: 100%;
		flex-grow: 0;
		width: 10rem;
		margin: auto;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--text);
		font-size: 2rem;
		font-family: 'Conthrax', 'Anton', sans-serif;
		text-shadow: 0 0 0.5rem #0008;

		.round-wins {
			position: absolute;
			top: -0.5rem;
			width: 100%;
			height: 0.5rem;
		}
	}

	.team_info {
		position: absolute;
		width: 100%;
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		gap: 50rem;
		& > div {
			display: flex;
			flex-direction: row;
			align-items: flex-start;
			flex-grow: 1;
		}
		img {
			width: 8em;
			aspect-ratio: 1/1;
			left: 0;
		}
		p {
			color: white;
			font-family: 'Conthrax', 'Anton', sans-serif;
			text-align: center;
			width: 100%;
			margin: 0;
			font-size: 2rem;
			width: 10rem;
			flex-grow: 1;
			flex-shrink: 1;
		}
	}

	.roster {
		flex-grow: 1;
		flex-shrink: 1;
		flex-basis: 0;
		position: relative;
		color: white;
		margin: 0 1rem;
		font-size: 1.2rem;
		font-weight: 100;
		height: 8rem;
		display: flex;
		flex-direction: column;

		font-family: 'Conthrax', 'Anton', sans-serif;
		// font-family: 'Courier New', Courier, monospace;

		p {
			margin: 0;
			flex-basis: 2rem;
			justify-content: center;
			align-items: center;
			display: flex;
			background: linear-gradient(90deg, #fff0, #000a, #fff0);
			// border-bottom: 0.1rem solid #fff2;

			&.possession {
				font-weight: 900;
			}
			&.invulnerable {
				opacity: 0.5;
			}
		}
	}

	.default-view {
		display: flex;
		width: 100%;

		.score {
			height: 4rem;
			flex-grow: 0;
			flex-shrink: 0;
			flex-basis: 5rem;
			display: flex;
			align-items: center;
			justify-content: center;

			font-family: 'Conthrax', 'Anton', sans-serif;
			color: var(--text);
			font-size: 2.5rem;
			text-shadow: 0 0 0.5rem #0008;

			&.orange {
				background: linear-gradient(#ffa500, rgb(143, 65, 17));
				// background: rgb(143, 65, 17);

				border-radius: 0.5rem 0 0 0.5rem;
			}

			&.blue {
				background: linear-gradient(#0095ff, rgb(22, 85, 119));
				// background: rgb(22, 85, 119);

				border-radius: 0 0.5rem 0.5rem 0;
			}
		}

		.team-name {
			flex-grow: 1;
			flex-shrink: 1;
			display: flex;
			align-items: center;
			text-align: center;
			justify-content: center;
			//color: var(--text);
			font-size: 1.4rem;
			padding: 0 1rem;
			font-family: 'Conthrax', 'Anton', sans-serif;
		}

		.joust {
			position: absolute;
			width: 5rem;
		}
	}
</style>
