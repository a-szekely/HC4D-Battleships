var config = {
    width: 600,
    height: 600,
    type: Phaser.AUTO,
    parent: 'phaser-example',
    scene: {
        create: create,
        drawShot: drawShot
    }
};

var game = new Phaser.Game(config);
var graphics;

function create ()
{
    graphics = this.add.graphics({ lineStyle: { width: 2, color: 0x2266aa }, fillStyle: { color: 0x2266aa } });

     var ships = [
        [[50, 50], [80, 50]],
        [[450, 50], [530, 50]],
        [[50, 100], [130, 100]],
        [[100, 150], [280, 150]],
        [[200, 200], [580, 200]],
        [[50, 300], [230, 300]],
        [[70, 350], [100, 350]],
        [[450, 350], [480, 350]],
        [[210, 400], [290, 400]],
        [[350, 450], [530, 450]],
        [[30, 550], [410, 550]],
    ]

    redraw();

    function redraw ()
    {
        graphics.clear();

        for(var i = 0; i < ships.length; i++)
        {
            graphics.fillStyle(0xffffff);
            graphics.fillRoundedRect(ships[i][0][0] - 10, ships[i][0][1] - 10, ships[i][1][0] - ships[i][0][0] + 20, 20, 10);      
        }
    }
}

function drawShot(x, y, hit){
    var color;
    if (hit){
        color = 0xD32F2F;
    } else{
        color = 0x999999;   
    }
    graphics.fillStyle(color);
    graphics.fillCircle(x, y, 20);   
}
