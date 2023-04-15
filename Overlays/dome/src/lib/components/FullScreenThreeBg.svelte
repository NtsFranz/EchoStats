<script lang="ts" type="module">
    import * as THREE from 'three';
    import {onMount} from 'svelte';

    export let free_cam_fov = 85;
    let canvas;

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


    $: if (camera_transform) updateCamera();

    let camPos = [];
    let camPosFront = [];

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
        camPosFront = [
            -(pos[2] + forward[2] * 200),
            pos[1] + forward[1] * 200,
            pos[0] + forward[0] * 200
        ];
        camPos = [
            -pos[2],
            pos[1],
            pos[0]
        ];

        if (camera) {
            camera.position.x = camPos[0];
            camera.position.y = camPos[1];
            camera.position.z = camPos[2];

            camera.lookAt(camPosFront[0], camPosFront[1], camPosFront[2]);

            if (free_cam_fov != camera.fov) {
                camera.fov = free_cam_fov;
                camera.updateProjectionMatrix();
            }

            renderer.render(scene, camera);
        }
    }

    

    const scene = new THREE.Scene();
    let camera: THREE.PerspectiveCamera;
    let renderer;

    onMount(() => {
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        camera = new THREE.PerspectiveCamera(free_cam_fov, canvas.width / canvas.height, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            shadows: true,
        });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(canvas.width, canvas.height);


        let light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);

        const geometry = new THREE.SphereGeometry(500, 60, 40);
        // invert geometry
        geometry.scale(-1, 1, 1);
        geometry.rotateY(-1);

        const tex = new THREE.TextureLoader().load('/dome/img/dome360DoubleFaded.jpg');
        const material = new THREE.MeshBasicMaterial({map: tex});

        const mesh = new THREE.Mesh(geometry, material);

        scene.add(mesh);
    });
</script>

<div style="position:absolute; top:0;left:0;width:100%;height:100%; overflow:hidden;">
	<canvas bind:this={canvas}></canvas>
</div>