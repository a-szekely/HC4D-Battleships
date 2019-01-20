var request = require('request');

var config = {
    width: 600,
    height: 600,
    type: Phaser.AUTO,
    parent: 'phaser-example',
    scene: {
        create: create
    }
};


var game = new Phaser.Game(config);

function create ()
{
    var graphics = this.add.graphics({ lineStyle: { width: 2, color: 0x2266aa }, fillStyle: { color: 0x2266aa } });

    var points = [
        new Phaser.Geom.Point(Math.random() * 400 + 200, Math.random() * 300 + 150)
    ];
    
    var points_colours = [
        0x999999
    ];
    
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
    ];
    
    var sunk = [];

    this.input.on('pointermove', function(pointer) {

        Phaser.Geom.Point.CopyFrom(pointer, points[0]);

        redraw();
    });

    this.input.on('pointerdown', function(pointer) {
        console.log(pointer.x, pointer.y);
        points.push(new Phaser.Geom.Point(pointer.x, pointer.y));
    
        request
        .post('http://localhost:5002/shot/', {
            json: {
                player:"xyz",
                x:pointer.x.toString(), 
                y:pointer.y.toString()
            }
         }, (error, res, body) => {
            if (error) {
                console.error(error)
                return
            }
            console.log(body);
            drawShot(body.ai_move[0], body.ai_move[1], isAHit(body.ai_move[0], body.ai_move[1]));
            if (body.hit=='1'){
                points_colours.push(0xD32F2F);
            } else{
                points_colours.push(0x999999);   
            }
            graphics.fillStyle(0x999999);
            graphics.fillCircle(pointer.x, pointer.y, 20);
            if (body.sunk=='1'){
                var ship = body.ship;
                sunk.push(ship);
                graphics.fillStyle(0xB71C1C);
                graphics.fillRoundedRect(ship[0][0] - 10, ship[0][1] - 10, ship[1][0] - ship[0][0] + 20, 20, 10);
            }
          })
       
        //redraw();
    });

    redraw();
    
    function isAHit(x, y){
        var max_dist = 30;
        for(var i = 0; i < ships.length; i++)
        {
            var flags = ships[i];
            var dist = distanceToLineSegment(x,y, flags[0][0], flags[0][1], flags[1][0], flags[1][1]);
            console.log(dist);
            if (dist < max_dist) {
                return true;
            }
        }
        return false;
    }

    function redraw ()
    {
        graphics.clear();

        //var rect = Phaser.Geom.Point.GetRectangleFromPoints(points);

        //graphics.strokeRectShape(rect);
        
        graphics.fillStyle(0x444444);
        graphics.fillCircle(points[0].x, points[0].y, 20);
        

        for(var i = 1; i < points.length; i++)
        {
            graphics.fillPointShape(points[i], 10);
            graphics.fillStyle(points_colours[i]);
            graphics.fillCircle(points[i].x, points[i].y, 20);
        }
        
        for(var i = 0; i < sunk.length; i++)
        {
            graphics.fillStyle(0x820000);
            graphics.fillRoundedRect(sunk[i][0][0] - 10, sunk[i][0][1] - 10, sunk[i][1][0] - sunk[i][0][0] + 20, 20, 10);
        }
    }
}

function distanceToLineSegment(x, y, x1, y1, x2, y2) {

  var A = x - x1;
  var B = y - y1;
  var C = x2 - x1;
  var D = y2 - y1;

  var dot = A * C + B * D;
  var len_sq = C * C + D * D;
  var param = -1;
  if (len_sq != 0) //in case of 0 length line
      param = dot / len_sq;

  var xx, yy;

  if (param < 0) {
    xx = x1;
    yy = y1;
  }
  else if (param > 1) {
    xx = x2;
    yy = y2;
  }
  else {
    xx = x1 + param * C;
    yy = y1 + param * D;
  }

  var dx = x - xx;
  var dy = y - yy;
  return Math.sqrt(dx * dx + dy * dy);
}
