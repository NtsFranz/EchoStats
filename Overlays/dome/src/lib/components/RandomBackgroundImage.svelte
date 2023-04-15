<script lang="ts">
	let images = [
		'/dome/img/domes/21.png',
		'/dome/img/domes/25.png',
		'/dome/img/domes/26.png',
		'/dome/img/domes/27.png',
		'/dome/img/domes/30.png',
		'/dome/img/domes/31.jpg',
		'/dome/img/domes/32.png',
		'/dome/img/domes/34.png',
		'/dome/img/domes/dome1.webp',
		'/dome/img/domes/dome2.webp',
		'/dome/img/domes/dome4.webp',
		'/dome/img/domes/dome5.webp',
		'/dome/img/domes/download.png',
		'/dome/img/domes/download_1.png',
		'/dome/img/domes/download_10.png',
		'/dome/img/domes/download_11.png',
		'/dome/img/domes/download_12.png',
		'/dome/img/domes/download_14.png',
		'/dome/img/domes/download_15.png',
		'/dome/img/domes/download_18.png',
		'/dome/img/domes/download_2.png',
		'/dome/img/domes/download_20.png',
		'/dome/img/domes/download_3.png',
		'/dome/img/domes/download_4.png',
		'/dome/img/domes/download_5.png',
		'/dome/img/domes/download_6.png',
		'/dome/img/domes/download_7.png',
		'/dome/img/domes/download_8.png',
		'/dome/img/domes/download_9.png',
		'/dome/img/domes/unknown.png',
		'/dome/img/domes/palidome.jpg'
	];

	let hero_image = images[Math.floor(Math.random() * images.length)];
	let hero_image_alt = images[Math.floor(Math.random() * images.length)];
	let bg_visible = true;
	let alt_bg_visible = false;

	// interval for changing the image
	// 0 means only on load
	export let interval = 0;
	let counter = 0;
	setInterval(() => {
		if (counter % 2 == 0) {
			if (alt_bg_visible) {
				hero_image = images[Math.floor(Math.random() * images.length)];
			}
			if (bg_visible) {
				hero_image_alt = images[Math.floor(Math.random() * images.length)];
			}
		} else {
			bg_visible = !bg_visible;
			alt_bg_visible = !alt_bg_visible;
		}
		counter += 1;
	}, interval * 500);
</script>

<div
	class="dome-background"
	class:visible={bg_visible}
	style="background-image: url({hero_image});"
/>
<div
	class="dome-background"
	class:visible={alt_bg_visible}
	style="background-image: url({hero_image_alt});"
/>

<style>
	.dome-background {
		opacity: 0;
		background-color: black;
		background-size: cover;
		height: 100%;
		width: 100%;
		position: absolute;
		top: 0;
		left: 0;
		/* animation: fade-in-background 5s; */
		/* animation-fill-mode: forwards; */
		filter: blur(1.2em) contrast(0.9) brightness(0.6);
		backface-visibility: hidden;
		z-index: 0;
		transition: opacity 1s;
	}

	.visible {
		opacity: 1;
	}

	@keyframes fade-in-background {
		0%,
		10% {
			opacity: 0;
		}
		100% {
			opacity: 1;
		}
	}
</style>
