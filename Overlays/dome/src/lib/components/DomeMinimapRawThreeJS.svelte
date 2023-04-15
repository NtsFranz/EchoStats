<script lang="ts" type="module">
    import * as THREE from 'three';
    import {onMount} from 'svelte';
    // import {CameraTransform} from "$lib/js/CameraTransform";
    // import {Frame} from "$lib/js/Frame";

    let model;
    let canvas;

    export let frame;
    export let camera_transform = {
        "position": {
            "X": 0,
            "Y": 0,
            "Z": 0
        },
        "rotation": {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0,
            "W": 1
        }
    };
    let camPos = [];
    let camRot = [];
    let lookPos = [];
    let camPosBehind = [];

    $: if (camera_transform) updateCamera();

    function updateCamera() {

        // using game api

        // let pos = frame['player']['vr_position'];
        // let forward = frame['player']['vr_forward'];


        // using writeapi

        let pos = [
            camera_transform['position']['X'],
            camera_transform['position']['Y'],
            camera_transform['position']['Z']
        ];
        let rot = new THREE.Quaternion(
            camera_transform['rotation']['X'],
            camera_transform['rotation']['Y'],
            camera_transform['rotation']['Z'],
            camera_transform['rotation']['W']
        );
        let forward = new THREE.Vector3(0, 0, 1).applyQuaternion(rot).toArray();

        camPosBehind = [
            -(pos[2] - forward[2] * 200),
            Math.max(
                Math.min(pos[1] - forward[1] * 200, 2000),
                50
            ),
            pos[0] - forward[0] * 200
        ];
        camPos = [
            -pos[2],
            pos[1],
            pos[0]
        ];
    }

    onMount(() => {
        canvas.style.width ='100%';
        canvas.style.height='100%';
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(20, canvas.width / canvas.height, 0.1, 1000);
		camera.position.setZ(30);
        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
	        alpha:true,
	        antialias: true,
	        shadows: true,
        });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(canvas.width, canvas.height);

        const geom = new THREE.TorusGeometry(10, 3, 16, 100);
        const mat = new THREE.MeshBasicMaterial({color: 0xFF3565, wireframe: true});
        const torus = new THREE.Mesh(geom, mat);
        scene.add(torus);

        function animate() {
            requestAnimationFrame(animate);

            camera.position.x = camPosBehind.x;
            camera.position.y = camPosBehind.y;
            camera.position.z = camPosBehind.z;

            torus.rotation.y += .01;

            renderer.render(scene, camera);
        }

        animate();
    });
</script>

<canvas bind:this={canvas}></canvas>