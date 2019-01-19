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
        [[50, 50], [300, 50]],
         [[50, 80], [300, 80]],
         [[100, 150], [300, 150]],
        [[300, 200], [500, 200]]
    ];

    redraw();

    function redraw ()
    {
        graphics.clear();

        for(var i = 0; i < ships.length; i++)
        {
            graphics.fillStyle(0xffffff);
            graphics.fillRoundedRect(ships[i][0][0] - 10, ships[i][0][1] - 10, ships[i][1][0] - ships[i][0][0] + 20, 20, 10);
            var points = ships[i];
            for(var j = 0; j < points.length; j++)
            {
                graphics.fillStyle(0xffffff);
                graphics.fillCircle(points[j][0], points[j][1], 10);
                
            }            
        }
    }
}

function drawShot(x, y, hit){
    var color;
    if (hit){
        color = 0xD32F2F;
    } else{
        color = 0xffffff;   
    }
    graphics.fillStyle(color);
    graphics.fillCircle(x, y, 10);   
}
