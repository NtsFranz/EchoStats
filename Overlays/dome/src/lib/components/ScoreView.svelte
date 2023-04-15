<script lang="ts">
	import type { Frame } from '../js/SparkConfig';

	export let frame: typeof Frame;
</script>

<div
	class="score-view"
	class:orange={frame['last_score']['team'] == 'orange'}
	class:blue={frame['last_score']['team'] == 'blue'}
	class:visible={frame['game_status'] == 'score'}
>
	<div class="point_amount">
		{frame['last_score']['point_amount']}<span style="font-size: .25em;">pts</span>
	</div>

	<div class="speeds column">
		<div class="space" />
		<div class="distance_thrown">{frame['last_score']['distance_thrown'].toFixed(1)} m</div>
		<div class="disc_speed">{frame['last_score']['disc_speed'].toFixed(1)} m/s</div>
		<div class="space" />
		<div class="space" />
	</div>
	<div class="column text-right">
		<div class="space" />
		<div class="goal_type">{frame['last_score']['goal_type']}</div>
		<div class="row">
			{#if frame['last_score']['assist_scored'] != '' && frame['last_score']['assist_scored'] != '[INVALID]'}
				<div class="assist_scored">
					<!-- <span class="assisted_by">Asst By: </span> -->
					{frame['last_score']['assist_scored']} ➜&nbsp;
				</div>
			{/if}
			<div class="person_scored">{frame['last_score']['person_scored']}</div>
		</div>

		<div class="space" />
		<div class="space" />
	</div>
</div>

<style type="text/scss">
	.score-view {
		position: relative;
		top: 0rem;
		margin: auto;
		width: 40rem;
		height: 100%;
		border-radius: 1rem;

		opacity: 0;
		transition: all 0.5s;
		color: var(--text);
		font-family: Arial, Helvetica, sans-serif;
		font-weight: 900;
		text-align: center;
		display: flex;
		flex-wrap: wrap;
		text-shadow: 0 0 0.2rem #0008;

		&.visible {
			opacity: 1;
			top: 2rem;
		}

		&.orange {
			background: linear-gradient(rgb(143, 65, 17), rgb(170, 118, 21));
		}
		&.blue {
			background: linear-gradient(rgb(22, 85, 119), rgb(16, 127, 206));
		}

		& > div {
			flex-grow: 1;
		}

		.point_amount {
			font-size: 3.5rem;
			font-weight: 900;
			margin: 0 0.5rem;

			font-family: 'Conthrax', 'Anton', sans-serif;
		}

		.assisted_by {
			//font-size: 0.9em;
			text-transform: uppercase;
		}

		.column {
			display: flex;
			flex-direction: column;

			align-items: center;
			justify-content: center;

			& > div {
				flex-grow: 1;
				// flex-shrink: 1;
			}
		}

		.row {
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: center;
		}

		.space {
			flex-basis: 0.2rem;
		}

		.person_scored {
			//font-size: 1.2em;
		}

		.goal_type {
			font-size: 1.3em;
		}

		.speeds {
			flex-basis: 2rem;
			flex-grow: 1;
			flex-shrink: 1;
			font-size: 1.2em;
			div {
				flex-grow: 1;
				display: flex;
				align-items: center;
			}
		}

		.text-right {
			flex-grow: 1;
			flex-shrink: 1;
		}
	}
</style>
