const s = (sk) => {
    const DIM = 600;
    let paused = false;

    sk.preload = () => { };

    sk.setup = () => {
        sk.createCanvas(DIM, DIM).parent('canvasHolder');
        sk.background(20);
        sk.frameRate(60);
    };

    sk.draw = () => {
        if (!paused) {

        }
    };

    sk.keyPressed = () => {
        if (sk.key == "p") paused = !paused;
    }
};

let myp5 = new p5(s);