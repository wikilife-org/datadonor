/* 
 * Wrapper for raphael library
 */
//(function extendRaphael() {
//  Raphael.el.zIndex = function(z) {
//    this.node.style.zIndex = z;
//  };
//})();

EdPieChart = function(r, elements, options){
  
  var _this = this;
  this.r = r;
  this.options = options;
  this.percentages = new Array();
  this.colors = new Array();
  this.R = 100; //Radio
  
  this.init = function(){
    for(var i in elements){
      this.percentages.push(elements[i]['percentage']);
      this.colors.push(elements[i]['color'])
    }
  }
  
  this.draw = function(){
    this.drawPie();
    this.drawCenter();
    this.drawReferences(elements);
  }
  
  this.drawPie = function(percentages, colors){
    this.r.piechart(this.options.centerx, this.options.centerx, this.options.radius, this.percentages,{
      strokewidth: 0,
      colors: this.colors
    });
  }
  
  this.drawCenter = function(){
    var centerRadio = this.options.radius - this.options.lineWidth;
    this.r.circle(this.options.centerx, this.options.centery, centerRadio).attr({
      fill: '#fff',
      "stroke-width": 0
    }).toFront();
  }
  
  this.drawReferences = function(elements){
    for(var i in elements){
      //console.log(elements[i]);
      this.r.text(elements[i]['x'], elements[i]['y'], elements[i]['text']).attr({
        fill: elements[i]['color'], 
        "font-size": this.options.fontSize}
      ).toFront();  
    }
  }
  
  this.init();
}

EdAnimatedPie = function(r, elements, options){
  var _this = this;
  this.r = r;
  this.options = options;
  this.percentages = new Array();
  this.colors = new Array();
  this.lines = new Array();
  this.texts = new Array();
  this.labelLocations = new Array();
  this.elements = elements;
  this.lastX = 0;
  this.lastY = 0;
  
  this.init = function(){
    this.elements.sort(function(a,b){
      if(a.percentage < b.percentage) return 1;
      if(a.percentage > b.percentage) return -1;
      return 0;
    });
    
    this.R = this.options.radius;
    
    for(var i in elements){
      this.percentages.push(elements[i]['percentage']);
      this.colors.push(elements[i]['color'])
    }
    this.setCustomAttributes();
  }
  
  this.setCustomAttributes = function(){
    this.r.customAttributes.arc = function (value, total, R) {
      //console.log('color: '+color);
      total = 100;
      
      color = '#6C47A7';
      var alpha = 360 / total * value,
          a = (90 - alpha) * Math.PI / 180,
          x = _this.options.centerx + R * Math.cos(a),
          y = _this.options.centery - R * Math.sin(a),
          //color = "hsb(".concat(Math.round(R) / 200, ",", value / total, ", .75)"),
          path;
      if (total == value) {
          path = [["M", _this.options.centerx, _this.options.centery - R], ["A", R, R, 0, 1, 1, (_this.options.centerx-0.01), _this.options.centery - R]];
      } else {
          path = [["M", _this.options.centerx, _this.options.centery - R], ["A", R, R, 0, +(alpha > 180), 1, x, y]];
      }
      
      return {path: path};
    };
  }
  
  this.draw = function(){
    this.drawLines();
    if(this.options.drawReferences) this.drawReferences();
    if(this.options.drawCenterImage) this.drawCenterImage();
    this.drawBorder();
    if(this.options.drawCenterText) this.drawCenterText();
  }
  
  this.drawLines = function(){
    //console.log('Drawing lines!');
    var total = 0;
    for(var i in elements){
      //console.log(elements[i]);
      var param = {stroke: elements[i]['color'], "stroke-width": this.options.lineWidth};
      var line = this.r.path().attr(param).attr({arc: [0, 100, this.R], stroke: elements[i]['color']}).toBack();
      if(this.options.useAnimationDelay){
        var delay = i*this.options.animationTime;
      }else{
        delay = 0;
      }
      line.animate(Raphael.animation({arc: [total+elements[i]['percentage'], 100, this.R]}, this.options.animationTime, this.options.easing).delay(delay));
      total = total + elements[i]['percentage'];
      this.lines.push(line);
    }
    //console.log(this.labelLocations);
  }
  
  this.drawReferences = function(){
    console.log('drawing references!');
    var c = 0;
    for(var i in this.elements){
      el = elements[i];
      //console.log('element percentage: '+elements[i]['percentage']);
      //console.log('total: '+c);
      var coords = this.getLabelsCoords(el["percentage"], c, this.R, this.options.centerx, this.options.centery);
      //console.log(coords);
      this.r.circle(coords[0], coords[1], 32).attr({"fill": this.options.bubbleColor, "stroke-width": 0});
      this.r.text(coords[0], coords[1]+10, el.text).attr({"font-family": 'Omnes-Semibold', "font-size": this.options.text.size, "fill": this.options.text.color});
      if(isDefined(el.image)){
        this.r.image(el.image.path, (coords[0]+parseInt(el.image.offsetx)), (coords[1]+parseInt(el.image.offsety)), el.image.width, el.image.height).toFront();
      }
      
      c = c+el["percentage"];
    }
  }
  
  this.getLabelsCoords = function(perc, prevPerc, R, cx, cy){
    var labelX, labelY;
    
    angle = ((perc*360)/100)/2;
    prevAngle = (prevPerc*360)/100;
    currentAngle = angle+prevAngle;
    labelX = cx + (R+this.options.lineWidth+5) * Math.cos(((90-currentAngle)*(Math.PI/180)));
    labelY = cy - (R+this.options.lineWidth+5) * Math.sin(((90-currentAngle)*(Math.PI/180)));
    
    /*console.log('RAD: '+R);
    console.log('ANGLE: '+angle);
    console.log('CENTER: '+cx+' - '+cy);
    console.log('PREV ANGLE: '+prevAngle);
    console.log('CURRENT ANGLE: '+currentAngle);
    console.log('COORDS: '+labelX+' - '+labelY);*/
    
    return [labelX, labelY];
  }
  
  this.drawCenterImage = function(){
    this.r.image(this.options.centerImage.path, this.options.centerImage.x, this.options.centerImage.y, this.options.centerImage.width, this.options.centerImage.height).toBack();
  }
  
  this.drawBorder = function(){
    var param = {stroke: this.options.borderColor, "stroke-width": this.options.lineWidth+this.options.borderMargin};
    var line = this.r.path().attr(param).attr({arc: [100, 100, this.R], stroke: this.options.borderColor}).toBack();
  }
  
  this.drawCenterText = function(){
    var offset = 0;
    if(this.options.centerText.text > 9){
      offset = this.options.centerText.unitOffset[0];
      xOffset = this.options.centerText.xOffset[0];
    }else{
      offset = this.options.centerText.unitOffset[1];
      xOffset = this.options.centerText.xOffset[1];
    }
    
    var txt1 = this.r.text(this.options.centerx+xOffset, this.options.centery, this.options.centerText.text).attr(
            {
            "font-family": this.options.centerText.font, 
            "font-size": this.options.centerText.size, 
            "fill": this.options.centerText.color, 
            'text-anchor': 'middle'}
    ).toFront();
    var txt2 = this.r.text(this.options.centerx+offset, this.options.centery+this.options.centerText.unitOffsetTop, this.options.centerText.unit).attr(
          {
          "font-family": this.options.centerText.unitFont,
          "font-size": this.options.centerText.unitSize, 
          "fill": this.options.centerText.color, 
          'text-anchor': 'middle'}
    ).toFront();
    this.texts.push(txt1);
    this.texts.push(txt2);
  }
  
  this.init();
}

EdQuarterAnimatedPie = function(r, elements, options){
  var _this = this;
  this.r = r;
  this.options = options;
  this.percentages = new Array();
  this.colors = new Array();
  this.lines = new Array();
  this.elements = elements;
  
  this.init = function(){
//    this.elements.sort(function(a,b){
//      if(a.percentage < b.percentage) return 1;
//      if(a.percentage > b.percentage) return -1;
//      return 0;
//    });
    
    this.R = this.options.radius;
    
    for(var i in elements){
      this.percentages.push(elements[i]['percentage']);
      this.colors.push(elements[i]['color'])
    }
    this.setCustomAttributes();
  }
  
  this.setCustomAttributes = function(){
    this.r.customAttributes.arc = function (value, total, R) {
      //console.log('color: '+color);
      total = 100;
      color = '#6C47A7';
      var alpha = 22.5 / (total/4) * (value/4),
          a = (22.5 - alpha) * Math.PI / 45,
          x = _this.options.centerx + R * Math.cos(a),
          y = _this.options.centery - R * Math.sin(a),
          //color = "hsb(".concat(Math.round(R) / 200, ",", value / total, ", .75)"),
          path;
      if (total == value) {
          path = [["M", _this.options.centerx, _this.options.centery - R], ["A", R, R, 0, 1, 1, (_this.options.centerx-0.01), _this.options.centery - R]];
      } else {
          path = [["M", _this.options.centerx, _this.options.centery - R], ["A", R, R, 0, +(alpha > 45), 1, x, y]];
      }
      return {path: path};
    };
  }
  
  this.draw = function(){
    this.drawLines();
    if(this.options.drawReferences) this.drawReferences();
  }
  
  this.drawLines = function(){
    console.log('Drawing lines!');
    for(var i in elements){
      //console.log(elements[i]);
      var param = {stroke: elements[i]['color'], "stroke-width": this.options.lineWidth};
      var line = this.r.path().attr(param).attr({arc: [0, 100, this.R], stroke: elements[i]['color']}).toBack();
      var emptyline = this.r.path().attr(param).attr({arc: [100, 100, this.R], stroke: '#F0EAE6'}).toBack();
      var whiteline = this.r.path().attr(param).attr({arc: [100, 100, this.R+2], stroke: '#ffffff'}).toBack();
      if(this.options.useAnimationDelay){
        var delay = this.options.animationTime;
      }else{
        delay = 0;
      }
      line.transform('s,-1,1, T,0,0').animate(Raphael.animation({arc: [elements[i]['percentage'], 100, this.R]}, this.options.animationTime, this.options.easing).delay(delay));
      this.R = this.R - (this.options.lineWidth + 2);
      this.lines.push(line);
    }
  }
  
  this.drawReferences = function(){
    console.log('drawing references!');
    for(var i in this.elements){
      this.r.text(elements[i]['x'], elements[i]['y'], elements[i]['text']).attr({
        fill: elements[i]['color'], 
        "font-size": this.options.fontSize}
      ).toFront();  
    }
  }
  
  this.init();
}

EdBarChart = function(r, options){
  
  var _this = this;
  this.r = r;
  this.options = options;
  this.elements;
  this.lines = [];
  this.avg_lines = [];
  this.multiplier = 1;
  
  this.init = function(){
    if(this.options.barsAxis == 'x') this.multiplier = '-1';
    this.elements = this.options.elements;
  }
  
  this.draw = function(){
    this.drawBars();
    if(this.options.drawLabels) this.drawLabels();
    if(this.options.drawAxis) this.drawAxis();
    if(this.options.drawValues) this.drawValues();
  }
  
  this.drawValues = function(){
    if(this.options.barsAxis == 'x'){
      for(var i in elements){
        this.r.text(elements[i]['x'], elements[i]['y'], elements[i]['text']);
      }
    }else{
      
    }
  }
  
  this.drawAxis = function(){
    //console.log(options);
    if(this.options.axis == 'both'){
      this.drawXAxis();
      this.drawYAxis();
    }else if(this.options.axis = 'y'){
      this.drawYAxis();
    }else if(this.options.axis == 'x'){
      this.drawXAxis();
    }
  }
  
  this.drawXAxis = function(){
    //Build x Axis
    console.log('DRAWING X AXIS');
    var xTarget = this.options.centerx + this.options.xAxis.length;
    this.r.path("M"+this.options.centerx+" "+this.options.centery+"L"+xTarget+" "+this.options.centery).attr({
      "stroke-width": this.options.xAxis["stroke-width"],
      "stroke": this.options.xAxis.color
    }).toBack();
  }
  
  this.drawYAxis = function(){
    //Build y Axis
    var yTarget = this.options.centery - this.options.yAxis.length;
    this.r.path("M"+this.options.centerx+" "+this.options.centery+"L"+this.options.centerx+" "+yTarget).attr({
      "stroke-width": this.options.yAxis["stroke-width"]
    });
  }
  
  this.drawLabels = function(){
    if(this.options.xAxis.labels.length){
      if(typeof this.options.xAxis.name != 'undefined'){
        this.r.text(this.options.centerx+this.options.canvasSize[0]-35, this.options.canvasSize[1]-10, this.options.xAxis.name).attr({"font-family": 'Omnes-Semibold', "font-size": '18', "fill": "#ADB6BF", 'text-anchor': 'end'});
      }
      for(var i in this.options.xAxis.labels){
        label = this.options.xAxis.labels[i];
        xPos = this.options.centerx + label.pos;
        //this.r.text(xPos, this.options.centery+10, label.text).attr({"font-size":label["font-size"], "font-family": label["font-family"]});
        if(label.type == 'dotted'){
          this.drawDottedLine(label, 'x');
        }else if(label.type == 'bubble'){
          this.r.circle(xPos, this.options.centery, 20).attr({"fill": '#3F4A5A', "stroke-width": 0}).toFront();
          this.r.text(xPos, this.options.centery, label['text']).attr({"fill": '#ffffff', "font-family": label["font-family"], "font-size": label["font-size"]}).toFront();
        }
        
      }
      
      console.log('SEND AVG TO FRONT!');
      console.log(this.avg_lines);
      for(var j in this.avg_lines){
        console.log('sending to front!');
        this.avg_lines[j].toFront();
      }
    }
    
    if(this.options.yAxis.labels.length){
      this.r.text(this.options.centerx, 10, this.options.yAxis.name).attr({"font-family": 'Omnes-Semibold', "font-size": '18', "fill": "#ADB6BF", 'text-anchor': 'start'});
      for(var i in this.options.yAxis.labels){
        label = this.options.yAxis.labels[i];
        yPos = this.options.centery - label.pos;
        var paddingTop = 0;
        if(label.text.indexOf('\n') != '-1'){
          paddingTop = 10; //Si hay salto de linea necesita mas espacio
        }
        var fontSize = '18px';
        if(typeof label["font-size"] != 'undefined') fontSize = label["font-size"];
        this.r.text(this.options.centerx, yPos+15+paddingTop, label.text).attr({"font-family": 'Omnes-Semibold', "font-size": fontSize, "fill": label['text-color'], 'text-anchor': 'start'}).toBack();
        if(label.type == 'dotted') this.drawDottedLine(label, 'y');
      }
    }
  }
  
  this.drawDottedLine = function(label, axis){
    console.log('dotted line single draw');
    if(axis == 'x'){
      var xTarget = this.options.centerx + (label['pos']*this.multiplier);
      var yTarget = this.options.centery - label['width'];
      //this.r.path("M"+this.options.centerx+" "+yTarget+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '- ', "stroke-width": 1});
      var line = this.r.path("M"+xTarget+" "+this.options.centery+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '.', "stroke-width": label["stroke-width"], "stroke": label["color"], "font-family": 'Omnes-Semibold'}).toBack();
      
    }else{
      console.log('IS AVG???');
      var yTarget = this.options.centery + (label['pos']*this.multiplier);
      var xTarget = this.options.centerx + label['width'];
      var line = this.r.path("M"+this.options.centerx+" "+yTarget+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '.', "stroke-width": label["stroke-width"], "stroke": label["color"], "font-family": 'Omnes-Semibold'}).toBack();
      
      if(typeof label['is_avg'] != 'undefined' && label['is_avg'] == true){
        this.avg_lines.push(line);
      }
    }
  }
  
  this.drawDottedLines = function(){
    console.log('Drawing dotted lines!');
    //paper.path("M 30 120 l 150 0 z").attr({"stroke-dasharray": '- '});
    //console.log(this.options.yAxis.labels);
    for(var i in this.options.yAxis.labels){
      var line = this.options.yAxis.labels[i];
      
      var yTarget = this.options.centery + (line['pos']*this.multiplier);
      var xTarget = this.options.centerx + line['width'];
      this.r.path("M"+this.options.centerx+" "+yTarget+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '- ', "stroke-width": 1}).toBack();
    }
  }
  
  this.drawBars = function(){
    console.log('Drawing bars!');
    for(var i in this.elements){
      //console.log('drawing item...');
      var item = this.elements[i];
      if(this.options.barsAxis == 'x'){
        st = r.set();
        xPos = this.options.centerx + item['pos'];
        var bar = this.r.rect(xPos, this.options.centery, item['width'], 0).attr({
          fill: item['color'],
          "stroke-width": 0
        }).transform('r180').toBack().animate({
          height: item['value']
        }, 1000, 'bounce');
        
        if(typeof(this.elements[i].callback === 'function' && typeof this.elements[i].callback_args != 'undefined')){
          bar.data('item-key', this.elements[i].key);
          bar.click(function(){
            console.log("CALLBACK!!!");
            console.log(item.callback);
            item.callback([this.data('item-key')]);
          });
        }
        
        if(typeof this.options.xAxis.labelsType == 'undefined' || this.options.xAxis.labelsType == 'automatic_bubble'){
          this.r.circle(xPos+(item['width']/2), this.options.centery - item['value'], 20).attr({"fill": '#3F4A5A', "stroke-width": 0});
          this.r.text(xPos+(item['width']/2), this.options.centery - item['value'], item['label']).attr({"fill": '#ffffff', "font-family": 'Gotham-Ultra', "font-size": 20});
        }
        
        if(typeof item.vlabel != 'undefined'){
          
          if(typeof(this.options.rotateBarLabels) != 'undefined'){
            if(this.options.rotateBarLabels){
              this.r.text(xPos+(item['width']/2), this.options.centery - item['value']+20, item['vlabel'])
                  .transform('r270')
                  .attr({"fill-opacity":0.5, "fill": '#ffffff', "font-family": 'Omnes-Semibold', "font-size": 30, "text-anchor": 'end'})
              ;
            }else{
              this.r.text(xPos+(item['width']/2), this.options.centery - item['value']+20, item['vlabel'])
              
                  .attr({"fill-opacity":0.5, "fill": '#ffffff', "font-family": 'Omnes-Semibold', "font-size": 30, "text-anchor": 'middle'})
              ;
            }
          }
        }
      }else{
        yPos = this.options.centery - item['pos'];
        this.r.rect(this.options.centerx, yPos, 0, item['width']).attr({
          fill: item['color'],
          "stroke-width": 0
        }).toBack().animate({
          width: item['value']
        }, 1000, 'bounce');
      }
    }
  }
  
  
  this.init();
}

EdDotChart = function(r, elements, options){
  
  var _this = this;
  this.r = r;
  this.options = options;
  this.elements = elements;
  
  this.init = function(){
    this.elements.sort(function(a,b){
      if(a.radius < b.radius) return 1;
      if(a.radius > b.radius) return -1;
      return 0;
    });
  }
  
  this.draw = function(){
    this.drawCircles();
    if(this.options.drawLabels) this.drawLabels();
  }
  
  this.drawCircles = function(){
    var isFirst = true;
    
    if(this.options.perimeter.display){
      p = this.r.circle(this.options.centerx, this.options.centery, this.options.perimeter.radius)
            .attr(
              { "stroke-width": 2, "stroke-dasharray": '. ', "stroke": this.options.perimeter.color }
            );
    }
    
    for(var i in this.elements){
      var el = this.elements[i];
      var delay = 0;
      var c;
      
      var animation = Raphael.animation({r: el.radius}, this.options.animationTime, this.options.easing);
      if(this.options.useAnimationDelay){
        delay = i*this.options.animationTime;
      }
      
      c = this.r.circle(this.options.centerx, this.options.centery, 0)
            .attr(
              { fill: el.color, "stroke-width": 0 }
            );
      if(isFirst){
        c.attr({'stroke-width': 0, stroke: '#fff'});
      }
                      
      c.animate(animation.delay(delay));
              
      isFirst = false;
    }
  }
  
  this.drawLabels = function(){
    var c = 0;
    var boxWidth = 100;
    var boxHeight = 80;
    var boxXPadding = 50
    var boxYPadding = 40;
    var firstElem;
    
    for(var i in this.elements){
      var el = this.elements[i];
      
      if(!firstElem) firstElem = el;
      
      var xPos = this.options.centerx - firstElem.radius;
      var yPos = this.options.centery + firstElem.radius - 10;
      var elemPos = xPos + (c*boxWidth);
      this.r.rect(elemPos, yPos, boxWidth, boxHeight).attr({
        fill: el['color'],
        "stroke-width": 0
      }).toBack();
      
      this.r.text(elemPos + boxXPadding, yPos + boxYPadding, el.label).attr({
        fill: '#fff', 
        "font-size": this.options.fontSize}
      ).toFront();  
      
      c++;
    }
  }
  
  this.init();
}

EdSingleBarChart = function(r, elements, options){
  
  var _this = this;
  this.r = r;
  this.options = options;
  this.elements = elements;
  
  this.init = function(){
    this.elements.sort(function(a,b){
      if(a.percentage < b.percentage) return 1;
      if(a.percentage > b.percentage) return -1;
      return 0;
    });
  }
  
  this.draw = function(){
    this.drawBarParts();
    this.drawIcon();
    //this.drawLabels();
    //this.drawMainLabel();
  }
  
  this.drawBarParts = function(){
    //console.log('LENGTH: '+this.elements.length);
    var xPos = this.options.x;
    var c = 0;
    
    for(var i in this.elements){
      var el = this.elements[i];
      var elWidth = (el.percentage*this.options.width)/100;
      //console.log('elWidth: '+elWidth);
      var radius = 0;
      var diff = 0;
      
      if(i == 0 || i >= (this.elements.length-1)) radius = 45;
      if(i == 1){
        diff = 45;
      }else if(i == (this.elements.length-1)){
        diff = 45;
      }else{
        diff = 0;
      }
      
      var x = xPos+c-diff;
      var width = elWidth+diff;
      var rect = this.r.rect(x, this.options.y, width, this.options.height, radius).attr({
        fill: el.color,
        "stroke-width": 0
      }).toBack();
      if(i == 1) rect.toFront();
      
      //this.drawArrow(el, x, width, i);
      this.drawLabel(el, x, width, i);
      
      c = c + elWidth;
    }
  }
  
  this.drawIcon = function(){
    this.r.image(this.options.first_icon, this.options.x+40, this.options.y, 61, 80).toFront();
  }
  
  this.drawLabel = function(el, x, width, elemNo){
    var diff = 15;
    var drawMainLabel = false;
    if(elemNo == 0){ 
      //console.log('FIRST BAR ELEMENT!');
      diff = 60;
    }else if(elemNo == (this.elements.length-1)){
      diff = 45;
      drawMainLabel = true;
    }
    //console.log('DIFFF: '+diff);
    
    var textX = x + width - diff;
    var textY = this.options.y+this.options.height/2;
    this.r.text(textX, textY, el.percentage).attr({
      fill: this.options.fontColor, 
      "font-size": this.options.fontSize,
      "font-family": 'Omnes-semibold',
      "text-anchor": 'end',
      "opacity": 0.8
    }).toFront(); 
    
    this.r.text(textX, textY+60, el.label).attr({
      fill: '#5b6d7f', 
      "font-size": 18,
      "font-family": 'Omnes-semibold',
      "text-anchor": 'end'
    }).toFront(); 
    
    if(drawMainLabel){
      this.drawMainLabel(x, width);
    }
    
  }
  
  this.drawArrow = function (el, x, width, i){
    var pathX = x + width - 45;
    if(i == 0 || i == (this.elements.length-1)) pathX = pathX - 10;
    var pathY = this.options.y + this.options.height;
    var path = this.r.path("M"+pathX+" "+pathY+"L"+(pathX+10)+" "+pathY+"L"+(pathX+5)+" "+(pathY+10)+"Z").attr({
      "stroke-width": 0,
      "fill": el.color
    });
  }
   
  this.drawMainLabel = function(x, width){
    console.log('DRAWING MAIN LABEL!');
    xPos = x + width;
    yPos = this.options.y+this.options.height/2;
    //this.r.circle(xPos, yPos, 30).attr({"fill": '#000000', "stroke-width": 0});
    //this.r.text(xPos, yPos, '%').attr({"text-anchor": "middle","font-family": 'Omnes-Semibold', "font-size": 35, "fill": "#ffffff"});
    this.r.image(this.options.end_icon, xPos-26, yPos-26, 53, 53).toFront();
  }
  
  this.init();
}

EdAnimatedPieLegacy = function(r, elements, options){
  var _this = this;
  this.r = r;
  this.options = options;
  this.percentages = new Array();
  this.colors = new Array();
  this.lines = new Array();
  this.labelLocations = new Array();
  this.elements = elements;
  this.lastX = 0;
  this.lastY = 0;
  
  this.init = function(){
    this.elements.sort(function(a,b){
      if(a.percentage < b.percentage) return 1;
      if(a.percentage > b.percentage) return -1;
      return 0;
    });
    
    this.R = this.options.radius;
    
    for(var i in elements){
      this.percentages.push(elements[i]['percentage']);
      this.colors.push(elements[i]['color'])
    }
    this.setCustomAttributes();
  }
  
  this.setCustomAttributes = function(){
    this.r.customAttributes.arc = function (value, total, R) {
      //console.log('color: '+color);
      total = 100;
      color = '#6C47A7';
      var alpha = 360 / total * value,
          a = (90 - alpha) * Math.PI / 180,
          x = _this.options.centerx + R * Math.cos(a),
          y = _this.options.centery - R * Math.sin(a),
          //color = "hsb(".concat(Math.round(R) / 200, ",", value / total, ", .75)"),
          path;
      if (total == value) {
          path = [["M", _this.options.centerx, _this.options.centery - R], ["A", R, R, 0, 1, 1, (_this.options.centerx-0.01), _this.options.centery - R]];
      } else {
          path = [["M", _this.options.centerx, _this.options.centery - R], ["A", R, R, 0, +(alpha > 180), 1, x, y]];
      }
      
      return {path: path};
    };
  }
  
  this.draw = function(){
    this.drawLines();
    if(this.options.drawReferences) this.drawReferences();
  }
  
  this.drawLines = function(){
    console.log('Drawing lines!');
    var total = 0;
    for(var i in elements){
      //console.log(elements[i]);
      var param = {stroke: elements[i]['color'], "stroke-width": this.options.lineWidth};
      var line = this.r.path().attr(param).attr({arc: [0, 100, this.R], stroke: elements[i]['color']}).toBack();
      if(this.options.useAnimationDelay){
        var delay = i*this.options.animationTime;
      }else{
        delay = 0;
      }
      line.animate(Raphael.animation({arc: [total+elements[i]['percentage'], 100, this.R]}, this.options.animationTime, this.options.easing).delay(delay));
      total = total + elements[i]['percentage'];
    }
    //console.log(this.labelLocations);
  }
  
  this.drawReferences = function(){
    console.log('drawing references!');
    for(var i in this.elements){
      //console.log('element percentage: '+elements[i]['percentage']);
    }
  }
  
  this.init();
}

function isDefined(variable){
  if(typeof variable != 'undefined') return true;
  return false;
}