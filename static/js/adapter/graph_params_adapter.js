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
        server_key: json.global_data[prop]["key"],
        index: json.global_data[prop]["index"]
      }
      if(json.global_data[prop]["key"] == userLevel){ 
        item.color = userColor;
        item.selected = true;
      }
      elements.push(item);
    }
    
    elements.sort(function(a,b){
      if(a.index < b.index) return 1;
      if(a.index > b.index) return -1;
      return 0;
    });
    
    return elements;
  }
  
}

//WorkAdapter = function(){
//  
//  this.getParameters = function(json, totalHeight, maxValue, barsCallback){
//    
//    var elements = [];
//    var xLabels = [];
//    var yLabels = [];
//    result = {};
//    this.barsCallback = barsCallback;
//    console.log('WORK ADAPTER PRAMS');
//    console.log(this.barsCallback);
//    
//    elements = this.addElements(json, totalHeight, maxValue);
//    yLabels = this.getYLabels(json, totalHeight, maxValue);
//    
//    result.elements = elements;
//    result.yLabels = yLabels;
//    
//    return result;
//  }
//  
//  this.getValueHeight = function(value, totalHeight, maxValue){
//    var valuePercentage = (value*100)/maxValue;
//    var valueHeight = (valuePercentage*totalHeight)/100;
//    return valueHeight;
//  }
//  
//  this.addElements = function(json, totalHeight, maxValue){
//    var currentPos = 70;
//    var userItem = false;
//    var globalColor = '#7737c7';
//    var userColor = '#E56666';
//    var elements = [];
//    var userXp = '';
//    
//    if(typeof json.user_data.user_experience != 'undefined') userXp = json.user_data.user_experience.key;
//    
//    for(var prop in json.global_data){
//      var item = {
//        pos: currentPos,
//        color: globalColor,
//        label: json.global_data[prop]["value"],
//        value: this.getValueHeight(json.global_data[prop]["value"], totalHeight, maxValue),
//        callback: this.barsCallback,
//        callback_args: [json.global_data[prop]["key"]]
//      }
//      if(json.global_data[prop]["key"] == userXp){
//        item.width = 90;
//        
//        var item2 = {
//          pos: currentPos+90,
//          width: 90,
//          color: userColor,
//          label: json.user_data.user_experience.value,
//          value: this.getValueHeight(json.user_data.user_experience.value, totalHeight, maxValue)
//        }
//        userItem = true;
//      }else{
//        item.width = 180;
//      }
//      
//      elements.push(item);
//      if(userItem) elements.push(item2);
//      userItem = false;
//      currentPos = currentPos + 190;
//    }
//    
//    return elements;
//  }
//  
//  this.getYLabels = function(json, totalHeight, maxValue){
//    var labels = [];
//    var currentY = 10;
//    
//    for(var i = 0; i < 6; i++){
//      var label = {
//        pos: this.getValueHeight(currentY, totalHeight, maxValue), 
//        text: currentY.toString(), 
//        width: 1090, 
//        type: 'dotted', 
//        "stroke-width": 3, 
//        color: '#F1F2F2', 
//        "text-color": "#ADB6BF"
//      }
//      labels.push(label);
//      currentY = currentY + 10;
//    }
//    
//    var avgLabel = {
//      pos: this.getValueHeight(json.avg, totalHeight, maxValue), 
//      text: json.avg.toString()+'\navg', 
//      width: 1090, 
//      type: 'dotted', 
//      "stroke-width": 3, 
//      color: '#7737c7', 
//      "text-color": "#7737c7"
//    }
//    labels.push(avgLabel);
//    
//    return labels;
//  }
//  
//}

StepsAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    var ordered = [];
    ordered.push([json.days.sunday,'Sunday']);
    ordered.push([json.days.monday,'Monday']);
    ordered.push([json.days.tuesday,'Tuesday']);
    ordered.push([json.days.wednesday,'Wednesday']);
    ordered.push([json.days.thursday,'Thursday']);
    ordered.push([json.days.friday,'Friday']);
    ordered.push([json.days.saturday,'Saturday']);
    
    elements = this.addElements(ordered, totalHeight, maxValue);
    yLabels = this.getYLabels(ordered, json, totalHeight, maxValue);
    xLabels = this.getXLabels(ordered);
    
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
    for(var i in json){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 62,
        label: json[i][0].global_steps,
        vlabel: json[i][0].global_steps,
        value: this.getValueHeight(json[i][0].global_steps, totalHeight, maxValue),
      }
      
      var userItem = {
        pos: currentPos+62,
        color: userColor,
        width: 62,
        label: json[i][0].user_steps,
        vlabel: json[i][0].user_steps,
        value: this.getValueHeight(json[i][0].user_steps, totalHeight, maxValue),
      }
      
      elements.push(item);
      elements.push(userItem);
      currentPos = currentPos + 144;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, orig_json, totalHeight, maxValue){
    var labels = [];
    var step = Math.ceil((maxValue/totalHeight))*100;
    
    console.log('MAX VALUE: '+maxValue);
    console.log('STEP: '+step);
    var currentY = step;
    
    //for(var i = 0; i < 6; i++){
    while(currentY <= maxValue){
      var label = {
        pos: this.getValueHeight(currentY, totalHeight, maxValue), 
        //text: currentY.toString(), 
        text: '', 
        width: 1090, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#F1F2F2', 
        "text-color": "#ADB6BF"
      }
      
      labels.push(label);
      currentY = currentY + step;
    }
    
    console.log(json);
    var gloabalAvgLabel = {
      pos: this.getValueHeight(orig_json.global_avg_steps, totalHeight, maxValue), 
      //text: orig_json.global_avg_steps.toString()+'\navg', 
      text: orig_json.global_avg_steps.toString(), 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7",
      is_avg: true
    }
    labels.push(gloabalAvgLabel);
    
    var userAvgLabel = {
      pos: this.getValueHeight(orig_json.user_avg_steps, totalHeight, maxValue), 
      text: orig_json.user_avg_steps.toString(), 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#E56666', 
      "text-color": "#E56666",
      is_avg: true
    }
    labels.push(userAvgLabel);
    
    return labels;
  }
  
  this.getXLabels = function(json){
    xLabels = [];
    currentPos = 132;
    for(var i in json){
      var label = {pos: currentPos, text: json[i][1][0].toUpperCase(), type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 144;
    }
    return xLabels;
  }
}

WorkAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue, barsCallback){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    this.barsCallback = barsCallback;
    console.log('WORK ADAPTER PRAMS');
    
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
      console.log(json.global_data[prop]["key"]);
      var item = {
        pos: currentPos,
        color: globalColor,
        label: json.global_data[prop]["value"],
        value: this.getValueHeight(json.global_data[prop]["value"], totalHeight, maxValue),
        key: json.global_data[prop]["key"],
        callback: this.barsCallback,
        callback_args: [prop]
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
    
    var avgLabel = {
      pos: this.getValueHeight(json.avg, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7",
      "font-size": 15,
      is_avg: true
    }
    labels.push(avgLabel);
    
    //for(var i = 0; i < 6; i++){
    while (currentY < totalHeight){
      var label = {
        pos: this.getValueHeight(currentY, totalHeight, maxValue), 
        //text: currentY.toString(), 
        text: '', 
        width: 1090, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#F1F2F2', 
        "text-color": "#ADB6BF"
      }
      labels.push(label);
      currentY = currentY + 10;
    }
    
    return labels;
  }
  
}

MilesAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue, yLabelsValues){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    var ordered = [];
    ordered.push([json.days.sunday,'Sunday']);
    ordered.push([json.days.monday,'Monday']);
    ordered.push([json.days.tuesday,'Tuesday']);
    ordered.push([json.days.wednesday,'Wednesday']);
    ordered.push([json.days.thursday,'Thursday']);
    ordered.push([json.days.friday,'Friday']);
    ordered.push([json.days.saturday,'Saturday']);
    
//    elements = this.addElements(json, totalHeight, maxValue);
//    elements = this.addElements(json, totalHeight, maxValue);
//    yLabels = this.getYLabels(json, totalHeight, maxValue, yLabelsValues);
//    xLabels = this.getXLabels(json);
    
    elements = this.addElements(ordered, totalHeight, maxValue);
    yLabels = this.getYLabels(ordered, json, totalHeight, maxValue, yLabelsValues);
    xLabels = this.getXLabels(ordered);
    
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
    
    for(var i in json){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 45,
        label: json[i][0].global_miles,
        value: this.getValueHeight(json[i][0].global_miles, totalHeight, maxValue),
      }
      
      var userItem = {
        pos: currentPos+15,
        color: userColor,
        width: 45,
        label: json[i][0].user_miles,
        value: this.getValueHeight(json[i][0].user_miles, totalHeight, maxValue),
      }
      
      elements.push(item);
      elements.push(userItem);
      currentPos = currentPos + 70;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, orig_json, totalHeight, maxValue, yLabels){
    //console.log(yLabels);
    var labels = [];
    var currentY = 10;
    
    var gloabalAvgLabel = {
      pos: this.getValueHeight(orig_json.global_avg_miles, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7"
    }
    labels.push(gloabalAvgLabel);
    
    var userAvgLabel = {
      pos: this.getValueHeight(orig_json.user_avg_miles, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#E56666', 
      "text-color": "#E56666"
    }
    labels.push(userAvgLabel);
    
    //for(var i = 0; i < 6; i++){
    //for(var i in yLabels){
    while(currentY <= maxValue){
      var label = {
        pos: this.getValueHeight(currentY, totalHeight, maxValue), 
        text: '', 
        width: 1090, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#ADB6BF', 
        "text-color": "#ADB6BF"
      }
      
      if($.inArray(currentY, yLabels) != '-1') label.text = currentY.toString();
      
      labels.push(label);
      currentY = currentY + 10;
    }
    
    return labels;
  }
  
  this.getXLabels = function(json){
    xLabels = [];
    currentPos = 60;
    for(var i in json){
      var label = {pos: currentPos, text: json[i][1][0].toUpperCase(), type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 70;
    }
    return xLabels;
  }
}

HoursAdapter = function(){
  
  this.getParameters = function(json, totalHeight, maxValue, yLabelsValues){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    var ordered = [];
    ordered.push([json.days.sunday,'Sunday']);
    ordered.push([json.days.monday,'Monday']);
    ordered.push([json.days.tuesday,'Tuesday']);
    ordered.push([json.days.wednesday,'Wednesday']);
    ordered.push([json.days.thursday,'Thursday']);
    ordered.push([json.days.friday,'Friday']);
    ordered.push([json.days.saturday,'Saturday']);
    
    elements = this.addElements(ordered, totalHeight, maxValue);
    yLabels = this.getYLabels(ordered, json, totalHeight, maxValue, yLabelsValues);
    xLabels = this.getXLabels(ordered);
    
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
    
    for(var i in json){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 45,
        label: json[i][0].global_hours,
        value: this.getValueHeight(json[i][0].global_hours, totalHeight, maxValue),
      }
      
      var userItem = {
        pos: currentPos+15,
        color: userColor,
        width: 45,
        label: json[i][0].user_hours,
        value: this.getValueHeight(json[i][0].user_hours, totalHeight, maxValue),
      }
      
      elements.push(item);
      elements.push(userItem);
      currentPos = currentPos + 70;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, orig_json, totalHeight, maxValue, yLabels){
    //console.log(yLabels);
    var labels = [];
    var currentY = 1;
    
    var gloabalAvgLabel = {
      pos: this.getValueHeight(orig_json.global_avg_hours, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#7737c7', 
      "text-color": "#7737c7"
    }
    labels.push(gloabalAvgLabel);
    
    var userAvgLabel = {
      pos: this.getValueHeight(orig_json.user_avg_hours, totalHeight, maxValue), 
      text: '', 
      width: 1090, 
      type: 'dotted', 
      "stroke-width": 3, 
      color: '#E56666', 
      "text-color": "#E56666"
    }
    labels.push(userAvgLabel);
    
    //for(var i = 0; i < 6; i++){
    //for(var i in yLabels){
    while(currentY <= maxValue){
      console.log('CURRENT Y HOURS '+currentY+' - '+maxValue);
      var label = {
        pos: this.getValueHeight(currentY, totalHeight, maxValue), 
        text: '', 
        width: 1090, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#ADB6BF', 
        "text-color": "#ADB6BF"
      }
      
      if($.inArray(currentY, yLabels) != '-1') label.text = currentY.toString();
      
      labels.push(label);
      currentY = currentY + 1;
    }
    
    return labels;
  }
  
  this.getXLabels = function(json){
    xLabels = [];
    currentPos = 60;
    for(var i in json){
      var label = {pos: currentPos, text: json[i][1][0].toUpperCase(), type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 70;
    }
    return xLabels;
  }
}

NutrientsAdapter = function(){
  
  this.getParameters = function(json, colors){
    var elements = [];
    var colorsIndex = 0;
    
    for(var i in json){
      var element = { 
        percentage: json[i].percentage, 
        color: colors[colorsIndex], 
        label: json[i].title
      }
      elements.push(element);
      
      if(colorsIndex == (colors.length-1)){
        colorsIndex = 0;
      }else{
        colorsIndex++;
      }
    }
    
    return elements;
  }
  
}

CronicalConditionsAdapter = function(){
  
  this.getParameters = function(json, color){
    
    var elements = [];
    
    var item = {
      percentage: json.percentage,
      color: color,
      text: json.percentage
    };
    elements.push(item);
    
    return elements;
  }
}

SleepAdapter = function(){
  
  this.getParameters = function(json, json_user, totalHeight, maxValue){
    
    var elements = [];
    var xLabels = [];
    var yLabels = [];
    result = {};
    
    var ordered = [];
    ordered.push([json.days.sunday,'Sunday']);
    ordered.push([json.days.monday,'Monday']);
    ordered.push([json.days.tuesday,'Tuesday']);
    ordered.push([json.days.wednesday,'Wednesday']);
    ordered.push([json.days.thursday,'Thursday']);
    ordered.push([json.days.friday,'Friday']);
    ordered.push([json.days.saturday,'Saturday']);
    
    var ordered_user = [];
    ordered_user.push([json_user.days.sunday,'Sunday']);
    ordered_user.push([json_user.days.monday,'Monday']);
    ordered_user.push([json_user.days.tuesday,'Tuesday']);
    ordered_user.push([json_user.days.wednesday,'Wednesday']);
    ordered_user.push([json_user.days.thursday,'Thursday']);
    ordered_user.push([json_user.days.friday,'Friday']);
    ordered_user.push([json_user.days.saturday,'Saturday']);
    
    elements = this.addElements(ordered, ordered_user, totalHeight, maxValue);
    yLabels = this.getYLabels(ordered, ordered_user, totalHeight, maxValue);
    xLabels = this.getXLabels(ordered);
    
//    elements = this.addElements(json, json_user, totalHeight, maxValue);
//    yLabels = this.getYLabels(json, json_user, totalHeight, maxValue);
//    xLabels = this.getXLabels(json);
    
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
  
  this.addElements = function(json, json_user, totalHeight, maxValue){
    var currentPos = 70;
    var globalColor = '#7737c7';
    var userColor = '#E56666';
    var elements = [];
    
    //for(var i = 0; i < json.data.length; i = i+2){
    for(var i in json){
      var item = {
        pos: currentPos,
        color: globalColor,
        width: 62,
        label: json[i][0].hours,
        vlabel: json[i][0].hours,
        value: this.getValueHeight(json[i][0].hours, totalHeight, maxValue),
      }
      
      var userItem = {
        pos: currentPos+62,
        color: userColor,
        width: 62,
        label: json_user[i][0].hours,
        vlabel: json_user[i][0].hours,
        value: this.getValueHeight(json_user[i][0].hours, totalHeight, maxValue),
      }
      
      elements.push(item);
      elements.push(userItem);
      currentPos = currentPos + 144;
    }
    
    return elements;
  }
  
  this.getYLabels = function(json, json_user, totalHeight, maxValue){
    var labels = [];
    var currentY = 57;
    
    for(var i = 1; i <= 12; i++){
      console.log('totalHeight: '+totalHeight);
      console.log('Max value: '+maxValue);
      console.log('CURRENT LABEL HEIGHT: '+this.getValueHeight(i, totalHeight, maxValue));
      var label = {
        pos: this.getValueHeight(i, totalHeight, maxValue), 
        text: i.toString(), 
        width: 1103, 
        type: 'dotted', 
        "stroke-width": 3, 
        color: '#F1F2F2', 
        "text-color": "#ADB6BF"
      }
      labels.push(label);
      currentY = currentY + 57;
    }
    
    return labels;
  }
  
  this.getXLabels = function(json){
    console.log(json);
    xLabels = [];
    currentPos = 132;
    for(var i in json){
      var label = {pos: currentPos, text: json[i][1][0].toUpperCase(), type: 'bubble', "font-size": 20, "font-family": 'Gotham-Ultra'};
      xLabels.push(label);
      currentPos = currentPos + 144;
    }
    return xLabels;
  }
}
