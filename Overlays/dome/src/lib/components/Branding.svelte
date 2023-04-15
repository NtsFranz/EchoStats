<svelte:head>
	<title>IgniteVR Metrics Branding</title>
</svelte:head>

<div id="background_container" class="branding">
	<div class="grid_container">
		<div class="choice2" style="display: flex;">
			<div>Powered By</div>
			<img src="http://localhost:6724/img/ignite_logo_primary_white_256.png" alt="" />
			<div>IgniteVR Metrics</div>
		</div>
	</div>
</div>

<style>
	@font-face {
		font-family: 'ubuntu';
		font-weight: 700;
		src: url('/fonts/ubuntu-700.woff2') format('woff2'),
			url('/fonts/ubuntu-700.ttf') format('truetype');
	}

	.grid_container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		position: absolute;
		top: 200px;
		left: 0;
		margin: 0;
		padding: 0;
	}

	.grid_container > div {
		width: 800px;
		height: 200px;
		position: relative;
	}

	.grid_container > div div {
		position: absolute;
		width: 340px;
		line-height: 0;
		top: 100px;
		font-family: 'ubuntu', Inconsolata, sans-serif;
		font-size: 32px;
		font-weight: 900;
	}

	.grid_container > div div:first-child {
		text-align: right;
		left: 0;
        opacity: 0;
		animation: animated_branding_left 3s 1s forwards;
		/* animation: animated_branding_left 5s; */
	}

	.grid_container > div div:last-child {
		right: 0;
        opacity: 0;
		animation: animated_branding_right 3s 1s forwards;
		/* animation: animated_branding_right 5s; */
	}

	.grid_container > div img {
		width: 128px;
		height: 128px;
		margin: auto;
		z-index: 2;
        opacity: 0;
		animation: animated_branding_img 3s 1s forwards;
		/* animation: animated_branding_img 5s; */
	}

	.grid_container .choice2 {
		color: white;
		text-shadow: 0 0 10px #0008;
	}

	@keyframes animated_branding_img {
		0% {
			transform: scale(0.5);
			opacity: 0;
		}

		25%,
		75% {
			transform: scale(1);
			opacity: 1;
		}
		100% {
			transform: scale(0.5);
			opacity: 0;
		}
	}

	@keyframes animated_branding_left {
		0%,
		5% {
			opacity: 0;
			transform: translateX(50px);
		}
		10% {
			opacity: 0;
		}

		30%,
		70% {
			transform: translateX(0);
			opacity: 1;
		}
		90% {
			opacity: 0;
		}
		95%,
		100% {
			opacity: 0;
			transform: translateX(50px);
		}
	}

	@keyframes animated_branding_right {
		0%,
		5% {
			opacity: 0;
			transform: translateX(-50px);
		}
		10% {
			opacity: 0;
		}

		30%,
		70% {
			transform: translateX(0);
			opacity: 1;
		}
		90% {
			opacity: 0;
		}
		95%,
		100% {
			opacity: 0;
			transform: translateX(-50px);
		}
	}
</style>
