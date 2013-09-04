/* 
 * Wrapper for raphael library
 */

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
      console.log(elements[i]);
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
  this.elements = elements;
  
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
      console.log(elements[i]);
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
      console.log(elements[i]);
      var param = {stroke: elements[i]['color'], "stroke-width": this.options.lineWidth};
      var line = this.r.path().attr(param).attr({arc: [0, 100, this.R], stroke: elements[i]['color']}).toBack();
      if(this.options.useAnimationDelay){
        var delay = this.options.animationTime;
      }else{
        delay = 0;
      }
      line.transform('s,-1,1, T,0,0').animate(Raphael.animation({arc: [elements[i]['percentage'], 100, this.R]}, this.options.animationTime, this.options.easing).delay(delay));
      this.R = this.R - (this.options.lineWidth + 5);
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
  this.multiplier = 1;
  
  this.init = function(){
    if(this.options.barsAxis == 'x') this.multiplier = '-1';
    this.elements = this.options.elements;
  }
  
  this.draw = function(){
    if(this.options.drawAxis) this.drawAxis();
    if(this.options.drawLabels) this.drawLabels();
    if(this.options.drawValues) this.drawValues();
    this.drawBars();
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
    console.log(options);
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
    var xTarget = this.options.centerx + this.options.xAxis.length;
    this.r.path("M"+this.options.centerx+" "+this.options.centery+"L"+xTarget+" "+this.options.centery).attr({
      "stroke-width": 1
    });
  }
  
  this.drawYAxis = function(){
    //Build y Axis
    var yTarget = this.options.centery - this.options.yAxis.length;
    this.r.path("M"+this.options.centerx+" "+this.options.centery+"L"+this.options.centerx+" "+yTarget).attr({
      "stroke-width": 1
    });
  }
  
  this.drawLabels = function(){
    if(this.options.xAxis.labels.length){
      for(var i in this.options.xAxis.labels){
        label = this.options.xAxis.labels[i];
        xPos = this.options.centerx + label.pos;
        this.r.text(xPos, this.options.centery+10, label.text);
        if(label.type == 'dotted') this.drawDottedLine(label, 'x');
      }
    }
    
    if(this.options.yAxis.labels.length){
      for(var i in this.options.yAxis.labels){
        label = this.options.yAxis.labels[i];
        yPos = this.options.centery - label.pos;
        this.r.text(this.options.centerx-10, yPos, label.text);
        if(label.type == 'dotted') this.drawDottedLine(label, 'y');
      }
    }
  }
  
  this.drawDottedLine = function(label, axis){
    if(axis == 'x'){
      var xTarget = this.options.centerx + (label['pos']*this.multiplier);
      var yTarget = this.options.centery - label['width'];
      //this.r.path("M"+this.options.centerx+" "+yTarget+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '- ', "stroke-width": 1});
      this.r.path("M"+xTarget+" "+this.options.centery+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '- ', "stroke-width": 1});
    }else{
      var yTarget = this.options.centery + (label['pos']*this.multiplier);
      var xTarget = this.options.centerx + label['width'];
      this.r.path("M"+this.options.centerx+" "+yTarget+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '- ', "stroke-width": 1});
    }
  }
  
  this.drawDottedLines = function(){
    console.log('Drawing dotted lines!');
    //paper.path("M 30 120 l 150 0 z").attr({"stroke-dasharray": '- '});
    console.log(this.options.yAxis.labels);
    for(var i in this.options.yAxis.labels){
      var line = this.options.yAxis.labels[i];
      
      var yTarget = this.options.centery + (line['pos']*this.multiplier);
      var xTarget = this.options.centerx + line['width'];
      this.r.path("M"+this.options.centerx+" "+yTarget+"L"+xTarget+" "+yTarget).attr({"stroke-dasharray": '- ', "stroke-width": 1});
    }
  }
  
  this.drawBars = function(){
    console.log('Drawing bars!');
    for(var i in this.elements){
      console.log('drawing item...');
      var item = this.elements[i];
      if(this.options.barsAxis == 'x'){
        xPos = this.options.centerx + item['pos'];
        this.r.rect(xPos, this.options.centery, item['width'], 0).attr({
          fill: item['color'],
          "stroke-width": 0
        }).transform('r180').toBack().animate({
          height: item['value']
        }, 1000, 'bounce');
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
      if(a.percentage < b.percentage) return 1;
      if(a.percentage > b.percentage) return -1;
      return 0;
    });
  }
  
  this.draw = function(){
    this.drawCircles();
    if(this.options.drawLabels) this.drawLabels();
  }
  
  this.drawCircles = function(){
    var isFirst = true;
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
        c.attr({'stroke-width': 5, stroke: '#fff'});
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
    this.drawLabels();
  }
  
  this.drawBarParts = function(){
    console.log('LENGTH: '+this.elements.length);
    var xPos = this.options.x;
    var c = 0;
    
    for(var i in this.elements){
      var el = this.elements[i];
      var elWidth = (el.percentage*this.options.width)/100;
      console.log('elWidth: '+elWidth);
      var radius = 0;
      var diff = 0;
      
      if(i == 0 || i >= (this.elements.length-1)) radius = 10;
      if(i == 1){
        diff = 10;
      }else if(i == (this.elements.length-1)){
        diff = 10;
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
      
      this.drawArrow(el, x, width, i);
      this.drawLabel(el, x, width);
      
      c = c + elWidth;
    }
  }
  
  this.drawLabel = function(el, x, width){
    var textX = x + width - 10;
    this.r.text(textX, (this.options.y+this.options.height+20), el.percentage+" %").attr({
      fill: this.options.fontColor, 
      "font-size": this.options.fontSize
    }).toFront();  
    
    var textX = x + width - 10;
    this.r.text(textX, (this.options.y+this.options.height+40), el.label).attr({
      fill: this.options.fontColor, 
      "font-size": this.options.fontSize
    }).toFront();  
  }
  
  this.drawArrow = function (el, x, width, i){
    var pathX = x + width - 10;
    if(i == 0 || i == (this.elements.length-1)) pathX = pathX - 10;
    var pathY = this.options.y + this.options.height;
    var path = this.r.path("M"+pathX+" "+pathY+"L"+(pathX+10)+" "+pathY+"L"+(pathX+5)+" "+(pathY+10)+"Z").attr({
      "stroke-width": 0,
      "fill": el.color
    });
  }
  
  this.drawLabels = function(){
    
  }
  
  this.init();
}