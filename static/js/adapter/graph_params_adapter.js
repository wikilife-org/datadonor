/* 
 * Adapter for ed.raphael.js
 */

SocialReachAdapter = function(){
  
  this.getParameters = function(json, colors){
    
    var elements = [];
    var colorCounter = 0;
    
    for(var prop in json){
      var item = {
        percentage: json[prop].percentage,
        color: colors[colorCounter],
        text: json[prop].count,
        image: {
          path: this.getImagePath(prop),
          width: '26',
          height: '20',
          offsetx: '-13',
          offsety: '-20'
        }
      }
      elements.push(item);
      colorCounter++;
    }
    
    return elements;
  }
  
  this.getImagePath = function(key){
    var path = '';
    if(key == 'twitter') path = "/static/img/iconos/6_twitter.png";
    if(key == 'foursquare') path = "/static/img/iconos/2_four.png";
    if(key == 'facebook') path = "/static/img/iconos/1_face.png";
    if(key == 'linkedin') path = "/static/img/iconos/3_linke.png";
    if(key == 'gmail') path = "/static/img/iconos/4_mail.png";
    return path;
  }
  
}

SocialShareAdapter = function(){
  
  this.getParameters = function(values, maxPerc, radius){
    var elements = [];
    console.log(values);
    var radius1 = this.getElementRadius(values[0], maxPerc, radius, values);
    var radius2 = this.getElementRadius(values[1], maxPerc, radius, values);
    
    elements = [
      {
        radius: radius1,
        color: '#7737c7'
      },
      {
        radius: radius2,
        color: '#e56666'
      }
    ];
    
    return elements;
  }
  
  this.getElementRadius = function(value, maxPerc, radius, values){
    var maxRad = (maxPerc*radius)/100;
    var totalPx = values[0]+values[1];
    var finalRadius = (value*maxRad)/totalPx;
    return finalRadius;
  }
  
}

EducationAdapter = function(){
  
  this.getParameters = function(json){
    
    var elements = [];
    var globalColor = '#7737c7';
    var userColor = '#E56666';
    var userLevel = json.user_data.user_level;
    
    for(var prop in json.global_data){
      var item = {
        percentage: json.global_data[prop]["percentage"],
        color: globalColor,
        text: json.global_data[prop]["title"]
      }
      if(json.global_data[prop]["key"] == userLevel) item.color = userColor;
      elements.push(item);
    }
    
    return elements;
  }
  
}

WorkAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    elements = this.addElements(json, totalHeight, maxValue);
    yLabels = this.getYLabels(json, totalHeight, maxValue);
    
    result.elements = elements;
    result.yLabels = yLabels;
    
    return result;
  }
  
  this.getValueHeight = function(value, totalHeight, maxValue){
    var valuePercentage = (value*100)/maxValue;
    var valueHeight = (valuePercentage*totalHeight)/100;
    return valueHeight;
  }
  
  this.addElements = function(json, totalHeight, maxValue){
    var currentPos = 70;
    var userItem = false;
    var globalColor = '#7737c7';
    var userColor = '#E56666';
    var userXp = json.user_data.user_experience.key;
    var elements = [];
    
    for(var prop in json.global_data){
      var item = {
        pos: currentPos,
        color: globalColor,
        label: json.global_data[prop]["value"],
        value: this.getValueHeight(json.global_data[prop]["value"], totalHeight, maxValue)
      }
      if(json.global_data[prop]["key"] == userXp){
        item.width = 90;
        
        var item2 = {
          pos: currentPos+90,
          width: 90,
          color: userColor,
          label: json.user_data.user_experience.value,
          value: this.getValueHeight(json.user_data.user_experience.value, totalHeight, maxValue)
        }
        userItem = true;
      }else{
        item.width = 180;
      }
      
      elements.push(item);
      if(userItem) elements.push(item2);
      userItem = false;
      currentPos = currentPos + 190;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, totalHeight, maxValue){
    var labels = [];
    var currentY = 10;
    
    for(var i = 0; i < 6; i++){
      var label = {
        pos: this.getValueHeight(currentY, totalHeight, maxValue), 
        text: currentY.toString(), 
        width: 1090, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#F1F2F2', 
        "text-color": "#ADB6BF"
      }
      labels.push(label);
      currentY = currentY + 10;
    }
    
    var avgLabel = {
      pos: this.getValueHeight(json.avg, totalHeight, maxValue), 
      text: json.avg.toString()+'\navg', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7"
    }
    labels.push(avgLabel);
    
    return labels;
  }
  
}


