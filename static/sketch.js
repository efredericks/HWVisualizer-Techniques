const s = (sk) => {
    const DIM = 1000;
    let paused = false;
    let status = "running";

    let activeTechnique, activeTechniqueObj;
    const changeOver = 250;
    let registry = {};
    let palette = ["#ff71ce", "#01cdfe", "#05ffa1", "#b967ff", "#fffb96"];

    const technique = "flowfield.js";
    // const technique = "cellularAutomata.js";

    sk.preload = () => {
    };

    sk.setup = () => {
        socket = io.connect("http://localhost:8081");
        sk.createCanvas(DIM, DIM).parent('canvasHolder');
        sk.background(20);
        sk.frameRate(60);

        loadNewScript(technique);

        // socket.on('status', (data) => {
        //     console.log("status requested");
        //     const _data = {
        //         status: status,
        //     };
        //     socket.emit("client_status", _data);
        // });
    };

    sk.draw = () => {
        if (!paused) {
            if (activeTechniqueObj != null) {
                activeTechniqueObj.update();
            } else {
                if (registry[technique] != null)
                    activeTechniqueObj = loadNewObject(technique);
            }

            if ((sk.frameCount % changeOver) == 0) {
                status = "done";
                console.log("Done");
                // socket.emit('disconnect');
                sk.noLoop();
                socket.emit("done", null);
                // console.log("Re-initializing.")
                // if (registry[technique] != null)
                //     activeTechniqueObj = loadNewObject(technique);
            }
        }
    };

    sk.keyPressed = () => {
        if (sk.key == "p") paused = !paused;
        if (sk.key == "e") sk.background(20);
    }

    // same approach to load a script as in the 'main' repo
    async function loadNewScript(scriptName) {
        // const module = await import(`/static/techniques/${scriptName}`);
        const module = await import(`./techniques/${scriptName}`);
        registry[scriptName] = module.default;
    }
    function loadNewObject(technique) {
        const obj = registry[technique];
        return obj ? new obj(sk, palette) : null;
    }
};

let myp5 = new p5(s);