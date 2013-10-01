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
    //console.log(values);
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
        text: json.global_data[prop]["title"],
        selected: false,
        server_key: json.global_data[prop]["key"]
      }
      if(json.global_data[prop]["key"] == userLevel){ 
        item.color = userColor;
        item.selected = true;
      }
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
    var elements = [];
    var userXp = '';
    
    if(typeof json.user_data.user_experience != 'undefined') userXp = json.user_data.user_experience.key;
    
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

StepsAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    elements = this.addElements(json, totalHeight, maxValue);
    yLabels = this.getYLabels(json, totalHeight, maxValue);
    xLabels = this.getXLabels(json);
    
    result.elements = elements;
    result.yLabels = yLabels;
    result.xLabels = xLabels;
    
    return result;
  }
  
  this.getValueHeight = function(value, totalHeight, maxValue){
    //console.log('VALUE: '+value);
    //console.log('TOTAL: '+totalHeight);
    //console.log('maxValue: '+maxValue);
    var valuePercentage = (value*100)/maxValue;
    var valueHeight = (valuePercentage*totalHeight)/100;
    return valueHeight;
  }
  
  this.addElements = function(json, totalHeight, maxValue){
    var currentPos = 70;
    var globalColor = '#7737c7';
    var userColor = '#E56666';
    var elements = [];
    
    //for(var i = 0; i < json.data.length; i = i+2){
    for(var i in json.data){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 62,
        label: json.data[i].global_data,
        vlabel: json.data[i].global_data,
        value: this.getValueHeight(json.data[i].global_data, totalHeight, maxValue),
      }
      
      var userItem = {
        pos: currentPos+62,
        color: userColor,
        width: 62,
        label: json.data[i].user_data,
        vlabel: json.data[i].user_data,
        value: this.getValueHeight(json.data[i].user_data, totalHeight, maxValue),
      }
      
      elements.push(item);
      elements.push(userItem);
      currentPos = currentPos + 144;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, totalHeight, maxValue){
    var labels = [];
    var currentY = 3000;
    
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
      currentY = currentY + 3000;
    }
    
    var gloabalAvgLabel = {
      pos: this.getValueHeight(json.global_avg, totalHeight, maxValue), 
      text: json.global_avg.toString()+'\navg', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7"
    }
    labels.push(gloabalAvgLabel);
    
    var userAvgLabel = {
      pos: this.getValueHeight(json.user_avg, totalHeight, maxValue), 
      text: json.user_avg.toString()+'\navg', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#E56666', 
      "text-color": "#E56666"
    }
    labels.push(userAvgLabel);
    
    return labels;
  }
  
  this.getXLabels = function(json){
    xLabels = [];
    currentPos = 132;
    for(var i in json.data){
      var label = {pos: currentPos, text: json.data[i].label, type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 144;
    }
    return xLabels;
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
    var elements = [];
    var userXp = '';
    
    if(typeof json.user_data.user_experience != 'undefined') userXp = json.user_data.user_experience.key;
    
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

MilesAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue, yLabelsValues){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    elements = this.addElements(json, totalHeight, maxValue);
    yLabels = this.getYLabels(json, totalHeight, maxValue, yLabelsValues);
    xLabels = this.getXLabels(json);
    
    result.elements = elements;
    result.yLabels = yLabels;
    result.xLabels = xLabels;
    
    return result;
  }
  
  this.getValueHeight = function(value, totalHeight, maxValue){
    var valuePercentage = (value*100)/maxValue;
    var valueHeight = (valuePercentage*totalHeight)/100;
    return valueHeight;
  }
  
  this.addElements = function(json, totalHeight, maxValue){
    var currentPos = 30;
    var globalColor = '#7737c7';
    var userColor = '#E56666';
    var elements = [];
    
    for(var i in json.data){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 45,
        label: json.data[i].global_data,
        value: this.getValueHeight(json.data[i].global_data, totalHeight, maxValue),
      }
      
      var userItem = {
        pos: currentPos+15,
        color: userColor,
        width: 45,
        label: json.data[i].user_data,
        value: this.getValueHeight(json.data[i].user_data, totalHeight, maxValue),
      }
      
      elements.push(item);
      elements.push(userItem);
      currentPos = currentPos + 70;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, totalHeight, maxValue, yLabels){
    console.log(yLabels);
    var labels = [];
    var currentY = 10;
    
    //for(var i = 0; i < 6; i++){
    for(var i in yLabels){
      var label = {
        pos: this.getValueHeight(yLabels[i], totalHeight, maxValue), 
        text: yLabels[i].toString(), 
        width: 1090, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#F1F2F2', 
        "text-color": "#ADB6BF"
      }
      labels.push(label);
      currentY = currentY + 10;
    }
    
    var gloabalAvgLabel = {
      pos: this.getValueHeight(json.global_avg, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7"
    }
    labels.push(gloabalAvgLabel);
    
    var userAvgLabel = {
      pos: this.getValueHeight(json.user_avg, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#E56666', 
      "text-color": "#E56666"
    }
    labels.push(userAvgLabel);
    
    return labels;
  }
  
  this.getXLabels = function(json){
    xLabels = [];
    currentPos = 60;
    for(var i in json.data){
      var label = {pos: currentPos, text: json.data[i].label, type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 70;
    }
    return xLabels;
  }
}

