<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js';
	import type { Frame } from '$lib/js/Frame';

	export let teamIndex = 0;
	export let frame: Frame;
	export let color = '#';

	let visible = true;

	let chartCanvas;
	let chart;

	let chartData = {
		labels: [],
		datasets: []
	};

	let chartOptions = {
		responsive: true,
		scales: {
			y: {
				beginAtZero: true
			},
			xAxes: [
				// display:false,
				{
					display: false
				}
			],
			yAxes: [
				{
					// gridLines: { color: '#ccc2' },
					display: false,
					ticks: {
						min: -40,
						max: 40
					}
				}
			]
		},
		legend: {
			display: false
		},
		events: [],
		plugins: {
			legend: {
				display: false
			},
			tooltips: {
				enabled: false
			}
		}
	};

	let frameHistoryLength = 1000;

	let playing = false;
	let wasPlaying = false;
	let jousting = false;
	function update() {
		playing = frame['game_status'] == 'playing';

		// if we transitioned into the playing state
		if (playing && !wasPlaying) {
			jousting = true;
			visible = true;

			// wait n seconds updating the joust
			setTimeout(() => {
				// then stop updating the joust
				jousting = false;

				// and wait another m seconds to hide the graph
				setTimeout(() => {
					visible = false;

					// clear the graph
					chartData.labels = [];
					chartData.datasets = [];
				}, 5000);
			}, 5000);
		}

		wasPlaying = playing;

		// don't update the graphs if we're not recording a joust
		if (!jousting) return;

		while (chartData.labels.length > frameHistoryLength) {
			chartData.labels.shift();
		}
		for (let d of chartData.datasets) {
			while (d.data.length > frameHistoryLength) {
				d.data.shift();
			}
		}

		chartData.labels.push(frame['game_clock_display']);
		for (let i = 0; i < frame['teams'][teamIndex]['players'].length; i++) {
			if (chartData.datasets.length <= i) {
				chartData.datasets.push({
					fill: true,
					backgroundColor: color + '22',
					lineTension: 0,
					borderColor: color,
					borderCapStyle: 'butt',
					pointRadius: 0,
					data: []
				});
			}
			chartData.datasets[i].data.push(
				frame['teams'][teamIndex]['players'][i]['head']['position'][2]
			);
		}

		// if the chart has been initialized already
		if (chart != null) {
			chart.update();
		}
	}

	$: if (frame) update();

	onMount(async () => {
		let ctx = chartCanvas.getContext('2d');
		chart = new Chart(ctx, {
			type: 'line',
			data: chartData,
			options: chartOptions
		});
	});
</script>

<div
	class="graph"
	style="{teamIndex == 0 ? 'right' : 'left'}:0;{teamIndex == 0 ? 'transform:scaleX(-1) scaleY(-1);' : ''}"
	class:hide={!visible}
>
	<canvas bind:this={chartCanvas} style="width: 100%; height: 100%;" />
</div>

<style>
	.graph {
		position: absolute;
		top: 0;
		width: 25rem;
		height: 10rem;
        transition: opacity 1s;
	}
	.hide {
		opacity: 0;
	}
</style>
