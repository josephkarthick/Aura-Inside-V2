
(function () {
    "use strict";

    const wrapper = document.getElementById("flag-wrapper");
    const renderArea = document.getElementById("renderArea");

    if (!wrapper || !renderArea || typeof THREE === "undefined") {
        console.error("Floating Flag: Required elements or Three.js missing.");
        return;
    }

    const SEG_W = 30;
    const SEG_H = 20;

    let scene, camera, renderer, flagMesh, flagTexture;
    let animationFrame;
    let dragging = false;
    let resizing = false;
    let previousPointer = { x: 0, y: 0 };
    let startSize = {};

    const el = id => document.getElementById(id);

    function get(id, fallback = "") {
        const node = el(id);
        return node ? node.value : fallback;
    }

    function number(id, fallback) {
        const value = parseFloat(get(id, fallback));
        return Number.isFinite(value) ? value : fallback;
    }

    const isAdminPreview =
        wrapper.dataset.editable === "true" ||
        wrapper.classList.contains("edit-mode");

    function getStage() {
        return wrapper.closest("[data-flag-stage]") ||
            document.getElementById("flag-stage") ||
            document.documentElement;
    }

    function getStageRect() {
        return getStage().getBoundingClientRect();
    }

    function getFlagDimensions() {
        return {
            width: Math.max(100, number("flag-width", 600)),
            height: Math.max(50, number("flag-height", 300))
        };
    }

    // INITIALIZE THREE.JS
    function init() {
        scene = new THREE.Scene();

        camera = new THREE.PerspectiveCamera(45, 1, 0.1, 4000);

        renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });

        renderer.setPixelRatio(
            Math.min(window.devicePixelRatio || 1, 2)
        );

        renderer.setClearColor(0x000000, 0);

        renderArea.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 1.2));

        const light = new THREE.DirectionalLight(0xffffff, 1.5);
        light.position.set(10, 20, 30);
        scene.add(light);

        createFlag();
        loadInitialTexture();
        setCamera();
        setPosition();
        enableDrag();
        enableResize();
        bindSettings();
        observeResize();

        animate();
    }

    // LOAD EXISTING IMAGE
    function loadInitialTexture() {
        const imageUrl = get("flag-image", "");

        if (imageUrl) {
            loadTexture(imageUrl);
        }
    }

    // LOAD IMAGE TEXTURE
    function loadTexture(imageUrl) {
        if (!imageUrl) return;

        new THREE.TextureLoader().load(
            imageUrl,
            texture => {
                if (flagTexture) {
                    flagTexture.dispose();
                }

                flagTexture = texture;

                if (flagMesh) {
                    flagMesh.material.map = flagTexture;
                    flagMesh.material.needsUpdate = true;
                }
            },
            undefined,
            error => {
                console.error("Flag image loading failed:", error);
            }
        );
    }

    // CREATE FLAG
    function createFlag() {
        if (!scene) return;

        const { width, height } = getFlagDimensions();

        const geometry = new THREE.PlaneGeometry(
            width,
            height,
            SEG_W,
            SEG_H
        );

        const material = new THREE.MeshLambertMaterial({
            color: get("flag-color", "#ffffff"),
            map: flagTexture || null,
            side: THREE.DoubleSide
        });

        if (flagMesh) {
            flagMesh.geometry.dispose();
            flagMesh.material.dispose();

            flagMesh.geometry = geometry;
            flagMesh.material = material;
        } else {
            flagMesh = new THREE.Mesh(geometry, material);
            scene.add(flagMesh);
        }

        geometry.userData.originalPositions =
            new Float32Array(geometry.attributes.position.array);

        setCamera();
        resizeRenderer();
    }

    // CAMERA
    function setCamera() {
        if (!camera) return;

        const { width, height } = getFlagDimensions();
        const angle = number("flag-angle", 0);

        const distance = Math.max(width, height) * 1.8;

        camera.position.set(
            distance * Math.sin(angle * Math.PI / 180),
            0,
            distance * Math.cos(angle * Math.PI / 180)
        );

        camera.lookAt(0, 0, 0);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    }

    // POSITION
    function setPosition() {
        const stage = getStageRect();
        const { width, height } = getFlagDimensions();

        let x = Math.max(0, Math.min(100, number("flag-pos-x", 50)));
        let y = Math.max(0, Math.min(100, number("flag-pos-y", 10)));

        wrapper.style.position = isAdminPreview ? "absolute" : "fixed";
        wrapper.style.width = width + "px";
        wrapper.style.height = height + "px";
        wrapper.style.transform = "none";

        if (isAdminPreview && stage.width && stage.height) {
            const maxX = Math.max(0, 100 - width / stage.width * 100);
            const maxY = Math.max(0, 100 - height / stage.height * 100);

            x = Math.min(x, maxX);
            y = Math.min(y, maxY);

            if (el("flag-pos-x")) el("flag-pos-x").value = x.toFixed(2);
            if (el("flag-pos-y")) el("flag-pos-y").value = y.toFixed(2);
        }

        wrapper.style.left = x + "%";
        wrapper.style.top = y + "%";

        resizeRenderer();
    }

    // RESIZE THREE.JS CANVAS
    function resizeRenderer() {
        if (!renderer || !camera) return;

        const width = renderArea.clientWidth;
        const height = renderArea.clientHeight;

        if (!width || !height) return;

        renderer.setSize(width, height, false);

        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    }

    function observeResize() {
        if ("ResizeObserver" in window) {
            const observer = new ResizeObserver(resizeRenderer);
            observer.observe(renderArea);
            observer.observe(wrapper);
        }

        window.addEventListener("resize", resizeRenderer);
        resizeRenderer();
    }

    // CLOTH ANIMATION - ORIGINAL WAVE FORMULA
    function animate() {
        animationFrame = requestAnimationFrame(animate);

        if (!flagMesh || !renderer) return;

        const animationCheckbox = el("flag-animation-enabled");

        if (animationCheckbox && !animationCheckbox.checked) {
            renderer.render(scene, camera);
            return;
        }

        const horizontal = number("flag-h", 0.5);
        const vertical = number("flag-v", 0.3);
        const strength = number("flag-w", 0.4);
        const speed = number("flag-s", 0.5);

        const direction = get("flag-direction", "both");

        const time = performance.now() * speed * 0.002;

        const geometry = flagMesh.geometry;
        const position = geometry.attributes.position;
        const original = geometry.userData.originalPositions;

        for (let y = 0; y <= SEG_H; y++) {
            for (let x = 0; x <= SEG_W; x++) {

                const index = y * (SEG_W + 1) + x;
                const offset = index * 3;

                const baseX = original[offset];
                const baseY = original[offset + 1];
                const baseZ = original[offset + 2];

                const depth = x / SEG_W;
                const verticalPosition = y / SEG_H;

                let displacement = 0;

                if (direction === "horizontal" || direction === "both") {
                    displacement += Math.sin(
                        horizontal * x +
                        vertical * y -
                        time
                    ) * strength * depth * 2;
                }

                if (direction === "vertical" || direction === "both") {
                    displacement += Math.sin(
                        vertical * y -
                        time * 0.8 +
                        horizontal * x * 0.3
                    ) * strength * verticalPosition * 1.5;
                }

                position.array[offset] = baseX;
                position.array[offset + 1] = baseY;
                position.array[offset + 2] = baseZ + displacement;
            }
        }

        position.needsUpdate = true;
        geometry.computeVertexNormals();

        renderer.render(scene, camera);
    }

    // ADMIN DRAG
    function enableDrag() {
        if (!isAdminPreview) return;

        wrapper.style.cursor = "grab";
        wrapper.style.touchAction = "none";

        wrapper.addEventListener("pointerdown", startDrag);
        document.addEventListener("pointermove", movePointer);
        document.addEventListener("pointerup", stopPointer);
        document.addEventListener("pointercancel", stopPointer);
    }

    function startDrag(event) {
        if (
            event.target.closest(
                "#flag-resize-handle, button, input, a"
            )
        ) return;

        dragging = true;

        previousPointer = {
            x: event.clientX,
            y: event.clientY
        };

        wrapper.style.cursor = "grabbing";

        event.preventDefault();
    }

    function dragFlag(event) {
        const stage = getStageRect();
        const flagRect = wrapper.getBoundingClientRect();

        if (!stage.width || !stage.height) return;

        const dx = event.clientX - previousPointer.x;
        const dy = event.clientY - previousPointer.y;

        let left = flagRect.left - stage.left + dx;
        let top = flagRect.top - stage.top + dy;

        left = Math.max(0, Math.min(stage.width - wrapper.offsetWidth, left));
        top = Math.max(0, Math.min(stage.height - wrapper.offsetHeight, top));

        const x = left / stage.width * 100;
        const y = top / stage.height * 100;

        wrapper.style.left = x + "%";
        wrapper.style.top = y + "%";

        if (el("flag-pos-x")) el("flag-pos-x").value = x.toFixed(2);
        if (el("flag-pos-y")) el("flag-pos-y").value = y.toFixed(2);

        previousPointer = {
            x: event.clientX,
            y: event.clientY
        };
    }

    // RESIZE HANDLE
    function enableResize() {
        if (!isAdminPreview) return;

        const handle = el("flag-resize-handle");
        if (!handle) return;

        handle.addEventListener("pointerdown", event => {
            resizing = true;

            previousPointer = {
                x: event.clientX,
                y: event.clientY
            };

            startSize = {
                width: wrapper.offsetWidth,
                height: wrapper.offsetHeight
            };

            event.preventDefault();
            event.stopPropagation();
        });
    }

    function resizeFlag(event) {
        const dx = event.clientX - previousPointer.x;
        const dy = event.clientY - previousPointer.y;

        const width = Math.max(
            100,
            Math.min(2000, startSize.width + dx)
        );

        const height = Math.max(
            50,
            Math.min(1200, startSize.height + dy)
        );

        wrapper.style.width = width + "px";
        wrapper.style.height = height + "px";

        if (el("flag-width")) el("flag-width").value = Math.round(width);
        if (el("flag-height")) el("flag-height").value = Math.round(height);

        resizeRenderer();
    }

    function movePointer(event) {
        if (dragging) dragFlag(event);
        if (resizing) resizeFlag(event);
    }

    function stopPointer() {
        dragging = false;
        resizing = false;

        if (isAdminPreview) {
            wrapper.style.cursor = "grab";
        }
    }

    // SETTINGS AND IMAGE UPLOAD
    function bindSettings() {

        ["flag-width", "flag-height"].forEach(id => {
            const input = el(id);
            if (!input) return;

            input.addEventListener("input", () => {
                const { width, height } = getFlagDimensions();

                wrapper.style.width = width + "px";
                wrapper.style.height = height + "px";

                createFlag();
                setPosition();
            });
        });

        const angle = el("flag-angle");
        if (angle) {
            angle.addEventListener("input", setCamera);
        }

        const color = el("flag-color");
        if (color) {
            color.addEventListener("input", createFlag);
        }

        ["flag-pos-x", "flag-pos-y"].forEach(id => {
            const input = el(id);
            if (input) {
                input.addEventListener("change", setPosition);
            }
        });

        // IMPORTANT: Show selected image immediately.
        const upload = el("flag-image-upload");

        if (upload) {
            upload.addEventListener("change", function () {

                const file = this.files && this.files[0];

                if (!file) return;

                if (!file.type.startsWith("image/")) {
                    alert("Please select a valid image.");
                    this.value = "";
                    return;
                }

                const previewUrl = URL.createObjectURL(file);

                loadTexture(previewUrl);
            });
        }

        // RESET
        const reset = el("flag-reset");

        if (reset) {
            reset.addEventListener("click", () => {

                if (el("flag-pos-x")) el("flag-pos-x").value = 50;
                if (el("flag-pos-y")) el("flag-pos-y").value = 10;

                if (el("flag-width")) el("flag-width").value = 600;
                if (el("flag-height")) el("flag-height").value = 300;

                setPosition();
                createFlag();
            });
        }
    }

    // START
    init();

    // CLEANUP
    window.destroyFloatingFlag = function () {

        if (animationFrame) {
            cancelAnimationFrame(animationFrame);
        }

        window.removeEventListener("resize", resizeRenderer);

        if (renderer) {
            renderer.dispose();
            renderer.domElement.remove();
        }

        if (flagTexture) {
            flagTexture.dispose();
        }
    };

})();
